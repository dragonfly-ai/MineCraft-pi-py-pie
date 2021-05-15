# MineCraft-pi-py-pie
Python code that makes minecraft-pi more fun!

In addition to building scripts for making simple shapes, spiral stair cases, and Death Stars.

How to use this library:

1.  Start MineCraft-Pi and enter a level.
2.  Open linux terminal.
3.  Navigate to the MineCraft-pi-py-pie folder:
	cd {path to}/MineCraft-pi-py-pie

```bash
$ python3
```

To play Ghost and Lava Monster Combat games:
```python
from BlockHitMenu import *
bhm = BlockHitMenu()
```

To summon a Ghost:
In game, find or place a full sized glass block, select the sword, and right mouse click the glass block.  A ghost will randomly spawn somewhere in the level and begin hunting you.  Ghosts move through walls and all terrain, so watch out!  If the ghost catches you, it will telleport you into a grave and then hunt you again.
To kill the ghost, right mouse click it with your sword.

To summon a Lava Monster:
In game, find or place a torch, select the sword, and right mouse click the torch.
A Lava Monster will randomly spawn somewhere in the level and begin hunting you.  Lava Monsters swing two lava swords around like helecopter blades, burn through walls and all terrain, so watch out!  If the Lava Monster catches you, you will die and it will hunt you again when you respawn.  To kill the Lava Monster, right mouse click it with your sword, but watch out because its lava blades will set you on fire!
