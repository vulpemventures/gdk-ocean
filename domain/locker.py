import logging
import asyncio
from typing import Dict
from xmlrpc.client import boolean
from domain.notification import UtxoLockedNotification, UtxoUnlockedNotification
from domain.utxo import Outpoint, Utxo
from typing import List
import time

# the amount of time to wait before freeing the utxo
LOCKTIME_SECONDS = 90

class Locker():
    def __init__(self) -> None:
        self._locked_utxos: Dict[int, List[Utxo]] = {}
        # accounts_by_utxo is a dict of utxo outpoints as str -> account_name
        # this is used to get the account name of the utxo when it is unlocked
        self._accounts_by_utxo: Dict[str, str] = {}
        self.notifications_queue: asyncio.Queue = None
        
    @classmethod
    async def create(cls) -> 'Locker':
        locker = cls()
        locker.notifications_queue = asyncio.Queue()
        return locker
    
    def _add_outpoint_to_locker(self, utxo: Utxo, account_name: str) -> None:
        """custom set in the locker, taking into account the lock time"""
        free_at = int(time.time()) + LOCKTIME_SECONDS
        currently_locked = self._locked_utxos.get(free_at)

        self._accounts_by_utxo[Outpoint.from_utxo(utxo).to_string()] = account_name
        if not currently_locked:
            self._locked_utxos[free_at] = [utxo]
        else:
            currently_locked.append(utxo)
            self._locked_utxos[free_at] = currently_locked
        self.notifications_queue.put_nowait(UtxoLockedNotification(utxo, account_name))

    def _is_in_locker(self, outpoint: Outpoint) -> boolean:
        """check if the outpoint is in the locker, ideally you should first call _free_locker() before calling this method"""
        if not self._locked_utxos:
            return False
        
        all_utxos = [u for utxos in self._locked_utxos.values() for u in utxos]
        for u in all_utxos:
            if u["txid"] == outpoint.txid and u["index"] == outpoint.index:
                return True
        
        return False
        
    def _free_locker(self):
        """free all the outpoints that are in the locker with time <= now"""
        now = int(time.time())
        for locked_time in self._locked_utxos.keys():
            if locked_time <= now:
                freed = self._locked_utxos.pop(locked_time)
                for freed_utxo in freed:
                    account_name = self._accounts_by_utxo.pop(Outpoint.from_utxo(freed_utxo).to_string(), "")
                    self.notifications_queue.put_nowait(UtxoUnlockedNotification(freed_utxo, account_name))
                    logging.debug(f"Unlocked {freed_utxo}")
                return True

    def lock(self, utxo: Utxo, account_name: str) -> None:
        """lock an utxo for a certain amount of time, defined by LOCKTIME_SECONDS"""
        self._add_outpoint_to_locker(utxo, account_name)

    def is_locked(self, outpoint: Outpoint) -> bool:
        """checks if the utxo is locked"""
        self._free_locker() # remove all free outpoints
        return self._is_in_locker(outpoint)
        