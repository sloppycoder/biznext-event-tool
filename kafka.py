import sys
from datetime import datetime
from uuid import uuid4

from confluent_kafka import Consumer, Producer
from google.protobuf import json_format
from google.protobuf.message import DecodeError

from models.core_helper.instruction_command_pb2 import InstructionCommand
from models.core_helper.instruction_status_executor_pb2 import InstructionStatusExecutor
from models.core_helper.instruction_status_update_pb2 import InstructionStatusUpdate

TYPES_MAP = {
    "instruction.command": InstructionCommand,
    "instruction_status_executor": InstructionStatusExecutor,
    "instruction_status_update": InstructionStatusUpdate,
}

bootstrap_servers = "localhost:9092"

consumer_conf = {
    "bootstrap.servers": bootstrap_servers,
    "group.id": "test-tool-consumer-1",
    "session.timeout.ms": 6000,
    "auto.offset.reset": "earliest",
    "enable.auto.offset.store": False,
}

producer_conf = {
    "bootstrap.servers": bootstrap_servers,
}


def json2protobuf(topic: str, json_file: str):
    with open(json_file, "r") as f:
        json = "".join(f.readlines())
        obj = TYPES_MAP[topic]()
        obj = json_format.Parse(json, obj)
        return obj


def protobuf2json(topic: str, json_str: str):
    try:
        obj = TYPES_MAP[topic]()
        obj.ParseFromString(json_str)
        return obj
    except KeyError:
        return json_str


def produce(conf: dict, topic: str, message) -> None:
    producer = Producer(conf)
    producer.produce(
        topic,
        key=str(uuid4()),
        value=message.SerializeToString(),
    )
    producer.flush()
    # producer.close()


def consume(conf: dict, topic: str, duration: int = 3):
    consumer = Consumer(conf)
    consumer.subscribe([topic])

    try:
        start_t = datetime.now().timestamp()
        now_t = start_t

        while now_t - start_t < duration:
            now_t = datetime.now().timestamp()

            msg = consumer.poll(1.0)
            if msg is None:
                continue

            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            key, val = msg.key(), msg.value()
            yield key, protobuf2json(topic, val)

            consumer.store_offsets(msg)
            consumer.commit()

    except KeyboardInterrupt:
        sys.stderr.write("%% Aborted by user\n")
    finally:
        consumer.close()


def dummy_payload() -> InstructionCommand:
    return InstructionCommand(
        data=InstructionCommand.Data(service="some_service", note=f"generated at {datetime.now().isoformat()}"),
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            """

        kafka.py <topic> <json_file>
        kafka.py consume <topic>

        """
        )
        sys.exit(-1)

    if sys.argv[1] == "consume":
        topic = sys.argv[2]
        for _, message in consume(consumer_conf, topic):
            try:
                print(json_format.MessageToJson(message))
            except DecodeError:
                print(f"*** f{message}")
    else:
        topic = sys.argv[1]
        message = json2protobuf(topic, sys.argv[2])
        print(f"publishing:...\n{json_format.MessageToJson(message)}")
        produce(producer_conf, topic, message)
