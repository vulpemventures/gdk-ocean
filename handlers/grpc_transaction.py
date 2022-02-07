import logging
from domain.receiver import Receiver
from domain.utxo import to_grpc_utxo
from services.transaction import TransactionService
from ocean.v1alpha import transaction_pb2, transaction_pb2_grpc

class GrpcTransactionServicer(transaction_pb2_grpc.TransactionServiceServicer):
    def __init__(self, transactionService: TransactionService):
        self._svc = transactionService
    
    def SelectUtxos(self, request: transaction_pb2.SelectUtxosRequest, _) -> transaction_pb2.SelectUtxosResponse:
        coinselection = self._svc.select_utxos(request.account_key.name, request.target_asset, request.target_amount)
        utxos = map(lambda utxo: to_grpc_utxo(utxo), coinselection['utxos'])
        logging.debug(f"Selected UTXOs: {coinselection}")
        return transaction_pb2.SelectUtxosResponse(
            utxos=utxos,
            change=coinselection['change'],
        )
    
    def EstimateFees(self, _, __) -> transaction_pb2.EstimateFeesResponse:
        fee_amount = self._svc.estimate_fees()
        return transaction_pb2.EstimateFeesResponse(fee_amount=fee_amount)
    
    def SignTransaction(self, request: transaction_pb2.SignTransactionRequest, _) -> transaction_pb2.SignTransactionResponse:
        signed = self._svc.sign_transaction(request.tx_hex)
        return transaction_pb2.SignTransactionResponse(tx_hex=signed)
    
    def BroadcastTransaction(self, request: transaction_pb2.BroadcastTransactionRequest, _) -> transaction_pb2.BroadcastTransactionResponse:
        txid = self._svc.broadcast_transaction(request.tx_hex)
        return transaction_pb2.BroadcastTransactionResponse(txid=txid)
    
    def CreatePset(self, request: transaction_pb2.CreatePsetRequest, context) -> transaction_pb2.CreatePsetResponse:
        pass
    
    def UpdatePset(self, request, context):
        pass
    
    def BlindPset(self, request, context):
        pass
    
    def SignPset(self, request, context):
        pass
    
    def Mint(self, request, context):
        pass
    
    def Remint(self, request, context):
        pass
    
    def Burn(self, request, context):
        pass
    
    def Transfer(self, request: transaction_pb2.TransferRequest, _) -> transaction_pb2.TransferResponse:
        transfer_tx = self._svc.transfer(request.account_key.name, [Receiver(address=receiver.address, sats=receiver.amount, asset=receiver.asset) for receiver in request.receivers])
        return transaction_pb2.TransferResponse(tx_hex=transfer_tx)
    
    def PegInAddress(self, request, context):
        pass
    
    def ClaimPegIn(self, request, context):
        pass