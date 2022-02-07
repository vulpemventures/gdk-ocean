import logging
import click
import grpc
from ocean.v1alpha import wallet_pb2_grpc, wallet_pb2, account_pb2_grpc, account_pb2, types_pb2, transaction_pb2_grpc, transaction_pb2, notification_pb2, notification_pb2_grpc

def _get_wallet_stub_from_context(ctx: click.Context) -> wallet_pb2_grpc.WalletServiceStub:
    return ctx.obj['wallet']

def _get_account_stub_from_context(ctx: click.Context) -> account_pb2_grpc.AccountServiceStub:
    return ctx.obj['account']

def _get_transaction_stub_from_context(ctx: click.Context) -> transaction_pb2_grpc.TransactionServiceStub:
    return ctx.obj['transaction']

def _get_notification_stub_from_context(ctx: click.Context) -> notification_pb2_grpc.NotificationServiceStub:
    return ctx.obj['notification']

@click.group()
@click.option('--debug', is_flag=True, default=True)
@click.option('--host', default='localhost')
@click.option('--port', default=50051)
@click.pass_context
def cli(ctx: click.Context, debug: bool, host: str, port: int):
    """
    A command line interface for Gdk-ocean.
    """
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
    Generate a random seed.
    """
    wallet_stub = _get_wallet_stub_from_context(ctx)
    seed = wallet_stub.GenSeed(wallet_pb2.GenSeedRequest())
    logging.info(seed.mnemonic)

@cli.command()
@click.option('--mnemonic', '-m', default=None)
@click.option('--password', '-p', default=None)
@click.pass_context
def create(ctx: click.Context, mnemonic: str, password: str):
    request = wallet_pb2.CreateWalletRequest()
    request.mnemonic = mnemonic
    request.password = password.encode('utf-8')
    
    wallet_stub = _get_wallet_stub_from_context(ctx)
    response = wallet_stub.CreateWallet(request)
    logging.info(response)


@cli.command()
@click.option('--password', '-p', default=None)
@click.pass_context
def unlock(ctx: click.Context, password: str):
    request = wallet_pb2.UnlockRequest()
    request.password = password.encode('utf-8')
    wallet_stub = _get_wallet_stub_from_context(ctx)
    response = wallet_stub.Unlock(request)
    logging.info(response)

@cli.command()
@click.option('--name', '-n', default="AMP Account")
@click.pass_context
def createaccount(ctx: click.Context, name: str):
    request = account_pb2.CreateAccountRequest(name=name)
    account_stub = _get_account_stub_from_context(ctx)
    response = account_stub.CreateAccount(request)
    logging.info(response)

@cli.command()
@click.option('--account', '-a', default=None)
@click.pass_context
def getnewaddress(ctx: click.Context, account: str):
    account_k = types_pb2.AccountKey()
    account_k.id = 0
    account_k.name = account
    request = account_pb2.DeriveAddressRequest(account_key=account_k)
    request.num_of_addresses = 1
    
    account_stub = _get_account_stub_from_context(ctx)
    
    response = account_stub.DeriveAddress(request)
    logging.info(response)
    
@cli.command()
@click.option('--account', '-a', default=None)
@click.pass_context
def listaddresses(ctx: click.Context, account: str):
    account_k = types_pb2.AccountKey()
    account_k.id = 0
    account_k.name = account
    request = account_pb2.ListAddressesRequest(account_key=account_k)
    
    account_stub = _get_account_stub_from_context(ctx)
    response = account_stub.ListAddresses(request)
    logging.info(response)


@cli.command()
@click.option('--account', '-a', default=None)
@click.pass_context
def balance(ctx: click.Context, account: str):
    account_k = types_pb2.AccountKey()
    account_k.id = 0
    account_k.name = account
    request = account_pb2.BalanceRequest(account_key=account_k)
    account_stub = _get_account_stub_from_context(ctx)
    response = account_stub.Balance(request)
    logging.info(response)

@cli.command()
@click.option('--account', '-a', default=None)
@click.pass_context
def listutxos(ctx: click.Context, account: str):
    account_k = types_pb2.AccountKey()
    account_k.id = 0
    account_k.name = account
    request = account_pb2.ListUtxosRequest(account_key=account_k)
    account_stub = _get_account_stub_from_context(ctx)
    response = account_stub.ListUtxos(request)
    logging.info(response)

@cli.command()
@click.pass_context
def fees(ctx: click.Context):
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
    account_k = types_pb2.AccountKey()
    account_k.id = 0
    account_k.name = account
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
    request = transaction_pb2.SelectUtxosRequest(account_key=types_pb2.AccountKey(id=0, name=account), target_amount=int(sats), target_asset=asset, strategy=0)
    transaction_stub = _get_transaction_stub_from_context(ctx)
    response = transaction_stub.SelectUtxos(request)
    logging.info(response)
    
@cli.command()
@click.option('--account', '-a', default=None)
@click.pass_context
def watchutxos(ctx: click.Context, account: str):
    request = notification_pb2.UtxosNotificationsRequest(account_key=types_pb2.AccountKey(id=0, name=account))
    notification_stub = _get_notification_stub_from_context(ctx)
    for notification in notification_stub.UtxosNotifications(request):
        logging.info(notification)
    
@cli.command()
@click.pass_context
def watchtxs(ctx: click.Context):
    request = notification_pb2.TransactionNotificationsRequest()
    notification_stub = _get_notification_stub_from_context(ctx)
    for notification in notification_stub.TransactionNotifications(request):
        logging.info(notification)

if __name__ == '__main__':
    cli(obj={})