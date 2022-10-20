import json
import logging
from typing import List, Tuple
import click
import grpc
from ocean.v1 import wallet_pb2_grpc, account_pb2_grpc, notification_pb2_grpc, transaction_pb2_grpc, wallet_pb2, account_pb2, transaction_pb2, notification_pb2, types_pb2

def _get_wallet_stub_from_context(ctx: click.Context) -> wallet_pb2_grpc.WalletServiceStub:
    return ctx.obj['wallet']

def _get_account_stub_from_context(ctx: click.Context) -> account_pb2_grpc.AccountServiceStub:
    return ctx.obj['account']

def _get_transaction_stub_from_context(ctx: click.Context) -> transaction_pb2_grpc.TransactionServiceStub:
    return ctx.obj['transaction']

def _get_notification_stub_from_context(ctx: click.Context) -> notification_pb2_grpc.NotificationServiceStub:
    return ctx.obj['notification']

def parse_address(address: str) -> Tuple[str, int]:
    if ':' in address:
        host, port = address.split(':')
        if not host:
            host = '0.0.0.0'
        return host, int(port)
    else:
        raise click.BadParameter(f'invalid address {address}')
    
@click.group()
@click.option('--debug', is_flag=True, default=True)
@click.option('--address', '-a', default='localhost:50051')
@click.pass_context
def cli(ctx: click.Context, debug: bool, address: str):
    """
    A command line interface for gdk-ocean.
    """
    host, port = parse_address(address)
    channel = grpc.insecure_channel(f'{host}:{port}')
    wallet_svc = wallet_pb2_grpc.WalletServiceStub(channel)
    account_svc = account_pb2_grpc.AccountServiceStub(channel)
    transaction_svc = transaction_pb2_grpc.TransactionServiceStub(channel)
    notifications_svc = notification_pb2_grpc.NotificationServiceStub(channel)
    
    ctx.ensure_object(dict)

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    
    ctx.obj['wallet'] = wallet_svc
    ctx.obj['account'] = account_svc
    ctx.obj['transaction'] = transaction_svc
    ctx.obj['notification'] = notifications_svc
    
    global verbose_flag
    verbose_flag = debug
    
@cli.command()
@click.pass_context
def genseed(ctx: click.Context):
    """
    Generate a random seed
    """
    wallet_stub = _get_wallet_stub_from_context(ctx)
    response = wallet_stub.GenSeed(wallet_pb2.GenSeedRequest())
    logging.info(response.mnemonic)

@cli.command()
@click.option('--mnemonic', '-m', default=None)
@click.option('--password', '-p', default=None)
@click.pass_context
def create(ctx: click.Context, mnemonic: str, password: str):
    """
    create a new wallet with a given mnemonic and password
    """
    request = wallet_pb2.CreateWalletRequest()
    request.mnemonic = mnemonic
    request.password = password
    
    wallet_stub = _get_wallet_stub_from_context(ctx)
    response = wallet_stub.CreateWallet(request)
    logging.info(response)


@cli.command()
@click.option('--password', '-p', default=None)
@click.pass_context
def unlock(ctx: click.Context, password: str):
    """ 
    unlock the wallet with a given password
    """
    request = wallet_pb2.UnlockRequest()
    request.password = password
    wallet_stub = _get_wallet_stub_from_context(ctx)
    response = wallet_stub.Unlock(request)
    logging.info(response)

@cli.command()
@click.option('--name', '-n', default="AMP Account")
@click.pass_context
def createaccount(ctx: click.Context, name: str):
    """
    create a new account with a given account name
    """
    request = account_pb2.CreateAccountCustomRequest(name=name)
    account_stub = _get_account_stub_from_context(ctx)
    response = account_stub.CreateAccountCustom(request)
    logging.info(response)

@cli.command()
@click.option('--account', '-a', default=None)
@click.pass_context
def getnewaddress(ctx: click.Context, account: str):
    """
    generate the next address for the given account name
    """
    request = account_pb2.DeriveAddressesRequest(account_name=account, num_of_addresses=1)
    account_stub = _get_account_stub_from_context(ctx)
    response = account_stub.DeriveAddresses(request)
    logging.info(response)
    
@cli.command()
@click.option('--account', '-a', default=None)
@click.pass_context
def listaddresses(ctx: click.Context, account: str):
    """
    list all addresses of an account
    """
    request = account_pb2.ListAddressesRequest(account_name=account)
    account_stub = _get_account_stub_from_context(ctx)
    response = account_stub.ListAddresses(request)
    logging.info(response)


@cli.command()
@click.option('--account', '-a', default=None)
@click.pass_context
def balance(ctx: click.Context, account: str):
    """
    get the balance of a given account
    """
    request = account_pb2.BalanceRequest(account_name=account)
    account_stub = _get_account_stub_from_context(ctx)
    response = account_stub.Balance(request)
    logging.info(response)

@cli.command()
@click.option('--account', '-a', default=None)
@click.pass_context
def listutxos(ctx: click.Context, account: str):
    """
    list all the unlocked utxos of a given account
    """
    request = account_pb2.ListUtxosRequest(account_name=account)
    account_stub = _get_account_stub_from_context(ctx)
    response = account_stub.ListUtxos(request)
    logging.info(response)

@cli.command()
@click.pass_context
def fees(ctx: click.Context):
    """
    get a real-time estimate of the chain fees
    """
    request = transaction_pb2.EstimateFeesRequest()
    transaction_stub = _get_transaction_stub_from_context(ctx)
    response = transaction_stub.EstimateFees(request)
    logging.info(response)
    
@cli.command()
@click.option('--account', '-a', default=None)
@click.option('--to', '-t', default=None)
@click.option('--sats', '-s', default=None)
@click.option('--asset', '-ass', default=None)
@click.pass_context
def transfer(ctx: click.Context, account: str, to: str, sats: str, asset: str):
    """
    send some funds from an account to a given address
    """
    out = types_pb2.Output()
    out.asset = asset
    out.amount = int(sats)
    out.address = to
    receivers = [out]
    request = transaction_pb2.TransferRequest(account_name=account, receivers=receivers)
    transaction_stub = _get_transaction_stub_from_context(ctx)
    response = transaction_stub.Transfer(request)
    logging.info(response)
    
@cli.command()
@click.option('--account', '-a', default=None)
@click.option('--sats', '-s', default=None)
@click.option('--asset', '-ass', default=None)
@click.pass_context
def selectutxos(ctx: click.Context, account: str, sats: str, asset: str):
    """
    select utxos to use for a given amount of sats (and asset)
    """
    request = transaction_pb2.SelectUtxosRequest(account_name=account, target_amount=int(sats), target_asset=asset, strategy=0)
    transaction_stub = _get_transaction_stub_from_context(ctx)
    response = transaction_stub.SelectUtxos(request)
    logging.info(response)
    
@cli.command()
@click.pass_context
def watchutxos(ctx: click.Context):
    """
    start a loop logging the new utxo notifications for a given account
    """
    request = notification_pb2.UtxosNotificationsRequest()
    notification_stub = _get_notification_stub_from_context(ctx)
    for notification in notification_stub.UtxosNotifications(request):
        logging.info(notification)
    
@cli.command()
@click.pass_context
def watchtxs(ctx: click.Context):
    """
    start a loop logging the new tx notifications for a given account
    """
    request = notification_pb2.TransactionNotificationsRequest()
    notification_stub = _get_notification_stub_from_context(ctx)
    for notification in notification_stub.TransactionNotifications(request):
        logging.info(notification)

@cli.command()
@click.option('--txid', '-t', default=None)
@click.pass_context
def gettransaction(ctx: click.Context, txid: str):
    """
    get a transaction by its txid
    """
    request = transaction_pb2.GetTransactionRequest(txid=txid)
    transaction_stub = _get_transaction_stub_from_context(ctx)
    response = transaction_stub.GetTransaction(request)
    logging.info(response)


def parse_input_string(input_str: str) -> types_pb2.Input:
    """
    parse the input string into a list of inputs
    """
    i = json.loads(input_str)
    if i['txid'] is None or i['index'] is None:
        raise Exception('txid and index are required')
    return types_pb2.Input(txid=i['txid'], index=i['index'])

def parse_output_string(output_str: str) -> types_pb2.Output:
    """
    parse the output string into a list of outputs
    """
    o = json.loads(output_str)
    if o['address'] is None or o['amount'] is None or o['asset'] is None:
        raise Exception('address, amount and asset are required')
    return types_pb2.Output(address=o['address'], amount=o['amount'], asset=o['asset'])

@cli.command()
@click.option('--input', '-i', multiple=True, default=[])
@click.option('--output', '-o', multiple=True, default=[])
@click.pass_context
def createpset(ctx: click.Context, input: List[str], output: List[str]):
    """
    create a pset from a list of inputs and outputs
    """
    inputs = [parse_input_string(i) for i in input]
    outputs = [parse_output_string(o) for o in output]
    transaction_stub = _get_transaction_stub_from_context(ctx)
    response = transaction_stub.CreatePset(transaction_pb2.CreatePsetRequest(inputs=inputs, outputs=outputs))
    logging.info(response.pset)
    
@cli.command()
@click.option('--pset', '-p', default=None)
@click.option('--input', '-i', multiple=True, default=[])
@click.option('--output', '-o', multiple=True, default=[])
@click.pass_context
def updatepset(ctx: click.Context, pset: str, input: List[str], output: List[str]):
    """
    update an existing pset
    """
    inputs = [parse_input_string(i) for i in input]
    outputs = [parse_output_string(o) for o in output]
    transaction_stub = _get_transaction_stub_from_context(ctx)
    response = transaction_stub.UpdatePset(transaction_pb2.UpdatePsetRequest(pset=pset, inputs=inputs, outputs=outputs))
    logging.info(response.pset)
    
@cli.command()
@click.option('--pset', '-p', default=None)
@click.pass_context
def blindpset(ctx: click.Context, pset: str):
    transaction_stub = _get_transaction_stub_from_context(ctx)
    response = transaction_stub.BlindPset(transaction_pb2.BlindPsetRequest(pset=pset))
    logging.info(response.pset)
    
@cli.command()
@click.option('--pset', '-p', default=None)
@click.pass_context
def signpset(ctx: click.Context, pset: str):
    transaction_stub = _get_transaction_stub_from_context(ctx)
    response = transaction_stub.SignPset(transaction_pb2.SignPsetRequest(pset=pset))
    logging.info(response.pset)

if __name__ == '__main__':
    cli(obj={})