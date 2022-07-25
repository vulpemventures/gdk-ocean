from typing import TypedDict, List
from domain.account_key import AccountKey
from ocean.v1alpha import types_pb2
import wallycore as wally

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
    
    def to_string(self) -> str:
        return f'{self.txid}:{self.index} (asset: {self.asset}, value: {self.value}, isConfidential: {self.confidential})'
    
def make_utxos_list_proto(account_name: str, utxos: List[Utxo]) -> types_pb2.Utxos:
    return types_pb2.UtxosList(
        account_key=AccountKey.from_name(account_name).to_proto(),
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