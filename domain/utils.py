from binascii import unhexlify
from wallycore import *

from domain.gdk import GdkAPI
from domain.types import GdkUtxo, h2b_rev

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


def add_input_utxo(gdk_api: GdkAPI, psbtb64: str, utxo: GdkUtxo) -> str:
    psbt = psbt_from_base64(psbtb64)
    # Add the input to the psbt
    idx = psbt_get_num_inputs(psbt)
    seq = 0xFFFFFFFE  # RBF not enabled for liquid yet
    funding_tx_hex = gdk_api.get_transaction_hex(utxo['txhash'])
    funding_tx = tx_from_hex(funding_tx_hex, WALLY_TX_FLAG_USE_ELEMENTS)
    proof = tx_get_output_rangeproof(funding_tx, utxo['pt_idx'])
    psbt_add_tx_input_at(psbt, idx, 0, tx_input_init(h2b_rev(utxo['txhash']), utxo['pt_idx'], seq, None, None))
    psbt_set_input_witness_utxo_from_tx(psbt, idx, funding_tx, utxo['pt_idx'])
    psbt_set_input_utxo_rangeproof(psbt, idx,  proof)

    # Redeemscript
    pubkey = hex_to_bytes(utxo['public_key']) if 'public_key' in utxo else None
    if utxo['address_type'] in ['csv', 'p2wsh']:
        # Note: 'p2wsh' for multisig is p2sh wrapped p2wsh.
        # For Green multisig swaps, Green server signing currently requires
        # that swap inputs are *provably* segwit in order to eliminate
        # malleation from the processing state machine.
        # For p2sh wrapped inputs, this currently requires passing
        # the witness program as the redeem script when signing; The server
        # uses this to validate the input before signing with the actual
        # script.
        # TODO: This isn't documented in the gdk or backend API docs, and
        # should probably be done with a PSET input extension field instead.
        script = hex_to_bytes(utxo['script'])
        script = witness_program_from_bytes(script, WALLY_SCRIPT_SHA256)
    elif utxo['address_type'] in ['p2sh-p2wpkh']:
        script = witness_program_from_bytes(pubkey, WALLY_SCRIPT_HASH160)
    else:
        assert False, 'unknown address type ' + utxo['address_type']

    return psbt_to_base64(psbt, 0)

