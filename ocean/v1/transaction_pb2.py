# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ocean/v1/transaction.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ocean.v1 import types_pb2 as ocean_dot_v1_dot_types__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1aocean/v1/transaction.proto\x12\x08ocean.v1\x1a\x14ocean/v1/types.proto\"+\n\x15GetTransactionRequest\x12\x12\n\x04txid\x18\x01 \x01(\tR\x04txid\"l\n\x16GetTransactionResponse\x12\x15\n\x06tx_hex\x18\x01 \x01(\tR\x05txHex\x12;\n\rblock_details\x18\x02 \x01(\x0b\x32\x16.ocean.v1.BlockDetailsR\x0c\x62lockDetails\"\x9a\x02\n\x12SelectUtxosRequest\x12!\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\tR\x0b\x61\x63\x63ountName\x12!\n\x0ctarget_asset\x18\x02 \x01(\tR\x0btargetAsset\x12#\n\rtarget_amount\x18\x03 \x01(\x04R\x0ctargetAmount\x12\x41\n\x08strategy\x18\x04 \x01(\x0e\x32%.ocean.v1.SelectUtxosRequest.StrategyR\x08strategy\"V\n\x08Strategy\x12\x18\n\x14STRATEGY_UNSPECIFIED\x10\x00\x12\x19\n\x15STRATEGY_BRANCH_BOUND\x10\x01\x12\x15\n\x11STRATEGY_FRAGMENT\x10\x02\"|\n\x13SelectUtxosResponse\x12$\n\x05utxos\x18\x01 \x03(\x0b\x32\x0e.ocean.v1.UtxoR\x05utxos\x12\x16\n\x06\x63hange\x18\x02 \x01(\x04R\x06\x63hange\x12\'\n\x0f\x65xpiration_date\x18\x03 \x01(\x03R\x0e\x65xpirationDate\"\x98\x01\n\x13\x45stimateFeesRequest\x12\'\n\x06inputs\x18\x01 \x03(\x0b\x32\x0f.ocean.v1.InputR\x06inputs\x12*\n\x07outputs\x18\x02 \x03(\x0b\x32\x10.ocean.v1.OutputR\x07outputs\x12,\n\x12millisats_per_byte\x18\x03 \x01(\x04R\x10millisatsPerByte\"5\n\x14\x45stimateFeesResponse\x12\x1d\n\nfee_amount\x18\x01 \x01(\x04R\tfeeAmount\"R\n\x16SignTransactionRequest\x12\x15\n\x06tx_hex\x18\x01 \x01(\tR\x05txHex\x12!\n\x0csighash_type\x18\x02 \x01(\rR\x0bsighashType\"0\n\x17SignTransactionResponse\x12\x15\n\x06tx_hex\x18\x01 \x01(\tR\x05txHex\"4\n\x1b\x42roadcastTransactionRequest\x12\x15\n\x06tx_hex\x18\x01 \x01(\tR\x05txHex\"2\n\x1c\x42roadcastTransactionResponse\x12\x12\n\x04txid\x18\x01 \x01(\tR\x04txid\"h\n\x11\x43reatePsetRequest\x12\'\n\x06inputs\x18\x01 \x03(\x0b\x32\x0f.ocean.v1.InputR\x06inputs\x12*\n\x07outputs\x18\x02 \x03(\x0b\x32\x10.ocean.v1.OutputR\x07outputs\"(\n\x12\x43reatePsetResponse\x12\x12\n\x04pset\x18\x01 \x01(\tR\x04pset\"|\n\x11UpdatePsetRequest\x12\x12\n\x04pset\x18\x01 \x01(\tR\x04pset\x12\'\n\x06inputs\x18\x02 \x03(\x0b\x32\x0f.ocean.v1.InputR\x06inputs\x12*\n\x07outputs\x18\x03 \x03(\x0b\x32\x10.ocean.v1.OutputR\x07outputs\"(\n\x12UpdatePsetResponse\x12\x12\n\x04pset\x18\x01 \x01(\tR\x04pset\"\x99\x01\n\x10\x42lindPsetRequest\x12\x12\n\x04pset\x18\x01 \x01(\tR\x04pset\x12!\n\x0clast_blinder\x18\x02 \x01(\x08R\x0blastBlinder\x12N\n\x16\x65xtra_unblinded_inputs\x18\x03 \x03(\x0b\x32\x18.ocean.v1.UnblindedInputR\x14\x65xtraUnblindedInputs\"\'\n\x11\x42lindPsetResponse\x12\x12\n\x04pset\x18\x01 \x01(\tR\x04pset\"H\n\x0fSignPsetRequest\x12\x12\n\x04pset\x18\x01 \x01(\tR\x04pset\x12!\n\x0csighash_type\x18\x02 \x01(\rR\x0bsighashType\"&\n\x10SignPsetResponse\x12\x12\n\x04pset\x18\x01 \x01(\tR\x04pset\"\x89\x02\n\x0bMintRequest\x12!\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\tR\x0b\x61\x63\x63ountName\x12!\n\x0c\x61sset_amount\x18\x02 \x01(\x04R\x0b\x61ssetAmount\x12!\n\x0ctoken_amount\x18\x03 \x01(\x04R\x0btokenAmount\x12\x1d\n\nasset_name\x18\x04 \x01(\tR\tassetName\x12!\n\x0c\x61sset_ticker\x18\x05 \x01(\tR\x0b\x61ssetTicker\x12!\n\x0c\x61sset_domain\x18\x06 \x01(\tR\x0b\x61ssetDomain\x12,\n\x12millisats_per_byte\x18\x07 \x01(\x04R\x10millisatsPerByte\"%\n\x0cMintResponse\x12\x15\n\x06tx_hex\x18\x01 \x01(\tR\x05txHex\"\x8e\x01\n\rRemintRequest\x12!\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\tR\x0b\x61\x63\x63ountName\x12\x14\n\x05\x61sset\x18\x02 \x01(\tR\x05\x61sset\x12\x16\n\x06\x61mount\x18\x03 \x01(\x04R\x06\x61mount\x12,\n\x12millisats_per_byte\x18\x04 \x01(\x04R\x10millisatsPerByte\"\'\n\x0eRemintResponse\x12\x15\n\x06tx_hex\x18\x01 \x01(\tR\x05txHex\"\x8e\x01\n\x0b\x42urnRequest\x12!\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\tR\x0b\x61\x63\x63ountName\x12.\n\treceivers\x18\x02 \x03(\x0b\x32\x10.ocean.v1.OutputR\treceivers\x12,\n\x12millisats_per_byte\x18\x03 \x01(\x04R\x10millisatsPerByte\"%\n\x0c\x42urnResponse\x12\x15\n\x06tx_hex\x18\x01 \x01(\tR\x05txHex\"\x92\x01\n\x0fTransferRequest\x12!\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\tR\x0b\x61\x63\x63ountName\x12.\n\treceivers\x18\x02 \x03(\x0b\x32\x10.ocean.v1.OutputR\treceivers\x12,\n\x12millisats_per_byte\x18\x03 \x01(\x04R\x10millisatsPerByte\")\n\x10TransferResponse\x12\x15\n\x06tx_hex\x18\x01 \x01(\tR\x05txHex\"\x15\n\x13PegInAddressRequest\"\x8a\x01\n\x14PegInAddressResponse\x12!\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\tR\x0b\x61\x63\x63ountName\x12,\n\x12main_chain_address\x18\x02 \x01(\tR\x10mainChainAddress\x12!\n\x0c\x63laim_script\x18\x03 \x01(\tR\x0b\x63laimScript\"w\n\x11\x43laimPegInRequest\x12\x1d\n\nbitcoin_tx\x18\x01 \x01(\tR\tbitcoinTx\x12 \n\x0ctx_out_proof\x18\x02 \x01(\tR\ntxOutProof\x12!\n\x0c\x63laim_script\x18\x03 \x01(\tR\x0b\x63laimScript\"+\n\x12\x43laimPegInResponse\x12\x15\n\x06tx_hex\x18\x01 \x01(\tR\x05txHex2\xe4\x08\n\x12TransactionService\x12S\n\x0eGetTransaction\x12\x1f.ocean.v1.GetTransactionRequest\x1a .ocean.v1.GetTransactionResponse\x12J\n\x0bSelectUtxos\x12\x1c.ocean.v1.SelectUtxosRequest\x1a\x1d.ocean.v1.SelectUtxosResponse\x12M\n\x0c\x45stimateFees\x12\x1d.ocean.v1.EstimateFeesRequest\x1a\x1e.ocean.v1.EstimateFeesResponse\x12V\n\x0fSignTransaction\x12 .ocean.v1.SignTransactionRequest\x1a!.ocean.v1.SignTransactionResponse\x12\x65\n\x14\x42roadcastTransaction\x12%.ocean.v1.BroadcastTransactionRequest\x1a&.ocean.v1.BroadcastTransactionResponse\x12G\n\nCreatePset\x12\x1b.ocean.v1.CreatePsetRequest\x1a\x1c.ocean.v1.CreatePsetResponse\x12G\n\nUpdatePset\x12\x1b.ocean.v1.UpdatePsetRequest\x1a\x1c.ocean.v1.UpdatePsetResponse\x12\x44\n\tBlindPset\x12\x1a.ocean.v1.BlindPsetRequest\x1a\x1b.ocean.v1.BlindPsetResponse\x12\x41\n\x08SignPset\x12\x19.ocean.v1.SignPsetRequest\x1a\x1a.ocean.v1.SignPsetResponse\x12\x35\n\x04Mint\x12\x15.ocean.v1.MintRequest\x1a\x16.ocean.v1.MintResponse\x12;\n\x06Remint\x12\x17.ocean.v1.RemintRequest\x1a\x18.ocean.v1.RemintResponse\x12\x35\n\x04\x42urn\x12\x15.ocean.v1.BurnRequest\x1a\x16.ocean.v1.BurnResponse\x12\x41\n\x08Transfer\x12\x19.ocean.v1.TransferRequest\x1a\x1a.ocean.v1.TransferResponse\x12M\n\x0cPegInAddress\x12\x1d.ocean.v1.PegInAddressRequest\x1a\x1e.ocean.v1.PegInAddressResponse\x12G\n\nClaimPegIn\x12\x1b.ocean.v1.ClaimPegInRequest\x1a\x1c.ocean.v1.ClaimPegInResponseb\x06proto3')



_GETTRANSACTIONREQUEST = DESCRIPTOR.message_types_by_name['GetTransactionRequest']
_GETTRANSACTIONRESPONSE = DESCRIPTOR.message_types_by_name['GetTransactionResponse']
_SELECTUTXOSREQUEST = DESCRIPTOR.message_types_by_name['SelectUtxosRequest']
_SELECTUTXOSRESPONSE = DESCRIPTOR.message_types_by_name['SelectUtxosResponse']
_ESTIMATEFEESREQUEST = DESCRIPTOR.message_types_by_name['EstimateFeesRequest']
_ESTIMATEFEESRESPONSE = DESCRIPTOR.message_types_by_name['EstimateFeesResponse']
_SIGNTRANSACTIONREQUEST = DESCRIPTOR.message_types_by_name['SignTransactionRequest']
_SIGNTRANSACTIONRESPONSE = DESCRIPTOR.message_types_by_name['SignTransactionResponse']
_BROADCASTTRANSACTIONREQUEST = DESCRIPTOR.message_types_by_name['BroadcastTransactionRequest']
_BROADCASTTRANSACTIONRESPONSE = DESCRIPTOR.message_types_by_name['BroadcastTransactionResponse']
_CREATEPSETREQUEST = DESCRIPTOR.message_types_by_name['CreatePsetRequest']
_CREATEPSETRESPONSE = DESCRIPTOR.message_types_by_name['CreatePsetResponse']
_UPDATEPSETREQUEST = DESCRIPTOR.message_types_by_name['UpdatePsetRequest']
_UPDATEPSETRESPONSE = DESCRIPTOR.message_types_by_name['UpdatePsetResponse']
_BLINDPSETREQUEST = DESCRIPTOR.message_types_by_name['BlindPsetRequest']
_BLINDPSETRESPONSE = DESCRIPTOR.message_types_by_name['BlindPsetResponse']
_SIGNPSETREQUEST = DESCRIPTOR.message_types_by_name['SignPsetRequest']
_SIGNPSETRESPONSE = DESCRIPTOR.message_types_by_name['SignPsetResponse']
_MINTREQUEST = DESCRIPTOR.message_types_by_name['MintRequest']
_MINTRESPONSE = DESCRIPTOR.message_types_by_name['MintResponse']
_REMINTREQUEST = DESCRIPTOR.message_types_by_name['RemintRequest']
_REMINTRESPONSE = DESCRIPTOR.message_types_by_name['RemintResponse']
_BURNREQUEST = DESCRIPTOR.message_types_by_name['BurnRequest']
_BURNRESPONSE = DESCRIPTOR.message_types_by_name['BurnResponse']
_TRANSFERREQUEST = DESCRIPTOR.message_types_by_name['TransferRequest']
_TRANSFERRESPONSE = DESCRIPTOR.message_types_by_name['TransferResponse']
_PEGINADDRESSREQUEST = DESCRIPTOR.message_types_by_name['PegInAddressRequest']
_PEGINADDRESSRESPONSE = DESCRIPTOR.message_types_by_name['PegInAddressResponse']
_CLAIMPEGINREQUEST = DESCRIPTOR.message_types_by_name['ClaimPegInRequest']
_CLAIMPEGINRESPONSE = DESCRIPTOR.message_types_by_name['ClaimPegInResponse']
_SELECTUTXOSREQUEST_STRATEGY = _SELECTUTXOSREQUEST.enum_types_by_name['Strategy']
GetTransactionRequest = _reflection.GeneratedProtocolMessageType('GetTransactionRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETTRANSACTIONREQUEST,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.GetTransactionRequest)
  })
_sym_db.RegisterMessage(GetTransactionRequest)

GetTransactionResponse = _reflection.GeneratedProtocolMessageType('GetTransactionResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETTRANSACTIONRESPONSE,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.GetTransactionResponse)
  })
_sym_db.RegisterMessage(GetTransactionResponse)

SelectUtxosRequest = _reflection.GeneratedProtocolMessageType('SelectUtxosRequest', (_message.Message,), {
  'DESCRIPTOR' : _SELECTUTXOSREQUEST,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.SelectUtxosRequest)
  })
_sym_db.RegisterMessage(SelectUtxosRequest)

SelectUtxosResponse = _reflection.GeneratedProtocolMessageType('SelectUtxosResponse', (_message.Message,), {
  'DESCRIPTOR' : _SELECTUTXOSRESPONSE,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.SelectUtxosResponse)
  })
_sym_db.RegisterMessage(SelectUtxosResponse)

EstimateFeesRequest = _reflection.GeneratedProtocolMessageType('EstimateFeesRequest', (_message.Message,), {
  'DESCRIPTOR' : _ESTIMATEFEESREQUEST,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.EstimateFeesRequest)
  })
_sym_db.RegisterMessage(EstimateFeesRequest)

EstimateFeesResponse = _reflection.GeneratedProtocolMessageType('EstimateFeesResponse', (_message.Message,), {
  'DESCRIPTOR' : _ESTIMATEFEESRESPONSE,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.EstimateFeesResponse)
  })
_sym_db.RegisterMessage(EstimateFeesResponse)

SignTransactionRequest = _reflection.GeneratedProtocolMessageType('SignTransactionRequest', (_message.Message,), {
  'DESCRIPTOR' : _SIGNTRANSACTIONREQUEST,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.SignTransactionRequest)
  })
_sym_db.RegisterMessage(SignTransactionRequest)

SignTransactionResponse = _reflection.GeneratedProtocolMessageType('SignTransactionResponse', (_message.Message,), {
  'DESCRIPTOR' : _SIGNTRANSACTIONRESPONSE,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.SignTransactionResponse)
  })
_sym_db.RegisterMessage(SignTransactionResponse)

BroadcastTransactionRequest = _reflection.GeneratedProtocolMessageType('BroadcastTransactionRequest', (_message.Message,), {
  'DESCRIPTOR' : _BROADCASTTRANSACTIONREQUEST,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.BroadcastTransactionRequest)
  })
_sym_db.RegisterMessage(BroadcastTransactionRequest)

BroadcastTransactionResponse = _reflection.GeneratedProtocolMessageType('BroadcastTransactionResponse', (_message.Message,), {
  'DESCRIPTOR' : _BROADCASTTRANSACTIONRESPONSE,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.BroadcastTransactionResponse)
  })
_sym_db.RegisterMessage(BroadcastTransactionResponse)

CreatePsetRequest = _reflection.GeneratedProtocolMessageType('CreatePsetRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEPSETREQUEST,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.CreatePsetRequest)
  })
_sym_db.RegisterMessage(CreatePsetRequest)

CreatePsetResponse = _reflection.GeneratedProtocolMessageType('CreatePsetResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEPSETRESPONSE,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.CreatePsetResponse)
  })
_sym_db.RegisterMessage(CreatePsetResponse)

UpdatePsetRequest = _reflection.GeneratedProtocolMessageType('UpdatePsetRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEPSETREQUEST,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.UpdatePsetRequest)
  })
_sym_db.RegisterMessage(UpdatePsetRequest)

UpdatePsetResponse = _reflection.GeneratedProtocolMessageType('UpdatePsetResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEPSETRESPONSE,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.UpdatePsetResponse)
  })
_sym_db.RegisterMessage(UpdatePsetResponse)

BlindPsetRequest = _reflection.GeneratedProtocolMessageType('BlindPsetRequest', (_message.Message,), {
  'DESCRIPTOR' : _BLINDPSETREQUEST,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.BlindPsetRequest)
  })
_sym_db.RegisterMessage(BlindPsetRequest)

BlindPsetResponse = _reflection.GeneratedProtocolMessageType('BlindPsetResponse', (_message.Message,), {
  'DESCRIPTOR' : _BLINDPSETRESPONSE,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.BlindPsetResponse)
  })
_sym_db.RegisterMessage(BlindPsetResponse)

SignPsetRequest = _reflection.GeneratedProtocolMessageType('SignPsetRequest', (_message.Message,), {
  'DESCRIPTOR' : _SIGNPSETREQUEST,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.SignPsetRequest)
  })
_sym_db.RegisterMessage(SignPsetRequest)

SignPsetResponse = _reflection.GeneratedProtocolMessageType('SignPsetResponse', (_message.Message,), {
  'DESCRIPTOR' : _SIGNPSETRESPONSE,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.SignPsetResponse)
  })
_sym_db.RegisterMessage(SignPsetResponse)

MintRequest = _reflection.GeneratedProtocolMessageType('MintRequest', (_message.Message,), {
  'DESCRIPTOR' : _MINTREQUEST,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.MintRequest)
  })
_sym_db.RegisterMessage(MintRequest)

MintResponse = _reflection.GeneratedProtocolMessageType('MintResponse', (_message.Message,), {
  'DESCRIPTOR' : _MINTRESPONSE,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.MintResponse)
  })
_sym_db.RegisterMessage(MintResponse)

RemintRequest = _reflection.GeneratedProtocolMessageType('RemintRequest', (_message.Message,), {
  'DESCRIPTOR' : _REMINTREQUEST,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.RemintRequest)
  })
_sym_db.RegisterMessage(RemintRequest)

RemintResponse = _reflection.GeneratedProtocolMessageType('RemintResponse', (_message.Message,), {
  'DESCRIPTOR' : _REMINTRESPONSE,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.RemintResponse)
  })
_sym_db.RegisterMessage(RemintResponse)

BurnRequest = _reflection.GeneratedProtocolMessageType('BurnRequest', (_message.Message,), {
  'DESCRIPTOR' : _BURNREQUEST,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.BurnRequest)
  })
_sym_db.RegisterMessage(BurnRequest)

BurnResponse = _reflection.GeneratedProtocolMessageType('BurnResponse', (_message.Message,), {
  'DESCRIPTOR' : _BURNRESPONSE,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.BurnResponse)
  })
_sym_db.RegisterMessage(BurnResponse)

TransferRequest = _reflection.GeneratedProtocolMessageType('TransferRequest', (_message.Message,), {
  'DESCRIPTOR' : _TRANSFERREQUEST,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.TransferRequest)
  })
_sym_db.RegisterMessage(TransferRequest)

TransferResponse = _reflection.GeneratedProtocolMessageType('TransferResponse', (_message.Message,), {
  'DESCRIPTOR' : _TRANSFERRESPONSE,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.TransferResponse)
  })
_sym_db.RegisterMessage(TransferResponse)

PegInAddressRequest = _reflection.GeneratedProtocolMessageType('PegInAddressRequest', (_message.Message,), {
  'DESCRIPTOR' : _PEGINADDRESSREQUEST,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.PegInAddressRequest)
  })
_sym_db.RegisterMessage(PegInAddressRequest)

PegInAddressResponse = _reflection.GeneratedProtocolMessageType('PegInAddressResponse', (_message.Message,), {
  'DESCRIPTOR' : _PEGINADDRESSRESPONSE,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.PegInAddressResponse)
  })
_sym_db.RegisterMessage(PegInAddressResponse)

ClaimPegInRequest = _reflection.GeneratedProtocolMessageType('ClaimPegInRequest', (_message.Message,), {
  'DESCRIPTOR' : _CLAIMPEGINREQUEST,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.ClaimPegInRequest)
  })
_sym_db.RegisterMessage(ClaimPegInRequest)

ClaimPegInResponse = _reflection.GeneratedProtocolMessageType('ClaimPegInResponse', (_message.Message,), {
  'DESCRIPTOR' : _CLAIMPEGINRESPONSE,
  '__module__' : 'ocean.v1.transaction_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.ClaimPegInResponse)
  })
_sym_db.RegisterMessage(ClaimPegInResponse)

_TRANSACTIONSERVICE = DESCRIPTOR.services_by_name['TransactionService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETTRANSACTIONREQUEST._serialized_start=62
  _GETTRANSACTIONREQUEST._serialized_end=105
  _GETTRANSACTIONRESPONSE._serialized_start=107
  _GETTRANSACTIONRESPONSE._serialized_end=215
  _SELECTUTXOSREQUEST._serialized_start=218
  _SELECTUTXOSREQUEST._serialized_end=500
  _SELECTUTXOSREQUEST_STRATEGY._serialized_start=414
  _SELECTUTXOSREQUEST_STRATEGY._serialized_end=500
  _SELECTUTXOSRESPONSE._serialized_start=502
  _SELECTUTXOSRESPONSE._serialized_end=626
  _ESTIMATEFEESREQUEST._serialized_start=629
  _ESTIMATEFEESREQUEST._serialized_end=781
  _ESTIMATEFEESRESPONSE._serialized_start=783
  _ESTIMATEFEESRESPONSE._serialized_end=836
  _SIGNTRANSACTIONREQUEST._serialized_start=838
  _SIGNTRANSACTIONREQUEST._serialized_end=920
  _SIGNTRANSACTIONRESPONSE._serialized_start=922
  _SIGNTRANSACTIONRESPONSE._serialized_end=970
  _BROADCASTTRANSACTIONREQUEST._serialized_start=972
  _BROADCASTTRANSACTIONREQUEST._serialized_end=1024
  _BROADCASTTRANSACTIONRESPONSE._serialized_start=1026
  _BROADCASTTRANSACTIONRESPONSE._serialized_end=1076
  _CREATEPSETREQUEST._serialized_start=1078
  _CREATEPSETREQUEST._serialized_end=1182
  _CREATEPSETRESPONSE._serialized_start=1184
  _CREATEPSETRESPONSE._serialized_end=1224
  _UPDATEPSETREQUEST._serialized_start=1226
  _UPDATEPSETREQUEST._serialized_end=1350
  _UPDATEPSETRESPONSE._serialized_start=1352
  _UPDATEPSETRESPONSE._serialized_end=1392
  _BLINDPSETREQUEST._serialized_start=1395
  _BLINDPSETREQUEST._serialized_end=1548
  _BLINDPSETRESPONSE._serialized_start=1550
  _BLINDPSETRESPONSE._serialized_end=1589
  _SIGNPSETREQUEST._serialized_start=1591
  _SIGNPSETREQUEST._serialized_end=1663
  _SIGNPSETRESPONSE._serialized_start=1665
  _SIGNPSETRESPONSE._serialized_end=1703
  _MINTREQUEST._serialized_start=1706
  _MINTREQUEST._serialized_end=1971
  _MINTRESPONSE._serialized_start=1973
  _MINTRESPONSE._serialized_end=2010
  _REMINTREQUEST._serialized_start=2013
  _REMINTREQUEST._serialized_end=2155
  _REMINTRESPONSE._serialized_start=2157
  _REMINTRESPONSE._serialized_end=2196
  _BURNREQUEST._serialized_start=2199
  _BURNREQUEST._serialized_end=2341
  _BURNRESPONSE._serialized_start=2343
  _BURNRESPONSE._serialized_end=2380
  _TRANSFERREQUEST._serialized_start=2383
  _TRANSFERREQUEST._serialized_end=2529
  _TRANSFERRESPONSE._serialized_start=2531
  _TRANSFERRESPONSE._serialized_end=2572
  _PEGINADDRESSREQUEST._serialized_start=2574
  _PEGINADDRESSREQUEST._serialized_end=2595
  _PEGINADDRESSRESPONSE._serialized_start=2598
  _PEGINADDRESSRESPONSE._serialized_end=2736
  _CLAIMPEGINREQUEST._serialized_start=2738
  _CLAIMPEGINREQUEST._serialized_end=2857
  _CLAIMPEGINRESPONSE._serialized_start=2859
  _CLAIMPEGINRESPONSE._serialized_end=2902
  _TRANSACTIONSERVICE._serialized_start=2905
  _TRANSACTIONSERVICE._serialized_end=4029
# @@protoc_insertion_point(module_scope)
