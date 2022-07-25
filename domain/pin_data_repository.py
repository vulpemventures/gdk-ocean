from typing import TypedDict
import json

class PinData(TypedDict):
    encrypted_data: str
    pin_identifier: str
    salt: str
    
class PinDataRepositoryInterface():
    def read(self) -> PinData:
        pass
    
    def write(self, _: PinData) -> None:
        pass
    
class InMemoryPinDataRepository(PinDataRepositoryInterface):
    def __init__(self):
        self.pin_data = None

    def read(self) -> PinData:
        if not self.pin_data:
            raise Exception('Pin data is not set')
        return self.pin_data
    
    def write(self, pin_data: PinData) -> None:
        self.pin_data = pin_data
        
class FilePinDataRepository(PinDataRepositoryInterface):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> PinData:
        with open(self.file_path, 'r') as f:
            r = json.load(f)
            return r
    
    def write(self, pin_data: PinData) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(pin_data, f)
        
    