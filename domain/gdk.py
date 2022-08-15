import http
import json
from typing import Dict, List, Tuple, TypedDict
import greenaddress as gdk
from domain.address_details import AddressDetails
from domain.pin_data_repository import PinData
from domain.receiver import Receiver, receiver_to_dict
from domain.types import BlockDetails, GdkUtxo, Utxo

class AccountDetails(TypedDict):
    name: str
    pointer: int
    receiving_id: str
    type: str 

class TransactionDetails(TypedDict):
    transaction: str
    transaction_locktime: int
    transaction_size: int
    transaction_version: int
    transaction_vsize: int
    transaction_weight: int
    txhash: str

class SignPsetResult(TypedDict):
    psbt: str
    utxos: List[GdkUtxo]

class GdkAccountAPI():
    def __init__(self, session: gdk.Session, account_pointer: int, name: str):
        self.session = session
        self.name = name
        self.account_pointer = account_pointer
        
    def details(self) -> AccountDetails:
        """get the account details"""
        return self.session.get_subaccount(self.account_pointer).resolve()

    def balance(self, min_num_confs: int = 0) -> Dict[str, int]:
        """get the balance of the account, sorted by asset in a dict"""
        return self.session.get_balance({'subaccount': self.account_pointer, 'num_confs': min_num_confs}).resolve()

    def get_new_address(self) -> AddressDetails:
        return self.session.get_receive_address({'subaccount': self.account_pointer}).resolve()

    def unspents_outputs(self, min_num_confs: int = 0) -> Dict[str, List[GdkUtxo]]:
        details = {
            'subaccount': self.account_pointer,
            'num_confs': min_num_confs,
        }
        return self.session.get_unspent_outputs(details).resolve()['unspent_outputs']

    def utxos(self, min_num_confs: int = 0) -> Dict[str, List[Utxo]]:
        """get the unspents_outputs result and then transform to Utxo objects"""
        unspents_outputs = self.unspents_outputs(min_num_confs)
        utxosByAsset = {}
        for asset, gdkUtxos in unspents_outputs.items():
            utxosByAsset[asset] = [Utxo(gdkUtxo) for gdkUtxo in gdkUtxos]
        return utxosByAsset
    
    def transactions(self, min_block_height: int = None) -> List[Dict]:
        # We'll use possible statuses of UNCONFIRMED, CONFIRMED, FINAL.
        all_txs = []
        index = 0
        # You can override the default number (30) of transactions returned:
        count = 30
        while(True):
            transactions = self.session.get_transactions({'subaccount': self.account_pointer, 'first': index, 'count': count}).resolve()
            for transaction in transactions['transactions']:
                if min_block_height and transaction['block_height'] >= min_block_height:
                    all_txs.append(transaction)

            nb_txs = len(transactions['transactions'])
            if nb_txs < count:
                break
            if min_block_height and transactions['transactions'][nb_txs - 1]['block_height'] < min_block_height:
                break

            index = index + 1
        return all_txs
    
    def _previous_addresses(self, pointer) -> Tuple[List[AddressDetails], int]:
        details = {
            'subaccount': self.account_pointer,
        }
        if pointer is not None:
            details['last_pointer'] = pointer

        res = self.session.get_previous_addresses(details).resolve()
        return res['list'], res['last_pointer'] if 'last_pointer' in res else None
    
    def addresses(self) -> List[AddressDetails]:
        addresses, last_pointer = self._previous_addresses(None)
        while last_pointer != None:
            new_addresses, last_pointer = self._previous_addresses(last_pointer)
            addresses.extend(new_addresses)
        
        return addresses
    
    def send(self, receivers: List[Receiver]) -> str:
        if len(receivers) == 0:
            raise ValueError('No receiver provided')
        details = {
            'subaccount': self.account_pointer,
            'addressees': [receiver_to_dict(receiver) for receiver in receivers],
        }
        
        details = self.session.create_transaction(details).resolve()
        details = self.session.sign_transaction(details).resolve()
        hex_tx = details['transaction']
        self.session.send_transaction(details).resolve()
        return hex_tx
    
class GdkAPI:
    AMP_ACCOUNT_TYPE = '2of2_no_recovery'
    TWO_OF_TWO_ACCOUNT_TYPE = '2of2'
    
    def __init__(self, session: gdk.Session):
        self.session = session

    def register_user(self, mnemonic: str) -> str:
        """creates a new gdk wallet"""
        details = {
            'mnemonic': mnemonic,
            'password': '', # BIP39 password is not used
        }
        details = self.session.register_user({}, details).resolve()
        return details

    def login_with_mnemonic(self, mnemonic: str) -> str:
        """login with a mnemonic to gdk instance"""
        details = {
            'mnemonic': mnemonic,
            'password': '', # BIP39 password is not used
        }
        details = self.session.login_user({}, details).resolve()
        return details

    def encrypt_with_pin(self, mnemonic: str, pin: int) -> PinData:
        """set a new PIN"""
        details = {
            'pin': pin,
            'plaintext': { 'mnemonic': mnemonic },
        }
        return self.session.encrypt_with_pin(details).resolve()['pin_data']

    def login_with_pindata(self, pinData: PinData, pin: str) -> str:
        """login with a pin to gdk instance"""
        details = {
            'pin_data': pinData,
            'pin': pin,
        }
        details = self.session.login_user({}, details).resolve()
        return details

    def get_acccounts(self) -> List[GdkAccountAPI]:
        """get all the existing subaccounts from gdk and create GdkAccount objects for them"""
        subaccounts = self.session.get_subaccounts({}).resolve()
        accounts = [GdkAccountAPI(self.session, account['pointer'], account['name']) for account in subaccounts['subaccounts']]
        return accounts
    
    def get_account(self, account_name: str) -> GdkAccountAPI:
        """get an account by account name"""
        all_accounts = self.get_acccounts()
        for a in all_accounts:
            if a.name == account_name:
                return a
        raise ValueError('Account "{}" not found'.format(account_name))
        
    def create_new_account(self, account_key: str, is_amp: bool) -> GdkAccountAPI:
        """create a new gdk subaccount"""
        account_type = self.AMP_ACCOUNT_TYPE if is_amp else self.TWO_OF_TWO_ACCOUNT_TYPE
        self.session.create_subaccount({'name': account_key, 'type': account_type}).resolve()
        return self.get_account(account_key)

    def broadcast(self, txhex: str) -> str:
        """broadcast a transaction to the network"""
        return self.session.broadcast_transaction(txhex).resolve()['txid']
    
    def get_transaction(self, txid: str) -> TransactionDetails:
        """get a transaction by txid"""
        return self.session.get_transaction(txid).resolve()

    def get_all_unspents_outputs(self) -> List[GdkUtxo]:
        """get all the gdkUtxo objects for all accounts"""
        accounts = self.get_acccounts()
        unspents = []
        for account in accounts:
            account_utxos = account.unspents_outputs()
            for _, utxos in account_utxos.items():
                unspents.extend(utxos)
        return unspents

    def get_all_utxos(self) -> List[Utxo]:
        """get all the Utxo objects for all accounts"""
        return [Utxo(utxo) for utxo in self.get_all_unspents_outputs()]

    def sign_pset(self, psetBase64: str, utxos: List[GdkUtxo], blinding_nonces: List) -> SignPsetResult:        
        details = {
            'psbt': psetBase64,
            'utxos': utxos,
            'blinding_nonces': blinding_nonces,
        }
        print(details)
        return self.session.psbt_sign(details).resolve()
        
    def get_transaction_hex(self, txid: str) -> str:
        """get a transaction by txid"""
        return self.session.get_transaction_details(txid)['transaction']
 
def make_session(network: str) -> gdk.Session:
    return gdk.Session({'name': network})

def get_esplora_url(network: str) -> Tuple[str, str]:
    """returns the esplora host and base url (depends on network)"""
    blockstream_host = 'blockstream.info'
    base = '/{}/api'

    if network == 'testnet-liquid':
        return blockstream_host, base.format('liquidtestnet')

    if network == 'liquid':
        return blockstream_host, base.format('liquid')

    raise Exception("Unable to find base esplora url for network {}".format(network))

def get_tx_status(network: str, txid: str) -> Dict:
    host, base_url = get_esplora_url(network)
    conn = http.client.HTTPSConnection(host)
    conn.request('GET', '{}/tx/{}/status'.format(base_url, txid))
    response = conn.getresponse()
    
    if response.status != 200:
        raise Exception("Error getting transaction status: {} {}".format(response.status, response.reason))

    return json.loads(response.read())

def get_block_details(network: str, txid: str) -> BlockDetails:
    tx_status = get_tx_status(network, txid)
    
    if not tx_status["confirmed"]:
        raise Exception("Transaction not confirmed, impossible to fetch block details")

    return BlockDetails(tx_status["block_hash"], tx_status["block_height"], tx_status["block_time"])
