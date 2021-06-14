from first import *
import json

def makePortal(v = mc.player.getTilePos(), ew = True):
    ns = not ew
    mc.setBlock(v + Vec3(-ew,-2,-ns),49, 0)
    mc.setBlock(v + Vec3(0,-2,0),49, 0)
    mc.setBlock(v + Vec3(ew,-2,ns),49, 0)
    mc.setBlock(v + Vec3(-ew,-1,-ns),49, 0)
    mc.setBlock(v + Vec3(ew,-1,ns),49, 0)
    mc.setBlock(v + Vec3(-ew,0,-ns),49, 0)
    mc.setBlock(v + Vec3(ew,0,ns),49, 0)
    mc.setBlock(v + Vec3(-ew,1,-ns),49, 0)
    mc.setBlock(v + Vec3(ew,1,ns),49, 0)
    mc.setBlock(v + Vec3(-ew,2,-ns),49, 0)
    mc.setBlock(v + Vec3(ew,2,ns),49, 0)
    mc.setBlock(v + Vec3(-ew,3,-ns),49, 0)
    mc.setBlock(v + Vec3(0,3,0),49, 0)

class PortalControl:
    def __init__(self, name):
        self.name = name
        with open(name + '.json') as f:
            self.portals = json.load(f)
        


# Vec3(-20,-58,24)
# Vec3(44,10,17)

# def writePortal(v):
#     
#     mc.setBlock()
# 
# c = 0
# for y in range(30, 100):
#     c = c + 1
#     v = Vec3(0, y, 0)
#     b = mc.getBlockWithData(v)
#     if b.id == 0:
#         mc.setBlock(v, 247, c)
#         print(str(v) + str(mc.getBlockWithData(v)))
#     print(str(v) + " " + str(b))