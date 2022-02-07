import logging
from domain.gdk_wallet import GdkWallet
import greenaddress as gdk

class WalletService:
    def __init__(self) -> None:
        self._wallet: GdkWallet = None
    
    """is_logged returns True in case of wallet is ready to be used"""
    def _is_logged(self) -> bool:
        if not self._wallet:
            return False
        
        return self._wallet.is_logged_in()
    
    def get_wallet(self) -> GdkWallet:
        if not self._is_logged():
            raise Exception('Wallet is not ready (locked or not set up)')
        return self._wallet
    
    def generate_seed(self) -> str:
        return gdk.generate_mnemonic()
    
    async def create_wallet(self, mnemonic: str, password: str, network: str) -> None:
        if self._is_logged():
            raise Exception('Wallet is already logged in') 
    
        self._wallet = await GdkWallet.create_new_wallet(mnemonic, password, network)

    async def login(self, password: bytes) -> None:
        if self._is_logged():
            raise Exception('Wallet is already logged in')
        
        logging.debug('logging in...')
        self._wallet = await GdkWallet.login_with_pin(str(password), 'testnet-liquid')
    
    def change_password(self, password: str, newPassword: str) -> None:
        pass
    