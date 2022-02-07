from ast import Dict
from domain.utxo import to_grpc_utxo
from services.account import AccountService
from ocean.v1alpha import account_pb2, account_pb2_grpc, types_pb2

class GrpcAccountServicer(account_pb2_grpc.AccountServiceServicer):
    def __init__(self, accountService: AccountService) -> None:
        self._svc = accountService
    
    def CreateAccount(self, request: account_pb2.CreateAccountRequest, _) -> account_pb2.CreateAccountResponse:
        self._svc.create_account(request.name)
        return account_pb2.CreateAccountResponse()
    
    def SetAccountTemplate(self, request, context):
        raise Exception("unimplemented rpc")
    
    def DeriveAddress(self, request: account_pb2.DeriveAddressRequest, _):
        addresses = self._svc.derive_address(request.account_key.name, request.num_of_addresses)
        return account_pb2.DeriveAddressResponse(addresses=map(lambda address: address['address'], addresses))
    
    def ListAddresses(self, request: account_pb2.ListAddressesRequest, _):
        addresses = self._svc.list_addresses(request.account_key.name)
        return account_pb2.ListAddressesResponse(
            addresses=map(lambda address: address['address'], addresses)
        )
    
    def Balance(self, request: account_pb2.BalanceRequest, _) -> account_pb2.BalanceResponse:
        total_balance = self._svc.balance(request.account_key.name, 0)
        confirmed_balance = self._svc.balance(request.account_key.name, 1)
        
        result: Dict[str, types_pb2.BalanceInfo] = {}
        
        for asset, balance in total_balance.items():
            result[asset] = types_pb2.BalanceInfo(
                unconfirmed_balance=balance - confirmed_balance[asset],
                confirmed_balance=confirmed_balance[asset],
                total_balance=balance
            )
        
        return account_pb2.BalanceResponse(balance=result)

    def ListUtxos(self, request: account_pb2.ListUtxosRequest, _):
        utxos = self._svc.list_utxos(request.account_key.name)
        spendable = [utxo for utxo in utxos if not utxo['is_locked']]
        locked = [utxo for utxo in utxos if utxo['is_locked']]
        
        account_k = types_pb2.AccountKey()
        account_k.id = 0
        account_k.name = request.account_key.name
        
        spendable_utxos_msg = types_pb2.Utxos(
            account_key=account_k,
            utxos=map(lambda utxo: to_grpc_utxo(utxo), spendable)
        )
        
        locked_utxos_msg = types_pb2.Utxos(
            account_key=account_k,
            utxos=map(lambda utxo: to_grpc_utxo(utxo), locked)
        )
        
        response = account_pb2.ListUtxosResponse(
            spendable_utxos=[spendable_utxos_msg],
            locked_utxos=[locked_utxos_msg]
        )
        return response
        