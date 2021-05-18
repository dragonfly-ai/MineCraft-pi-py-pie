from first import *

class GhostGame:
    def __init__(self):
        self.g = Ghost()

    def start(self):
        self.g.alive = True
        mc.postToChat("Ghost!")

    def hit(self, blockHit):
        if self.g.alive and dist(blockHit.pos, self.g.pos) < 1:
            self.g.kill()

class Ghost:
    def __init__(self, pos = randomSurface()):
        self.pos = pos
        self.alive = False
        self.ghostId = 30 # 246
        self.ghostSubId = 0
    def kill(self):
        self.alive = False
        print("Ghost Busters!")
        mc.postToChat("Ghost Busters!")

    def update(self):
        if self.alive:
            ptp = mc.player.getPos()
            prev = self.pos
            course = ptp + Vec3(0, 1, 0) - self.pos
            course = Vec3(orZero(course.x), orZero(course.y), orZero(course.z))
            self.pos = self.pos + course
            print("Ghost: " + str(self.pos))

            if mc.getBlock(self.pos) == 0:
                mc.setBlock(self.pos, self.ghostId, self.ghostSubId)
            if mc.getBlock(prev) == self.ghostId:
                mc.setBlock(prev, 0, 0)
            d = dist(self.pos, ptp)
            print("Ghost " + str(d) + " away!")
            if d < 1.1:
                randomBurial()
                mc.postToChat("Ghost GOTCHA!")
        else:
            mc.setBlock(self.pos, 0,0)


