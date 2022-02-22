from ocean.v1alpha import types_pb2

class AccountKey():
    def __init__(self, name: str, account_id: int) -> None:
        self.name = name
        self.id = account_id
        
    @classmethod
    def from_name(cls, name: str) -> 'AccountKey':
        return cls(name, 0)
    
    def to_proto(self) -> types_pb2.AccountKey:
        return types_pb2.AccountKey(
            name=self.name,
            id=self.id,
        )
        