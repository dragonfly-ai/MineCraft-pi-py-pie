#################################################
# notes.py
#
# Code snippets and examples for future reference
#################################################

# basic block hit detection
def blockHitTest():
	while True:
		blockHits = mc.events.pollBlockHits()
		for blockHit in blockHits:
			print(str(blockHit.pos) + " " + str(blockHit.face) + " " + str(blockHit.type) + " " + str(blockHit.entityId))
			if mc.getBlock(blockHit.pos) == 46:
				mc.setBlock(blockHit.pos, 46, 1)
		time.sleep(0.5)

bhtThread = threading.Thread(target=blockHitTest)
print("starting blockHitTest")
bhtThread.start()



#randomize blocks in volume
d = [1, 3, 4, 5, 7, 12, 13, 14, 15, 16, 17, 20, 21, 22, 24, 30, 35, 41, 42, 43, 44, 45, 48, 49, 53, 56, 57, 67, 71, 73, 82, 89, 95, 98, 246, 247]
spot = mc.player.getPos()
mc.player.setPos(spot.x, spot.y + 10, spot.z)
for x in range(-1, 25):
	for y in range(-1, 25):
		for z in range(-1, 25):
			if mc.getBlock(spot.x+x, spot.y+y, spot.z+z) != 0:
				choice = random.choice(d)
				mc.setBlock(spot.x+x, spot.y+y, spot.z+z, random.randint(1, choice))

# fill air blocks in a square with given block
def fillPlane(seed, dX, dZ, blockId, blockData):
	for x in range(-dX, dX):
		for z in range(-dZ, dZ):
			tile = seed + Vec3(x, 0, z)
			try:
				print(str(mc.getBlock(tile)))
				if mc.getBlock(tile) == 0:
					mc.setBlock(tile, blockId, blockData)
			except ValueError:
				print("ValueError")


# copy blocks from one mc instance to another.
def copyBlocks(loc, dX, dY, dZ, mcL, mcR, rem):
	for x in range(-dX, dX):
		for y in range(-dY, dY):
			for z in range(-dZ, dZ):
				try:
					bd = mcL.getBlockWithData(loc + Vec3(x, y, z))
					mcR.setBlock(rem + Vec3(x, y, z), bd.id, bd.data)
				except TypeError:
					print("TypeError")
				except ValueError:
					print("ValueError")
                
# find and replace

def findAndReplace(xRange, yRange, zRange, oldId, oldData, newId, newData):
    for x in xRange:
        for y in yRange:
            for z in zRange:
                loc = Vec3(x, y, z)
                bd = mc.getBlockWithData(loc)
                if bd.id == oldId and bd.data == oldData:
                    mc.setBlock(loc, newId, newData)
                    
