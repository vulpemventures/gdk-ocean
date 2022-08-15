from typing import Any
from ocean.v1alpha import notification_pb2, types_pb2
from domain import Utxo, AccountKey, BlockDetails
from enum import Enum

class NotificationType(Enum):
    UTXO_SPENT = 0
    UTXO_LOCKED = 1
    UTXO_UNLOCKED = 2
    UTXO_UNSPECIFIED = 3
    
    TX_BROADCASTED = 4
    TX_CONFIRMED = 5
    TX_UNCONFIRMED = 6
    TX_UNSPECIFIED = 7

class BaseNotification():
    def __init__(self) -> None:
        self.type: NotificationType = None
        
    def to_proto(self) -> Any:
        raise Exception('to_proto method must be implemented by a child notification class')
    
class UtxoNotification(BaseNotification):
    def __init__(self, n_type: NotificationType, utxo: Utxo, account_name: str):
        self.type = n_type
        self.utxo = utxo
        self.account = AccountKey.from_name(account_name)
        
    def _type_to_tx_event_type(self) -> types_pb2.UtxoEventType:
        if self.type is NotificationType.UTXO_SPENT:
            return types_pb2.UTXO_EVENT_TYPE_SPENT
        elif self.type is NotificationType.UTXO_LOCKED:
            return types_pb2.UTXO_EVENT_TYPE_LOCKED
        elif self.type is NotificationType.UTXO_UNSPECIFIED:
            return types_pb2.UTXO_EVENT_TYPE_UNSPECIFIED
        elif self.type is NotificationType.UTXO_UNLOCKED:
            return types_pb2.UTXO_EVENT_TYPE_UNLOCKED
        else:
            raise Exception(f"Unknown utxo event type: {self.type}")
    
    def to_proto(self) :
        utxo_proto = self.utxo.to_proto()
        account_proto = self.account.to_proto()
        return notification_pb2.UtxosNotificationsResponse(
            account_key=account_proto,
            utxo=utxo_proto,
            event_type=self._type_to_tx_event_type()
        )
    
class UtxoSpentNotification(UtxoNotification):
    def __init__(self, utxo: Utxo, account_name: str):
        super().__init__(NotificationType.UTXO_SPENT, utxo, account_name)
        
class UtxoUnspecifiedNotification(UtxoNotification):
    def __init__(self, utxo: Utxo, account_name: str):
        super().__init__(NotificationType.UTXO_UNSPECIFIED, utxo, account_name)
    
class UtxoLockedNotification(UtxoNotification):
    def __init__(self, data: Utxo, account_name: str):
        super().__init__(NotificationType.UTXO_LOCKED, data, account_name)

class UtxoUnlockedNotification(UtxoNotification):
    def __init__(self, utxo: Utxo, account_name: str):
        super().__init__(NotificationType.UTXO_UNLOCKED, utxo, account_name)

class TxNotification(BaseNotification):
    def __init__(self, n_type: NotificationType, txid: str, block_details: BlockDetails, account_name: str):
        self.type = n_type
        self.txid = txid
        self.block_details = block_details
        self.account = AccountKey.from_name(account_name)
    
    def _type_to_tx_event_type(self) -> types_pb2.TxEventType:
        if self.type is NotificationType.TX_CONFIRMED:
            return types_pb2.TX_EVENT_TYPE_CONFIRMED
        elif self.type is NotificationType.TX_UNCONFIRMED:
            return types_pb2.TX_EVENT_TYPE_UNCONFIRMED
        elif self.type is NotificationType.TX_UNSPECIFIED:
            return types_pb2.TX_EVENT_TYPE_UNSPECIFIED
        elif self.type is NotificationType.TX_BROADCASTED:
            return types_pb2.TX_EVENT_TYPE_BROADCASTED
        else:
            raise Exception(f"Unknown tx event type: {self.type}")
    
    def to_proto(self) -> notification_pb2.TransactionNotificationsResponse:
        return notification_pb2.TransactionNotificationsResponse(
            txid=self.txid,
            event_type=self._type_to_tx_event_type(),
            block_details=self.block_details.to_proto(),
            account_key=self.account.to_proto(),
        )
        
class TxConfirmedNotification(TxNotification):
    def __init__(self, txid: str, block_details: BlockDetails, account_name: str):
        super().__init__(NotificationType.TX_CONFIRMED, txid, block_details, account_name)
    
class TxUnconfirmedNotification(TxNotification):
    def __init__(self, txid: str, block_details: BlockDetails, account_name: str):
        super().__init__(NotificationType.TX_UNCONFIRMED, txid, block_details, account_name)

class TxUnspecifiedNotification(TxNotification):
    def __init__(self, txid: str, block_details: BlockDetails, account_name: str):
        super().__init__(NotificationType.TX_UNSPECIFIED, txid, block_details, account_name)
