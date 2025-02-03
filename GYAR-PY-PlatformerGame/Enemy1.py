#from Entity import Entity
from Enemy import Enemy, Entity
from BlockManager import BlockManager
from Text import Text

class Enemy1(Enemy):
    _health = 1
    _texture = 'E'
    _colour = Text.Formatting.BrightYellow
    _collision = False

    def __init__(self, x, y, faceRight, _LvLManagerHandle):
        super().__init__(self._health, self._texture, self._colour, self._collision, x, y, faceRight, _LvLManagerHandle)
        if faceRight:
            self.states |= Entity.Right

    def Update(self):
        self.Move()

    def TakeDamage(self):
        self.health -= 1
        if self.health <= 0:
            del self

    def Move(self):
        # is grounded check
        if not BlockManager.getCollision(self._LvLManagerHandle.mapp[self.x][self.y + 1]):
            self.y += 1  # fall
            self.states &= ~self.Down
            return
        # If we pass here, we know we are on the ground
        elif not (self.states & self.Down):
            self.states |= self.Down
            return
    
        # left n right movment
        if self.states & self.Right:
            if self.x < len(self._LvLManagerHandle.mapp) - 1 and not BlockManager.getCollision(self._LvLManagerHandle.mapp[self.x + 1][self.y]):
                self.x += 1
            elif self.x > 0 and not BlockManager.getCollision(self._LvLManagerHandle.mapp[self.x - 1][self.y]):
                self.states &= ~self.Right
                self.x -= 1
        else:
            if self.x > 0 and not BlockManager.getCollision(self._LvLManagerHandle.mapp[self.x - 1][self.y]):
                self.x -= 1
            elif self.x < len(self._LvLManagerHandle.mapp) - 1 and not BlockManager.getCollision(self._LvLManagerHandle.mapp[self.x + 1][self.y]):
                self.states |= self.Right
                self.x += 1
    
        self.states &= ~self.Down
    
        # check if out of bounds
        if self.x < 0 or self.x >= len(self._LvLManagerHandle.mapp) or self.y < 0 or self.y >= len(self._LvLManagerHandle.mapp[0]):
            del self