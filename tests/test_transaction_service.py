from binascii import unhexlify
import pytest
import wallycore as wally
import greenaddress as gdk
from domain.gdk import GdkAPI
from domain.gdk_utils import make_session
from domain.locker import Locker
from domain.pin_data_repository import FilePinDataRepository, InMemoryPinDataRepository
from domain.utils import Asset, add_input_utxo

from services.transaction import TransactionService
from services.wallet import WalletService
from services.account import AccountService

gdk.init({})

TEST_PASSWORD = 'testdonotuse'
TEST_MNEMONIC = 'fault barrel struggle connect render join style comic divert provide cable field social normal retreat space gospel ribbon diet gallery elegant equip grant mammal'

def test_create_pset():
    walletSvc = WalletService('localtest-liquid')
    transactionSvc = TransactionService(walletSvc)
    psetb64 = transactionSvc.create_empty_pset()
    pset = wally.psbt_from_base64(psetb64)
    assert pset is not None
    outputs_len = wally.psbt_get_num_outputs(pset)
    inputs_len = wally.psbt_get_num_inputs(pset)
    assert inputs_len == 0
    assert outputs_len == 0

@pytest.mark.asyncio
@pytest.mark.skip('not implemented')
async def test_send_pset():
    walletSvc = WalletService(FilePinDataRepository('pin_data.json'), 'local')
    transactionSvc = TransactionService(walletSvc)
    accountSvc = AccountService(walletSvc)
    await walletSvc.create_wallet(TEST_MNEMONIC, TEST_PASSWORD)
    # await walletSvc.login()

    utxos = accountSvc.list_utxos('fees')
    assert len(utxos) > 0
    utxo = None
    for u in utxos:
        if u.confidential == False:
            utxo = u
            break
    assert utxo is not None

    addr = accountSvc.derive_address('test', 1)

    pset = wally.psbt_from_base64(transactionSvc.create_empty_pset())
    wally.psbt_add_tx_input_at(pset, 0, 0, utxo.to_tx_input())
    b64 = wally.psbt_to_base64(pset, 0)

    lbtc = Asset.from_hex(utxo.asset).to_bytes()
    
    output0 = wally.tx_elements_output_init(
        unhexlify(addr[0]['script']),
        lbtc,
        wally.tx_confidential_value_from_satoshi(utxo.value - 1000),
    )

    wally.psbt_add_tx_output_at(pset, 0, 0, output0)

    output1 = wally.tx_elements_output_init(
        None,
        lbtc,
        wally.tx_confidential_value_from_satoshi(1000),
    )
    wally.psbt_add_tx_output_at(pset, 1, 0, output1)

    b64 = wally.psbt_to_base64(pset, 0)
    details = transactionSvc.sign_pset(b64)
    pset = wally.psbt_from_base64(details['psbt'])
    tx = wally.psbt_extract(pset)
    h = wally.tx_to_hex(tx, 0)
    
@pytest.mark.asyncio
async def test_send_amp_confidential_pset():
    session = make_session('testnet-liquid')
    walletSvc = WalletService(session, FilePinDataRepository('pin_data.json'))
    # walletSvc.create_wallet(TEST_MNEMONIC, TEST_PASSWORD)
    walletSvc.login_with_pin(TEST_PASSWORD)
    lockerSvc = await Locker.create()
    transactionSvc = TransactionService(session, lockerSvc)
    accountSvc = AccountService(session, lockerSvc, walletSvc)

    fees_selection = transactionSvc.select_utxos('amp', '144c654344aa716d6f3abcc1ca90e5641e4e2a7f633bc09fe3baf64585819a49', 1000)
    amp_selection = transactionSvc.select_utxos('amp', 'bea126b86ac7f7b6fc4709d1bb1a8482514a68d35633a5580d50b18504d5c322', 1)

    utxo = amp_selection.utxos[0]
    fee_utxo = fees_selection.utxos[0]

    receiveAddr = 'vjTvPHdcJFZrYL9LmFpPootd1tmWqzugF9MXwhet6cdeCKEK6WJrb2mPEQGw7WNpikAoTq9ui22GU2pS' 
    receiveScript = wally.address_to_scriptpubkey(receiveAddr, 'testnet-liquid')
    blindingPubKey = wally.confidential_addr_to_ec_public_key(receiveAddr, wally.WALLY_CA_PREFIX_LIQUID_TESTNET)

    pset = wally.psbt_from_base64(transactionSvc.create_empty_pset())
    add_input_utxo(GdkAPI(session), pset, utxo.gdk_utxo)
    add_input_utxo(GdkAPI(session), pset, fee_utxo.gdk_utxo)

    amp_asset = Asset.from_hex('bea126b86ac7f7b6fc4709d1bb1a8482514a68d35633a5580d50b18504d5c322').to_bytes()
    lbtc = Asset.from_hex('144c654344aa716d6f3abcc1ca90e5641e4e2a7f633bc09fe3baf64585819a49').to_bytes()
    
    output0 = wally.tx_elements_output_init(
        unhexlify(receiveScript),
        amp_asset,
        wally.tx_confidential_value_from_satoshi(utxo.value),
    )

    output1 = wally.tx_elements_output_init(
        None,
        lbtc,
        wally.tx_confidential_value_from_satoshi(1000),
    )
    wally.psbt_add_tx_output_at(pset, 0, 0, output0)
    wally.psbt_add_tx_output_at(pset, 1, 0, output1)
    wally.psbt_set_output_blinding_public_key(pset, 0, blindingPubKey)
    wally.psbt_set_output_blinder_index(pset, 0, 0)

    b64 = wally.psbt_to_base64(pset, 0)
    blinded = transactionSvc.blind_pset(b64)
    signed = transactionSvc.sign_pset(blinded)    

    if not wally.psbt_finalize(signed) == wally.WALLY_OK:
        raise Exception('Failed to finalize PSBT')
    
    tx = wally.psbt_extract(signed)
    print(tx)
    
    