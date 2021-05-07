from GhostGame import *
from LavaMonsterGame import *

class BlockHitMenu:
	def glass(self, blockHit):
		mc.setBlock(blockHit.pos, 20, 0)
		self.gg.start()
	def tnt(self, blockHit):
		mc.setBlock(blockHit.pos, 46, 1)
	def torch(self, blockHit):
		block = mc.getBlockWithData(blockHit.pos)
		mc.setBlock(blockHit.pos, block.id, block.data)
		self.lmg.start()
	def ghost(self, blockHit):
		self.gg.hit(blockHit)
	def lavaMonster(self, blockHit):
		self.lmg.hit(blockHit)

	def blockHitMenuLoop(self):
		while True:
			try:
				blockHits = mc.events.pollBlockHits()
				for blockHit in blockHits:
					block = mc.getBlockWithData(blockHit.pos)
					print("BlockHit: " + str(blockHit.pos) + " " + str(block))
					if block.id in self.detectors:
						self.detectors[block.id](blockHit)
				if self.gg.g.alive:
					self.gg.g.update()
				if self.lmg.lm.alive:
					self.lmg.lm.update()
			except TypeError:
					print("TypeError")
			except ValueError:
					print("ValueError")
		time.sleep(0.5)

	def __init__(self):
		print("starting BlockHitMenu")
		self.gg = GhostGame()
		self.lmg = LavaMonsterGame()
		self.detectors = {
			46 : self.tnt,
			30 : self.ghost,
			20 : self.glass,
			50 : self.torch,
			246 : self.lavaMonster
		}
		self.bhmThread = threading.Thread(target=self.blockHitMenuLoop)
		self.bhmThread.start()
