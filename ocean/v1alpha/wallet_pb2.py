# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ocean/v1alpha/wallet.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ocean.v1alpha import types_pb2 as ocean_dot_v1alpha_dot_types__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1aocean/v1alpha/wallet.proto\x12\rocean.v1alpha\x1a\x19ocean/v1alpha/types.proto\"\x10\n\x0eGenSeedRequest\"-\n\x0fGenSeedResponse\x12\x1a\n\x08mnemonic\x18\x01 \x01(\tR\x08mnemonic\"M\n\x13\x43reateWalletRequest\x12\x1a\n\x08mnemonic\x18\x01 \x01(\tR\x08mnemonic\x12\x1a\n\x08password\x18\x03 \x01(\tR\x08password\"\x16\n\x14\x43reateWalletResponse\"+\n\rUnlockRequest\x12\x1a\n\x08password\x18\x01 \x01(\tR\x08password\"\x10\n\x0eUnlockResponse\"e\n\x15\x43hangePasswordRequest\x12)\n\x10\x63urrent_password\x18\x01 \x01(\tR\x0f\x63urrentPassword\x12!\n\x0cnew_password\x18\x02 \x01(\tR\x0bnewPassword\"\x18\n\x16\x43hangePasswordResponse\"N\n\x14RestoreWalletRequest\x12\x1a\n\x08mnemonic\x18\x01 \x01(\tR\x08mnemonic\x12\x1a\n\x08password\x18\x03 \x01(\tR\x08password\"\x17\n\x15RestoreWalletResponse\"\x0f\n\rStatusRequest\"f\n\x0eStatusResponse\x12 \n\x0binitialized\x18\x01 \x01(\x08R\x0binitialized\x12\x16\n\x06synced\x18\x02 \x01(\x08R\x06synced\x12\x1a\n\x08unlocked\x18\x03 \x01(\x08R\x08unlocked\"\x10\n\x0eGetInfoRequest\"\xde\x02\n\x0fGetInfoResponse\x12@\n\x07network\x18\x01 \x01(\x0e\x32&.ocean.v1alpha.GetInfoResponse.NetworkR\x07network\x12!\n\x0cnative_asset\x18\x02 \x01(\tR\x0bnativeAsset\x12\x1b\n\troot_path\x18\x03 \x01(\tR\x08rootPath\x12.\n\x13master_blinding_key\x18\x04 \x01(\tR\x11masterBlindingKey\x12\x36\n\x08\x61\x63\x63ounts\x18\x05 \x03(\x0b\x32\x1a.ocean.v1alpha.AccountInfoR\x08\x61\x63\x63ounts\"a\n\x07Network\x12\x17\n\x13NETWORK_UNSPECIFIED\x10\x00\x12\x13\n\x0fNETWORK_MAINNET\x10\x01\x12\x13\n\x0fNETWORK_TESTNET\x10\x02\x12\x13\n\x0fNETWORK_REGTEST\x10\x03\x32\xc5\x04\n\rWalletService\x12H\n\x07GenSeed\x12\x1d.ocean.v1alpha.GenSeedRequest\x1a\x1e.ocean.v1alpha.GenSeedResponse\x12W\n\x0c\x43reateWallet\x12\".ocean.v1alpha.CreateWalletRequest\x1a#.ocean.v1alpha.CreateWalletResponse\x12\x45\n\x06Unlock\x12\x1c.ocean.v1alpha.UnlockRequest\x1a\x1d.ocean.v1alpha.UnlockResponse\x12]\n\x0e\x43hangePassword\x12$.ocean.v1alpha.ChangePasswordRequest\x1a%.ocean.v1alpha.ChangePasswordResponse\x12Z\n\rRestoreWallet\x12#.ocean.v1alpha.RestoreWalletRequest\x1a$.ocean.v1alpha.RestoreWalletResponse\x12\x45\n\x06Status\x12\x1c.ocean.v1alpha.StatusRequest\x1a\x1d.ocean.v1alpha.StatusResponse\x12H\n\x07GetInfo\x12\x1d.ocean.v1alpha.GetInfoRequest\x1a\x1e.ocean.v1alpha.GetInfoResponseB\xd8\x01\n\x11\x63om.ocean.v1alphaB\x0bWalletProtoP\x01Zagithub.com/vulpemventures/ocean/api-spec/protobuf/ocean/v1alpha/gen/go/ocean/v1alpha;oceanv1alpha\xa2\x02\x03OXX\xaa\x02\rOcean.V1alpha\xca\x02\rOcean\\V1alpha\xe2\x02\x19Ocean\\V1alpha\\GPBMetadata\xea\x02\x0eOcean::V1alphab\x06proto3')



_GENSEEDREQUEST = DESCRIPTOR.message_types_by_name['GenSeedRequest']
_GENSEEDRESPONSE = DESCRIPTOR.message_types_by_name['GenSeedResponse']
_CREATEWALLETREQUEST = DESCRIPTOR.message_types_by_name['CreateWalletRequest']
_CREATEWALLETRESPONSE = DESCRIPTOR.message_types_by_name['CreateWalletResponse']
_UNLOCKREQUEST = DESCRIPTOR.message_types_by_name['UnlockRequest']
_UNLOCKRESPONSE = DESCRIPTOR.message_types_by_name['UnlockResponse']
_CHANGEPASSWORDREQUEST = DESCRIPTOR.message_types_by_name['ChangePasswordRequest']
_CHANGEPASSWORDRESPONSE = DESCRIPTOR.message_types_by_name['ChangePasswordResponse']
_RESTOREWALLETREQUEST = DESCRIPTOR.message_types_by_name['RestoreWalletRequest']
_RESTOREWALLETRESPONSE = DESCRIPTOR.message_types_by_name['RestoreWalletResponse']
_STATUSREQUEST = DESCRIPTOR.message_types_by_name['StatusRequest']
_STATUSRESPONSE = DESCRIPTOR.message_types_by_name['StatusResponse']
_GETINFOREQUEST = DESCRIPTOR.message_types_by_name['GetInfoRequest']
_GETINFORESPONSE = DESCRIPTOR.message_types_by_name['GetInfoResponse']
_GETINFORESPONSE_NETWORK = _GETINFORESPONSE.enum_types_by_name['Network']
GenSeedRequest = _reflection.GeneratedProtocolMessageType('GenSeedRequest', (_message.Message,), {
  'DESCRIPTOR' : _GENSEEDREQUEST,
  '__module__' : 'ocean.v1alpha.wallet_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1alpha.GenSeedRequest)
  })
_sym_db.RegisterMessage(GenSeedRequest)

GenSeedResponse = _reflection.GeneratedProtocolMessageType('GenSeedResponse', (_message.Message,), {
  'DESCRIPTOR' : _GENSEEDRESPONSE,
  '__module__' : 'ocean.v1alpha.wallet_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1alpha.GenSeedResponse)
  })
_sym_db.RegisterMessage(GenSeedResponse)

CreateWalletRequest = _reflection.GeneratedProtocolMessageType('CreateWalletRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEWALLETREQUEST,
  '__module__' : 'ocean.v1alpha.wallet_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1alpha.CreateWalletRequest)
  })
_sym_db.RegisterMessage(CreateWalletRequest)

CreateWalletResponse = _reflection.GeneratedProtocolMessageType('CreateWalletResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEWALLETRESPONSE,
  '__module__' : 'ocean.v1alpha.wallet_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1alpha.CreateWalletResponse)
  })
_sym_db.RegisterMessage(CreateWalletResponse)

UnlockRequest = _reflection.GeneratedProtocolMessageType('UnlockRequest', (_message.Message,), {
  'DESCRIPTOR' : _UNLOCKREQUEST,
  '__module__' : 'ocean.v1alpha.wallet_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1alpha.UnlockRequest)
  })
_sym_db.RegisterMessage(UnlockRequest)

UnlockResponse = _reflection.GeneratedProtocolMessageType('UnlockResponse', (_message.Message,), {
  'DESCRIPTOR' : _UNLOCKRESPONSE,
  '__module__' : 'ocean.v1alpha.wallet_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1alpha.UnlockResponse)
  })
_sym_db.RegisterMessage(UnlockResponse)

ChangePasswordRequest = _reflection.GeneratedProtocolMessageType('ChangePasswordRequest', (_message.Message,), {
  'DESCRIPTOR' : _CHANGEPASSWORDREQUEST,
  '__module__' : 'ocean.v1alpha.wallet_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1alpha.ChangePasswordRequest)
  })
_sym_db.RegisterMessage(ChangePasswordRequest)

ChangePasswordResponse = _reflection.GeneratedProtocolMessageType('ChangePasswordResponse', (_message.Message,), {
  'DESCRIPTOR' : _CHANGEPASSWORDRESPONSE,
  '__module__' : 'ocean.v1alpha.wallet_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1alpha.ChangePasswordResponse)
  })
_sym_db.RegisterMessage(ChangePasswordResponse)

RestoreWalletRequest = _reflection.GeneratedProtocolMessageType('RestoreWalletRequest', (_message.Message,), {
  'DESCRIPTOR' : _RESTOREWALLETREQUEST,
  '__module__' : 'ocean.v1alpha.wallet_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1alpha.RestoreWalletRequest)
  })
_sym_db.RegisterMessage(RestoreWalletRequest)

RestoreWalletResponse = _reflection.GeneratedProtocolMessageType('RestoreWalletResponse', (_message.Message,), {
  'DESCRIPTOR' : _RESTOREWALLETRESPONSE,
  '__module__' : 'ocean.v1alpha.wallet_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1alpha.RestoreWalletResponse)
  })
_sym_db.RegisterMessage(RestoreWalletResponse)

StatusRequest = _reflection.GeneratedProtocolMessageType('StatusRequest', (_message.Message,), {
  'DESCRIPTOR' : _STATUSREQUEST,
  '__module__' : 'ocean.v1alpha.wallet_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1alpha.StatusRequest)
  })
_sym_db.RegisterMessage(StatusRequest)

StatusResponse = _reflection.GeneratedProtocolMessageType('StatusResponse', (_message.Message,), {
  'DESCRIPTOR' : _STATUSRESPONSE,
  '__module__' : 'ocean.v1alpha.wallet_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1alpha.StatusResponse)
  })
_sym_db.RegisterMessage(StatusResponse)

GetInfoRequest = _reflection.GeneratedProtocolMessageType('GetInfoRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETINFOREQUEST,
  '__module__' : 'ocean.v1alpha.wallet_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1alpha.GetInfoRequest)
  })
_sym_db.RegisterMessage(GetInfoRequest)

GetInfoResponse = _reflection.GeneratedProtocolMessageType('GetInfoResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETINFORESPONSE,
  '__module__' : 'ocean.v1alpha.wallet_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1alpha.GetInfoResponse)
  })
_sym_db.RegisterMessage(GetInfoResponse)

_WALLETSERVICE = DESCRIPTOR.services_by_name['WalletService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\021com.ocean.v1alphaB\013WalletProtoP\001Zagithub.com/vulpemventures/ocean/api-spec/protobuf/ocean/v1alpha/gen/go/ocean/v1alpha;oceanv1alpha\242\002\003OXX\252\002\rOcean.V1alpha\312\002\rOcean\\V1alpha\342\002\031Ocean\\V1alpha\\GPBMetadata\352\002\016Ocean::V1alpha'
  _GENSEEDREQUEST._serialized_start=72
  _GENSEEDREQUEST._serialized_end=88
  _GENSEEDRESPONSE._serialized_start=90
  _GENSEEDRESPONSE._serialized_end=135
  _CREATEWALLETREQUEST._serialized_start=137
  _CREATEWALLETREQUEST._serialized_end=214
  _CREATEWALLETRESPONSE._serialized_start=216
  _CREATEWALLETRESPONSE._serialized_end=238
  _UNLOCKREQUEST._serialized_start=240
  _UNLOCKREQUEST._serialized_end=283
  _UNLOCKRESPONSE._serialized_start=285
  _UNLOCKRESPONSE._serialized_end=301
  _CHANGEPASSWORDREQUEST._serialized_start=303
  _CHANGEPASSWORDREQUEST._serialized_end=404
  _CHANGEPASSWORDRESPONSE._serialized_start=406
  _CHANGEPASSWORDRESPONSE._serialized_end=430
  _RESTOREWALLETREQUEST._serialized_start=432
  _RESTOREWALLETREQUEST._serialized_end=510
  _RESTOREWALLETRESPONSE._serialized_start=512
  _RESTOREWALLETRESPONSE._serialized_end=535
  _STATUSREQUEST._serialized_start=537
  _STATUSREQUEST._serialized_end=552
  _STATUSRESPONSE._serialized_start=554
  _STATUSRESPONSE._serialized_end=656
  _GETINFOREQUEST._serialized_start=658
  _GETINFOREQUEST._serialized_end=674
  _GETINFORESPONSE._serialized_start=677
  _GETINFORESPONSE._serialized_end=1027
  _GETINFORESPONSE_NETWORK._serialized_start=930
  _GETINFORESPONSE_NETWORK._serialized_end=1027
  _WALLETSERVICE._serialized_start=1030
  _WALLETSERVICE._serialized_end=1611
# @@protoc_insertion_point(module_scope)
