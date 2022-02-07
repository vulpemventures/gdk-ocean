import asyncio
from cmath import log
import logging
from typing import Dict, List
from domain.notification import BaseNotification, NotificationType
from ocean.v1alpha import notification_pb2, notification_pb2_grpc
from services.notifications import NotificationsService

class _Subscriber():
    def __init__(self, subscribe_to: List[NotificationType]) -> None:
        # it lets to limit the number of notifications in the queue for each subscriber
        # so the subscriber can't block the server
        MAX_QUEUE_SIZE = 100
        
        self.queue = asyncio.Queue(MAX_QUEUE_SIZE)
        self._types_to_broadcast = subscribe_to
        
    @classmethod
    def transactions(cls): 
        transactions_types = [NotificationType.TX_CONFIRMED, NotificationType.TX_BROADCASTED, NotificationType.TX_UNCONFIRMED, NotificationType.TX_UNSPECIFIED]
        return cls(transactions_types)
    
    @classmethod
    def utxos(cls):
        utxos_types = [NotificationType.UTXO_SPENT, NotificationType.UTXO_UNSPECIFIED, NotificationType.UTXO_LOCKED, NotificationType.UTXO_UNLOCKED]
        return cls(utxos_types)
    
    def _is_ok_type(self, notification_type: NotificationType) -> bool:
        for t in self._types_to_broadcast:
            if t == notification_type:
                return True
        
        return False    
    
    def put(self, notification: BaseNotification) -> None:
        if self._is_ok_type(notification.type):
            logging.debug("new notification {} put in queue".format(notification.type))
            self.queue.put_nowait(notification)
        
    async def get(self) -> BaseNotification:
        next_notification = await self.queue.get()
        return next_notification

class GrpcNotificationsServicer(notification_pb2_grpc.NotificationServiceServicer):
    def __init__(self) -> None:
        self.task: asyncio.Task = None
        self._subscribers: Dict[int, _Subscriber] = {}
        self._svc: NotificationsService = None
        self.next_id = 0
    
    @classmethod
    async def create(cls, notif_svc: NotificationsService):
        self = cls()
        self._svc = notif_svc
        self.task = asyncio.create_task(self._consumer())
        return self
        
    async def _consumer(self):
        while True:
            notification = await self._svc.queue.get()
            for subscriber in self._subscribers.values():
                subscriber.put(notification)
            self._svc.queue.task_done()
        
    def _add_subscriber(self, sub: _Subscriber):
        id_sub = self.next_id
        self._subscribers[self.next_id] = sub
        self.next_id += 1
        return id_sub
    
    async def TransactionNotifications(self, request: notification_pb2.TransactionNotificationsRequest, _):
        id_subscriber = self._add_subscriber(_Subscriber.transactions())
        
        try:
            while True:
                notification = await self._subscribers[id_subscriber].get()
                proto_msg = notification.to_proto()
                yield proto_msg
        finally:
            del self._subscribers[id_subscriber]

    async def UtxosNotifications(self, request: notification_pb2.UtxosNotificationsRequest, _):
        self._svc.add_utxos_check_account(request.account_key.name)
        id_subscriber = self._add_subscriber(_Subscriber.utxos())

        try:
            while True:
                notification = await asyncio.create_task(self._subscribers[id_subscriber].get())
                proto_msg = notification.to_proto()
                yield proto_msg
        finally:
            del self._subscribers[id_subscriber]
            self._svc.remove_utxos_check_account(request.account_key.name)