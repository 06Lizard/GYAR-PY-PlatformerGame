#from sre_constants import JUMP
import keyboard
from Entity import Entity
from BlockManager import BlockManager
from Text import Text

class Player(Entity):
    _health = 1
    _texture = '#'
    _colour = Text.Formatting.Red
    _collision = False

    def __init__(self, x, y, _LvLManager=None): #set lvl manager as null and set it later
        super().__init__(self._health, self._texture, self._colour, self._collision, x, y)
        self._LvLManager = _LvLManager

    def setLvLManager(self, _LvLManager): # sets the lvl manager here to avoid circular dependency ishues :)
        self._LvLManager = _LvLManager

    def Update(self):
        self.Input()
        self.Move()
        self.Collision()        

    def TakeDamage(self):
        self.health -= 1
        if self.health <= 0:
            self._LvLManager.GameOver()
        else:
            self._LvLManager.ResetLvL()

    def Reset(self):
        self.health = self._health

    def Input(self):
        self.states &= ~0b00001111  # reset movement states

        if keyboard.is_pressed('w') or keyboard.is_pressed('up'):  # W or Up arrow key
            self.states |= Entity.Up
        if keyboard.is_pressed('a') or keyboard.is_pressed('left'):  # A or Left arrow key
            self.states |= Entity.Left
        if keyboard.is_pressed('s') or keyboard.is_pressed('down'):  # S or Down arrow key
            self.states |= Entity.Down
        if keyboard.is_pressed('d') or keyboard.is_pressed('right'):  # D or Right arrow key
            self.states |= Entity.Right

    def Move(self):
        # is grounded check
        if BlockManager.getCollision(self._LvLManager.mapp[self.x][self.y + 1]):
            self.states |= Entity.isGrounded
        else:
            self.states &= ~Entity.isGrounded

        # stop jumping if Up and jumping
        if not (self.states & Entity.Up) and (self.states & Entity.isJump):
            self.states &= ~Entity.isJump  # clears isJump flag
            self.states = self.states & ~Entity.isJump  # clears bits 6 and 7

        # fall down if not grounded and not jumping
        elif not (self.states & Entity.isGrounded) and not (self.states & Entity.isJump):
            if BlockManager.getCollision(self._LvLManager.mapp[self.x][self.y + 1]):
                self.states |= Entity.isGrounded  # set isGrounded flag
            else:
                self.y += 1  # fall down
                for enemy in self._LvLManager.enemies:
                    if self.x == enemy.x and self.y == enemy.y:
                        enemy.TakeDamage()

        # begin jumping if Up is pressed and player is on ground and no block above
        elif (self.states & Entity.Up) and (self.states & Entity.isGrounded):
            if not BlockManager.getCollision(self._LvLManager.mapp[self.x][self.y - 1]):
                self.states |= Entity.isJump  # set isJump flag
                self.states &= ~Entity.isGrounded  # clears isGrounded flag
                self.y -= 1  # move up
                self.states = (self.states & ~Entity.jumpTime) | (1 << 6)
            else:
                self.states &= ~Entity.isJump

        # continue jump if Up is still pressed and jumpTime is less than 3
        elif (self.states & Entity.Up) and (self.states & Entity.isJump):
            if (((self.states >> 6) & 0b11) < 3 and not BlockManager.getCollision(self._LvLManager.mapp[self.x][self.y - 1])):            
                self.y -= 1  # move up
                self.states = (self.states & ~Entity.jumpTime) | (((self.states >> 6) & 0b11) + 1) << 6  # increment jumpTime
            else:
                self.states &= ~Entity.isJump

        # Left & Right movement
        if self.states & Entity.Left and not (self.states & Entity.Right):
            if self.x > 0 and not BlockManager.getCollision(self._LvLManager.mapp[self.x - 1][self.y]):
                self.x -= 1
        elif not (self.states & Entity.Left) and self.states & Entity.Right:
            if self.x < self._LvLManager.width - 1 and not BlockManager.getCollision(self._LvLManager.mapp[self.x + 1][self.y]):
                self.x += 1

    def Collision(self):
        block = self._LvLManager.mapp[self.x][self.y]
        if block == BlockManager.flag or block == BlockManager.flagPole:
            self._LvLManager.LvLFinished()

        for enemy in self._LvLManager.enemies:
            if self.x == enemy.x and self.y == enemy.y:
                self.TakeDamage()

        for projectile in self._LvLManager.projectiles:
            if self.x == projectile.x and self.y == projectile.y:
                self.TakeDamage()