from app import static_file_content
from kafka import TYPES_MAP, decode, json2protobuf
from models.core_helper.instruction_command_pb2 import InstructionCommand  # type: ignore[attr-defined]


def test_json2protobuf():
    valid = """
        {
        "data": {
            "service": "some_service",
            "note": "generated at 2022-12-11T11:21:15.035710"
        }
        }
    """
    assert isinstance(json2protobuf("instruction.command", valid), InstructionCommand)

    gibberish = "ABX+x\0101ysl"
    assert json2protobuf("instruction.command", gibberish) is None


def test_decode():
    valid = b"\x127\x12\x0csome_serviceZ'generated at 2022-12-11T11:21:15.035710"
    obj = decode("instruction.command", valid)
    assert isinstance(obj, InstructionCommand)
    assert obj.data.service == "some_service"

    gibberish = bytes("ABX+x\0101ysl", "utf-8")
    obj = decode("instruction.command", gibberish)
    assert not isinstance(obj, InstructionCommand)
    assert obj == gibberish


def test_static_json_files():
    for topic in TYPES_MAP:
        json_str = static_file_content(f"{topic}.json")
        obj = json2protobuf(topic, json_str)
        assert isinstance(obj, TYPES_MAP[topic])
