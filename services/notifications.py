import asyncio
import logging
from typing import Dict, Set, List
from domain import BaseNotification, TxConfirmedNotification, UtxoSpentNotification, UtxoUnspecifiedNotification, Utxo, get_block_details, GdkAPI
import greenaddress as gdk

from services.wallet import WalletService

def _get_utxos_by_account(gdk_api: GdkAPI) -> Dict[str, Dict[str, List[Utxo]]]:
    """this is an utility function to get the utxos for all the wallet accounts"""
    utxos_by_account: Dict[str, Dict[str, List[Utxo]]] = {}
    accounts = gdk_api.get_acccounts()
    for account in accounts:
        utxos_by_account[account.name] = account.utxos()
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

class NotificationsService():
    def __init__(self, session: gdk.Session, wallet_svc: WalletService) -> None:
        self._session = session
        self._gdk_api = GdkAPI(session)
        self._started = False
        self._wallet_svc = wallet_svc
        
        self.queue = asyncio.Queue()
        
        # the accounts to compute diff from
        self._utxos_check_accounts: Set[str] = set()
        self._chaintip: int = None

        # init the state
        try:
            self._utxos_by_account = _get_utxos_by_account(self._gdk_api)
        except:
            self._utxos_by_account = {}    
    
    def _get_last_block_height(self) -> int:
        """return the last block height"""
        while True:
            notification = self._session.notifications.get(block=True, timeout=None)
            if notification['event'] == 'block':
                return notification['block']['block_height']
    
    def _get_chain_tip(self) -> int:
        if not self._chaintip:
            self._chaintip = self._get_last_block_height()
            
        return self._chaintip
    
    async def _put_in_queue(self, notification: BaseNotification) -> None:
        logging.debug("new notification {} put in queue".format(notification.type))
        await self.queue.put(notification)
    
    async def _put_utxos_notifications(self) -> None:
        new_utxos_by_account = _get_utxos_by_account(self._gdk_api)
        for account_name in self._utxos_check_accounts:
            utxos_notifications = _diff_utxos_list(self._utxos_by_account.get(account_name), new_utxos_by_account.get(account_name), account_name)
            for notification in utxos_notifications:
                await self._put_in_queue(notification)
        # update the cache with the new state
        self._utxos_by_account = new_utxos_by_account
    
    async def _put_confirmed_txs_notifications(self) -> None:
        notifications: List[TxConfirmedNotification] = []
        last_block_heigth = self._get_chain_tip()
        for account in self._gdk_api.get_acccounts():
            try:
                txs_for_height = account.transactions(last_block_heigth)
                notifications = notifications + [TxConfirmedNotification(tx['txhash'], get_block_details(tx['txhash']), account.name) for tx in txs_for_height] 
            except Exception as e:
                logging.exception(e)
                continue

        for notif in notifications:
            if notif.block_details.block_height > last_block_heigth:
                self._chaintip = notif.block_details.block_height
                
            await self._put_in_queue(notif)

    
    async def _wait_for_wallet(self):
        """this let to wait for the wallet is ready (either unlocked or created if not exist)"""
        while True:
            try:
                if self._wallet_svc.is_logged():
                    return
                raise 'wallet not logged'
            except:
                await asyncio.sleep(2)

    async def _handle_gdk_notifications(self) -> None:
        """async worker waiting for new GDK block notification and then process Ocean notifications
        returns TX_CONFIRMED, UTXO_SPENT, UTXO_UNSPECIFIED (add) via the queue argument"""
        
        # every 30 seconds, try to get new notifications from wallet state
        while self._started:
            await asyncio.gather(
                self._put_utxos_notifications(), 
                self._put_confirmed_txs_notifications()
            )
            await asyncio.sleep(30)
        
    async def _handle_locker_notifications(self) -> None:
        wallet = self._wallet_svc.get_wallet()
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

        # wait for the wallet to be ready (either unlocked or created if not exist)
        await self._wait_for_wallet()
        self._started = True
        
        await asyncio.gather(
            self._handle_gdk_notifications(), 
            self._handle_locker_notifications()
        )
    