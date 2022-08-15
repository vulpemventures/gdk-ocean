from binascii import unhexlify
from wallycore import *

from domain.gdk import GdkAPI
from domain.types import GdkUtxo

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


def add_input_utxo(gdk_api: GdkAPI, psbt: str, utxo: GdkUtxo):
    # Add the input to the psbt
    idx = psbt_get_num_inputs(psbt)
    seq = 0xFFFFFFFE  # RBF not enabled for liquid yet
    psbt_add_tx_input_at(psbt, idx, 0, tx_input_init(h2b_rev(utxo['txhash']), utxo['pt_idx'], seq, None, None))
    funding_tx_hex = gdk_api.get_transaction_hex(utxo['txhash'])
    funding_tx = tx_from_hex(funding_tx_hex, WALLY_TX_FLAG_USE_ELEMENTS)
    psbt_set_input_witness_utxo_from_tx(psbt, idx, funding_tx, utxo['pt_idx'])
    psbt_set_input_utxo_rangeproof(psbt, idx, tx_get_output_rangeproof(funding_tx, utxo['pt_idx']))
    return idx

def h2b_rev(h: str):
    return hex_to_bytes(h)[::-1]
