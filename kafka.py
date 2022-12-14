import os
import sys
from datetime import datetime
from typing import Any, Iterator, List, Tuple, Union
from uuid import uuid4

from confluent_kafka import TIMESTAMP_NOT_AVAILABLE, Consumer, Producer
from google._upb._message import Message
from google.protobuf.json_format import MessageToJson, Parse, ParseError
from google.protobuf.message import DecodeError

# mypy cannot analyze files generated by protoc
from models.core_helper.instruction_command_pb2 import InstructionCommand  # type: ignore[attr-defined]
from models.core_helper.instruction_status_executor_pb2 import InstructionStatusExecutor  # type: ignore[attr-defined]
from models.core_helper.instruction_status_update_pb2 import InstructionStatusUpdate  # type: ignore[attr-defined]
from models.core_helper.invoice_presentment_message_pb2 import InvoicePresentmentMessageProtobuf  # type: ignore

TYPES_MAP = {
    "instruction.command": InstructionCommand,
    "instruction.status.executor": InstructionStatusExecutor,
    "instruction.status.update": InstructionStatusUpdate,
    "stream.eipp-engine.presentment.submission.entry": InvoicePresentmentMessageProtobuf,
}


def known_topics() -> List[str]:
    return list(TYPES_MAP.keys())


def consumer_conf(servers: str, group_id: str) -> dict:
    print(f"bootstrap_servers={servers}")
    return {
        "bootstrap.servers": servers,
        "group.id": group_id,
        "session.timeout.ms": 6000,
        "auto.offset.reset": "earliest",
        "enable.auto.offset.store": False,
    }


def producer_conf(servers: str) -> dict:
    print(f"bootstrap_servers={servers}")
    return {"bootstrap.servers": servers, "topic.acks": 1}


def json2protobuf(topic: str, json_str: str) -> Message:
    """
    convert a json string to a protobuf message
    """
    try:
        obj = TYPES_MAP[topic]()
        Parse(json_str, obj)
        return obj
    except (KeyError, ParseError):
        return None


def decode(topic: str, message_pb: bytes) -> Union[Message, bytes]:
    """
    decode a protobuf message to an obj of the known type
    return the message as is in case the message is not recognized or
    cannot be decoded
    """
    try:
        obj = TYPES_MAP[topic]()
        obj.ParseFromString(message_pb)
        return obj
    except (DecodeError, KeyError):
        return message_pb


def produce(servers: str, topic: str, message_pb: Message) -> int:
    """
    send messages to a topic
    returns the number of messages not sent
    """
    producer = Producer(producer_conf(servers))
    producer.produce(
        topic,
        key=str(uuid4()),
        value=message_pb.SerializeToString(),
    )
    return producer.flush(3)


def consume(servers: str, topic: str, group_id: str, duration: float = 3.0) -> Iterator[Tuple[str, Any, datetime]]:
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

            key, message_pb, (ts_type, timestamp) = str(msg.key()), msg.value(), msg.timestamp()
            if ts_type == TIMESTAMP_NOT_AVAILABLE:
                timestamp = None

            yield key, decode(topic, message_pb), datetime.fromtimestamp(timestamp / 1000)

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
        for key, message_pb, timestamp in consume(bootstrap_servers, topic, "biznext-event-tool", duration):
            try:
                print(f"key====>{key} at {timestamp.isoformat()}")
                print(MessageToJson(message_pb))
            except AttributeError:
                print(f"*** {message_pb}")
    else:
        topic = sys.argv[1]
        with open(sys.argv[2], "r") as f:
            json_str = f.read()
            message_pb = json2protobuf(topic, json_str)
            print(f"publishing:...\n{MessageToJson(message_pb)}")
            produce(bootstrap_servers, topic, message_pb)
