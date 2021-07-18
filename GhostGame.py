from first import *

class GhostGame:
    def __init__(self):
        self.g = Ghost()

    def start(self):
        mc.postToChat("Ghost!")
        self.g = Ghost()
        self.g.alive = True


    def hit(self, blockHit):
        if self.g.alive and dist(blockHit.pos, self.g.pos) < 1:
            self.g.kill()

class Ghost:
    def __init__(self, pos = randomSurface()):
        self.frame = 0
        self.pos = randomSurface()
        self.alive = False
        self.ghostId = 30 # 246
        self.ghostSubId = 0
    def kill(self):
        self.alive = False
        mc.setBlock(self.pos, 0, 0)
        print("Ghost Busters!")
        mc.postToChat("Ghost Busters!")

    def update(self):
        if self.alive:
            pid = nearestPlayerId(self.pos)
            ptp = mc.entity.getPos(pid)
            prev = self.pos
            if self.frame % 4 == 0:
                course = ptp + Vec3(0, 1, 0) - self.pos
                course = normalize(Vec3(orZero(course.x), orZero(course.y), orZero(course.z)))
                self.pos = self.pos + course
                if mc.getBlock(prev) == self.ghostId:
                    mc.setBlock(prev, 0, 0)
            if mc.getBlock(self.pos) == 0:
                mc.setBlock(self.pos, self.ghostId, self.ghostSubId)
            d = dist(self.pos, ptp)
            if self.frame % 240 == 0:
                mc.postToChat("Ghost " + str(d) + " away!")
            if d < 1.1:
                randomBurial(pid)
                mc.postToChat("Ghost GOTCHA!")
            self.frame = self.frame + 1
        else:
            mc.setBlock(self.pos, 0,0)
