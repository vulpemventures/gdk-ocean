from ocean.v1alpha import wallet_pb2, wallet_pb2_grpc
from services.wallet import WalletService

class GrpcWalletServicer(wallet_pb2_grpc.WalletServiceServicer):
    def __init__(self, walletService: WalletService):
        self._svc = walletService
    
    def GenSeed(self, _, __):
        seed = self._svc.generate_seed()
        response = wallet_pb2.GenSeedResponse()
        response.mnemonic = seed
        return response
    
    async def CreateWallet(self, request: wallet_pb2.CreateWalletRequest, _):
        await self._svc.create_wallet(request.mnemonic, request.password, "testnet-liquid")
        return wallet_pb2.CreateWalletResponse()
    
    async def Unlock(self, request: wallet_pb2.UnlockRequest, _):
        await self._svc.login(request.password)
        return wallet_pb2.UnlockResponse()
    
    def ChangePassword(self, request: wallet_pb2.ChangePasswordRequest, _):
        self._svc.change_password(request.current_password, request.newPassword)
        return wallet_pb2.ChangePasswordResponse()
    
    async def RestoreWallet(self, request: wallet_pb2.RestoreWalletRequest, _):
        await self._svc.login(request.password)
        return wallet_pb2.RestoreWalletResponse()

    def Status(self, _, __):
        if self._svc.is_logged_in():
            return wallet_pb2.StatusResponse(status=wallet_pb2.Status.OPEN)

        return wallet_pb2.StatusResponse(status=wallet_pb2.Status.CLOSED)
            
    def GetInfo(self, _, __):
        return wallet_pb2.GetInfoResponse() # TODO