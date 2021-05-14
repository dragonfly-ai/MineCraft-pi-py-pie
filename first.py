from mcpi.minecraft import Minecraft
from mcpi.minecraft import Vec3
from math import *
import mcpi.block as block
import random
import time
import threading

mc = Minecraft.create()

minX = -161
maxX = 94

minZ = -100
maxZ = 155

def vequals(v0, v1):
	return v0.x == v1.x and v0.y == v1.y and v0.z == v1.z

def orZero(c):
	if c == 0:
		return 0
	else:
		return c / abs(c)

def dist(v1, v2):
	d = v1 - v2
	return math.sqrt(d.x * d.x + d.y * d.y + d.z * d.z)

def randomXZ():
	return Vec3(random.randint(minX, maxX), 0, random.randint(minZ, maxZ))

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
	mc.setBlock(grave + Vec3(0, 4, 0), 44, 11)
	mc.setBlock(grave + Vec3(0, 3, 0), 0, 0)
	mc.setBlock(grave + Vec3(0, 2, 0), 50, 1)
	mc.setBlock(grave + Vec3(0, 1, 0), 0, 0)
	mc.setBlock(grave, 0, 0)
	teleport(grave)

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
	def __init__(self, duration, start, end, blockId = 0, blockData = 0):
		self.duration = duration
		self.start = start
		self.end = end
		self.frame = 0
		self.blockId = blockId
		self.blockData = blockData
		self.alive = self.frame < self.duration
		self.beams = [
			Beam(self.duration, start + Vec3(-4,3,6), start, blockId, blockData),
			Beam(self.duration, start + Vec3(4,3,6), start, blockId, blockData),
			Beam(self.duration, start + Vec3(-4,-3,6), start, blockId, blockData),
			Beam(self.duration, start + Vec3(4,-3,6), start, blockId, blockData)
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

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dz = abs(z2 - z1)

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
    if (dx >= dy and dx >= dz):        
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while (x1 != x2):
            x1 += xs
            if (p1 >= 0):
                y1 += ys
                p1 -= 2 * dx
            if (p2 >= 0):
                z1 += zs
                p2 -= 2 * dx
            p1 += 2 * dy
            p2 += 2 * dz
            mc.setBlock(Vec3(x1, y1, z1), blockId, blockData)
  
    # Driving axis is Y-axis"
    elif (dy >= dx and dy >= dz):       
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while (y1 != y2):
            y1 += ys
            if (p1 >= 0):
                x1 += xs
                p1 -= 2 * dy
            if (p2 >= 0):
                z1 += zs
                p2 -= 2 * dy
            p1 += 2 * dx
            p2 += 2 * dz
            mc.setBlock(Vec3(x1, y1, z1), blockId, blockData)
  
    # Driving axis is Z-axis"
    else:        
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while (z1 != z2):
            z1 += zs
            if (p1 >= 0):
                y1 += ys
                p1 -= 2 * dz
            if (p2 >= 0):
                x1 += xs
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx
            mc.setBlock(Vec3(x1, y1, z1), blockId, blockData)


# find and replace

def findAndReplace(xRange, yRange, zRange, oldId, oldData, newId, newData):
    for x in xRange:
        for y in yRange:
            for z in zRange:
                loc = Vec3(x, y, z)
                try:
                    if mc.getBlock(loc) == oldId:
                        bd = mc.getBlockWithData(loc)
                        if bd.id == oldId and bd.data == oldData:
                            mc.setBlock(loc, newId, newData)
                except ValueError:
                        print("error: " + str(loc))
