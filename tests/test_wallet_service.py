import pytest
from services.wallet import WalletService
from domain import make_session, InMemoryPinDataRepository

@pytest.fixture
def static_pin_data():
    # test data for login call, password is "testdonotuse"
    return {"encrypted_data": "6465b118a4b672db35a502fc85a7edcbcaaf3d7acb45893e5d92bb1a25cff5bf8f94e8053dc7d7ff176e2fbb47716e8e97788b6707b0ee873ca4f6724e56e0e6752abf8b4d10d9fc1c44f9ccc9024a7cc182dfcfa4c997b4ba94530633b6545410927d1039bb288b00d5a51d3ec9c1110f01d01ee6844781a47323eee3f7ef2a81cccb16b614b82fc02172a1c0e66c667a83e6d5a62163a02902663a0c066702edac847277990492df19a52b34fcc492954d2e8ff16fa02f25b4da3abaea8572618c6f96d5a237070431fbdcab1cc22e", "pin_identifier": "1fbf94a0-9265-4d58-ad88-080e041b67e4", "salt": "SBzZ3uK6RPC6HIHEgYvGVg=="}

@pytest.fixture
def password():
    return 'testdonotuse'

def test_login(static_pin_data, password):
    session = make_session('testnet-liquid')
    repo = InMemoryPinDataRepository()
    repo.write(static_pin_data)
    walletSvc = WalletService(session, repo)
    walletSvc.login_with_pin(password)
    assert walletSvc.is_logged() is True

def test_create_wallet(password: str):
    pin_data_repo = InMemoryPinDataRepository()
    session = make_session('testnet-liquid')
    walletSvc = WalletService(session, pin_data_repo)
    seed = walletSvc.generate_seed()
    walletSvc.create_wallet(seed, password)
    assert walletSvc.is_logged() is True
    pin_data = pin_data_repo.read()
    assert pin_data is not None
