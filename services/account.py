import greenaddress as gdk
from domain import AddressDetails, GdkAPI, GdkAccountAPI, Locker, Outpoint, Utxo
from typing import Dict, List

class AccountService:
    def __init__(self, session: gdk.Session, locker: Locker):
        self._locker = locker
        self._gdkAPI = GdkAPI(session)
        
    def _account_exists_guard(self, account_name: str):
        """check if the account already exists"""
        existing_accounts = self._gdkAPI.get_accounts()
        if account_name in [a.name for a in existing_accounts]:
            raise Exception(f'account {account_name} already exists')
        
    def create_amp_account(self, account_name: str) -> GdkAccountAPI:
        """create a new GDK account for AMP assets"""
        self._account_exists_guard(account_name)
        return self._gdkAPI.create_new_account(account_name, True)
    
    def create_account(self, account_name: str) -> GdkAccountAPI:
        """create a new GDK account"""
        self._account_exists_guard(account_name)
        return self._gdkAPI.create_new_account(account_name, False)
    
    def derive_address(self, account_name: str, num_addresses: int) -> List[AddressDetails]:
        """derive new addresses for an account"""
        if num_addresses < 1:
            raise ValueError("num_addresses must be >= 1")
        
        account = self._gdkAPI.get_account(account_name)
        addresses = [account.get_new_address() for _ in range(num_addresses)]
        return addresses

    def list_addresses(self, account_name: str) -> List[AddressDetails]:
        """list all known addresses of the account"""
        account = self._gdkAPI.get_account(account_name)
        return account.addresses()

    def list_all_addresses(self) -> List[AddressDetails]:
        """list all accounts addresses"""
        accounts = self._gdkAPI.get_accounts()
        result = []
        for account in accounts:
            for addresses in account.addresses():
                result.append(addresses)
        return result
    
    def balance(self, account_name: str, min_num_confs: int) -> Dict[str, int]:
        """get the balance of the account, include only unspent where min_num_confs is met"""
        account = self._gdkAPI.get_account(account_name)
        return account.get_balance(min_num_confs)
    
    def list_utxos(self, account_name: str) -> List[Utxo]:
        """list all the unlocked known unspents for an account"""
        account = self._gdkAPI.get_account(account_name)
        utxosByAsset = account.utxos()
        utxos: List[Utxo] = []
        for utxosForAsset in utxosByAsset.values():
            unlocked = [utxo for utxo in utxosForAsset if not self._locker.is_locked(Outpoint.from_utxo(utxo))]
            utxos.extend(unlocked)
        return utxos
    
    def list_all_utxos(self) -> List[Utxo]:
        """list all unlocked utxos for all accounts"""
        accounts = self._gdkAPI.get_accounts()
        result = []
        for account in accounts:
            account_utxos = self.list_utxos(account.name)
            result += account_utxos
        return result
    
    def get_utxo(self, txid: str, index: int) -> Utxo:
        """get a specific utxo"""
        all_utxos = self.list_all_utxos()
        for u in all_utxos:
            if u.txid == txid and u.index == index:
                return u

    def get_GAID(self, account_name: str) -> str:
        """get the account GAID for the given account name"""
        account = self._gdkAPI.get_account(account_name)
        return account.details()['receiving_id']