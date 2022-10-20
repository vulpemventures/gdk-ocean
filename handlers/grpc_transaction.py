import logging
import wallycore as wally
from domain import Receiver 
from domain.types import PsetOutputArgs
from handlers.utils import make_utxo_proto, make_utxos_list_proto, unblinded_input_proto_to_blinding_data
from services import TransactionService, AccountService
from ocean.v1 import transaction_pb2, transaction_pb2_grpc

class GrpcTransactionServicer(transaction_pb2_grpc.TransactionServiceServicer):
    def __init__(self, transactionService: TransactionService, accountService: AccountService, explorerURL: str):
        self._transaction_svc = transactionService
        self._account_svc = accountService
        self._explorerURL = explorerURL
    
    def GetTransaction(self, request: transaction_pb2.GetTransactionRequest, _) -> transaction_pb2.GetTransactionResponse:
        transaction_details = self._transaction_svc.get_transaction(request.txid)
        return transaction_pb2.GetTransactionResponse(tx_hex=transaction_details['transaction'])
    
    def SelectUtxos(self, request: transaction_pb2.SelectUtxosRequest, _) -> transaction_pb2.SelectUtxosResponse:
        coinselection = self._transaction_svc.select_utxos(request.account_name, request.target_asset, request.target_amount)
        selected_utxos = [make_utxo_proto(utxo, self._explorerURL) for utxo in coinselection['utxos']]
        logging.debug(f"Selected UTXOs: {coinselection}")
        return transaction_pb2.SelectUtxosResponse(
            utxos=make_utxos_list_proto(request.account_name, selected_utxos, self._explorerURL),
            change=coinselection['change'],
        )
    
    def EstimateFees(self, _, __) -> transaction_pb2.EstimateFeesResponse:
        fee_amount = self._transaction_svc.estimate_fees()
        return transaction_pb2.EstimateFeesResponse(fee_amount=fee_amount)
    
    def SignTransaction(self, request: transaction_pb2.SignTransactionRequest, _) -> transaction_pb2.SignTransactionResponse:
        signed = self._transaction_svc.sign_transaction(request.tx_hex)
        return transaction_pb2.SignTransactionResponse(tx_hex=signed)
    
    def BroadcastTransaction(self, request: transaction_pb2.BroadcastTransactionRequest, _) -> transaction_pb2.BroadcastTransactionResponse:
        txid = self._transaction_svc.broadcast_transaction(request.tx_hex)
        return transaction_pb2.BroadcastTransactionResponse(txid=txid)
    
    def CreatePset(self, request: transaction_pb2.CreatePsetRequest, _) -> transaction_pb2.CreatePsetResponse:
        inputs = []
        outputs = []
        
        for i in request.inputs:
            utxo = self._account_svc.get_utxo(i.txid, i.index)
            inputs.append(utxo.to_pset_input_args())
            
        for o in request.outputs:
            outputs.append(PsetOutputArgs(address=o.address, amount=o.amount, asset=o.asset, blinder_index=0))
        
        pset = self._transaction_svc.create_pset(inputs, outputs)
        return transaction_pb2.CreatePsetResponse(pset=pset)
    
    def UpdatePset(self, request: transaction_pb2.UpdatePsetRequest, _) -> transaction_pb2.UpdatePsetResponse:
        pset = wally.psbt_from_base64(request.pset)
        blind_index = wally.psbt_get_num_inputs(pset) # we'll use next in index as blinder index
        
        inputs = []
        outputs = []
        
        for i in request.inputs:
            utxo = self._account_svc.get_utxo(i.txid, i.index)
            inputs.append(utxo.to_pset_input_args())
            
        for o in request.outputs:
            outputs.append(PsetOutputArgs(address=o.address, amount=o.amount, asset=o.asset, blinder_index=blind_index))

        return transaction_pb2.UpdatePsetResponse(pset=self._transaction_svc.update_pset(pset, inputs, outputs))
    
    def BlindPset(self, request: transaction_pb2.BlindPsetRequest, _) -> transaction_pb2.BlindPsetResponse:
        extra_blinding_data = [unblinded_input_proto_to_blinding_data(i) for i in request.extra_unblinded_inputs]
        blinded = self._transaction_svc.blind_pset(request.pset, extra_blinding_data)
        return transaction_pb2.BlindPsetResponse(pset=blinded)
    
    def SignPset(self, request: transaction_pb2.SignPsetRequest, _) -> transaction_pb2.SignPsetResponse:
        pset = wally.psbt_from_base64(request.pset)
        if request.sighash_type is not None:
            for i in range(wally.psbt_get_num_inputs(pset)):
                wally.psbt_set_input_sighash(pset, i, request.sighash_type)
        signed = self._transaction_svc.sign_pset(wally.psbt_to_base64(pset))
        return transaction_pb2.SignPsetResponse(pset=signed)
    
    def Mint(self, request, context):
        raise NotImplementedError
    
    def Remint(self, request, context):
        raise NotImplementedError
    
    def Burn(self, request, context):
        raise NotImplementedError
    
    def Transfer(self, request: transaction_pb2.TransferRequest, _) -> transaction_pb2.TransferResponse:
        transfer_tx = self._transaction_svc.transfer(request.account_name, [Receiver(address=receiver.address, sats=receiver.amount, asset=receiver.asset) for receiver in request.receivers])
        return transaction_pb2.TransferResponse(tx_hex=transfer_tx)
    
    def PegInAddress(self, request, context):
        raise NotImplementedError
    
    def ClaimPegIn(self, request, context):
        raise NotImplementedError