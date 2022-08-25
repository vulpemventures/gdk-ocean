from ocean.v1 import types_pb2

class BlockDetails():
    def __init__(self, block_hash: str, block_height: int, block_time: int):
        self.block_hash = block_hash
        self.block_height = block_height
        self.block_time = block_time
    
    def to_proto(self) -> types_pb2.BlockDetails:
        return types_pb2.BlockDetails(
            hash=bytes.fromhex(self.block_hash),
            height=self.block_height,
            timestamp=self.block_time,
        )