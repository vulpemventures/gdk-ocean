from ast import Dict
from handlers.utils import make_utxos_list_proto
from services import AccountService
from domain import Outpoint
from ocean.v1 import account_pb2, account_pb2_grpc, types_pb2

class GrpcAccountServicer(account_pb2_grpc.AccountServiceServicer):
    def __init__(self, accountService: AccountService, explorerURL: str) -> None:
        self._svc = accountService
        self._explorerURL = explorerURL
    
    def CreateAccountBIP44(self, request, context):
        raise Exception("unimplemented rpc")
    
    def CreateAccountCustom(self, request: account_pb2.CreateAccountCustomRequest, _) -> account_pb2.CreateAccountCustomResponse:
        self._svc.create_amp_account(request.name)
        return account_pb2.CreateAccountCustomResponse(account_name=request.name)
    
    def SetAccountTemplate(self, request, context):
        raise Exception("unimplemented rpc")
    
    def DeriveAddresses(self, request: account_pb2.DeriveAddressesRequest, _) -> account_pb2.DeriveAddressesResponse:
        addresses = self._svc.derive_address(request.account_name, request.num_of_addresses)
        return account_pb2.DeriveAddressesResponse(addresses=map(lambda address: address['address'], addresses))
    
    def DeriveChangeAddress(self, request, _):
        return self.DeriveAddresses(request, _)
    
    def ListAddresses(self, request: account_pb2.ListAddressesRequest, _):
        addresses = self._svc.list_addresses(request.account_name)
        return account_pb2.ListAddressesResponse(
            addresses=map(lambda address: address['address'], addresses)
        )
    
    def Balance(self, request: account_pb2.BalanceRequest, _) -> account_pb2.BalanceResponse:
        total_balance = self._svc.balance(request.account_name, 0)
        confirmed_balance = self._svc.balance(request.account_name, 1)
        
        result: Dict[str, types_pb2.BalanceInfo] = {}
        
        for asset, balance in total_balance.items():
            result[asset] = types_pb2.BalanceInfo(
                unconfirmed_balance=balance - confirmed_balance[asset],
                confirmed_balance=confirmed_balance[asset],
                total_balance=balance
            )
        
        return account_pb2.BalanceResponse(balance=result)

    def ListUtxos(self, request: account_pb2.ListUtxosRequest, _):
        utxos = self._svc.list_utxos(request.account_name)
        spendable = []
        locked = []
        for utxo in utxos:
            if self._svc._locker.is_locked(Outpoint.from_utxo(utxo)):
                locked.append(utxo)
            else:
                spendable.append(utxo)
        
        spendable_utxos_msg = make_utxos_list_proto(request.account_name, spendable, self._explorerURL)
        locked_utxos_msg = make_utxos_list_proto(request.account_name, locked, self._explorerURL)
        
        response = account_pb2.ListUtxosResponse(
            spendable_utxos=spendable_utxos_msg,
            locked_utxos=locked_utxos_msg
        )
        return response
        