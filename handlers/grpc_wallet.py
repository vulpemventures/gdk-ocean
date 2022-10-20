from ocean.v1 import wallet_pb2, wallet_pb2_grpc
from services import WalletService

class GrpcWalletServicer(wallet_pb2_grpc.WalletServiceServicer):
    def __init__(self, walletService: WalletService):
        self._svc = walletService
    
    def GenSeed(self, _, __):
        mnemonic = self._svc.generate_mnemonic()
        return wallet_pb2.GenSeedResponse(mnemonic=mnemonic)
    
    def CreateWallet(self, request: wallet_pb2.CreateWalletRequest, _):
        self._svc.create_wallet(request.mnemonic, request.password)
        return wallet_pb2.CreateWalletResponse()
    
    def Unlock(self, request: wallet_pb2.UnlockRequest, _):
        self._svc.login_with_pin(request.password)
        return wallet_pb2.UnlockResponse()
    
    def ChangePassword(self, request: wallet_pb2.ChangePasswordRequest, _):
        self._svc.change_password(request.current_password, request.newPassword)
        return wallet_pb2.ChangePasswordResponse()
    
    def RestoreWallet(self, request: wallet_pb2.RestoreWalletRequest, _):
        self._svc.login_with_mnemonic(request.mnemonic)
        return wallet_pb2.RestoreWalletResponse()

    def Status(self, _, __):
        if self._svc.is_logged_in():
            return wallet_pb2.StatusResponse(initialized=True, synced=True, unlocked=True)
        return wallet_pb2.StatusResponse(initialized=False, synced=False, unlocked=False)
            
    def GetInfo(self, _, __):
        return wallet_pb2.GetInfoResponse() # TODO