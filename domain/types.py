from binascii import unhexlify
from enum import Enum
from typing import Any, Optional, TypedDict, List
from ocean.v1 import notification_pb2, types_pb2
import wallycore as wally

class PsetInputArgs(TypedDict):
    txhash: str
    vout: int
    script: str
    address_type: str
    
class PsetOutputArgs(TypedDict):
    address: Optional[str]
    amount: int
    asset: str
    blinder_index: Optional[int]

class InputBlindingData(TypedDict):
    asset_blinder: bytes
    value_blinder: bytes
    asset: bytes
    value: bytes
    input_index: int

class GdkUtxo(TypedDict):
    address_type: str
    amountblinder: str # 64 zeros if not confidential
    assetblinder: str # 64 zeros if not confidential
    asset_id: str
    asset_tag: str
    block_height: int
    commitment: str
    confidential: bool
    is_internal: bool
    nonce_commitment: str
    pt_idx: int # vout
    satoshi: int
    script: str
    script_type: int
    subaccount: int
    subtype: int
    txhash: str
    user_status: int
    skip_signing: bool

class Utxo():
    def __init__(self, gdk_utxo: GdkUtxo) -> None:
        self.gdk_utxo = gdk_utxo
        self.txid = gdk_utxo['txhash']
        self.index = gdk_utxo['pt_idx']
        self.asset = gdk_utxo['asset_id']
        self.value = gdk_utxo['satoshi']
        self.script = gdk_utxo['script']
        self.nonce_commitment = gdk_utxo['nonce_commitment']
        self.value_commitment = gdk_utxo['commitment']
        self.asset_commitment = gdk_utxo['asset_tag']
        self.asset_blinder = gdk_utxo['assetblinder']
        self.value_blinder = gdk_utxo['amountblinder']
        self.confidential = gdk_utxo['confidential']
        self.is_confirmed = True
        self._validate()
    
    def _validate(self) -> None:
        if self.confidential:
            if not self.asset_blinder:
                raise Exception('Asset blinder is required for confidential utxos')
            if not self.value_blinder:
                raise Exception('Value blinder is required for confidential utxos')
            zeros = '0' * 64
            if self.asset_blinder == zeros:
                raise Exception('Asset blinder is null for confidential utxo')
            if self.value_blinder == zeros:
                raise Exception('Value blinder is null for confidential utxo')

    def to_proto(self, is_locked: bool) -> types_pb2.Utxo:
        return types_pb2.Utxo(
            txid=self.txid,
            index=self.index,
            asset=self.asset,
            value=self.value,
            script=bytes.fromhex(self.script),
            is_confirmed=self.is_confirmed,
            is_locked=is_locked,
        )
    
    def to_blinding_data(self, input_index: int) -> InputBlindingData:
        return {
            'asset_blinder': h2b_rev(self.asset_blinder),
            'value_blinder': h2b_rev(self.value_blinder),
            'asset': h2b_rev(self.asset),
            'value': wally.tx_confidential_value_from_satoshi(self.value),
            'input_index': input_index,
        }
    
    def to_pset_input_args(self) -> PsetInputArgs:
        return {
            'address_type': self.gdk_utxo['address_type'],
            'script': self.script,
            'txhash': self.txid,
            'vout': self.index,
        }
    
    def to_string(self) -> str:
        return f'{self.txid}:{self.index} (asset: {self.asset}, value: {self.value}, isConfidential: {self.confidential})'
    
def make_utxos_list_proto(account_name: str, utxos: List[Utxo]) -> types_pb2.Utxos:
    return types_pb2.Utxos(
        account_key=account_name,
        utxos=[utxo.to_proto() for utxo in utxos]
    )

class Outpoint():
    def __init__(self, txid: str, index: int):
        self.txid = txid
        self.index = index
    
    @classmethod
    def from_utxo(cls, utxo: Utxo) -> 'Outpoint':
        return cls(utxo.txid, utxo.index)
    
    def to_string(self) -> str:
        return f"{self.txid}:{self.index}"
    
class CoinSelectionResult():
    def __init__(self, asset: str, amount: int, change: int, utxos: List[Utxo]):
        self.asset = asset
        self.amount = amount
        self.change = change
        self.utxos = utxos

def h2b_rev(hexstr: str) -> bytes:
    return wally.hex_to_bytes(hexstr)[::-1]


class BlockDetails():
    def __init__(self, block_hash: str, block_height: int, block_time: int):
        self.block_hash = block_hash
        self.block_height = block_height
        self.block_time = block_time

class AddressDetails(TypedDict):
    address: str
    address_type: str
    branch: int
    pointer: int
    script: str
    script_type: int
    subaccount: int
    subtype: int
    blinding_key: str
    blinding_script: str
    is_blinded: bool
    unblinded_address: str

class Receiver(TypedDict):
    address: str
    sats: int
    asset: str

def receiver_to_dict(receiver: Receiver) -> dict:
    """
    This function is used to convert a receiver to a dictionary.
    """
    return {
        'address': receiver['address'],
        'satoshi': receiver['sats'],
        'asset_id': receiver['asset'],
    }
    
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
        self.account = account_name
        
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
        self.account = account_name
    
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

CONFIDENTIAL_PREFIXES = [0x0a, 0x0b]
UNCONFIDENTIAL_PREFIX = 0x01

class Asset:
    def __init__(self, prefix: int, value: bytes):
        self.prefix = prefix
        self.value = value

    @classmethod
    def from_bytes(self, b: bytes) -> 'Asset':
        if len(b) == 32:
            return Asset(UNCONFIDENTIAL_PREFIX, b)

        if len(b) == 33:
            prefix = b[0]
            if prefix not in CONFIDENTIAL_PREFIXES.extend(UNCONFIDENTIAL_PREFIX):
                raise ValueError('Invalid prefix')
            return Asset(prefix, b[1:])

        raise ValueError('Invalid asset length (must be 32 or 33 bytes)')

    @classmethod
    def from_hex(self, hex_asset: str) -> 'Asset':
        if len(hex_asset) == 64:
            value = unhexlify(hex_asset)
            return Asset.from_bytes(value[::-1])

        if len(hex_asset) == 66:
            value = unhexlify(hex_asset[1:])
            prefix = value[0]
            value = value[1:]
            return Asset.from_bytes(prefix + value[::-1])

    def to_bytes(self) -> bytes:
        return bytes([self.prefix]) + bytes(self.value)

    def to_bytes_without_prefix(self) -> bytearray:
        return bytearray(self.value)
