from mcpi.minecraft import Minecraft
from mcpi.minecraft import Vec3
from mcpi.block import *
from GhostGame import *
from LavaMonsterGame import *
from queue import *
from mcpi.connection import *

class BlockHitMenu:
    def glass(self, blockHit, block):
        mc.setBlock(blockHit.pos, 20, 0)
        self.gg.start()
    def tnt(self, blockHit, block):
        mc.setBlock(blockHit.pos, 46, 1)
    def torch(self, blockHit, block):
        mc.setBlock(blockHit.pos, block.id, block.data)
        self.lmg.start()
    def ghost(self, blockHit, block):
        self.gg.hit(blockHit)
    def lavaMonster(self, blockHit, block):
        self.lmg.hit(blockHit)
    def windowGlass(self, blockHit, block):
        barrol = mc.player.getTilePos() + Vec3(0, 1, 0)
        mc.player.setPos(mc.player.getTilePos() + Vec3(0.5, 0, 0.5))
        clip = 9.0
        range = 40.0
        aim = blockHit.pos - barrol
        mag = sqrt(aim.x * aim.x + aim.y * aim.y + aim.z * aim.z)
        scale = clip / mag
        start = barrol + Vec3(aim.x * scale, aim.y * scale, aim.z * scale)
        scale = range / mag
        end = barrol + Vec3(aim.x * scale, aim.y * scale, aim.z * scale)
        self.beamQueue.put(QuadBeam(6, self.beamOrigin, start, end, 35, 5))
#     def strawberry(self, blockHit, block):
#         print(str(blockHit.pos))
#         mc.setBlock(blockHit.pos, 33, 1)

    def blockHitMenuLoop(self):
        while True:
            try:
                blockHits = mc.events.pollBlockHits()
                for blockHit in blockHits:
                    block = mc.getBlockWithData(blockHit.pos)
                    print("BlockHit: " + str(blockHit.pos) + " " + str(block))
                    if block.id in self.detectors:
                        self.detectors[block.id](blockHit, block)
                if self.gg.g.alive:
                    self.gg.g.update()
                if self.lmg.lm.alive:
                    self.lmg.lm.update()
                bq = Queue(10)
                while not self.beamQueue.empty():
                    b = self.beamQueue.get()
                    b.update()
                    if b.alive:
                        bq.put(b)
                self.beamQueue = bq
            except TypeError as te:
                print(te)
            except ValueError as ve:
                print(ve)
            except RequestError as re:
                print(re)
                
        time.sleep(0.5)

    def __init__(self):
        print("starting BlockHitMenu")
        self.gg = GhostGame()
        self.lmg = LavaMonsterGame()
        self.beamOrigin = Vec3(1,40,-96)
        self.beamQueue = Queue(10)
        self.detectors = {
            20 : self.glass,
            30 : self.ghost,
#             2 : self.strawberry,
            46 : self.tnt,
            50 : self.torch,
            95 : self.windowGlass,
            246 : self.lavaMonster
        }
        self.bhmThread = threading.Thread(target=self.blockHitMenuLoop)
        self.bhmThread.start()


bhm = BlockHitMenu()
