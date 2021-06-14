from mcpi.minecraft import Minecraft
from mcpi.minecraft import Vec3
from mcpi.block import *
from math import *
import random
import time
import threading

#mc = Minecraft.create("uri.pi", 4711)
mc = Minecraft.create()

minX = -90
maxX = 90

minY = -64
maxY = 50

minZ = -90
maxZ = 90

def vequals(v0, v1):
    return v0.x == v1.x and v0.y == v1.y and v0.z == v1.z

def orZero(c):
    if c == 0:
        return 0
    else:
        return c / abs(c)

def magnitude(v):
    return sqrt(v.x*v.x + v.y*v.y + v.z*v.z)

def dist(v1, v2):
    d = v1 - v2
    return magnitude(d)

def randomVector(r = 1.0):
    return scale(
        normalize(
            Vec3(
                random.random() - 0.5,
                random.random() - 0.5,
                random.random() - 0.5
            )
        ),
        r
    )

def normalize(v):
    mag = magnitude(v)
    return Vec3(v.x / mag, v.y / mag, v.z / mag)

def scale(v, r):
    return Vec3(v.x * r, v.y * r, v.z * r)

def alphaBlend(v1, v2, alpha):
    return Vec3(
        (v1.x * alpha) + (v2.x * (1.0 - alpha)),
        (v1.y * alpha) + (v2.y * (1.0 - alpha)),
        (v1.z * alpha) + (v2.z * (1.0 - alpha))
    )

def randomXZ(y = 0):
    return Vec3(random.randint(minX, maxX), y, random.randint(minZ, maxZ))

def randative(bounds):
    return Vec3(random.randint(-bounds.x, bounds.x), random.randint(-bounds.y, bounds.y), random.randint(-bounds.z, bounds.z))

def randomSurface():
    h = -64
    while h == -64:
        prospect = randomXZ()
        h = mc.getHeight(prospect.x, prospect.z)
    return Vec3(prospect.x, h, prospect.z)

def randomSubterranean():
    s = randomSurface()
    while s.y - 5 < -63:
        s = randomSurface()
    return Vec3(s.x, s.y - 4, s.z)

def randomBurial():
    grave = randomSubterranean()
    mc.setBlock(grave + Vec3(0, 3, 0), 44, 11)
    mc.setBlock(grave + Vec3(0, 2, 0), 0, 0)
    mc.setBlock(grave + Vec3(0, 1, 0), 50, 1)
    mc.setBlock(grave + Vec3(0, 0, 0), 0, 0)
    mc.setBlock(grave + Vec3(0, -1, 0), 0, 0)
    teleport(grave + Vec3(0.5, -1, 0.5))

def teleport(loc = randomSurface()):
    mc.player.setPos(loc)

def square(radius = 1, height = 4, blocktype = 1, blockdata = 0, loc = mc.player.getPos()):
    for y in range(0, height):
        for x in range(-radius, radius):
            mc.setBlock(loc.x+x, loc.y + y, loc.z+radius, blocktype, blockdata)
            mc.setBlock(loc.x+x, loc.y + y, loc.z-radius, blocktype, blockdata)
        for z in range(-radius, radius):
            mc.setBlock(loc.x+radius, loc.y + y, loc.z+z, blocktype, blockdata)
            mc.setBlock(loc.x-radius, loc.y + y, loc.z+z, blocktype, blockdata)

def plane(r = 1, blockType = 1, blockData = 0, loc = mc.player.getPos()):
    mc.setBlocks(loc.x - r, loc.y-1, loc.z - r, loc.x + r, loc.y, loc.z + r, blockType)


def block(l = 1, w = 1, h = 0, blockType = 1, blockData = 0, loc = mc.player.getPos()):
    mc.setBlocks(loc.x - l, loc.y-h/2, loc.z - w, loc.x + l, loc.y + h/2, loc.z + w, blockType, blockData)

def cone(v, base, height, blockId, blockData, pointsUp = True):
    def up(y, height):
        return y / height
    def down(y, height):
        return 1 - up(y, height)
    f = up
    if pointsUp:
        f = down
    for y in range(0, int(height)):
        disk(
            v + Vec3(0, y, 0),
            max(1, round(base*f(y, height))),
            blockId,
            blockData
        )

# mc.setBlocks(-20, 3, -20, 20, 90, 20, 0)
# all spirals consist of double blocks: 43 and half blocks: 44.
# materials range from 0-5 for double blocks and lower halves, and 8-13 for upper halves.
def spiral(height = 4, material = 0, mast = mc.player.getPos()):
    mc.setBlocks(mast + Vec3(-1, 0, -1), mast + Vec3(1, height, 1), 0) # clear the stair well
    mc.setBlocks(mast, mast + Vec3(0, height, 0), 43, material) # central mast
    spiralOffsets = [ Vec3(-1,0,-1), Vec3(-1,0,0), Vec3(-1,1,1), Vec3(0,1,1), Vec3(1,2,1), Vec3(1,2,0), Vec3(1,3,-1), Vec3(0,3,-1), Vec3(-1, 4, -1) ]
    h = 0
    while h < height:
        base = Vec3(0, h, 0)
        for v in spiralOffsets:
            ul = (1-abs(v.x*v.z)) * 8
            print("mc.setBlock( " + str(mast + v + base) + ", " + str(44) + ", " + str(material + ul) + ")")
            mc.setBlock(mast + v + base, 44, material + ul)
        h = h + 4


#spiral(48, 3, Vec3(7, 0, 0))
#spiral(48, 3, Vec3(7, 0, 7))
#spiral(48, 3, Vec3(7, 0, -7))


class RClmn:
    def __init__(self, rPos, height, blockType = 0, blockData = 0):
        self.rPos = rPos
        self.height = height
        self.blockType = blockType
        self.blockData = blockData
    def setBlocksRelativeTo(self, center):
        mc.setBlocks(center + self.rPos, center + self.rPos + Vec3(0, self.height, 0), self.blockType, self.blockData)

#RClmn(Vec3(3, 0, 0), 5, 1, 0).setBlocksRelativeTo(Vec3(0,0,0))


class RBlock:
    def __init__(self, rPos, blockType = 0, blockData = 0):
        self.rPos = rPos
        self.blockType = blockType
        self.blockData = blockData
    def setBlockRelativeTo(self, center):
        mc.setBlock(center + self.rPos, self.blockType, self.blockData)

#RBlock(Vec3(0, 2, 3), 0, 0).setBlockRelativeTo(Vec3(0,0,0))

class Step:
    def __init__(self, rPos, upper = 0):
        self.rPos = rPos
        self.upper = upper
    def setBlockRelativeTo(self, center, blockData = 3):
        mc.setBlock(center + self.rPos, 44, blockData + (8 * self.upper))

#Step(Vec3(0, 0, 4), 0).setBlockRelativeTo(Vec3(0,0,0))

def grandSpiral(segmentCount = 1, postBlock=43, blockData = 3, center = mc.player.getPos()):
    height = 4 * segmentCount
    posts = [
        RClmn(Vec3(0, 0, 4), height, postBlock, blockData), RClmn(Vec3(1, 0, 4), height, postBlock, blockData),
        RClmn(Vec3(-2, 0, 3), height, postBlock, blockData), RClmn(Vec3(-1, 0, 3), height, postBlock, blockData), RClmn(Vec3(0, 0, 3), height), RClmn(Vec3(1, 0, 3), height), RClmn(Vec3(2, 0, 3), height, postBlock, blockData), 
        RClmn(Vec3(-3, 0, 2), height, postBlock, blockData), RClmn(Vec3(-2, 0, 2), height), RClmn(Vec3(-1, 0, 2), height), RClmn(Vec3(0, 0, 2), height), RClmn(Vec3(1, 0, 2), height), RClmn(Vec3(2, 0, 2), height), RClmn(Vec3(3, 0, 2), height, postBlock, blockData),
        RClmn(Vec3(-4, 2, 1), height, postBlock, blockData), RClmn(Vec3(-3, 0, 1), height), RClmn(Vec3(-2, 0, 1), height), RClmn(Vec3(-1, 0, 1), height), RClmn(Vec3(0, 0, 1), height), RClmn(Vec3(1, 0, 1), height), RClmn(Vec3(2, 0, 1), height), RClmn(Vec3(3, 0, 1), height, postBlock, blockData),
        RClmn(Vec3(-4, 2, 0), height, postBlock, blockData), RClmn(Vec3(-3, 0, 0), height), RClmn(Vec3(-2, 0, 0), height), RClmn(Vec3(-1, 0, 0), height), RClmn(Vec3(0, 0, 0), height, postBlock, blockData), RClmn(Vec3(1, 0, 0), height), RClmn(Vec3(2, 0, 0), height), RClmn(Vec3(3, 0, 0), height), RClmn(Vec3(4, 0, 0), height, postBlock, blockData),
        RClmn(Vec3(-3, 2, -1), height, postBlock, blockData), RClmn(Vec3(-2, 0, -1), height), RClmn(Vec3(-1, 0, -1), height), RClmn(Vec3(0, 0, -1), height), RClmn(Vec3(1, 0, -1), height), RClmn(Vec3(2, 0, -1), height), RClmn(Vec3(3, 0, -1), height), RClmn(Vec3(4, 0, -1), height, postBlock, blockData),
        RClmn(Vec3(-3, 0, -2), height, postBlock, blockData), RClmn(Vec3(-2, 0, -2), height), RClmn(Vec3(-1, 0, -2), height), RClmn(Vec3(0, 0, -2), height), RClmn(Vec3(1, 0, -2), height), RClmn(Vec3(2, 0, -2), height), RClmn(Vec3(3, 0, -2), height, postBlock, blockData),
        RClmn(Vec3(-2, 0, -3), height, postBlock, blockData), RClmn(Vec3(-1, 0, -3), height), RClmn(Vec3(0, 0, -3), height), RClmn(Vec3(1, 0, -3), height, postBlock, blockData), RClmn(Vec3(2, 0, -3), height, postBlock, blockData),
        RClmn(Vec3(-1, 0, -4), height, postBlock, blockData), RClmn(Vec3(0, 0, -4), height, postBlock, blockData)
    ]
    for post in posts:
        post.setBlocksRelativeTo(center)
    U = 1
    L = 0
    steps = [
        Step(Vec3(0, 0, 3), U), Step(Vec3(1, 0, 3), U),
        Step(Vec3(-2, 0, 2), L), Step(Vec3(-1, 0, 2), L), Step(Vec3(0, 0, 2), L), Step(Vec3(1, 0, 2), U), Step(Vec3(2, 1, 2), L),
        Step(Vec3(-3, 3, 1), U), Step(Vec3(-2, 3, 1), U), Step(Vec3(-1, 3, 1), U), Step(Vec3(0, 0, 1), L), Step(Vec3(1, 0, 1), U), Step(Vec3(2, 1, 1), L),
        Step(Vec3(-3, 3, 0), U), Step(Vec3(-2, 3, 0), L), Step(Vec3(-1, 3, 0), L), Step(Vec3(1, 1, 0), L), Step(Vec3(2, 1, 0), L), Step(Vec3(3, 1, 0), U),
        Step(Vec3(-2, 3, -1), L), Step(Vec3(-1, 2, -1), U), Step(Vec3(0, 2, -1), L), Step(Vec3(1, 1, -1), U), Step(Vec3(2, 1, -1), U), Step(Vec3(3, 1, -1), U),
        Step(Vec3(-2, 3, -2), L), Step(Vec3(-1, 2, -2), U), Step(Vec3(0, 2, -2), L), Step(Vec3(1, 2, -2), L), Step(Vec3(2, 2, -2), L),
        Step(Vec3(-1, 2, -3), U), Step(Vec3(0, 2, -3), U)
    ]
    torches = [ RBlock(Vec3(0, 1, 3), 50, 5), RBlock(Vec3(3, 2, 0), 50, 5), RBlock(Vec3(0, 3, 3), 50, 5), RBlock(Vec3(-3, 4, 0), 50, 5)]
    h = 0
    while h < segmentCount:
        s = "placing steps at level " + str(h)
        print(s)
        for step in steps:
            step.setBlockRelativeTo(center + Vec3(0, h*4, 0), blockData)
        for torch in torches:
            torch.setBlockRelativeTo(center + Vec3(0, h*4, 0))
        h = h + 1

#grandSpiral(4, 43, 3, p)
#grandSpiral(10, 20, 3, stairs1)
#grandSpiral(3, 20, 3, Vec3(0, 0, 9))

def rectRoof(radius, blockType, position):
    for x in range(0, radius):
        d = radius - x
        mc.setBlocks(position.x - d, position.y, position.z + d, position.x - d, position.y + x, position.z + d, blockType, 0)

# couch
def couch(v, ew = True):
    ns = not ew
    mc.setBlock(v, 26, ew + 0)
    mc.setBlock(v + Vec3(-ew, 0, ns), 26, ew + 2)

# TNT
def boom(radius = 1, blockType = 46, blockData = 0, boom = mc.player.getPos()):
    mc.setBlock(boom.x, boom.y + 1, boom.z, 0)
    mc.player.setPos(boom.x, boom.y + 1, boom.z)
    for x in range(-radius, radius):
        for z in range(-radius, radius):
            mc.setBlock(boom.x+x, boom.y-1, boom.z+z, blockType, blockData)
            mc.setBlock(boom.x+x, boom.y, boom.z+z, blockType, blockData)

def tnt(boom = mc.player.getPos()):
    mc.setBlock(boom.x, boom.y-1, boom.z, 46, 1)

class QuadBeam:
    def __init__(self, duration, start, origin, end, blockId = 0, blockData = 0):
        self.duration = duration
        self.start = start
        self.end = end
        self.frame = 0
        self.blockId = blockId
        self.blockData = blockData
        self.alive = self.frame < self.duration
        self.beams = [
            Beam(3, origin + Vec3(-8,5,0), start, blockId, blockData),
            Beam(3, origin + Vec3(8,5,0), start, blockId, blockData),
            Beam(3, origin + Vec3(-8,-2,0), start, blockId, blockData),
            Beam(3, origin + Vec3(8,-2,0), start, blockId, blockData)
        ]
        line(self.start, self.end, self.blockId, self.blockData)
    def update(self):
        self.frame = self.frame + 1
        if self.frame == self.duration:
            line(self.start, self.end, 0, 0)
        self.alive = self.frame < self.duration
        for b in self.beams:
            b.update()

class DoubleBeam:
    def __init__(self, duration, origin, start, end, blockId = 0, blockData = 0):
        self.duration = duration
        self.start = start
        self.end = end
        self.frame = 0
        self.blockId = blockId
        self.blockData = blockData
        self.alive = self.frame < self.duration
        self.beams = [
            Beam(3, origin + Vec3(-8,0,0), start, blockId, blockData),
            Beam(3, origin + Vec3(8,0,0), start, blockId, blockData)
        ]
        line(self.start, self.end, self.blockId, self.blockData)
    def update(self):
        self.frame = self.frame + 1
        if self.frame == self.duration:
            line(self.start, self.end, 0, 0)
        self.alive = self.frame < self.duration
        for b in self.beams:
            b.update()

class Beam:
    def __init__(self, duration, start, end, blockId = 0, blockData = 0):
        self.duration = duration
        self.start = start
        self.end = end
        self.frame = 0
        self.blockId = blockId
        self.blockData = blockData
        self.alive = self.frame < self.duration
        line(self.start, self.end, self.blockId, self.blockData)
    def update(self):
        self.frame = self.frame + 1
        if self.frame == self.duration:
            line(self.start, self.end, 0, 0)
        self.alive = self.frame < self.duration

# line implementation from:
# https://www.geeksforgeeks.org/bresenhams-algorithm-for-3-d-line-drawing/

def line(p1, p2, blockId, blockData):
    mc.setBlock(p1, blockId, blockData)

    x1 = round(p1.x)
    y1 = round(p1.y)
    z1 = round(p1.z)

    x2 = round(p2.x)
    y2 = round(p2.y)
    z2 = round(p2.z)

    dX = abs(x2 - x1)
    dy = abs(y2 - y1)
    dZ = abs(z2 - z1)

    if (x2 > x1):
        xs = 1
    else:
        xs = -1
    if (y2 > y1):
        ys = 1
    else:
        ys = -1
    if (z2 > z1):
        zs = 1
    else:
        zs = -1
  
    # Driving axis is X-axis"
    if (dX >= dy and dX >= dZ):        
        p1 = 2 * dy - dX
        p2 = 2 * dZ - dX
        while (x1 != x2):
            x1 += xs
            if (p1 >= 0):
                y1 += ys
                p1 -= 2 * dX
            if (p2 >= 0):
                z1 += zs
                p2 -= 2 * dX
            p1 += 2 * dy
            p2 += 2 * dZ
            mc.setBlock(Vec3(x1, y1, z1), blockId, blockData)
  
    # Driving axis is Y-axis"
    elif (dy >= dX and dy >= dZ):       
        p1 = 2 * dX - dy
        p2 = 2 * dZ - dy
        while (y1 != y2):
            y1 += ys
            if (p1 >= 0):
                x1 += xs
                p1 -= 2 * dy
            if (p2 >= 0):
                z1 += zs
                p2 -= 2 * dy
            p1 += 2 * dX
            p2 += 2 * dZ
            mc.setBlock(Vec3(x1, y1, z1), blockId, blockData)
  
    # Driving axis is Z-axis"
    else:        
        p1 = 2 * dy - dZ
        p2 = 2 * dX - dZ
        while (z1 != z2):
            z1 += zs
            if (p1 >= 0):
                y1 += ys
                p1 -= 2 * dZ
            if (p2 >= 0):
                x1 += xs
                p2 -= 2 * dZ
            p1 += 2 * dy
            p2 += 2 * dX
            mc.setBlock(Vec3(x1, y1, z1), blockId, blockData)

# circle
# https://rosettacode.org/wiki/Bitmap/Midpoint_circle_algorithm#Python
def circle(c, r, blockId, blockData):
    c = Vec3(floor(c.x) + 0.5, floor(c.y) + 0.5, floor(c.z) + 0.5)
    f = 1 - r
    dX = 1
    dZ = -2 * r
    x = 0
    z = r
    mc.setBlock(c.x, c.y, c.z + r, blockId, blockData)
    mc.setBlock(c.x, c.y, c.z - r, blockId, blockData)
    mc.setBlock(c.x + r, c.y, c.z, blockId, blockData)
    mc.setBlock(c.x - r, c.y, c.z, blockId, blockData)

    while x < z:
        if f >= 0:
            z -= 1
            dZ += 2
            f += dZ
        x += 1
        dX += 2
        f += dX
        mc.setBlock(c.x + x, c.y, c.z + z, blockId, blockData)
        mc.setBlock(c.x - x, c.y, c.z + z, blockId, blockData)
        mc.setBlock(c.x + x, c.y, c.z - z, blockId, blockData)
        mc.setBlock(c.x - x, c.y, c.z - z, blockId, blockData)
        mc.setBlock(c.x + z, c.y, c.z + x, blockId, blockData)
        mc.setBlock(c.x - z, c.y, c.z + x, blockId, blockData)
        mc.setBlock(c.x + z, c.y, c.z - x, blockId, blockData)
        mc.setBlock(c.x - z, c.y, c.z - x, blockId, blockData)

def disk(c, r, blockId, blockData):
    r2 = (r-0.45) * (r-0.45)
    for x in range(-r, r):
        for z in range(-r, r):
            if x*x + z*z < r2:
                mc.setBlock(Vec3(x + c.x, c.y, z + c.z), blockId, blockData)

def sphere(c, r, blockId, blockData, solid = False):
    f = circle
    if solid:
        f = disk
    f(c, r, blockId, blockData)
    for y in range(1,r):
        dY = Vec3(0,y,0)
        rY = int(r * cos(asin(y/r)))
        f(c + dY, rY, blockId, blockData)
        f(c - dY, rY, blockId, blockData)

naturalBlocks = {
    0 : True,
    1 : True,
    2 : True,
    3 : True,
    7 : True,
    8 : True,
    9 : True,
    10 : True,
    11 : True,
    12 : True,
    13 : True,
    87 : True,
    89 : True
}

def recordBlocks(c, d):
    for y in range(-d.y, d.y):
        for x in range(-d.x, d.x):
            for z in range(-d.z, d.z):
                x1 = x + c.x
                y1 = y + c.y
                z1 = z + c.z
                try:
                    b = mc.getBlockWithData(x1, y1, z1)
                    if not b.id in naturalBlocks:
                        print("mc.setBlock(loc + Vec3(" + str(x) + "," + str(y) + "," + str(z) + ")," + str(b.id) + ", " + str(b.data) + ")")
                except ValueError:
                    print("grrr")

# find and replace
def findAndReplace(c, d, oldId, oldData, newId, newData):
    for y in range(-d.y, d.y):
        for x in range(-d.x, d.x):
            for z in range(-d.z, d.z):
                loc = Vec3(x + c.x, y + c.y, z + c.z)
                try:
                    if mc.getBlock(loc) == oldId:
                        bd = mc.getBlockWithData(loc)
                        if bd.id == oldId and bd.data == oldData:
                            mc.setBlock(loc, newId, newData)
                except ValueError:
                        print("error: " + str(loc))

#def floodFill(c, oldId, oldData, newId, newData):