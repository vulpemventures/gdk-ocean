from typing import TypedDict

class AddressDetails(TypedDict):
    address: str
    address_type: str
    branch: int
    pointer: int
    script: str
    script_type: int
    subaccount: int
    subtype: int
    blinding_key: str
    blinding_script: str
    is_blinded: bool
    unblinded_address: str