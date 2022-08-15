import asyncio
import logging
import grpc
import argparse

from domain import FilePinDataRepository, Locker, make_session
from services import WalletService, TransactionService, NotificationsService, AccountService
from handlers import GrpcWalletServicer, GrpcTransactionServicer, GrpcAccountServicer, GrpcNotificationsServicer

from signal import SIGINT, SIGTERM
from ocean.v1alpha import wallet_pb2_grpc, notification_pb2_grpc, transaction_pb2_grpc, account_pb2_grpc
import greenaddress as gdk

logging.basicConfig(level=logging.DEBUG)

async def main():
    parser = argparse.ArgumentParser(description='Ocean gRPC server')
    parser.add_argument('--port', type=int, default=50051, help='gRPC port')
    parser.add_argument('--pin_data_path', type=str, default='./pin_data.json', help='path to encrypted pin data file')
    parser.add_argument('--network', type=str, default='testnet-liquid', help='network to run the session on (testnet-liquid or liquid)')
    
    args = parser.parse_args()

    # init GDK config
    gdk.init({})
    
    address = 'localhost:%d' % args.port
    
    # create the gdk session
    session = make_session(args.network)
    
    # create the file store for the pin_data
    pin_data_repo = FilePinDataRepository(args.pin_data_path)
    
    wallet_service = WalletService(session, pin_data_repo)
    locker = await Locker.create()
    account_service = AccountService(session, locker)
    transaction_service = TransactionService(session, locker)
    notifications_service = NotificationsService(wallet_service)
    
    # start the grpc server
    server = grpc.aio.server()
    server.add_insecure_port(address)
    
    wallet_servicer = GrpcWalletServicer(wallet_service)
    transaction_servicer = GrpcTransactionServicer(transaction_service)
    account_servicer = GrpcAccountServicer(account_service)
    
    wallet_pb2_grpc.add_WalletServiceServicer_to_server(wallet_servicer, server)
    transaction_pb2_grpc.add_TransactionServiceServicer_to_server(transaction_servicer, server)
    account_pb2_grpc.add_AccountServiceServicer_to_server(account_servicer, server)

    # notificiation servicer is async, we need to await the start of notifications service
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
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    main_task = asyncio.ensure_future(main())
    
    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, lambda: main_task.cancel())
    
    try:
        loop.run_until_complete(main_task)
    finally:
        loop.close()
