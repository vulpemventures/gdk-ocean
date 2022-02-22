from typing import TypedDict

class Receiver(TypedDict):
    address: str
    sats: int
    asset: str

def receiver_to_dict(receiver: Receiver) -> dict:
    """
    This function is used to convert a receiver to a dictionary.
    """
    return {
        'address': receiver['address'],
        'satoshi': receiver['sats'],
        'asset_id': receiver['asset'],
    }