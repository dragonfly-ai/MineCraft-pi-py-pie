from first import *

class WaterMonsterGame:

    def __init__(self):
        self.wm = WaterMonster()

    def start(self):
        self.frame = 0
        mc.postToChat("Water Monster!")
        self.wm = WaterMonster()
        self.wm.alive = True

    def hit(self, blockHit):
        if self.wm.alive and dist(blockHit.pos, self.wm.pos) < 1:
            self.wm.kill()

class WaterMonster:

    def __init__(self,):
        self.frame = 0
        self.pos = randomSurface()
        self.alive = False
        self.WaterId = 57
        self.WaterSubId = 0
        self.flareId = 9
        self.flareSubId = 0
        self.flarePositions = [
            Vec3(0, 1, 0),
            Vec3(-1, 0, -1), Vec3(-1, 0, 0), Vec3(-1, 0, 1), Vec3(0, 0, 1), Vec3(1, 0, 1), Vec3(1, 0, 0), Vec3(1, 0, -1),
            Vec3(0, 0, -1), Vec3(-1, 1, -1), Vec3(-1, 1, 0), Vec3(-1, 1, 1), Vec3(0, 1, 1), Vec3(1, 1, 1), Vec3(1, 1, 0),
            Vec3(1, 1, -1), Vec3(0, 1, -1)
        ]
        self.flare = 0
        self.navigableBlocks = {0:True, 8:True, 9:True}

    def kill(self):
        self.alive = False
        print("Splish Splash!")
        mc.postToChat("Splish Splash!")
        mc.setBlock(self.pos, 0, 0)
        for f in self.flarePositions:
            mc.setBlock(self.pos + f, 0, 0)
            mc.setBlock(self.pos + f + Vec3(0, -1, 0), 0, 0)

    def update(self):
        if self.alive:
            ptp = mc.player.getPos()
            prev = self.pos
            if self.frame % 4 == 0:
                course = ptp - self.pos
                course = Vec3(orZero(course.x), orZero(course.y), orZero(course.z))
                newPos = self.pos + course
                newPos = Vec3(newPos.x, orZero(mc.getHeight(newPos.x, newPos.z)), newPos.z)
                block = mc.getBlock(newPos)
                if block in self.navigableBlocks:
                    self.pos = newPos
                print("Water Monster: " + str(self.pos))
                mc.setBlock(prev, 0, 0)
            mc.setBlock(self.pos, self.WaterId, self.WaterSubId)
            # flare
            self.flare = self.flare + 1
            for f in self.flarePositions:
                fpos = prev + f   
                block = mc.getBlock(fpos)
                if block in self.navigableBlocks:
                    mc.setBlock(fpos, 0, 0)
            for f in self.flarePositions:
                flarePos = self.pos + f
                block = mc.getBlock(flarePos)
                if block in self.navigableBlocks:
                    mc.setBlock(flarePos, self.flareId, random.randint(0, 7))
                    # kill?
                    d = dist(flarePos, ptp)
            print("Water Monster " + str(d) + " away!")
            if d < 1:
                mc.postToChat("Drown and Washed Away!")
                teleport(Vec3(-1000, -1000, -1000))
            self.frame = self.frame + 1
        else:
            mc.setBlock(self.pos, 0,0)

