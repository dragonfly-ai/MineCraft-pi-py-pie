from first import *

class Block:
    def __init__(self, v, blockId, blockData):
        self.v = v
        self.blockId = blockId
        self.blockData = blockData

class BlockCache:
    def __init__(self):
        self.cache = []
    def setBlock(self, v, blockId, blockData):
        self.cache.append(Block(v, blockId, blockData))
        mc.setBlock(v, blockId, blockData)
    def overwriteBlocks(self, blockTransform = lambda v, bid, bd: Block(v, bid, bd)):
        for b in self.cache:
            bt = blockTransform(b.v, b.blockId, b.blockData)
            mc.setBlock(bt.v, bt.blockId, bt.blockData)
