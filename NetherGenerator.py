from first import *

debug = False

fill = True
cavernBlock = 0
wallBlock = 87

if debug:
    fill = False
    cavernBlock = 87
    wallBlock = 0

maxR = 9
diameter = 2*maxR
roof = -30
floor = -60
midY = int((roof + floor) / 2)

def randomNodeOffset():
    return Vec3(
        random.randint(-maxR, maxR),
        random.randint(-9, 9),
        random.randint(-maxR, maxR)
    )

def connectNodes(v1, v2, r1, r2):
    n1 = v1 + randomVector(r1-1)
    n2 = v2 + randomVector(r2 - 1)
    detour = alphaBlend(n1, n2, 0.5) + randomVector((r1 + r2)/4.0)
    d = dist(n1, n2) # - (r1 + r2)
    alpha = 0
    while alpha <= 1.0:
        r = random.randint(2, 4)
        sphere(alphaBlend(n1, detour, alpha), r, cavernBlock, 0, fill)
        alpha = alpha + (r / d)
    alpha = 0
    while alpha <= 1.0:
        r = random.randint(2, 4)
        sphere(alphaBlend(detour, n2, alpha), r, cavernBlock, 0, fill)
        alpha = alpha + (r / d)

def randomLava(v1, r1):
    mc.setBlock(v1 + randomVector(r1), 10, 0)

def stalactite(v, base, height, blockId = 89, blockData = 0):
    cone(v, base, height, blockId, blockData, False)

def stalagmite(v, base, height, blockId = 89, blockData = 0):
    cone(v, base, height, blockId, blockData, True)

def nether():
    mc.setBlocks(minX+1, floor, minZ+1, maxX-1, roof, maxZ-1, wallBlock, 0)

    nodeOffsets = {}
    radii = {}

    x = minX + diameter
    while x < minX / 2:#maxX - diameter:
        z = minZ + diameter
        nodeOffsets[x] = {}
        radii[x] = {}
        while z < minZ / 2:#maxZ - diameter:
            nodeOffsets[x][z] = randomNodeOffset()
            radii[x][z] = random.randint(3, maxR-1)
            z = z + diameter
        x = x + diameter

    print("... Node Generation Complete!")
  
    mc.player.setPos(Vec3(minX + diameter, midY, minZ + diameter) + nodeOffsets[minX + diameter][minZ + diameter])

    print("Making caverns ...")
    for x in nodeOffsets:
        for z in nodeOffsets[x]:
            nodeOffset = nodeOffsets[x][z]
            node = Vec3(x, midY, z) + nodeOffset
            r = radii[x][z]
            print("sphere(" + str(node) + ", " + str(r) + ", " + str(cavernBlock) + ", 0, " + str(fill) + ")")
            sphere(node, r, cavernBlock, 0, fill)
            for i in range(1, random.randint(1, 4)):
                nE = node + randomVector(random.randint(2, r))
                sphere(nE, r, cavernBlock, 0, fill)
            if (x+diameter) in nodeOffsets:
                neighbor = Vec3(x + diameter, midY, z) + nodeOffsets[x+diameter][z]
                r1 = radii[x+diameter][z]
                connectNodes(node, neighbor, r, r1)
            if (z+diameter) in nodeOffsets[x]:
                neighbor = Vec3(x, midY, z + diameter) + nodeOffsets[x][z+diameter]
                r1 = radii[x][z+diameter]
                connectNodes(node, neighbor, r, r1)
    for x in nodeOffsets:
        for z in nodeOffsets[x]:
            nodeOffset = nodeOffsets[x][z]
            node = Vec3(x, midY, z) + nodeOffset
            r = radii[x][z]
            for i in range(0, random.randint(0, 4)):
                v = node + randomVector(r-3)
                base = random.randint(1, int(1 + round(maxR / 4)))
                height = 1
                if random.random() > 0.25:
                    while mc.getBlock( v + Vec3(0, height, 0) ) == 0:
                        height = height + 1
                    stalactite(v, base, height + 3, 89, 0)
                else:
                    while mc.getBlock(v) == 0:
                        height = height + 1
                        v = v + Vec3(0, -1, 0)
                    stalagmite(v, base, height, 89, 0)
            if random.random() > 0.5:
                randomLava(node, r)


nether()