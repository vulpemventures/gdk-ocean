import asyncio
import logging
import grpc
from handlers.grpc_account import GrpcAccountServicer
from handlers.grpc_notifications import GrpcNotificationsServicer
from handlers.grpc_transaction import GrpcTransactionServicer
from handlers.grpc_wallet import GrpcWalletServicer
from services.account import AccountService
from services.notifications import NotificationsService
from services.transaction import TransactionService
from services.wallet import WalletService

from signal import SIGINT, SIGTERM
from ocean.v1alpha import wallet_pb2_grpc, notification_pb2_grpc, transaction_pb2_grpc, account_pb2_grpc
import greenaddress as gdk

async def main():
    wallet_service = WalletService()
    transaction_service = TransactionService(wallet_service)
    notifications_service = NotificationsService(wallet_service)
    account_service = AccountService(wallet_service)
    
    logging.basicConfig(level=logging.DEBUG)
    
    # start the grpc server
    server = grpc.aio.server()
    address = 'localhost:50051'
    server.add_insecure_port(address)
    
    wallet_servicer = GrpcWalletServicer(wallet_service)
    transaction_servicer = GrpcTransactionServicer(transaction_service)
    account_servicer = GrpcAccountServicer(account_service)
    wallet_pb2_grpc.add_WalletServiceServicer_to_server(wallet_servicer, server)
    transaction_pb2_grpc.add_TransactionServiceServicer_to_server(transaction_servicer, server)
    account_pb2_grpc.add_AccountServiceServicer_to_server(account_servicer, server)

    # notificiation servicer is async, we need to await the start of notifications service
    logging.debug("start the notifications service...")
    notifications_servicer = await GrpcNotificationsServicer.create(notifications_service)
    notification_pb2_grpc.add_NotificationServiceServicer_to_server(notifications_servicer, server)
    notif_svc_task = asyncio.create_task(notifications_service.start())
    logging.debug("notifications service started")
    
    logging.info("starting grpc server... " + address)
    
    try:
        await asyncio.gather(
            server.start(),
            notif_svc_task,
            notifications_servicer.task,
        )
    except asyncio.CancelledError:
        logging.info("stopping grpc server...")
        await server.stop(5)
        
    
if __name__ == "__main__":
    gdk.init({})
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    main_task = asyncio.ensure_future(main())
    
    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, lambda: main_task.cancel())
    
    try:
        loop.run_until_complete(main_task)
    finally:
        loop.close()
