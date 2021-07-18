from mcpi.minecraft import Minecraft
from mcpi.minecraft import Vec3
from mcpi.block import *
from GhostGame import *
from LavaMonsterGame import *
from WaterMonsterGame import *
from projectile import *
from queue import *
from mcpi.connection import *

class BlockHitMenu:
    def lightFurnace(self, blockHit, block):
        mc.setBlock(blockHit.pos, 62, block.data)
    def smotherFurnace(self, blockHit, block):
        mc.setBlock(blockHit.pos, 61, block.data)
    def glass(self, blockHit, block):
        if block.data == 1:
            self.tieFighterLasers(blockHit, block);
        else:
            self.gg.start()
    def tnt(self, blockHit, block):
        mc.setBlock(blockHit.pos, 46, 1)
    def lapis2gabi(self, blockHit, block):
        mc.setBlock(blockHit.pos, 8, 0)
    def gold2lava(self, blockHit, block):
        mc.setBlock(blockHit.pos, 10, 0)
    def portal(self, blockHit, block):
        vP = blockHit.pos + Vec3(0, -1, 0)
        base = mc.getBlock(vP)
        print(str(base))
    def torch(self, blockHit, block):
        mc.setBlock(blockHit.pos, block.id, block.data)
        self.lmg.start()
    def diamondOre(self, blockHit, block):
        mc.setBlock(blockHit.pos, block.id, block.data)
        self.wmg.start()
    def ghost(self, blockHit, block):
        self.gg.hit(blockHit)
    def lavaMonster(self, blockHit, block):
        self.lmg.hit(blockHit)
    def waterMonster(self, blockHit, block):
        self.wmg.hit(blockHit)
    def tieFighterLasers(self, blockHit, block):
        barrol = mc.player.getTilePos() + Vec3(0, 1, 0)
        print(str(barrol))
        beamRange = 50.0
        aim = normalize(blockHit.pos - barrol)
        print(str(aim))
        end = barrol + scale(aim, beamRange)
        self.beamQueue.put(Beam(3, self.beamOrigin + Vec3(0,0,-1), end, 35, 5))
        self.beamQueue.put(Beam(3, self.beamOrigin + Vec3(0,0,1), end, 35, 5))
        #DoubleBeam(6, self.beamOrigin, start, end, 35, 5)
    def fireworks(self, blockHit, block):
        self.fireworkShow.source = blockHit.pos + Vec3(0, 3, 0)
        if self.fireworkShow.active():
            mc.postToChat("Fireworks Off!")
            self.fireworkShow.stop()
        else:
            mc.postToChat("Fireworks On!")
            self.fireworkShow.start()
            
#     def strawberry(self, blockHit, block):
#         print(str(blockHit.pos))
#         mc.setBlock(blockHit.pos, 33, 1)

    def blockHitMenuLoop(self):
        while True:
            ptp = mc.player.getTilePos()
#             height = mc.getHeight(ptp.x, ptp.z)
#             print(str(mc.getBlock(ptp.x, height-1, ptp.z)))
            try:
                blockHits = mc.events.pollBlockHits()
                
                for blockHit in blockHits:
                    print(blockHit)
                    block = mc.getBlockWithData(blockHit.pos)
                    print("BlockHit: " + str(blockHit.pos) + " " + str(block))
                    if block.id in self.detectors:
                        self.detectors[block.id](blockHit, block)
                if self.gg.g.alive:
                    self.gg.g.update()
                if self.lmg.lm.alive:
                    self.lmg.lm.update()
                if self.wmg.wm.alive:
                    self.wmg.wm.update()
                if self.fireworkShow.active():
                    self.fireworkShow.step()
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
            time.sleep(0.1)

    def __init__(self):
        print("starting BlockHitMenu")
        self.fireworkShow = FireworkShow(Vec3(0, 1000, 0))
        self.gg = GhostGame()
        self.lmg = LavaMonsterGame()
        self.wmg = WaterMonsterGame()
        self.beamOrigin = Vec3(-2,0,0)
        self.beamQueue = Queue(10)
        self.portals = {}
        self.detectors = {
            20 : self.glass,
            22 : self.lapis2gabi,
            30 : self.ghost,
#             2 : self.strawberry,
            41 : self.gold2lava,
            46 : self.tnt,
            49 : self.portal,
            50 : self.torch,
            56 : self.diamondOre,
            57 : self.waterMonster,
            61 : self.lightFurnace,
            62 : self.smotherFurnace,
            #95 : self.tieFighterLasers,
            246 : self.lavaMonster,
            247 : self.fireworks
        }
        self.bhmThread = threading.Thread(target=self.blockHitMenuLoop)
        self.bhmThread.start()


bhm = BlockHitMenu()
