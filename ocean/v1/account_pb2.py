# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ocean/v1/account.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ocean.v1 import types_pb2 as ocean_dot_v1_dot_types__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16ocean/v1/account.proto\x12\x08ocean.v1\x1a\x14ocean/v1/types.proto\"/\n\x19\x43reateAccountBIP44Request\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\"\xa1\x01\n\x1a\x43reateAccountBIP44Response\x12!\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\tR\x0b\x61\x63\x63ountName\x12#\n\raccount_index\x18\x02 \x01(\rR\x0c\x61\x63\x63ountIndex\x12\x12\n\x04xpub\x18\x03 \x01(\tR\x04xpub\x12\'\n\x0f\x64\x65rivation_path\x18\x04 \x01(\tR\x0e\x64\x65rivationPath\"0\n\x1a\x43reateAccountCustomRequest\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\"}\n\x1b\x43reateAccountCustomResponse\x12!\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\tR\x0b\x61\x63\x63ountName\x12\'\n\x0f\x64\x65rivation_path\x18\x02 \x01(\tR\x0e\x64\x65rivationPath\x12\x12\n\x04xpub\x18\x03 \x01(\tR\x04xpub\"n\n\x19SetAccountTemplateRequest\x12!\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\tR\x0b\x61\x63\x63ountName\x12.\n\x08template\x18\x02 \x01(\x0b\x32\x12.ocean.v1.TemplateR\x08template\"\x1c\n\x1aSetAccountTemplateResponse\"e\n\x16\x44\x65riveAddressesRequest\x12!\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\tR\x0b\x61\x63\x63ountName\x12(\n\x10num_of_addresses\x18\x02 \x01(\x04R\x0enumOfAddresses\"7\n\x17\x44\x65riveAddressesResponse\x12\x1c\n\taddresses\x18\x01 \x03(\tR\taddresses\"k\n\x1c\x44\x65riveChangeAddressesRequest\x12!\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\tR\x0b\x61\x63\x63ountName\x12(\n\x10num_of_addresses\x18\x02 \x01(\x04R\x0enumOfAddresses\"=\n\x1d\x44\x65riveChangeAddressesResponse\x12\x1c\n\taddresses\x18\x01 \x03(\tR\taddresses\"9\n\x14ListAddressesRequest\x12!\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\tR\x0b\x61\x63\x63ountName\"5\n\x15ListAddressesResponse\x12\x1c\n\taddresses\x18\x01 \x03(\tR\taddresses\"Q\n\x0e\x42\x61lanceRequest\x12!\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\tR\x0b\x61\x63\x63ountName\x12\x1c\n\taddresses\x18\x03 \x03(\tR\taddresses\"\xa6\x01\n\x0f\x42\x61lanceResponse\x12@\n\x07\x62\x61lance\x18\x01 \x03(\x0b\x32&.ocean.v1.BalanceResponse.BalanceEntryR\x07\x62\x61lance\x1aQ\n\x0c\x42\x61lanceEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12+\n\x05value\x18\x02 \x01(\x0b\x32\x15.ocean.v1.BalanceInfoR\x05value:\x02\x38\x01\"S\n\x10ListUtxosRequest\x12!\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\tR\x0b\x61\x63\x63ountName\x12\x1c\n\taddresses\x18\x03 \x03(\tR\taddresses\"\x81\x01\n\x11ListUtxosResponse\x12\x38\n\x0fspendable_utxos\x18\x01 \x01(\x0b\x32\x0f.ocean.v1.UtxosR\x0espendableUtxos\x12\x32\n\x0clocked_utxos\x18\x02 \x01(\x0b\x32\x0f.ocean.v1.UtxosR\x0blockedUtxos\"9\n\x14\x44\x65leteAccountRequest\x12!\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\tR\x0b\x61\x63\x63ountName\"\x17\n\x15\x44\x65leteAccountResponse2\xa2\x06\n\x0e\x41\x63\x63ountService\x12_\n\x12\x43reateAccountBIP44\x12#.ocean.v1.CreateAccountBIP44Request\x1a$.ocean.v1.CreateAccountBIP44Response\x12\x62\n\x13\x43reateAccountCustom\x12$.ocean.v1.CreateAccountCustomRequest\x1a%.ocean.v1.CreateAccountCustomResponse\x12_\n\x12SetAccountTemplate\x12#.ocean.v1.SetAccountTemplateRequest\x1a$.ocean.v1.SetAccountTemplateResponse\x12V\n\x0f\x44\x65riveAddresses\x12 .ocean.v1.DeriveAddressesRequest\x1a!.ocean.v1.DeriveAddressesResponse\x12h\n\x15\x44\x65riveChangeAddresses\x12&.ocean.v1.DeriveChangeAddressesRequest\x1a\'.ocean.v1.DeriveChangeAddressesResponse\x12P\n\rListAddresses\x12\x1e.ocean.v1.ListAddressesRequest\x1a\x1f.ocean.v1.ListAddressesResponse\x12>\n\x07\x42\x61lance\x12\x18.ocean.v1.BalanceRequest\x1a\x19.ocean.v1.BalanceResponse\x12\x44\n\tListUtxos\x12\x1a.ocean.v1.ListUtxosRequest\x1a\x1b.ocean.v1.ListUtxosResponse\x12P\n\rDeleteAccount\x12\x1e.ocean.v1.DeleteAccountRequest\x1a\x1f.ocean.v1.DeleteAccountResponseb\x06proto3')



_CREATEACCOUNTBIP44REQUEST = DESCRIPTOR.message_types_by_name['CreateAccountBIP44Request']
_CREATEACCOUNTBIP44RESPONSE = DESCRIPTOR.message_types_by_name['CreateAccountBIP44Response']
_CREATEACCOUNTCUSTOMREQUEST = DESCRIPTOR.message_types_by_name['CreateAccountCustomRequest']
_CREATEACCOUNTCUSTOMRESPONSE = DESCRIPTOR.message_types_by_name['CreateAccountCustomResponse']
_SETACCOUNTTEMPLATEREQUEST = DESCRIPTOR.message_types_by_name['SetAccountTemplateRequest']
_SETACCOUNTTEMPLATERESPONSE = DESCRIPTOR.message_types_by_name['SetAccountTemplateResponse']
_DERIVEADDRESSESREQUEST = DESCRIPTOR.message_types_by_name['DeriveAddressesRequest']
_DERIVEADDRESSESRESPONSE = DESCRIPTOR.message_types_by_name['DeriveAddressesResponse']
_DERIVECHANGEADDRESSESREQUEST = DESCRIPTOR.message_types_by_name['DeriveChangeAddressesRequest']
_DERIVECHANGEADDRESSESRESPONSE = DESCRIPTOR.message_types_by_name['DeriveChangeAddressesResponse']
_LISTADDRESSESREQUEST = DESCRIPTOR.message_types_by_name['ListAddressesRequest']
_LISTADDRESSESRESPONSE = DESCRIPTOR.message_types_by_name['ListAddressesResponse']
_BALANCEREQUEST = DESCRIPTOR.message_types_by_name['BalanceRequest']
_BALANCERESPONSE = DESCRIPTOR.message_types_by_name['BalanceResponse']
_BALANCERESPONSE_BALANCEENTRY = _BALANCERESPONSE.nested_types_by_name['BalanceEntry']
_LISTUTXOSREQUEST = DESCRIPTOR.message_types_by_name['ListUtxosRequest']
_LISTUTXOSRESPONSE = DESCRIPTOR.message_types_by_name['ListUtxosResponse']
_DELETEACCOUNTREQUEST = DESCRIPTOR.message_types_by_name['DeleteAccountRequest']
_DELETEACCOUNTRESPONSE = DESCRIPTOR.message_types_by_name['DeleteAccountResponse']
CreateAccountBIP44Request = _reflection.GeneratedProtocolMessageType('CreateAccountBIP44Request', (_message.Message,), {
  'DESCRIPTOR' : _CREATEACCOUNTBIP44REQUEST,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.CreateAccountBIP44Request)
  })
_sym_db.RegisterMessage(CreateAccountBIP44Request)

CreateAccountBIP44Response = _reflection.GeneratedProtocolMessageType('CreateAccountBIP44Response', (_message.Message,), {
  'DESCRIPTOR' : _CREATEACCOUNTBIP44RESPONSE,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.CreateAccountBIP44Response)
  })
_sym_db.RegisterMessage(CreateAccountBIP44Response)

CreateAccountCustomRequest = _reflection.GeneratedProtocolMessageType('CreateAccountCustomRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEACCOUNTCUSTOMREQUEST,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.CreateAccountCustomRequest)
  })
_sym_db.RegisterMessage(CreateAccountCustomRequest)

CreateAccountCustomResponse = _reflection.GeneratedProtocolMessageType('CreateAccountCustomResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEACCOUNTCUSTOMRESPONSE,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.CreateAccountCustomResponse)
  })
_sym_db.RegisterMessage(CreateAccountCustomResponse)

SetAccountTemplateRequest = _reflection.GeneratedProtocolMessageType('SetAccountTemplateRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETACCOUNTTEMPLATEREQUEST,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.SetAccountTemplateRequest)
  })
_sym_db.RegisterMessage(SetAccountTemplateRequest)

SetAccountTemplateResponse = _reflection.GeneratedProtocolMessageType('SetAccountTemplateResponse', (_message.Message,), {
  'DESCRIPTOR' : _SETACCOUNTTEMPLATERESPONSE,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.SetAccountTemplateResponse)
  })
_sym_db.RegisterMessage(SetAccountTemplateResponse)

DeriveAddressesRequest = _reflection.GeneratedProtocolMessageType('DeriveAddressesRequest', (_message.Message,), {
  'DESCRIPTOR' : _DERIVEADDRESSESREQUEST,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.DeriveAddressesRequest)
  })
_sym_db.RegisterMessage(DeriveAddressesRequest)

DeriveAddressesResponse = _reflection.GeneratedProtocolMessageType('DeriveAddressesResponse', (_message.Message,), {
  'DESCRIPTOR' : _DERIVEADDRESSESRESPONSE,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.DeriveAddressesResponse)
  })
_sym_db.RegisterMessage(DeriveAddressesResponse)

DeriveChangeAddressesRequest = _reflection.GeneratedProtocolMessageType('DeriveChangeAddressesRequest', (_message.Message,), {
  'DESCRIPTOR' : _DERIVECHANGEADDRESSESREQUEST,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.DeriveChangeAddressesRequest)
  })
_sym_db.RegisterMessage(DeriveChangeAddressesRequest)

DeriveChangeAddressesResponse = _reflection.GeneratedProtocolMessageType('DeriveChangeAddressesResponse', (_message.Message,), {
  'DESCRIPTOR' : _DERIVECHANGEADDRESSESRESPONSE,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.DeriveChangeAddressesResponse)
  })
_sym_db.RegisterMessage(DeriveChangeAddressesResponse)

ListAddressesRequest = _reflection.GeneratedProtocolMessageType('ListAddressesRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTADDRESSESREQUEST,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.ListAddressesRequest)
  })
_sym_db.RegisterMessage(ListAddressesRequest)

ListAddressesResponse = _reflection.GeneratedProtocolMessageType('ListAddressesResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTADDRESSESRESPONSE,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.ListAddressesResponse)
  })
_sym_db.RegisterMessage(ListAddressesResponse)

BalanceRequest = _reflection.GeneratedProtocolMessageType('BalanceRequest', (_message.Message,), {
  'DESCRIPTOR' : _BALANCEREQUEST,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.BalanceRequest)
  })
_sym_db.RegisterMessage(BalanceRequest)

BalanceResponse = _reflection.GeneratedProtocolMessageType('BalanceResponse', (_message.Message,), {

  'BalanceEntry' : _reflection.GeneratedProtocolMessageType('BalanceEntry', (_message.Message,), {
    'DESCRIPTOR' : _BALANCERESPONSE_BALANCEENTRY,
    '__module__' : 'ocean.v1.account_pb2'
    # @@protoc_insertion_point(class_scope:ocean.v1.BalanceResponse.BalanceEntry)
    })
  ,
  'DESCRIPTOR' : _BALANCERESPONSE,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.BalanceResponse)
  })
_sym_db.RegisterMessage(BalanceResponse)
_sym_db.RegisterMessage(BalanceResponse.BalanceEntry)

ListUtxosRequest = _reflection.GeneratedProtocolMessageType('ListUtxosRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTUTXOSREQUEST,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.ListUtxosRequest)
  })
_sym_db.RegisterMessage(ListUtxosRequest)

ListUtxosResponse = _reflection.GeneratedProtocolMessageType('ListUtxosResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTUTXOSRESPONSE,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.ListUtxosResponse)
  })
_sym_db.RegisterMessage(ListUtxosResponse)

DeleteAccountRequest = _reflection.GeneratedProtocolMessageType('DeleteAccountRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEACCOUNTREQUEST,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.DeleteAccountRequest)
  })
_sym_db.RegisterMessage(DeleteAccountRequest)

DeleteAccountResponse = _reflection.GeneratedProtocolMessageType('DeleteAccountResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETEACCOUNTRESPONSE,
  '__module__' : 'ocean.v1.account_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.DeleteAccountResponse)
  })
_sym_db.RegisterMessage(DeleteAccountResponse)

_ACCOUNTSERVICE = DESCRIPTOR.services_by_name['AccountService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _BALANCERESPONSE_BALANCEENTRY._options = None
  _BALANCERESPONSE_BALANCEENTRY._serialized_options = b'8\001'
  _CREATEACCOUNTBIP44REQUEST._serialized_start=58
  _CREATEACCOUNTBIP44REQUEST._serialized_end=105
  _CREATEACCOUNTBIP44RESPONSE._serialized_start=108
  _CREATEACCOUNTBIP44RESPONSE._serialized_end=269
  _CREATEACCOUNTCUSTOMREQUEST._serialized_start=271
  _CREATEACCOUNTCUSTOMREQUEST._serialized_end=319
  _CREATEACCOUNTCUSTOMRESPONSE._serialized_start=321
  _CREATEACCOUNTCUSTOMRESPONSE._serialized_end=446
  _SETACCOUNTTEMPLATEREQUEST._serialized_start=448
  _SETACCOUNTTEMPLATEREQUEST._serialized_end=558
  _SETACCOUNTTEMPLATERESPONSE._serialized_start=560
  _SETACCOUNTTEMPLATERESPONSE._serialized_end=588
  _DERIVEADDRESSESREQUEST._serialized_start=590
  _DERIVEADDRESSESREQUEST._serialized_end=691
  _DERIVEADDRESSESRESPONSE._serialized_start=693
  _DERIVEADDRESSESRESPONSE._serialized_end=748
  _DERIVECHANGEADDRESSESREQUEST._serialized_start=750
  _DERIVECHANGEADDRESSESREQUEST._serialized_end=857
  _DERIVECHANGEADDRESSESRESPONSE._serialized_start=859
  _DERIVECHANGEADDRESSESRESPONSE._serialized_end=920
  _LISTADDRESSESREQUEST._serialized_start=922
  _LISTADDRESSESREQUEST._serialized_end=979
  _LISTADDRESSESRESPONSE._serialized_start=981
  _LISTADDRESSESRESPONSE._serialized_end=1034
  _BALANCEREQUEST._serialized_start=1036
  _BALANCEREQUEST._serialized_end=1117
  _BALANCERESPONSE._serialized_start=1120
  _BALANCERESPONSE._serialized_end=1286
  _BALANCERESPONSE_BALANCEENTRY._serialized_start=1205
  _BALANCERESPONSE_BALANCEENTRY._serialized_end=1286
  _LISTUTXOSREQUEST._serialized_start=1288
  _LISTUTXOSREQUEST._serialized_end=1371
  _LISTUTXOSRESPONSE._serialized_start=1374
  _LISTUTXOSRESPONSE._serialized_end=1503
  _DELETEACCOUNTREQUEST._serialized_start=1505
  _DELETEACCOUNTREQUEST._serialized_end=1562
  _DELETEACCOUNTRESPONSE._serialized_start=1564
  _DELETEACCOUNTRESPONSE._serialized_end=1587
  _ACCOUNTSERVICE._serialized_start=1590
  _ACCOUNTSERVICE._serialized_end=2392
# @@protoc_insertion_point(module_scope)