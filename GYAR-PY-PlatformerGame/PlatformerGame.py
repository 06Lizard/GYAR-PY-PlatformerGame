from ast import List
import string
import time
import keyboard
from Enemy import Enemy
from Player import Player
from LvLManager import LvLManager
from BlockManager import BlockManager
from Position import Position
from DeltaTimeCounter import DeltaTimeCounter
from BoolWrapper import BoolWrapper
from Text import Text

class PlatformerGame:
    def __init__(self):
        self.running = BoolWrapper(True)
        self.player = Player(10, 10, None)
        self.cameraPos = Position()
        self._LvLManager = LvLManager(self.running, self.cameraPos, self.player)
        self.player.setLvLManager(self._LvLManager)

    def Run(self):
        print("\033[0m\033[?25l") # reset formating & hide cursor 
        self.Menu()
        print("\033[2J\033[0m\033[3;5H Thanks for playing", end='', flush=True)

    def Menu(self):
        menueLoop = True
        while menueLoop:
            optionLoop = True
            menuOption = True
            print("\033[2J\033[3;6HPlatformerGame\033[4;6H StartGame \033[5;6H Quit ")
            keyboard.read_event() # await key press

            while optionLoop:
                time.sleep(0.1)
                if menuOption: 
                    print("\033[2J\033[3;6HPlatformerGame\033[4;6H<StartGame>\033[5;6H Quit ")
                else:
                    print("\033[2J\033[3;6HPlatformerGame\033[4;6H StartGame \033[5;6H<Quit>")

                time.sleep(0.1)
                if keyboard.is_pressed('w') or keyboard.is_pressed('up') or keyboard.is_pressed('s') or keyboard.is_pressed('down'):
                    menuOption = not menuOption
                if keyboard.is_pressed('enter') or keyboard.is_pressed('space'):
                    optionLoop = False

            if menuOption:
                self.GameLoop() # starts the actual game
            else:
                menueLoop = False # leaves menue and exits the game

    def Initzialize(self):
        self.running.state = True
        self.player.Reset() # reset player

        # set camera pos
        self.cameraPos.x = self.player.x
        self.cameraPos.y = self.player.y
        self.UpdateCamera()

        # set the mapp
        self._LvLManager.Initzialize()

    def GameLoop(self):
        self.Initzialize()
        delta_frame_counter = DeltaTimeCounter()

        while self.running.state:
            #self.Render(); # depricated # 7.9 ms
            self.OptimizedRender() # 4.3 ms
            self.Update() # 0.7 ms
            delta_frame_counter.Count()
            delta_frame_counter.Display(1, 1, "Frame") # change the second number to 17 if trying the depricated update
            time.sleep(0.05) # 0.2 ms

    def Update(self):
        self._LvLManager.Update()
        self.player.Update()
        self.UpdateCamera()

    # depricated, renders the mapp on an avrage time of 7.9 ms
    def Render(self):
        worldX = 0
        worldY = 0
        for y in range(LvLManager.screenHight):
            for x in range(LvLManager.screenWidth):
                # move out for efichency!?
                worldX = x + self.cameraPos.x
                worldY = y + self.cameraPos.y
    
                if self.player.x != worldX or self.player.y != worldY:
                    blockMask = self._LvLManager.mapp[worldX][worldY]
                    print(f"\033[{y + 1};{x + 1}H\033[{BlockManager.getColour(blockMask)}m{BlockManager.getTexture(blockMask)}", end="")
                else:
                    print(f"\033[{y + 1};{x + 1}H\033[{self.player.getColour()}m{self.player.getTexture()}", end="")
    
                # Temporary area for entity rendering
                for enemy in self._LvLManager.enemies:
                    if enemy.x == worldX and enemy.y == worldY:
                        print(f"\033[{y + 1};{x + 1}H\033[{enemy.getColour()}m{enemy.getTexture()}", end="")
                # and the same thing for the projectile rendering (unnececary as this is depricated anyways)

    # renders the mapp on an avrage time of 4.3 ms
    def OptimizedRender(self):
        # 1: Populate/prepare the screenBuffer
        class DisplayElement:
            def __init__(self, texture=' ', colour=0):
                self.texture = texture
                self.colour = colour
    
        # Corrected initialization order to match [x][y]
        screenBuffer = [[DisplayElement() for _ in range(self._LvLManager.screenHight)] for _ in range(self._LvLManager.screenWidth)]
    
        for x in range(self._LvLManager.screenWidth):
            for y in range(self._LvLManager.screenHight):
                worldX = x + self.cameraPos.x
                worldY = y + self.cameraPos.y
    
                element = DisplayElement()
    
                # If not player's position, amend map
                if self.player.x != worldX or self.player.y != worldY:
                    if 0 <= worldX < len(self._LvLManager.mapp) and 0 <= worldY < len(self._LvLManager.mapp[0]):  # Bounds check
                        blockMask = self._LvLManager.mapp[worldX][worldY]
                        if blockMask:
                            element.texture = BlockManager.getTexture(blockMask)
                            element.colour = BlockManager.getColour(blockMask)
                else:  # Player's position
                    element.texture = self.player.getTexture()
                    element.colour = self.player.getColour()
    
                # Entity handling
                for enemy in self._LvLManager.enemies:
                    if enemy.x == worldX and enemy.y == worldY:
                        element.texture = enemy.getTexture()
                        element.colour = enemy.getColour()
                        break  # Prioritize first enemy found
    
                # Projectile handling
                for projectile in self._LvLManager.projectiles:
                    if projectile.x == worldX and projectile.y == worldY:
                        element.texture = projectile.getTexture()
                        element.colour = projectile.getColour()
                        break  # Prioritize first projectile found
    
                # Update screenBuffer
                screenBuffer[x][y] = element
    
        # 2: Construct the screenOutput string from screenBuffer
        screenOutput = []
        screenOutput.append("\033[2;2H")  # Set initial cursor position
    
        for y in range(self._LvLManager.screenHight):
            for x in range(self._LvLManager.screenWidth):
                element = screenBuffer[x][y]
                screenOutput.append(f"\033[{element.colour}m{element.texture}")
            screenOutput.append('\n')  # End of row
    
        # 3: Render the screen in a single print statement
        print("".join(screenOutput), flush=True)
     
    def UpdateCamera(self):
        camera_left_bound = 10
        camera_right_bound = LvLManager.screenWidth - 10

        if (self.player.x < self.cameraPos.x + camera_left_bound):
            self.cameraPos.x = self.player.x - camera_left_bound
        elif (self.player.x > self.cameraPos.x + camera_right_bound):
            self.cameraPos.x = self.player.x - camera_right_bound

        self.cameraPos.y = 1

        self.cameraPos.x = max(0, min(self.cameraPos.x, LvLManager.width - LvLManager.screenWidth))