import greenaddress as gdk
import wallycore as wally
import secrets

from binascii import hexlify 
from copy import copy
from typing import List, Tuple, TypedDict 
from domain import GdkAPI, TransactionDetails, Locker, Receiver, CoinSelectionResult, GdkUtxo, InputBlindingData, Outpoint, PsetInputArgs, PsetOutputArgs, Utxo, Asset
from services.account import AccountService

# For each output to blind, we need 32 bytes of entropy for each of:
# - Output assetblinder
# - Output amountblinder
# - Ephemeral rangeproof ECDH key
# - Explicit value rangeproof
# - Surjectionproof seed
OUTPUT_ENTROPY_SIZE = 5 * 32

def h2b_rev(h: str):
    return wally.hex_to_bytes(h)[::-1]

class TransactionService:
    def __init__(self, session: gdk.Session, locker: Locker) -> None:
        self._session = session
        self._gdk_api = GdkAPI(session)
        self._locker = locker
        self._account_service = AccountService(session, locker)
        self._ephemeral_priv_keys = {}

    def sign_transaction(self, txHex: str) -> str:
        pass

    def broadcast_transaction(self, txHex: str) -> str:
        return self._gdk_api.broadcast(txHex)

    def analyze_pset(self, psetBase64):
        details = {
            'psbt': psetBase64,
            'utxos': self._gdk_api.get_all_unspents_outputs(),
        }
        return self._session.psbt_get_details(details).resolve()

    def _add_redeem_scripts(self, psetBase64: str) -> str:
        psbt = wally.psbt_from_base64(psetBase64)
        addresses = self._account_service.list_all_addresses()
        for i in range(wally.psbt_get_num_inputs(psbt)):
            witness_utxo = wally.psbt_get_input_witness_utxo(psbt, i)
            prevout_script = wally.tx_output_get_script(witness_utxo)
            for a in addresses:
                if a['blinding_script'] == wally.hex_from_bytes(prevout_script) and a['script_type'] in [14, 15]: # p2wsh, csv
                    script = wally.witness_program_from_bytes(wally.hex_to_bytes(a['script']), wally.WALLY_SCRIPT_SHA256)
                    wally.psbt_set_input_redeem_script(psbt, i, script)
                    break
        return wally.psbt_to_base64(psbt, 0)

    def _add_input_to_pset(self, psetb64: str, psetInput: PsetInputArgs) -> str:
        """add an input to a pset at the next available index, add witnessUtxo, utxoRangeproof and redeemScript if needed

        Args:
            psetb64 (str): the pset to add input to
            psetInput (PsetInput): the input to add

        Returns:
            str: pset with input added as base64
        """
        pset = wally.psbt_from_base64(psetb64)
        # Add the input to the psbt
        idx = wally.psbt_get_num_inputs(pset)
        seq = 0xFFFFFFFE  # RBF not enabled for liquid yet
        wally.psbt_add_tx_input_at(pset, idx, 0, wally.tx_input_init(h2b_rev(psetInput['txhash']), psetInput['vout'], seq, None, None))
        funding_tx_hex = self._gdk_api.get_transaction_hex(psetInput['txhash'])
        funding_tx = wally.tx_from_hex(funding_tx_hex, wally.WALLY_TX_FLAG_USE_ELEMENTS)
        wally.psbt_set_input_witness_utxo_from_tx(pset, idx, funding_tx, psetInput['vout'])
        wally.psbt_set_input_utxo_rangeproof(pset, idx, wally.tx_get_output_rangeproof(funding_tx, psetInput['vout']))
        psetb64 = wally.psbt_to_base64(pset, 0)

        # Add the redeem script if needed
        psetb64 = self._add_redeem_scripts(psetb64)
        return psetb64

    def _add_output_to_pset(self, psetb64: str, psetOutput: PsetOutputArgs) -> str:
        pset = wally.psbt_from_base64(psetb64)
        script = None
        blindingPubKey = None
        
        if psetOutput['address'] is not None:
            decoded_addr = decode_address(psetOutput['address'])
            script = wally.hex_to_bytes(decoded_addr['scriptPubKey'])
            blindingPubKey = wally.hex_to_bytes(decoded_addr['blindingPubKey'])
        
        output = wally.tx_elements_output_init(
            script,
            Asset.from_hex(psetOutput['asset']).to_bytes(),
            wally.tx_confidential_value_from_satoshi(psetOutput['amount']),
        )
        
        idx = wally.psbt_get_num_outputs(pset)
        wally.psbt_add_tx_output_at(pset, idx, 0, output)
        
        if psetOutput['blinder_index'] is not None:
            wally.psbt_set_output_blinder_index(pset, idx, psetOutput['blinder_index'])
        if blindingPubKey is not None:
            wally.psbt_set_output_blinding_public_key(pset, idx, blindingPubKey)
            
        return wally.psbt_to_base64(pset, 0)

    def _empty_pset(self) -> str:
        pset = wally.psbt_init(2, 0, 0, 0, wally.WALLY_PSBT_INIT_PSET)
        return wally.psbt_to_base64(pset, 0)

    def update_pset(self, psetb64: str, ins: List[PsetInputArgs], outs: List[PsetOutputArgs]) -> str:
        pset = psetb64
        for inp in ins:
            pset = self._add_input_to_pset(pset, inp)
        for out in outs:
            pset = self._add_output_to_pset(pset, out)
        return pset

    def create_pset(self, ins: List[PsetInputArgs], outs: List[PsetOutputArgs]) -> str:
        pset = self._empty_pset()
        return self.update_pset(pset, ins, outs)

    def blind_pset(self, psetBase64: str, extra_blinding_data: List[InputBlindingData] = []) -> str:
        psbt = wally.psbt_from_base64(psetBase64)
        wallet_blinding_data = self._get_inputs_blinding_data_from_wallet(psetBase64)
        inputs_blinding_data = wallet_blinding_data + extra_blinding_data

        valueBlindingFactors, values, assetBlindingFactors, assets = [wally.map_init(len(inputs_blinding_data), None) for _ in range(4)]
        for _, blinding_data in enumerate(inputs_blinding_data):
            i = blinding_data['input_index']
            wally.map_add_integer(values, i, blinding_data['value'])
            wally.map_add_integer(valueBlindingFactors, i, blinding_data['value_blinder'])
            wally.map_add_integer(assets, i, blinding_data['asset'])
            wally.map_add_integer(assetBlindingFactors, i, blinding_data['asset_blinder'])

        blinder_indexes_to_blind = set([u['input_index'] for u in inputs_blinding_data])
        num_outputs = wally.psbt_get_num_outputs(psbt)
        num_outputs_to_blind = 0
        for i in range(num_outputs):
            if wally.psbt_get_output_script_len(psbt, i) == 0:
                continue # skip the fee outputs
            out_blinder_index = wally.psbt_get_output_blinder_index(psbt, i)
            if out_blinder_index in blinder_indexes_to_blind:
                if wally.psbt_get_output_blinding_public_key_len(psbt, i) == 0:
                    raise Exception('output blinding pubkey not set but has blinder index')
                num_outputs_to_blind += 1

        entropy = secrets.token_bytes(num_outputs_to_blind * 5 * 32)

        ephemeral_key = wally.psbt_blind(psbt, values, valueBlindingFactors,
                         assets, assetBlindingFactors, entropy, 0xffffffff, 0)
        
        psbt_id = wally.psbt_get_id(psbt, 0)
        
        self._ephemeral_priv_keys[hexlify(psbt_id)] = ephemeral_key
        return wally.psbt_to_base64(psbt, 0)

    def sign_pset(self, psetBase64: str) -> str:
        psbt = wally.psbt_from_base64(psetBase64)
        outputs_len = wally.psbt_get_num_outputs(psbt)
        for i in range(outputs_len):
            out_status = wally.psbt_get_output_blinding_status(psbt, i, 0)
            # raise an error if blinding is required
            blinding_status_guard_sign(i, out_status)
        
        utxos = self._gdk_api.get_all_utxos()
        utxos_to_sign: List[Tuple[int, Utxo]] = []
        
        inputs_len = wally.psbt_get_num_inputs(psbt)
        for input_index in range(inputs_len):
            input_txid = b2h_rev(wally.psbt_get_input_previous_txid(psbt, input_index))
            input_vout = wally.psbt_get_input_output_index(psbt, input_index)
            for u in utxos:
                if u.txid == input_txid and u.index == input_vout:
                    utxos_to_sign.append((input_index, u))
    
        if len(utxos_to_sign) == 0:
            raise Exception("No inputs to sign")
    
        blinding_nonces = []
        have_ephemeral_key = True
        psbt_id = wally.psbt_get_id(psbt, 0)
        try:
            ephemeral_keys = self._ephemeral_priv_keys[hexlify(psbt_id)]
        except KeyError:
            have_ephemeral_key = False
        
        if have_ephemeral_key:
            for out_index in range(outputs_len):
                if wally.psbt_get_output_script_len(psbt, out_index) == 0 or wally.psbt_get_output_ecdh_public_key_len(psbt, out_index) == 0 or wally.psbt_get_output_blinding_public_key_len(psbt, out_index) == 0:
                    blinding_nonces.append('')
                    continue
                nonce = get_blinding_nonce(psbt, ephemeral_keys, out_index)
                blinding_nonces.append(wally.hex_from_bytes(nonce))
    
        utxos_arr = [u[1].gdk_utxo for u in utxos_to_sign]
        signed_result = self._gdk_api.sign_pset(psetBase64, utxos_arr, blinding_nonces)   
        psetBase64 = signed_result['psbt']
        return psetBase64

    def transfer(self, account_key: str, receivers: List[Receiver]) -> str:
        account = self._gdk_api.get_account(account_key)
        return account.send(receivers)

    def select_utxos(self, account_key: str, asset: str, amount: int) -> CoinSelectionResult:
        account = self._gdk_api.get_account(account_key)
        try:
            utxos_for_asset = account.utxos()[asset]
        except KeyError:
            raise Exception("No UTXOs found for asset {}".format(asset))
        utxos = [u for u in utxos_for_asset if not self._locker.is_locked(Outpoint.from_utxo(u))]
        selected_amount = 0
        selected_utxos = []
        for u in utxos:
            if selected_amount >= amount:
                break
            selected_utxos.append(u)
            selected_amount += u.value
        
        if selected_amount < amount:
            raise Exception("Not enough funds")
    
        result = CoinSelectionResult(asset, selected_amount, selected_amount - amount, selected_utxos) 
        for utxo in result.utxos:
            self._locker.lock(utxo, account_key)
        return result

    def estimate_fees(self) -> int:
        fees = self._gdk_api.get_fee_estimates(1)
        return fees

    def get_transaction(self, txid: str) -> TransactionDetails:
        return self._gdk_api.get_transaction(txid)

    def _get_inputs_blinding_data_from_wallet(self, psbtb64: str) -> List[InputBlindingData]:
        blinding_data = []
        utxos = self._gdk_api.get_all_utxos()
        psbt = wally.psbt_from_base64(psbtb64)
        num_inputs = wally.psbt_get_num_inputs(psbt)
        for input_index in range(num_inputs):
            input_txid = b2h_rev(wally.psbt_get_input_previous_txid(psbt, input_index))
            input_vout = wally.psbt_get_input_output_index(psbt, input_index)
            for u in utxos:
                if u.txid == input_txid and u.index == input_vout:
                    blinding_data.append(u.to_blinding_data(input_index))
                    break
        return blinding_data

def blinding_status_guard_sign(output_index: int, blinding_status: int):
    if blinding_status == wally.WALLY_PSET_BLINDED_NONE:
        return
    if blinding_status == wally.WALLY_PSET_BLINDED_REQUIRED:
        raise Exception('Output ' + str(output_index) +
                        ' is required to be blinded (has blinding pub key)')
    if blinding_status == wally.WALLY_PSET_BLINDED_PARTIAL:
        raise Exception('Output ' + str(output_index) +
                        ' is partially blinded')
    if blinding_status == wally.WALLY_PSET_BLINDED_FULL:
        return

def b2h_rev(b: bytes) -> str:
    return wally.hex_from_bytes(b[::-1])

def skipped_utxo(u: GdkUtxo) -> GdkUtxo:
    cpy = copy(u)
    cpy['skip_signing'] = True
    return cpy

def get_blinding_nonce(psbt, ephemeral_keys, output_index):
    ephemeral_key_index = wally.map_find_integer(ephemeral_keys, output_index)
    if not ephemeral_key_index:
        raise Exception('Output ' + str(output_index) + ' blinding key not found')
    ephemeral_key = wally.map_get_item(ephemeral_keys, ephemeral_key_index - 1)
    blinding_pubkey = wally.psbt_get_output_blinding_public_key(psbt, output_index)
    return wally.ecdh_nonce_hash(blinding_pubkey, ephemeral_key)

def h2b_rev(h: str):
    return wally.hex_to_bytes(h)[::-1]

class AnalyzeAddressResult(TypedDict):
    network: str
    isSegwit: bool

def analyze_address(address: str) -> AnalyzeAddressResult:
    """Returns the network from the address (regtest not supported)"""
    if address.startswith('lq'):
        return { 'network': 'liquid', 'isSegwit': True }
    if address.startswith('tlq'):
        return { 'network': 'liquidtestnet', 'isSegwit': True }
    
    decoded = wally.base58check_to_bytes(address)
    if (decoded[0] == wally.WALLY_CA_PREFIX_LIQUID_TESTNET):
        return {'network': 'liquidtestnet', 'isSegwit': False }
    if (decoded[0] == wally.WALLY_CA_PREFIX_LIQUID):
        return {'network': 'liquid', 'isSegwit': False }
    
    raise Exception('Unknown network for address ' + address)

class DecodeAddressResult(TypedDict):
    scriptPubKey: str
    blindingPubKey: str

def decode_address(address: str) -> DecodeAddressResult:
    analyzer_result = analyze_address(address)
    unconf_addr = None
    try:
        unconf_addr = wally.confidential_addr_to_addr(address, wally.WALLY_CA_PREFIX_LIQUID if analyzer_result['network'] == 'liquid' else wally.WALLY_CA_PREFIX_LIQUID_TESTNET)
    except:
        unconf_addr = address
    scriptpubkey = wally.address_to_scriptpubkey(unconf_addr, wally.WALLY_NETWORK_LIQUID if analyzer_result['network'] == 'liquid' else wally.WALLY_NETWORK_LIQUID_TESTNET)
    blindingPubKey = wally.confidential_addr_to_ec_public_key(address, wally.WALLY_CA_PREFIX_LIQUID if analyzer_result['network'] == 'liquid' else wally.WALLY_CA_PREFIX_LIQUID_TESTNET)
    return {
        'scriptPubKey': wally.hex_from_bytes(scriptpubkey),
        'blindingPubKey': wally.hex_from_bytes(blindingPubKey)
    }