import keyboard
from ctypes.wintypes import SIZE
from typing import List, Callable
from Position import Position
from Player import Player
from Enemy import Enemy
from Enemy1 import Enemy1
from Projectile import Projectile
from BlockManager import BlockManager
from BoolWrapper import BoolWrapper

class LvLManager:
    screenWidth = 32
    screenHight = 16
    width = 64
    hight = 32

    class LvLManagerHandle:
        #def __init__(self, mapp_data: List[List[str]], projectileCallback: Callable[[int, int, bool], None]):
        #    self.mapp = mapp_data
        #    self.createProjectileCallBack = projectileCallback
        #
        #def createProjectile(self, x: int, y: int, facingRight: bool):
        #    if self.createProjectileCallBack:
        #        self.createProjectileCallBack(x, y, facingRight)        
        def __init__(self, lvl_manager: "LvLManager"):
            self.lvl_manager = lvl_manager  # store reference to the full LvLManager, dosn't expose it

        @property
        def mapp(self):
            return self.lvl_manager.mapp  # read-only access to mapp

        def createProjectile(self, x: int, y: int, facingRight: bool):
            self.lvl_manager.addProjectile(x, y, facingRight)  # direct access to addProjectile()

    def __init__(self, running: BoolWrapper, cameraPos: Position, player: Player):
        self.runningRef = running
        self.cameraPos = cameraPos
        self.player = player
        self.lvl = 0
        self.mapp: List[List[str]] = []
        self.mapp = [[None] * self.hight for _ in range(self.width)] # makes the list be acsesd as [x][y] 
        self.enemies = []
        self.projectiles = []
        self.handle = self.LvLManagerHandle(self)

    def Initzialize(self):
        self.score = 0
        self.lvl = 0
        self.LoadLvL()

    def ResetLvL(self):
        self.LoadLvL()

    def LvLFinished(self):
        self.lvl += 1
        self.ResetLvL()

    def GameOver(self):
        self.runningRef.state = False
        print("\033[2J\033[0m\033[3;5H Game Over\033[4;5H Score: ", self.score, "\033[5;5H Level: ", self.lvl)
        # Simulating Beep
        print('\a')
        # Sleep for half a second
        import time
        time.sleep(3)
        # Wait for key press
        print("Press any key to continue...")
        keyboard.read_event()

    def Update(self):
        for enemy in self.enemies:
            x, y = enemy.x, enemy.y           
            if ((self.cameraPos.x <= x + 2) and (x - 2 < self.cameraPos.x + self.screenWidth) and
			    (self.cameraPos.y <= y + 2) and (y - 2 < self.cameraPos.y + self.screenHight)):
                enemy.Update()

        for projectile in self.projectiles:
            projectile.Update()    

    def addEnemy(self, enemy: Enemy):
        self.enemies.append(enemy)

    def addProjectile(self, x: int, y: int, isRight: bool):
        self.projectiles.append(Projectile(x, y, isRight, self.getHandle()))

    def LoadLvL(self):
        self.enemies.clear()
        self.projectiles.clear()

        if self.lvl == 0:
            self.LvL0()
        elif self.lvl == 1:
            self.LvL1()
        elif self.lvl == 2:
            self.LvL2()
        else:
            self.GameWon()

    def GameWon(self):
        self.runningRef.state = False
        print("\033[2J\033[0m\033[3;5H Game Won\033[4;5H Score: ", self.score, "\033[5;5H Level: ", self.lvl)
        # simulating Beep
        print('\a')
        # sleep for half a second
        import time
        time.sleep(3)
        # wait for key press
        print("Press any key to continue...")
        keyboard.read_event()

    def LvL0(self):
        # set size
        self.mapp = [[None] * self.hight for _ in range(self.width)]
    
        # floor
        for x in range(self.width):
            self.mapp[x][16] = BlockManager.ground
    
        # platform
        for x in range(8, 12):
            self.mapp[x][13] = BlockManager.ground
    
        # lone block
        self.mapp[3][15] = BlockManager.ground
    
        # flag and flagpole
        flag_x = self.width - 1
        for y in range(11, 16):
            self.mapp[flag_x][y] = BlockManager.flagPole
        self.mapp[flag_x][10] = BlockManager.flag
    
        # add enemy
        self.addEnemy(Enemy1(5, 5, False, self.getHandle()))
    
        # set player position
        self.player.x, self.player.y = 10, 10

    def LvL1(self):
        self.LvLFinished()

    def LvL2(self):
        self.LvLFinished()

    def getHandle(self):
        return self.handle