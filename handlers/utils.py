
from typing import List
from domain import Utxo, PsetInputArgs, BlockDetails, NotificationType, TxNotification, UtxoNotification
from domain.gdk import get_block_details
from ocean.v1 import notification_pb2, types_pb2
from services import AccountService

def make_utxo_proto(utxo: Utxo, explorerURL: str) -> types_pb2.Utxo:
    utxo_pb = types_pb2.Utxo(
        txid=utxo.txid,
        index=utxo.index,
        asset=utxo.asset,
        value=utxo.value,
        script=bytes.fromhex(utxo.script),
        asset_blinder=bytes.fromhex(utxo.asset_blinder),
        value_blinder=bytes.fromhex(utxo.value_blinder),
        account_name=utxo.account,
        confirmed_status=types_pb2.UtxoStatus(txid=utxo.txid, block_info=make_block_details_proto(get_block_details(explorerURL, utxo.txid)) if utxo.is_confirmed else None),
    )
    return utxo_pb
    
def make_utxos_list_proto(account_name: str, utxos: List[Utxo], explorerURL: str) -> types_pb2.Utxos:
    return types_pb2.Utxos(
        account_name=account_name,
        utxos=[make_utxo_proto(utxo, explorerURL) for utxo in utxos]
    )

def grpc_input_to_pset_input_arg(account_svc: AccountService, input: types_pb2.Input) -> PsetInputArgs:
    return PsetInputArgs(
        txhash=input.txid,
        vout=input.index,
        script=input.script.hex(),
        address_type=input.address_type,
    )

def make_utxo_event_type_proto(t: NotificationType) -> types_pb2.UtxoEventType:
    if t is NotificationType.UTXO_SPENT:
        return types_pb2.UTXO_EVENT_TYPE_SPENT
    elif t is NotificationType.UTXO_LOCKED:
        return types_pb2.UTXO_EVENT_TYPE_LOCKED
    elif t is NotificationType.UTXO_UNSPECIFIED:
        return types_pb2.UTXO_EVENT_TYPE_UNSPECIFIED
    elif t is NotificationType.UTXO_UNLOCKED:
        return types_pb2.UTXO_EVENT_TYPE_UNLOCKED
    else:
        raise Exception(f"Unknown utxo event type: {t}")


def make_utxo_notification_proto(notification: UtxoNotification) -> notification_pb2.UtxosNotificationsResponse:
    return notification_pb2.UtxosNotificationsResponse(
        utxos=[notification.utxo],
        event_type=make_utxo_event_type_proto(notification.type)
    )

def make_tx_event_type_proto(t: NotificationType) -> types_pb2.TxEventType:
    if t is NotificationType.TX_CONFIRMED:
        return types_pb2.TX_EVENT_TYPE_CONFIRMED
    elif t is NotificationType.TX_UNCONFIRMED:
        return types_pb2.TX_EVENT_TYPE_UNCONFIRMED
    elif t is NotificationType.TX_UNSPECIFIED:
        return types_pb2.TX_EVENT_TYPE_UNSPECIFIED
    elif t is NotificationType.TX_BROADCASTED:
        return types_pb2.TX_EVENT_TYPE_BROADCASTED
    else:
        raise Exception(f"Unknown tx event type: {t}")

def make_block_details_proto(block_details: BlockDetails) -> types_pb2.BlockDetails:
    return types_pb2.BlockDetails(
        hash=block_details.block_hash,
        height=block_details.block_height,
        timestamp=block_details.block_time,
    )

def make_tx_notification_proto(notification: TxNotification) -> notification_pb2.TransactionNotificationsResponse:
    return notification_pb2.TransactionNotificationsResponse(
        account_names=[notification.account],
        txid=notification.txid,
        event_type=make_tx_event_type_proto(notification.type),
        block_details=make_block_details_proto(notification.block_details),
    )