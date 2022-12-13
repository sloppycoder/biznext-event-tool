import os
import sys
from datetime import datetime
from typing import Any
from uuid import uuid4

from confluent_kafka import TIMESTAMP_NOT_AVAILABLE, Consumer, Producer
from google.protobuf import json_format
from google.protobuf.message import DecodeError

from models.core_helper.instruction_command_pb2 import InstructionCommand
from models.core_helper.instruction_status_executor_pb2 import InstructionStatusExecutor
from models.core_helper.instruction_status_update_pb2 import InstructionStatusUpdate
from models.core_helper.invoice_presentment_message_pb2 import InvoicePresentmentMessageProtobuf

TYPES_MAP = {
    "instruction.command": InstructionCommand,
    "instruction.status.executor": InstructionStatusExecutor,
    "instruction.status.update": InstructionStatusUpdate,
    "stream.eipp-engine.presentment.submission.entry": InvoicePresentmentMessageProtobuf,
}


def is_known_topic(topic: str) -> bool:
    return topic in TYPES_MAP


def consumer_conf(servers: str, group_id: str):
    print(f"bootstrap_servers={servers}")
    return {
        "bootstrap.servers": servers,
        "group.id": group_id,
        "session.timeout.ms": 6000,
        "auto.offset.reset": "earliest",
        "enable.auto.offset.store": False,
    }


def producer_conf(servers: str):
    print(f"bootstrap_servers={servers}")
    return {"bootstrap.servers": servers, "topic.acks": 1}


def json2protobuf(topic: str, json_str: str):
    obj = TYPES_MAP[topic]()
    obj = json_format.Parse(json_str, obj)
    return obj


def protobuf2json(topic: str, message: str):
    try:
        obj = TYPES_MAP[topic]()
        obj.ParseFromString(message)
        return obj
    except (DecodeError, KeyError):
        return message


def produce(servers: str, topic: str, message: Any, timeout=3.0) -> int:
    producer = Producer(producer_conf(servers))
    producer.produce(
        topic,
        key=str(uuid4()),
        value=message.SerializeToString(),
    )
    return producer.flush(timeout)


def consume(servers: str, topic: str, group_id="biznext-event-tool", duration: int = 3):
    conf = consumer_conf(servers, group_id)
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

            key, val, (ts_type, timestamp) = msg.key(), msg.value(), msg.timestamp()
            if ts_type == TIMESTAMP_NOT_AVAILABLE:
                timestamp = None

            yield key, protobuf2json(topic, val), timestamp

            consumer.store_offsets(msg)
            consumer.commit()

    except KeyboardInterrupt:
        sys.stderr.write("%% Aborted by user\n")
    finally:
        consumer.close()


if __name__ == "__main__":
    bootstrap_servers = os.environ.get("BOOTSTRAP_SERVERS", "localhost:9092")

    if len(sys.argv) < 2:
        print(
            """

        kafka.py <topic> <json_file>
        kafka.py consume <topic> <-f>

        """
        )
        sys.exit(-1)

    if sys.argv[1] == "consume":
        # listen on the topic for 30 by default, unless -f is specified
        duration = 30
        if len(sys.argv) > 3 and sys.argv[3] == "-f":
            duration = sys.maxsize

        topic = sys.argv[2]
        for key, message, timestamp in consume(bootstrap_servers, topic, duration):
            try:
                print(f"key====>{key} at {datetime.fromtimestamp(timestamp/1000).isoformat()}")
                print(json_format.MessageToJson(message))
            except AttributeError:
                print(f"*** {message}")
    else:
        topic = sys.argv[1]
        with open(sys.argv[2], "r") as f:
            json_str = f.read()
            message = json2protobuf(topic, json_str)
            print(f"publishing:...\n{json_format.MessageToJson(message)}")
            produce(bootstrap_servers, topic, message)
