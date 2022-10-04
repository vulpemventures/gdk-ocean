import logging
from typing import Tuple
import click
import grpc
from ocean import v1 as proto

# AccountKey class is a duplicate version of AccountKey class in domain/account_key.py
# it lets to run the cli without the domain package (and thus without the dependencies)
class AccountKey():
    def __init__(self, name: str, account_id: int) -> None:
        self.name = name
        self.id = account_id
        
    @classmethod
    def from_name(cls, name: str) -> 'AccountKey':
        return cls(name, 0)

def _get_wallet_stub_from_context(ctx: click.Context) -> proto.WalletServiceStub:
    return ctx.obj['wallet']

def _get_account_stub_from_context(ctx: click.Context) -> proto.AccountServiceStub:
    return ctx.obj['account']

def _get_transaction_stub_from_context(ctx: click.Context) -> proto.TransactionServiceStub:
    return ctx.obj['transaction']

def _get_notification_stub_from_context(ctx: click.Context) -> proto.NotificationServiceStub:
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
    wallet_svc = proto.WalletServiceStub(channel)
    account_svc = proto.AccountServiceStub(channel)
    transaction_svc = proto.TransactionServiceStub(channel)
    notifications_svc = proto.NotificationServiceStub(channel)
    
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
    seed = wallet_stub.GenSeed(wallet_pb2.GenSeedRequest())
    logging.info(seed.mnemonic)

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
    request = account_pb2.CreateAccountRequest(name=name)
    account_stub = _get_account_stub_from_context(ctx)
    response = account_stub.CreateAccount(request)
    logging.info(response)

@cli.command()
@click.option('--account', '-a', default=None)
@click.pass_context
def getnewaddress(ctx: click.Context, account: str):
    """
    generate the next address for the given account name
    """
    account_k = AccountKey.from_name(account).to_proto()
    request = account_pb2.DeriveAddressRequest(account_key=account_k)
    request.num_of_addresses = 1
    
    account_stub = _get_account_stub_from_context(ctx)
    
    response = account_stub.DeriveAddress(request)
    logging.info(response)
    
@cli.command()
@click.option('--account', '-a', default=None)
@click.pass_context
def listaddresses(ctx: click.Context, account: str):
    """
    list all addresses of an account
    """
    account_k = AccountKey.from_name(account).to_proto()
    request = account_pb2.ListAddressesRequest(account_key=account_k)
    
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
    account_k = AccountKey.from_name(account).to_proto()
    request = account_pb2.BalanceRequest(account_key=account_k)
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
    account_k = AccountKey.from_name(account).to_proto()
    request = account_pb2.ListUtxosRequest(account_key=account_k)
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
    account_k = AccountKey.from_name(account).to_proto()
    out = types_pb2.Output()
    out.asset = asset
    out.amount = int(sats)
    out.address = to
    receivers = [out]
    request = transaction_pb2.TransferRequest(account_key=account_k, receivers=receivers)
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
    account_k = AccountKey.from_name(account).to_proto()
    request = transaction_pb2.SelectUtxosRequest(account_key=account_k, target_amount=int(sats), target_asset=asset, strategy=0)
    transaction_stub = _get_transaction_stub_from_context(ctx)
    response = transaction_stub.SelectUtxos(request)
    logging.info(response)
    
@cli.command()
@click.option('--account', '-a', default=None)
@click.pass_context
def watchutxos(ctx: click.Context, account: str):
    """
    start a loop logging the new utxo notifications for a given account
    """
    account_k = AccountKey.from_name(account).to_proto()
    request = notification_pb2.UtxosNotificationsRequest(account_key=account_k)
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

if __name__ == '__main__':
    cli(obj={})