from typing import TypedDict, List
from domain.account_key import AccountKey
from ocean.v1alpha import types_pb2

class Utxo():
    def __init__(self, txid: str, index: int, asset: str, value: int, script: str, is_confirmed: bool, is_locked: bool) -> None:
        self.txid = txid
        self.index = index
        self.asset = asset
        self.value = value
        self.script = script
        self.is_confirmed = is_confirmed
        self.is_locked = is_locked

    def to_proto(self) -> types_pb2.Utxo:
        return types_pb2.Utxo(
            txid=self.txid,
            index=self.index,
            asset=self.asset,
            value=self.value,
            script=bytes.fromhex(self.script),
            is_confirmed=self.is_confirmed,
            is_locked=self.is_locked
        )

def make_utxos_list_proto(account_name: str, utxos: List[Utxo]) -> types_pb2.Utxos:
    return types_pb2.Utxos(
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
    
class CoinSelectionResult(TypedDict):
    asset: str
    total: int
    change: int
    utxos: List[Utxo]