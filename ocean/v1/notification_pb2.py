# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ocean/v1/notification.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ocean.v1 import types_pb2 as ocean_dot_v1_dot_types__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bocean/v1/notification.proto\x12\x08ocean.v1\x1a\x14ocean/v1/types.proto\"!\n\x1fTransactionNotificationsRequest\"\xe4\x01\n TransactionNotificationsResponse\x12\x34\n\nevent_type\x18\x01 \x01(\x0e\x32\x15.ocean.v1.TxEventTypeR\teventType\x12#\n\raccount_names\x18\x02 \x03(\tR\x0c\x61\x63\x63ountNames\x12\x14\n\x05txhex\x18\x03 \x01(\tR\x05txhex\x12\x12\n\x04txid\x18\x04 \x01(\tR\x04txid\x12;\n\rblock_details\x18\x05 \x01(\x0b\x32\x16.ocean.v1.BlockDetailsR\x0c\x62lockDetails\"\x1b\n\x19UtxosNotificationsRequest\"z\n\x1aUtxosNotificationsResponse\x12\x36\n\nevent_type\x18\x01 \x01(\x0e\x32\x17.ocean.v1.UtxoEventTypeR\teventType\x12$\n\x05utxos\x18\x02 \x03(\x0b\x32\x0e.ocean.v1.UtxoR\x05utxos\"\x82\x01\n\x11\x41\x64\x64WebhookRequest\x12\x1a\n\x08\x65ndpoint\x18\x01 \x01(\tR\x08\x65ndpoint\x12\x39\n\nevent_type\x18\x02 \x01(\x0e\x32\x1a.ocean.v1.WebhookEventTypeR\teventType\x12\x16\n\x06secret\x18\x03 \x01(\tR\x06secret\"$\n\x12\x41\x64\x64WebhookResponse\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"&\n\x14RemoveWebhookRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"\x17\n\x15RemoveWebhookResponse\"P\n\x13ListWebhooksRequest\x12\x39\n\nevent_type\x18\x01 \x01(\x0e\x32\x1a.ocean.v1.WebhookEventTypeR\teventType\"P\n\x14ListWebhooksResponse\x12\x38\n\x0cwebhook_info\x18\x01 \x03(\x0b\x32\x15.ocean.v1.WebhookInfoR\x0bwebhookInfo\"X\n\x0bWebhookInfo\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x1a\n\x08\x65ndpoint\x18\x02 \x01(\tR\x08\x65ndpoint\x12\x1d\n\nis_secured\x18\x03 \x01(\x08R\tisSecured2\xdd\x03\n\x13NotificationService\x12s\n\x18TransactionNotifications\x12).ocean.v1.TransactionNotificationsRequest\x1a*.ocean.v1.TransactionNotificationsResponse0\x01\x12\x61\n\x12UtxosNotifications\x12#.ocean.v1.UtxosNotificationsRequest\x1a$.ocean.v1.UtxosNotificationsResponse0\x01\x12I\n\nAddWebhook\x12\x1b.ocean.v1.AddWebhookRequest\x1a\x1c.ocean.v1.AddWebhookResponse\"\x00\x12R\n\rRemoveWebhook\x12\x1e.ocean.v1.RemoveWebhookRequest\x1a\x1f.ocean.v1.RemoveWebhookResponse\"\x00\x12O\n\x0cListWebhooks\x12\x1d.ocean.v1.ListWebhooksRequest\x1a\x1e.ocean.v1.ListWebhooksResponse\"\x00\x62\x06proto3')



_TRANSACTIONNOTIFICATIONSREQUEST = DESCRIPTOR.message_types_by_name['TransactionNotificationsRequest']
_TRANSACTIONNOTIFICATIONSRESPONSE = DESCRIPTOR.message_types_by_name['TransactionNotificationsResponse']
_UTXOSNOTIFICATIONSREQUEST = DESCRIPTOR.message_types_by_name['UtxosNotificationsRequest']
_UTXOSNOTIFICATIONSRESPONSE = DESCRIPTOR.message_types_by_name['UtxosNotificationsResponse']
_ADDWEBHOOKREQUEST = DESCRIPTOR.message_types_by_name['AddWebhookRequest']
_ADDWEBHOOKRESPONSE = DESCRIPTOR.message_types_by_name['AddWebhookResponse']
_REMOVEWEBHOOKREQUEST = DESCRIPTOR.message_types_by_name['RemoveWebhookRequest']
_REMOVEWEBHOOKRESPONSE = DESCRIPTOR.message_types_by_name['RemoveWebhookResponse']
_LISTWEBHOOKSREQUEST = DESCRIPTOR.message_types_by_name['ListWebhooksRequest']
_LISTWEBHOOKSRESPONSE = DESCRIPTOR.message_types_by_name['ListWebhooksResponse']
_WEBHOOKINFO = DESCRIPTOR.message_types_by_name['WebhookInfo']
TransactionNotificationsRequest = _reflection.GeneratedProtocolMessageType('TransactionNotificationsRequest', (_message.Message,), {
  'DESCRIPTOR' : _TRANSACTIONNOTIFICATIONSREQUEST,
  '__module__' : 'ocean.v1.notification_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.TransactionNotificationsRequest)
  })
_sym_db.RegisterMessage(TransactionNotificationsRequest)

TransactionNotificationsResponse = _reflection.GeneratedProtocolMessageType('TransactionNotificationsResponse', (_message.Message,), {
  'DESCRIPTOR' : _TRANSACTIONNOTIFICATIONSRESPONSE,
  '__module__' : 'ocean.v1.notification_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.TransactionNotificationsResponse)
  })
_sym_db.RegisterMessage(TransactionNotificationsResponse)

UtxosNotificationsRequest = _reflection.GeneratedProtocolMessageType('UtxosNotificationsRequest', (_message.Message,), {
  'DESCRIPTOR' : _UTXOSNOTIFICATIONSREQUEST,
  '__module__' : 'ocean.v1.notification_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.UtxosNotificationsRequest)
  })
_sym_db.RegisterMessage(UtxosNotificationsRequest)

UtxosNotificationsResponse = _reflection.GeneratedProtocolMessageType('UtxosNotificationsResponse', (_message.Message,), {
  'DESCRIPTOR' : _UTXOSNOTIFICATIONSRESPONSE,
  '__module__' : 'ocean.v1.notification_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.UtxosNotificationsResponse)
  })
_sym_db.RegisterMessage(UtxosNotificationsResponse)

AddWebhookRequest = _reflection.GeneratedProtocolMessageType('AddWebhookRequest', (_message.Message,), {
  'DESCRIPTOR' : _ADDWEBHOOKREQUEST,
  '__module__' : 'ocean.v1.notification_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.AddWebhookRequest)
  })
_sym_db.RegisterMessage(AddWebhookRequest)

AddWebhookResponse = _reflection.GeneratedProtocolMessageType('AddWebhookResponse', (_message.Message,), {
  'DESCRIPTOR' : _ADDWEBHOOKRESPONSE,
  '__module__' : 'ocean.v1.notification_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.AddWebhookResponse)
  })
_sym_db.RegisterMessage(AddWebhookResponse)

RemoveWebhookRequest = _reflection.GeneratedProtocolMessageType('RemoveWebhookRequest', (_message.Message,), {
  'DESCRIPTOR' : _REMOVEWEBHOOKREQUEST,
  '__module__' : 'ocean.v1.notification_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.RemoveWebhookRequest)
  })
_sym_db.RegisterMessage(RemoveWebhookRequest)

RemoveWebhookResponse = _reflection.GeneratedProtocolMessageType('RemoveWebhookResponse', (_message.Message,), {
  'DESCRIPTOR' : _REMOVEWEBHOOKRESPONSE,
  '__module__' : 'ocean.v1.notification_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.RemoveWebhookResponse)
  })
_sym_db.RegisterMessage(RemoveWebhookResponse)

ListWebhooksRequest = _reflection.GeneratedProtocolMessageType('ListWebhooksRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTWEBHOOKSREQUEST,
  '__module__' : 'ocean.v1.notification_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.ListWebhooksRequest)
  })
_sym_db.RegisterMessage(ListWebhooksRequest)

ListWebhooksResponse = _reflection.GeneratedProtocolMessageType('ListWebhooksResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTWEBHOOKSRESPONSE,
  '__module__' : 'ocean.v1.notification_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.ListWebhooksResponse)
  })
_sym_db.RegisterMessage(ListWebhooksResponse)

WebhookInfo = _reflection.GeneratedProtocolMessageType('WebhookInfo', (_message.Message,), {
  'DESCRIPTOR' : _WEBHOOKINFO,
  '__module__' : 'ocean.v1.notification_pb2'
  # @@protoc_insertion_point(class_scope:ocean.v1.WebhookInfo)
  })
_sym_db.RegisterMessage(WebhookInfo)

_NOTIFICATIONSERVICE = DESCRIPTOR.services_by_name['NotificationService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TRANSACTIONNOTIFICATIONSREQUEST._serialized_start=63
  _TRANSACTIONNOTIFICATIONSREQUEST._serialized_end=96
  _TRANSACTIONNOTIFICATIONSRESPONSE._serialized_start=99
  _TRANSACTIONNOTIFICATIONSRESPONSE._serialized_end=327
  _UTXOSNOTIFICATIONSREQUEST._serialized_start=329
  _UTXOSNOTIFICATIONSREQUEST._serialized_end=356
  _UTXOSNOTIFICATIONSRESPONSE._serialized_start=358
  _UTXOSNOTIFICATIONSRESPONSE._serialized_end=480
  _ADDWEBHOOKREQUEST._serialized_start=483
  _ADDWEBHOOKREQUEST._serialized_end=613
  _ADDWEBHOOKRESPONSE._serialized_start=615
  _ADDWEBHOOKRESPONSE._serialized_end=651
  _REMOVEWEBHOOKREQUEST._serialized_start=653
  _REMOVEWEBHOOKREQUEST._serialized_end=691
  _REMOVEWEBHOOKRESPONSE._serialized_start=693
  _REMOVEWEBHOOKRESPONSE._serialized_end=716
  _LISTWEBHOOKSREQUEST._serialized_start=718
  _LISTWEBHOOKSREQUEST._serialized_end=798
  _LISTWEBHOOKSRESPONSE._serialized_start=800
  _LISTWEBHOOKSRESPONSE._serialized_end=880
  _WEBHOOKINFO._serialized_start=882
  _WEBHOOKINFO._serialized_end=970
  _NOTIFICATIONSERVICE._serialized_start=973
  _NOTIFICATIONSERVICE._serialized_end=1450
# @@protoc_insertion_point(module_scope)
