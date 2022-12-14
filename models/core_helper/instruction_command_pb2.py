# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: instruction_command.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19instruction_command.proto\x12 th.co.ktb.biznext.channel.common\"\xf0\r\n\x12InstructionCommand\x12K\n\x06header\x18\x01 \x01(\x0b\x32;.th.co.ktb.biznext.channel.common.InstructionCommand.Header\x12G\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\x39.th.co.ktb.biznext.channel.common.InstructionCommand.Data\x1a\x8c\x01\n\x06Header\x12\x11\n\tuserRefId\x18\x01 \x01(\t\x12\x16\n\x0e\x63orporateRefId\x18\x02 \x01(\t\x12\x0c\n\x04role\x18\x03 \x01(\t\x12\x0f\n\x07\x63hannel\x18\x04 \x01(\t\x12\x15\n\rcorrelationId\x18\x05 \x01(\t\x12\x11\n\teventType\x18\x06 \x01(\t\x12\x0e\n\x06userId\x18\x07 \x01(\t\x1a\x82\x01\n\x10PayeeInformation\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\taccountNo\x18\x02 \x01(\t\x12\x10\n\x08\x62\x61nkName\x18\x03 \x01(\t\x12\x10\n\x08\x62illerNo\x18\x04 \x01(\t\x12\x0c\n\x04ref1\x18\x05 \x01(\t\x12\x1b\n\x13\x66\x61voriteBillerRefId\x18\x06 \x01(\t\x1a\x45\n\x10PayerInformation\x12\x0e\n\x06nameTh\x18\x01 \x01(\t\x12\x0e\n\x06nameEn\x18\x02 \x01(\t\x12\x11\n\taccountNo\x18\x03 \x01(\t\x1a\xc6\x02\n\x10\x46inancialDetails\x12\x1b\n\x13subInstructionRefNo\x18\x01 \x01(\t\x12\x19\n\x11transactionItemId\x18\x02 \x01(\t\x12\x10\n\x08\x64\x61tetime\x18\x03 \x01(\t\x12\x12\n\nsubService\x18\x04 \x01(\t\x12\\\n\x06\x61mount\x18\x05 \x01(\x0b\x32L.th.co.ktb.biznext.channel.common.InstructionCommand.FinancialDetails.Amount\x12\x15\n\rfromAccountNo\x18\x06 \x01(\t\x12\x13\n\x0b\x62illerRefId\x18\x07 \x01(\t\x12\x1e\n\x16isRecurringTransaction\x18\x08 \x01(\t\x1a*\n\x06\x41mount\x12\x0e\n\x06\x61mount\x18\x01 \x01(\t\x12\x10\n\x08\x63urrency\x18\x02 \x01(\t\x1a\xbc\x01\n\x16\x46inancialDetailSummary\x12\x12\n\nsubService\x18\x01 \x01(\t\x12\x62\n\x06\x61mount\x18\x02 \x01(\x0b\x32R.th.co.ktb.biznext.channel.common.InstructionCommand.FinancialDetailSummary.Amount\x1a*\n\x06\x41mount\x12\x0e\n\x06\x61mount\x18\x01 \x01(\t\x12\x10\n\x08\x63urrency\x18\x02 \x01(\t\x1a\xe0\x05\n\x04\x44\x61ta\x12\x10\n\x08\x64\x61tetime\x18\x01 \x01(\t\x12\x0f\n\x07service\x18\x02 \x01(\t\x12\x12\n\nsubService\x18\x03 \x03(\t\x12\x17\n\x0finstructionType\x18\x04 \x01(\t\x12\x18\n\x10instructionRefNo\x18\x05 \x01(\t\x12_\n\x10payeeInformation\x18\x06 \x01(\x0b\x32\x45.th.co.ktb.biznext.channel.common.InstructionCommand.PayeeInformation\x12_\n\x10payerInformation\x18\x07 \x01(\x0b\x32\x45.th.co.ktb.biznext.channel.common.InstructionCommand.PayerInformation\x12_\n\x10\x66inancialDetails\x18\x08 \x03(\x0b\x32\x45.th.co.ktb.biznext.channel.common.InstructionCommand.FinancialDetails\x12\x14\n\x0c\x63urrencyCode\x18\t \x01(\t\x12\x0e\n\x06\x61mount\x18\n \x01(\t\x12\x0c\n\x04note\x18\x0b \x01(\t\x12\r\n\x05isWht\x18\x0c \x01(\x08\x12\x15\n\rsourceOrderId\x18\r \x01(\t\x12\x1f\n\x17\x64iscardedSourceOrderIds\x18\x0e \x03(\t\x12\x10\n\x08metadata\x18\x0f \x01(\t\x12\x1c\n\x14numberOfTransactions\x18\x10 \x01(\x05\x12k\n\x16\x66inancialDetailSummary\x18\x11 \x03(\x0b\x32K.th.co.ktb.biznext.channel.common.InstructionCommand.FinancialDetailSummary\x12\x1e\n\x16isRecurringTransaction\x18\x12 \x01(\t\x12\x13\n\x0b\x62illerRefId\x18\x13 \x01(\tB\x1c\x42\x1aInstructionCommandProtobufb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'instruction_command_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'B\032InstructionCommandProtobuf'
  _INSTRUCTIONCOMMAND._serialized_start=64
  _INSTRUCTIONCOMMAND._serialized_end=1840
  _INSTRUCTIONCOMMAND_HEADER._serialized_start=237
  _INSTRUCTIONCOMMAND_HEADER._serialized_end=377
  _INSTRUCTIONCOMMAND_PAYEEINFORMATION._serialized_start=380
  _INSTRUCTIONCOMMAND_PAYEEINFORMATION._serialized_end=510
  _INSTRUCTIONCOMMAND_PAYERINFORMATION._serialized_start=512
  _INSTRUCTIONCOMMAND_PAYERINFORMATION._serialized_end=581
  _INSTRUCTIONCOMMAND_FINANCIALDETAILS._serialized_start=584
  _INSTRUCTIONCOMMAND_FINANCIALDETAILS._serialized_end=910
  _INSTRUCTIONCOMMAND_FINANCIALDETAILS_AMOUNT._serialized_start=868
  _INSTRUCTIONCOMMAND_FINANCIALDETAILS_AMOUNT._serialized_end=910
  _INSTRUCTIONCOMMAND_FINANCIALDETAILSUMMARY._serialized_start=913
  _INSTRUCTIONCOMMAND_FINANCIALDETAILSUMMARY._serialized_end=1101
  _INSTRUCTIONCOMMAND_FINANCIALDETAILSUMMARY_AMOUNT._serialized_start=868
  _INSTRUCTIONCOMMAND_FINANCIALDETAILSUMMARY_AMOUNT._serialized_end=910
  _INSTRUCTIONCOMMAND_DATA._serialized_start=1104
  _INSTRUCTIONCOMMAND_DATA._serialized_end=1840
# @@protoc_insertion_point(module_scope)
