from typing import Tuple
import pytest

from domain import make_session, InMemoryPinDataRepository, Locker, GdkAPI
from services import AccountService, WalletService
import greenaddress as gdk

async def init_account_service() -> Tuple[AccountService, GdkAPI]:
    session = make_session('testnet-liquid')
    repo = InMemoryPinDataRepository()
    walletSvc = WalletService(session, repo)
    seed = walletSvc.generate_seed()
    walletSvc.create_wallet(seed, 'testdonotuse')
    locker = await Locker.create()
    accountSvc = AccountService(walletSvc, locker)
    return accountSvc, GdkAPI(session)

@pytest.mark.asyncio
async def test_create_amp_account():
    accountSvc, api = await init_account_service()
    accountSvc.create_amp_account('test')
    a = api.get_account('test')
    assert a.details()['type'] == GdkAPI.AMP_ACCOUNT_TYPE
    
@pytest.mark.asyncio
async def test_create_amp_account_with_existing_name():
    accountSvc, _ = await init_account_service()
    accountSvc.create_amp_account('test')
    with pytest.raises(Exception) as e:
        accountSvc.create_amp_account('test')
    assert e.value.args[0] == 'account test already exists'
    
@pytest.mark.asyncio
async def test_create_account():
    accountSvc, api = await init_account_service()
    accountSvc.create_account('test')
    a = api.get_account('test')
    assert a.details()['type'] == GdkAPI.TWO_OF_TWO_ACCOUNT_TYPE

@pytest.mark.asyncio
async def test_derive_address():
    accountSvc, _ = await init_account_service()
    accountSvc.create_account('deriveaddresstestaccount')
    addrs = accountSvc.derive_address('deriveaddresstestaccount', 2)
    assert len(addrs) == 2
    assert len(accountSvc.list_addresses('deriveaddresstestaccount')) == 2
    accountSvc.derive_address('deriveaddresstestaccount', 3)
    assert len(accountSvc.list_addresses('deriveaddresstestaccount')) == 5
    
    
   