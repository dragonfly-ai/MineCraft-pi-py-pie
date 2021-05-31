from first import *

def stalactite(sLoc):
    height = random.randint(0, 8)
    base = random.randint(0, 6)
    for y in range(0, min(base, height)):
        disk(sLoc - Vec3(0, y, 0), max(1, base-y), 89, 0)

def stalagmite(sLoc):
    height = random.randint(0, 6)
    base = random.randint(0, 10)
    for y in range(0, min(base, height)):
        disk(sLoc + Vec3(0, y, 0), max(1, base-y), 87, 0)

def netherPocket(nether = Vec3(0, -30, 0), r=20):
    disk(nether + Vec3(0, 6, 0), r, 87, 0) # top
    disk(nether - Vec3(0, 6, 0), r, 87, 0) # bottom
    disk(nether - Vec3(0, 5, 0), r, 10, 0) # lava
    for y in range(-5, 5): # dig
        disk(nether - Vec3(0, y, 0), 20, 0, 0)
    for i in range(0, 21):
        s0 = randative(Vec3(r,r,r))
        s0 = Vec3(s0.x, nether.y + 5, s0.y)
        stalactite(s0)
        s1 = randative(Vec3(r,r,r))
        s1 = Vec3(s1.x, nether.y - 5, s1.y)
        stalagmite(s1)
    for y in range(-5, 5): # walls
        circle(nether - Vec3(0, y, 0), 20, 87, 0)
    for i in range(0, 4):
        s0 = randative(Vec3(r,r,r))
        mc.setBlock(Vec3(s0.x, nether.y + 5, s0.y), 10, 0)
    