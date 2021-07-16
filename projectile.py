from BlockCache import *

def defaultStop(projectile):
    if projectile.frame > 3 * projectile.frameRate:
        projectile.finished = True
    else:
        projectile.finished = False

class Projectile:
    def __init__(self, pos, velocity, blockId = 35, blockData = 0, stop = defaultStop):
        self.frame = 0
        self.frameRate = 0.1
        self.gravity = Vec3(0, -9.806 * self.frameRate, 0)
        self.startPos = pos
        self.pos = pos
        self.prev = pos
        self.prevBlockCache = BlockCache()
        self.velocity = velocity
        self.blockId = blockId
        self.blockData = blockData
        self.finished = False
        self.stop = stop

    def step(self):
        self.stop(self)
        if self.finished:
            self.prevBlockCache.overwriteBlocks(lambda v, bid, bd: Block(v, 0, 0))
            return
        else:
            tempPrev = self.prev
            self.prev = self.pos
            self.pos = self.pos + self.velocity
            # -9.806 * t
            self.velocity = self.velocity + self.gravity
            bc = BlockCache()
            line(self.prev, self.pos, self.blockId, self.blockData, bc.setBlock)
            tempCache = self.prevBlockCache
            tempCache.overwriteBlocks(lambda v, bid, bd: Block(v, 0, 0))
            self.prevBlockCache = bc
            self.frame = self.frame + 1
    def fire(self):
        while not self.finished:
            self.step()
            time.sleep(self.frameRate)

#p = Projectile(Vec3(85,14,58), Vec3(-2, 10, 0.4), 35, 1)
#p.fire()

def fireworkBurst(firework, projectile):
    if projectile.velocity.y < 0:
        firework.projectiles = []
        for i in range(0, 10):
            firework.projectiles.append(firework.randomProjectile(projectile.pos))
        projectile.finished = True

class Firework:
    def __init__(self, pos, velocity, color = -1):
        self.startPos = pos
        self.colors = [0, 1, 2, 3, 4, 5, 6, 10, 14]
        if color < 0:
            self.color = self.colors[random.randint(0,8)]
        else:
            self.color = color
        self.projectiles = [Projectile(pos, velocity, 35, self.color, lambda projectile: fireworkBurst(self, projectile))]
        self.blockData = self.color
        self.frameRate = 0.1
        self.frame = 0
    def randomProjectile(self, start):
        def l(projectile):
            if projectile.pos.y < self.startPos.y + 2:
                projectile.finished = True
            else:
                projectile.finished = False
        return Projectile(start, randomVector(3), 35, self.color, l)
    def step(self):
        for p in self.projectiles:
            p.step()
    def finished(self):
        for p in self.projectiles:
            if not p.finished:
                return False
        return True
    def launch(self):
        print("launching!")
        while not self.finished():
            self.step()
            time.sleep(self.frameRate)

class FireworkShow:
    def __init__(self, source):
        self.frame = 0
        self.on = False
        self.source = source + Vec3(0, 3, 0)
        self.activeFireworks = []

    def active(self):
        return self.on or len(self.activeFireworks) > 0

    def start(self):
        self.on = True
        self.frame = 0

    def stop(self):
        self.on = False

    def step(self):
        if self.active():
            self.frame = self.frame + 1
            tempFireworks = []
            if self.frame > 60 / 0.1:
                self.on = False
            if self.on:
                if len(self.activeFireworks) < 1:
                    rV = randomVector(2)
                    rV.y = 0
                    tempFireworks.append(Firework(self.source, rV + Vec3(0, 7, 0)))
                if len(self.activeFireworks) < 5 and random.random() < 0.1:
                    rV = randomVector(2)
                    rV.y = 0
                    tempFireworks.append(Firework(self.source, rV + Vec3(0, 7, 0)))
            for f in self.activeFireworks:
                f.step()
                if not f.finished():
                    tempFireworks.append(f)
            self.activeFireworks = tempFireworks


# f = Firework(start, Vec3(0, 4, 0))
# f.launch()