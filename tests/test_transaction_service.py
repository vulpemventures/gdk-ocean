from typing import TypedDict
import pytest
import wallycore as wally

from domain import FilePinDataRepository, make_session, Locker, GdkAPI, InMemoryPinDataRepository
from services import TransactionService, WalletService, AccountService
from tests.utils import get_env_var

TEST_PASSWORD = 'testdonotuse'
TEST_MNEMONIC = get_env_var('TESTNET_TEST_MNEMONIC')
ALICE_MNEMONIC = TEST_MNEMONIC
BOB_MNEMONIC = get_env_var('TESTNET_TEST_MNEMONIC_2')

@pytest.mark.asyncio
async def test_send_pset():
    accountName = 'mainAccountTest'
    session = make_session('testnet-liquid')
    locker = await Locker.create()
    transactionSvc = TransactionService(session, locker)
    accountSvc = AccountService(session, locker)
    walletSvc = WalletService(session, InMemoryPinDataRepository())
    walletSvc.create_wallet(TEST_MNEMONIC, TEST_PASSWORD)

    addrs = accountSvc.derive_address(accountName, 2)
    coinSelection = transactionSvc.select_utxos(accountName, '144c654344aa716d6f3abcc1ca90e5641e4e2a7f633bc09fe3baf64585819a49', 100000)
    FEE = 500
    
    gdkAPI = GdkAPI(session)
    
    lbtc = '144c654344aa716d6f3abcc1ca90e5641e4e2a7f633bc09fe3baf64585819a49'
    outputs = [
        { 'address': addrs[0]['address'], 'amount': coinSelection.amount - FEE, 'asset': lbtc, 'blinder_index': 0 },
    ]
    
    if coinSelection.change > 0:
        outputs += [{ 'address': addrs[1]['address'], 'amount': coinSelection.change, 'asset': lbtc, 'blinder_index': 0 }]
    
    outputs += [{ 'address': None, 'amount': FEE, 'asset': lbtc, 'blinder_index': None }]
    
    psetb64 = transactionSvc.create_pset([u.to_pset_input_args() for u in coinSelection.utxos], outputs)
    blinded = transactionSvc.blind_pset(psetb64)
    signed = transactionSvc.sign_pset(blinded)
    assert signed is not None

    pset = wally.psbt_from_base64(signed)
    wally.psbt_finalize(pset)
    tx = wally.psbt_extract(pset)
    assert tx is not None

@pytest.mark.asyncio
async def test_send_amp_confidential_pset():
    accountName = 'mainAccountTest'
    ampAccountName = 'ampAccountTest'
    session = make_session('testnet-liquid')
    walletSvc = WalletService(session, FilePinDataRepository('pin_data.json'))
    walletSvc.create_wallet(TEST_MNEMONIC, TEST_PASSWORD)
    # walletSvc.login_with_pin(TEST_PASSWORD)
    lockerSvc = await Locker.create()
    accountSvc = AccountService(session, lockerSvc)
    transactionSvc = TransactionService(session, lockerSvc)

    FEE = 500
    fees_selection = transactionSvc.select_utxos(accountName, '144c654344aa716d6f3abcc1ca90e5641e4e2a7f633bc09fe3baf64585819a49', FEE)
    amp_selection = transactionSvc.select_utxos(ampAccountName, 'bea126b86ac7f7b6fc4709d1bb1a8482514a68d35633a5580d50b18504d5c322', 1)
    receiveAddr = 'vjTvPHdcJFZrYL9LmFpPootd1tmWqzugF9MXwhet6cdeCKEK6WJrb2mPEQGw7WNpikAoTq9ui22GU2pS' 

    outputs = [
        {'address': receiveAddr, 'amount': 1, 'asset': 'bea126b86ac7f7b6fc4709d1bb1a8482514a68d35633a5580d50b18504d5c322', 'blinder_index': 0},
    ]
    
    if fees_selection.change > 0:
        changeAddr = accountSvc.derive_address(accountName, 1)[0]
        outputs += [{ 'address': changeAddr['address'], 'amount': fees_selection.change, 'asset': '144c654344aa716d6f3abcc1ca90e5641e4e2a7f633bc09fe3baf64585819a49', 'blinder_index': 0 }]
    
    outputs += [{'address': None, 'amount': FEE, 'asset': '144c654344aa716d6f3abcc1ca90e5641e4e2a7f633bc09fe3baf64585819a49', 'blinder_index': None}]

    b64 = transactionSvc.create_pset(
        [u.to_pset_input_args() for u in fees_selection.utxos] + [u.to_pset_input_args() for u in amp_selection.utxos], 
        outputs
    )
    
    blinded = transactionSvc.blind_pset(b64)
    signed = transactionSvc.sign_pset(blinded)    
    assert signed is not None

    pset = wally.psbt_from_base64(signed)
    wally.psbt_finalize(pset)
    tx = wally.psbt_extract(pset)
    assert tx is not None
    
@pytest.mark.asyncio
async def test_send_fee_nonlast_amp_confidential_pset():
    accountName = 'mainAccountTest'
    ampAccountName = 'ampAccountTest'
    session = make_session('testnet-liquid')
    walletSvc = WalletService(session, FilePinDataRepository('pin_data.json'))
    walletSvc.create_wallet(TEST_MNEMONIC, TEST_PASSWORD)
    # walletSvc.login_with_pin(TEST_PASSWORD)
    lockerSvc = await Locker.create()
    accountSvc = AccountService(session, lockerSvc)
    transactionSvc = TransactionService(session, lockerSvc)

    FEE = 500
    fees_selection = transactionSvc.select_utxos(accountName, '144c654344aa716d6f3abcc1ca90e5641e4e2a7f633bc09fe3baf64585819a49', FEE)
    amp_selection = transactionSvc.select_utxos(ampAccountName, 'bea126b86ac7f7b6fc4709d1bb1a8482514a68d35633a5580d50b18504d5c322', 1)
    receiveAddr = 'vjTvPHdcJFZrYL9LmFpPootd1tmWqzugF9MXwhet6cdeCKEK6WJrb2mPEQGw7WNpikAoTq9ui22GU2pS' 

    outputs = [
        {'address': receiveAddr, 'amount': 1, 'asset': 'bea126b86ac7f7b6fc4709d1bb1a8482514a68d35633a5580d50b18504d5c322', 'blinder_index': 0},
        {'address': None, 'amount': FEE, 'asset': '144c654344aa716d6f3abcc1ca90e5641e4e2a7f633bc09fe3baf64585819a49', 'blinder_index': None}
    ]
    
    if fees_selection.change > 0:
        changeAddr = accountSvc.derive_address(accountName, 1)[0]
        outputs += [{ 'address': changeAddr['address'], 'amount': fees_selection.change, 'asset': '144c654344aa716d6f3abcc1ca90e5641e4e2a7f633bc09fe3baf64585819a49', 'blinder_index': 0 }]
    
    b64 = transactionSvc.create_pset(
        [u.to_pset_input_args() for u in fees_selection.utxos] + [u.to_pset_input_args() for u in amp_selection.utxos], 
        outputs
    )
    
    blinded = transactionSvc.blind_pset(b64)
    signed = transactionSvc.sign_pset(blinded)    
    assert signed is not None

    pset = wally.psbt_from_base64(signed)
    wally.psbt_finalize(pset)
    tx = wally.psbt_extract(pset)
    assert tx is not None


class Services(TypedDict):
    walletSvc: WalletService
    accountSvc: AccountService
    transactionSvc: TransactionService

async def create_gdk_ocean_services(mnemonic: str) -> Services:
    session = make_session('testnet-liquid')
    walletSvc = WalletService(session, InMemoryPinDataRepository())
    walletSvc.create_wallet(mnemonic, TEST_PASSWORD)
    # walletSvc.login_with_pin(TEST_PASSWORD)
    lockerSvc = await Locker.create()
    accountSvc = AccountService(session, lockerSvc)
    transactionSvc = TransactionService(session, lockerSvc)
    return {
        'walletSvc': walletSvc,
        'accountSvc': accountSvc,
        'transactionSvc': transactionSvc
    }

@pytest.mark.asyncio
async def test_swap_pset():
    TEST_asset_hash = '38fca2d939696061a8f76d4e6b5eecd54e3b4221c846f24a6b279e79952850a5'
    LBTC_asset_hash = '144c654344aa716d6f3abcc1ca90e5641e4e2a7f633bc09fe3baf64585819a49'
    
    aliceAccountName = 'swapTestAccount'
    bobAccountName = 'swapTestAccount'
    bobAccountNameForFee = 'swapTestAccountFee'
    
    
    alice = await create_gdk_ocean_services(ALICE_MNEMONIC)
    bob = await create_gdk_ocean_services(BOB_MNEMONIC)

    # alice pays the fees and sends 1 BTC to bob
    # bob send 1 TEST to alice
    # alice blinds the outputs
    
    FEES_AMOUNT = 500
    
    blinder_index = 0
    bob_address = bob['accountSvc'].derive_address(bobAccountName, 1)[0]
    bob_utxos_selection = bob['transactionSvc'].select_utxos(bobAccountName, TEST_asset_hash, 1500)
    bob_utxos_selection_fees = bob['transactionSvc'].select_utxos(bobAccountNameForFee, LBTC_asset_hash, FEES_AMOUNT)
    
    bob_inputs = [u.to_pset_input_args() for u in bob_utxos_selection.utxos] + [u.to_pset_input_args() for u in bob_utxos_selection_fees.utxos]
    bob_outputs = [
        {'address': bob_address['address'], 'amount': 1500, 'asset': LBTC_asset_hash, 'blinder_index': blinder_index},
        {'address': None, 'amount': FEES_AMOUNT, 'asset': LBTC_asset_hash, 'blinder_index': None}
    ]
    
    if bob_utxos_selection.change > 0:
        bob_outputs += [{ 'address': bob_address['address'], 'amount': bob_utxos_selection.change, 'asset': TEST_asset_hash, 'blinder_index': blinder_index }]

    if bob_utxos_selection_fees.change > 0:
        bob_outputs += [{ 'address': bob_address['address'], 'amount': bob_utxos_selection_fees.change, 'asset': LBTC_asset_hash, 'blinder_index': blinder_index }]
    
    # bob creates the pset and send it to alice with the blinding data associated with inputs
    pset = bob['transactionSvc'].create_pset(bob_inputs, bob_outputs)
    bob_blinding_data = []
    num_inputs = len(bob_inputs)
    pset_wally = wally.psbt_from_base64(pset) 
    for i in range(num_inputs):
        txid = wally.hex_from_bytes(wally.psbt_get_input_previous_txid(pset_wally, i)[::-1])
        for u in bob_utxos_selection.utxos:
            if u.txid == txid:
                bob_blinding_data.append(u.to_blinding_data(i))
                break
    
    # alice receives the pset and blinding data
    alice_address = alice['accountSvc'].derive_address(aliceAccountName, 1)[0]
    alice_utxos_selection = alice['transactionSvc'].select_utxos(aliceAccountName, LBTC_asset_hash, 1500)
    
    alice_inputs = [u.to_pset_input_args() for u in alice_utxos_selection.utxos]
    alice_outputs = [
        {'address': alice_address['address'], 'amount': 1500, 'asset': TEST_asset_hash, 'blinder_index': blinder_index},
    ]

    if alice_utxos_selection.change > 0:
        alice_outputs += [{ 'address': alice_address['address'], 'amount': alice_utxos_selection.change, 'asset': LBTC_asset_hash, 'blinder_index': blinder_index }]
        
    # alice adds its inputs and outputs to the pset
    pset = alice['transactionSvc'].update_pset(pset, alice_inputs, alice_outputs)
    
    # alice blinds the outputs (using the bob's blinding data)
    blinded_pset = alice['transactionSvc'].blind_pset(pset, bob_blinding_data)

    # alice signs the pset
    signed = alice['transactionSvc'].sign_pset(blinded_pset)
    
    # bob receives the signed pset from alice and add signatures
    signed = bob['transactionSvc'].sign_pset(signed)
    
    pset = wally.psbt_from_base64(signed)
    wally.psbt_finalize(pset)
    tx = wally.psbt_extract(pset)
    assert tx is not None
    hex_tx = wally.tx_to_hex(tx, 0)
    print(hex_tx)
    