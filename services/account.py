from domain.address_details import AddressDetails
from domain.gdk_account import GdkAccount
from domain.gdk_wallet import GdkWallet
from typing import Dict, List

from domain.utxo import Utxo
from services.wallet import WalletService

class AccountService:
    def __init__(self, wallet_svc: WalletService) -> None:
        self._wallet_svc = wallet_svc
        
    """create a new GDK account"""
    def create_account(self, account_name: str) -> GdkAccount:
        wallet = self._wallet_svc.get_wallet()
        return wallet.create_new_account(account_name)
    
    """derive new addresses for an account"""
    def derive_address(self, account_name: str, num_addresses: int) -> List[AddressDetails]:
        wallet = self._wallet_svc.get_wallet()
        account = wallet.get_account(account_name)
        addresses = []
        for _ in range(num_addresses):
            addresses.append(account.get_new_address())
        return addresses

    """list all known addresses of the account"""
    def list_addresses(self, account_name: str) -> List[AddressDetails]:
        wallet = self._wallet_svc.get_wallet()
        account = wallet.get_account(account_name)
        return account.list_all_addresses()
    
    """get the balance of the account, include only unspent where min_num_confs is met"""
    def balance(self, account_name: str, min_num_confs: int) -> Dict[str, int]:
        wallet = self._wallet_svc.get_wallet()
        account = wallet.get_account(account_name)
        return account.get_balance(min_num_confs)
    
    """list all the known unspents for an account"""
    def list_utxos(self, account_name: str) -> List[Utxo]:
        wallet = self._wallet_svc.get_wallet()
        account = wallet.get_account(account_name)
        utxosByAsset = account.get_all_utxos(False)
        utxos: List[Utxo] = []
        for utxosForAsset in utxosByAsset.values():
            utxos.extend(utxosForAsset)
        return utxos