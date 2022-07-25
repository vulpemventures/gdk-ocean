import json
import pytest
from domain.gdk_utils import make_session
from domain.pin_data_repository import FilePinDataRepository, InMemoryPinDataRepository
from services.wallet import WalletService
import greenaddress as gdk
import wallycore as wally

@pytest.fixture
def static_pin_data():
    # test data for login call, password is "test"
    return json.loads("{\"encrypted_data\": \"0e0cba65a194175ff6190de56ae029af5468b179ec35d727a9dac2cf1248e4a0f775fee0190accff12113eff99b54394016653a2a05d1cad837789dc27a7bdb7202cc4a7818fa3101bbcebbf70092fff513b3878c0541290edf48ad3f2a6ade8b850c3f8ab7d3b79d97b1d54cf0ba38c361d27cebcc28a720360d4f62702caa07ee870b08c8b7233507b41026e9e74e8e96e19b773654b638f4a1519032fc111c43c63ea70452144acf555939f06bf9e\", \"pin_identifier\": \"e4d0f354-41a4-4a31-83ba-454e1ed97825\", \"salt\": \"oKytrCoTo+dqHYEzcSo0jw==\"}")

@pytest.fixture(scope="function")
def repository():
    return InMemoryPinDataRepository()

@pytest.fixture
def password():
    return 'test'

@pytest.mark.asyncio
async def test_login(static_pin_data):
    repo = InMemoryPinDataRepository()
    repo.write(static_pin_data)
    walletSvc = WalletService(repo, 'testnet-liquid')
    await walletSvc.login('test')
    assert walletSvc.get_wallet().is_logged_in()

@pytest.mark.asyncio
async def test_create_wallet(password: str):
    walletSvc = WalletService(FilePinDataRepository('./pin.json'), 'testnet-liquid')
    seed = walletSvc.generate_seed()
    await walletSvc.create_wallet(seed, password)
    wallet = walletSvc.get_wallet()
    assert wallet is not None

@pytest.mark.asyncio
async def test_encrypt_with_pin():
    details = {
        'pin': 1875,
        'plaintext': "test"
    }
        
    session = make_session('testnet-liquid')
    session = gdk.Session({'name': 'testnet-liquid'})
    pin_data = session.encrypt_with_pin({ 'pin': '1234', 'plaintext': 'word word word word'}).resolve()
    print(pin_data)
    json_pin_data = json.dumps(pin_data['pin_data'])
