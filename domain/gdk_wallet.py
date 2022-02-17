import logging
from typing import Dict, Tuple, TypedDict
import json
import http.client
import greenaddress as gdk
from domain.block_details import BlockDetails
from domain.gdk_utils import make_session, gdk_resolve
from domain.gdk_account import GdkAccount
from domain.locker import Locker

class GdkWallet:
    def __init__(self, net: str):
        self.AMP_ACCOUNT_TYPE = '2of2_no_recovery'
        self.PIN_DATA_FILENAME = 'pin_data.json'

        self.last_block_height = 0
        self.accounts: Dict[str, GdkAccount] = {}
        self.locker: Locker = None
        self.network = net
        self.session = make_session(self.network)
        
    @classmethod
    async def create_new_wallet(cls, mnemonic: str, pin: str, network: str):
        """Class method to create and return an instance of gdk_wallet"""
        self = cls(network)
        self.locker = await Locker.create()
        self.session.register_user({}, mnemonic).resolve()
        self.session.login_user({}, {'mnemonic': mnemonic, 'password': ""}).resolve()
        self.set_pin(mnemonic, pin)
        self._get_existing_subaccounts()
        return self

    @classmethod
    async def login_with_pin(cls, pin: str, network: str):
        """Class method to create and return an instance of gdk_wallet"""
        self = cls(network)
        self.locker = await Locker.create()
        pin_data = json.loads(open(self.PIN_DATA_FILENAME).read())
        self.session.login_user({}, {'pin': pin, 'pin_data': pin_data}).resolve()
        self._get_existing_subaccounts()
        logging.debug('Logged in')
        return self
    
    def _get_existing_subaccounts(self):
        """get all the existing subaccounts from gdk and create GdkAccount objects for them"""
        subaccounts = self.session.get_subaccounts({}).resolve()
        for account in subaccounts['subaccounts']:
            self.accounts[account['name']] = GdkAccount(self.session, account['name'], self.locker)

    def is_logged_in(self) -> bool:
        return self.session is not None

    def set_pin(self, mnemonic, pin):
        pin_data = gdk.set_pin(self.session.session_obj, mnemonic, str(pin), str('device_id_1'))
        open(self.PIN_DATA_FILENAME, 'w').write(pin_data)
        return pin_data

    def sign_transaction(self, tx_hex: str) -> str:
        details = {
            'subaccount': self.subaccount_pointer,
            'transaction': tx_hex
            # TODO other members
        }
        details = gdk_resolve(gdk.sign_transaction(self.session.session_obj, json.dumps(details)))
        return details['tx_hex']
    
    def get_account(self, account_key: str) -> GdkAccount:
        acc = self.accounts[account_key]
        if acc is None:
            raise Exception("Account not found")

        return acc
    
    def create_new_account(self, account_key: str) -> GdkAccount:
        """create a new gdk subaccount + the corresponding GdkAccount object"""
        self.session.create_subaccount({'name': account_key, 'type': self.AMP_ACCOUNT_TYPE}).resolve()
        new_account = GdkAccount(self.session, account_key, self.locker)
        self.accounts[account_key] = new_account
        return new_account
        
        
    def get_transaction_hex(self, txid: str) -> str:
        """get the transaction as hex string, the transaction must be associated with wallet"""
        details = self.session.get_transaction_details(txid)
        return details["transaction"]

    def _get_esplora_url(self) -> Tuple[str, str]:
        """returns the esplora host and base url (depends on network)"""
        blockstream_host = 'blockstream.info'
        base = '/{}/api'

        if self.network == 'testnet-liquid':
            return blockstream_host, base.format('liquidtestnet')

        if self.network == 'liquid':
            return blockstream_host, base.format('liquid')

        raise Exception("Unable to find base esplora url for network {}".format(self.network))
    
    def _get_tx_status(self, txid: str) -> Dict:
        host, base_url = self._get_esplora_url()
        conn = http.client.HTTPSConnection(host)
        conn.request('GET', '{}/tx/{}/status'.format(base_url, txid))
        response = conn.getresponse()
        
        if response.status != 200:
            raise Exception("Error getting transaction status: {} {}".format(response.status, response.reason))

        return json.loads(response.read())
       
    def get_block_details(self, txid: str) -> BlockDetails:
        tx_status = self._get_tx_status(txid)
        
        if not tx_status["confirmed"]:
            raise Exception("Transaction not confirmed, impossible to fetch block details")

        return BlockDetails(tx_status["block_hash"], tx_status["block_height"], tx_status["block_time"])
    