from first import *

class LavaMonsterGame:

	def __init__(self):
		self.lm = LavaMonster()

	def start(self):
		self.frame = 0
		mc.postToChat("Lava Monster!")
		self.pos = randomSurface() + Vec3(0, 30, 0)
		self.lm.alive = True

	def hit(self, blockHit):
		if self.lm.alive and dist(blockHit.pos, self.lm.pos) < 1:
			self.lm.kill()

class LavaMonster:

	def __init__(self,):
		self.frame = 0
		self.pos = randomSurface() + Vec3(0, 30, 0)
		self.alive = False
		self.lavaId = 246
		self.lavaSubId = 0
		self.flarePositions = [Vec3(-1, 0, -1), Vec3(-1, 0, 0), Vec3(-1, 0, 1), Vec3(0, 0, 1), Vec3(1, 0, 1), Vec3(1, 0, 0), Vec3(1, 0, -1), Vec3(0, 0, -1),Vec3(-1, 1, -1), Vec3(-1, 1, 0), Vec3(-1, 1, 1), Vec3(0, 1, 1), Vec3(1, 1, 1), Vec3(1, 1, 0), Vec3(1, 1, -1), Vec3(0, 1, -1)]
		self.flare = 0

	def kill(self):
		self.alive = False
		print("Chill Out!")
		mc.postToChat("Chill Out!")
		for f in self.flarePositions:
			try:
				if mc.getBlock(self.pos + f) == 11:
					mc.setBlock(self.pos, 0, 0)
					mc.setBlock(self.pos + f, 0, 0)
			except ValueError:
					print("error: mc.setBlock(" + str(self.pos + f) + ", 0, 0)")

	def update(self):
		if self.alive:
			ptp = mc.player.getPos()
			prev = self.pos
			if self.frame % 4 == 0:
				course = ptp + Vec3(0, 1, 0) - self.pos
				course = Vec3(orZero(course.x), orZero(course.y), orZero(course.z))
				self.pos = self.pos + course
				print("Lava Monster: " + str(self.pos))
				mc.setBlock(prev, 0, 0)
			mc.setBlock(self.pos, self.lavaId, self.lavaSubId)
			# flare
			mc.setBlock(prev + self.flarePositions[self.flare%16], 0, 0)
			mc.setBlock(prev + self.flarePositions[(self.flare + 4)%16], 0, 0)
			self.flare = self.flare + 1
			flarePos = self.pos + self.flarePositions[self.flare%16]
			mc.setBlock(flarePos, 11, 7)
			flarePos = self.pos + self.flarePositions[(self.flare + 4)%16]
			mc.setBlock(flarePos, 11, 7)
			# kill?
			d = dist(flarePos, ptp)
			print("Lava Monster " + str(d) + " away!")
			if d < 1:
				mc.postToChat("Ouch! Sick Burn!")
				teleport(Vec3(-1000, -1000, -1000))
			self.frame = self.frame + 1
		else:
			mc.setBlock(self.pos, 0,0)