import logging
import greenaddress as gdk
from domain.gdk import GdkAPI
from domain.pin_data_repository import PinDataRepositoryInterface

class WalletService:
    def __init__(self, session: gdk.Session, pin_data_repo: PinDataRepositoryInterface) -> None:
        self._pin_data_repository = pin_data_repo
        self._gdkAPI = GdkAPI(session)
    
    def is_logged(self) -> bool:
        """is_logged returns True in case of wallet is ready to be used"""
        if self._gdkAPI is None or self._gdkAPI.session is None:
            return False
        
        try:
            self._gdkAPI.get_acccounts()
            return True
        except:
            return False
            
    def generate_seed(self) -> str:
        return gdk.generate_mnemonic()
    
    def create_wallet(self, mnemonic: str, password: str) -> None:
        self._gdkAPI.register_user(mnemonic)
        self._gdkAPI.login_with_mnemonic(mnemonic)
        pin_data = self._gdkAPI.encrypt_with_pin(mnemonic, password)
        self._pin_data_repository.write(pin_data)

    def login_with_mnemonic(self, mnemonic: str) -> None:
        if self.is_logged():
            raise Exception('Wallet is already logged in')
        
        logging.debug('logging in...')
        self._gdkAPI.login_with_mnemonic(mnemonic)
    
    def login_with_pin(self, pin: str) -> None:
        if self.is_logged():
            raise Exception('Wallet is already logged in')
        
        logging.debug('logging in...')
        pin_data = self._pin_data_repository.read()
        self._gdkAPI.login_with_pindata(pin_data, pin)
    
    def change_password(self, password: str, newPassword: str) -> None:
        raise Exception('Not implemented')
    