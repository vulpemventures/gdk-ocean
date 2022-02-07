from ocean.v1alpha import notification_pb2, types_pb2
from domain.utxo import Utxo, to_grpc_utxo
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
        
    def to_proto(self):
        raise Exception('to_proto method must be implemented by a child notification class')
    
class UtxoNotification(BaseNotification):
    def __init__(self, n_type: NotificationType, data: Utxo, account_name: str):
        self.type = n_type
        self.data = data
        self.account_name = account_name
        
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
        account_key = types_pb2.AccountKey(id=0, name=self.account_name)
        utxo_proto = to_grpc_utxo(self.data)
        utxo_with_event = types_pb2.UtxoWithEvent(account_key=account_key, utxo=utxo_proto, event_type=self._type_to_tx_event_type())
        return notification_pb2.UtxosNotificationsResponse(utxos=[utxo_with_event])
    
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
    def __init__(self, data: Utxo, account_name: str):
        super().__init__(NotificationType.UTXO_UNLOCKED, data, account_name)

class TxNotification(BaseNotification):
    def __init__(self, n_type: NotificationType, txid: str, block_height: int, block_hash: str):
        self.type = n_type
        self.data = {
            "txid": txid,
            "block_height": block_height,
            "block_hash": block_hash,
        }
    
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
    
    def _get_block_details(self) -> notification_pb2.BlockDetails:
        return notification_pb2.BlockDetails(
            hash=bytes.fromhex(self.data["block_hash"]),
            height=self.data["block_height"],
            timestamp=0,
        )
    
    def to_proto(self) -> notification_pb2.TransactionNotificationsResponse:
        return notification_pb2.TransactionNotificationsResponse(
            txid=self.data["txid"],
            event_type=self._type_to_tx_event_type(),
            block_details=self._get_block_details(),
        )
        
class TxConfirmedNotification(TxNotification):
    def __init__(self, txid: str, block_hash: str, block_height: int):
        super().__init__(NotificationType.TX_CONFIRMED, txid, block_height, block_hash)
    
class TxUnconfirmedNotification(TxNotification):
    def __init__(self, txid: str, block_height: int, block_hash: str):
        super().__init__(NotificationType.TX_UNCONFIRMED, txid, block_height, block_hash)

class TxUnspecifiedNotification(TxNotification):
    def __init__(self, txid: str, block_height: int, block_hash: str):
        super().__init__(NotificationType.TX_UNSPECIFIED, txid, block_height, block_hash)
