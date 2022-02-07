from typing import TypedDict, List
from ocean.v1alpha import types_pb2

class Utxo(TypedDict):
    txid: str
    index: int
    asset: str
    value: int
    script: str
    is_confirmed: bool
    is_locked: bool

class Outpoint():
    def __init__(self, txid: str, index: int):
        self.txid = txid
        self.index = index
    
    @classmethod
    def from_utxo(cls, utxo: Utxo) -> 'Outpoint':
        return cls(utxo['txid'], utxo['index'])
    
    def to_string(self) -> str:
        return f"{self.txid}:{self.index}"

def to_grpc_utxo(utxo: Utxo) -> types_pb2.Utxo:
    return types_pb2.Utxo(
        txid=utxo['txid'],
        index=utxo['index'],
        asset=bytes.fromhex(utxo['asset']),
        value=utxo['value'].to_bytes(8, 'big'),
        script=bytes.fromhex(utxo['script']),
        is_confirmed=utxo['is_confirmed'],
        is_locked=utxo['is_locked']
    )
    
class CoinSelectionResult(TypedDict):
    asset: str
    total: int
    change: int
    utxos: List[Utxo]