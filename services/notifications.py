import asyncio
import logging
from typing import Dict, Set, TypedDict, List
from domain.gdk_wallet import GdkWallet
from domain.notification import BaseNotification, TxConfirmedNotification, UtxoSpentNotification, UtxoUnspecifiedNotification
from domain.utxo import Utxo
from services.wallet import WalletService

def _get_utxos_by_account(wallet: GdkWallet) -> Dict[str, Dict[str, List[Utxo]]]:
    """this is an utility function to get the utxos for all the wallet accounts"""
    utxos_by_account: Dict[str, Dict[str, List[Utxo]]] = {}
    
    for name, account in wallet.accounts.items():
        utxos = account.get_all_utxos(False)
        utxos_by_account[name] = utxos
    
    return utxos_by_account    

def _diff_utxos_list(current: Dict[str, List[Utxo]], new: Dict[str, List[Utxo]], account: str) -> List[BaseNotification]:
    """this function is called when a new block is received, and returns a list of notifications after new/old utxos are compared"""
    if not current:
        current = {}
    if not new:
        new = {}
    
    notifs: List[BaseNotification] = []
    
    current_list: List[Utxo] = []
    new_list: List[Utxo] = []
    
    for utxos in current.values():
        current_list.extend(utxos)
    
    for utxos in new.values():
        new_list.extend(utxos)
        
    for utxo in new_list:
        if utxo not in current_list:
            notifs.append(UtxoUnspecifiedNotification(utxo, account))
    
    for utxo in current_list:
        if utxo not in new_list:
            notifs.append(UtxoSpentNotification(utxo, account))
    
    return notifs

class _BlockNotification(TypedDict):
    """this is not an Ocean notification! it represents the GDK block notification dict"""
    block_hash: str
    block_height: int

class NotificationsService():
    def __init__(self, wallet_svc: WalletService):
        self._wallet_svc = wallet_svc
        self._started = False
        
        self.queue = asyncio.Queue()
        
        # the accounts to compute diff from
        self._utxos_check_accounts: Set[str] = set()

        # init the state
        try:
            wallet = self._wallet_svc.get_wallet() 
            self._utxos_by_account = _get_utxos_by_account(wallet)
        except:
            self._utxos_by_account = {}    
    
    async def _put_in_queue(self, notification: BaseNotification) -> None:
        logging.debug("new notification {} put in queue".format(notification.type))
        await self.queue.put(notification)
    
    async def _put_utxos_notifications(self) -> None:
        wallet = self._wallet_svc.get_wallet()
        new_utxos_by_account = _get_utxos_by_account(wallet)
        
        for account_name in self._utxos_check_accounts:
            utxos_notifications = _diff_utxos_list(self._utxos_by_account.get(account_name), new_utxos_by_account.get(account_name), account_name)
            for notification in utxos_notifications:
                await self._put_in_queue(notification)
        # update the cache with the new state
        self._utxos_by_account = new_utxos_by_account
    
    async def _put_confirmed_txs_notifications(self, height: int, block_hash: str) -> None:
        wallet = self._wallet_svc.get_wallet()
        all_accounts_names = list(wallet.accounts.keys())
        for account_name in all_accounts_names:
            try:
                account = wallet.get_account(account_name)
                txs_for_height = account.get_transactions(height)
                tx_confirmed_notifications = [TxConfirmedNotification(tx['txhash'], block_hash, height) for tx in txs_for_height] 
                for notif in tx_confirmed_notifications:
                    await self._put_in_queue(notif)
            except:
                continue
    
    async def _wait_for_wallet(self) -> GdkWallet:
        """this let to wait for the wallet is ready (either unlocked or created if not exist)"""
        wallet = None
        while wallet is None:
            try:
                wallet = self._wallet_svc.get_wallet()
            except:
                await asyncio.sleep(2)
        return wallet

    async def _handle_gdk_notifications(self, wallet: GdkWallet) -> None:
        """async worker waiting for new GDK block notification and then process Ocean notifications
        returns TX_CONFIRMED, UTXO_SPENT, UTXO_UNSPECIFIED (add) via the queue argument"""
        gdk_notifications = wallet.session.notifications

        async def next_notification():
            while True:
                try:
                    return gdk_notifications.get(block=False)
                except:
                    await asyncio.sleep(0.5)

        while self._started:
            notification = await next_notification()
            event = notification['event']
            
            if event == 'block':
                logging.debug(f"new block: {notification['block']['block_height']} {notification['block']['block_hash']}")
                block = _BlockNotification(notification['block'])
                # compute notifications from new state each time we get a block
                await self._put_utxos_notifications()
                await self._put_confirmed_txs_notifications(block['block_height'], block['block_hash'])

            await asyncio.sleep(1)
        
    async def _handle_locker_notifications(self, wallet: GdkWallet) -> None:
        locker_notifications_queue = wallet.locker.notifications_queue
        while True:
            n = await locker_notifications_queue.get()
            await self._put_in_queue(n)
        
    def _check_not_started(self):
        if self._started:
            raise Exception('NotificationsService started')
        
    def add_utxos_check_account(self, account_name: str) -> None:
        self._utxos_check_accounts.add(account_name)
    
    def remove_utxos_check_account(self, account_name: str) -> None:
        self._utxos_check_accounts.remove(account_name)
    
    async def start(self) -> None:
        self._check_not_started()
        self._started = True
        wallet = await self._wait_for_wallet()
        
        await asyncio.gather(
            self._handle_gdk_notifications(wallet), 
            self._handle_locker_notifications(wallet)
        )
    
    def stop(self):
        self._started = False
        