import logging
from typing import Dict
import json
import greenaddress as gdk
from domain.gdk_utils import make_session, gdk_resolve
from domain.gdk_account import GdkAccount
from domain.locker import Locker

class GdkWallet:
    def __init__(self):
        self.AMP_ACCOUNT_TYPE = '2of2_no_recovery'
        self.PIN_DATA_FILENAME = 'pin_data.json'

        self.session: gdk.Session = None
        self.last_block_height = 0
        self.accounts: Dict[str, GdkAccount] = {}
        self.locker: Locker = None
        
    @classmethod
    async def create_new_wallet(cls, mnemonic: str, pin: str, network: str):
        """Class method to create and return an instance of gdk_wallet"""
        self = cls()
        self.locker = await Locker.create()
        self.session = make_session(network)
        self.session.register_user({}, mnemonic).resolve()
        self.session.login_user({}, {'mnemonic': mnemonic, 'password': ""}).resolve()
        self.set_pin(mnemonic, pin)
        self._get_existing_subaccounts()
        return self

    @classmethod
    async def login_with_pin(cls, pin: str, network: str):
        """Class method to create and return an instance of gdk_wallet"""
        self = cls()
        self.locker = await Locker.create()
        pin_data = json.loads(open(self.PIN_DATA_FILENAME).read())
        self.session = make_session(network)
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
        return self.session is not None and self.session.session_obj is not None 

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
        