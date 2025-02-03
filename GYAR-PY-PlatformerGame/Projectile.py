from Entity import Entity
from BlockManager import BlockManager  # Assuming BlockManager class is defined
from Text import Text

class Projectile(Entity):
    _health = 8
    _texture = '*'
    _colour = Text.Formatting.BrightMagenta
    _collision = False

    def __init__(self, x, y, isRight, lvl_manager_handle):
        super().__init__(self._health, self._texture, self._colour, self._collision, x, y)
        self._LvLManagerHandle = lvl_manager_handle
        self.isRight = isRight

    def Update(self):
        self.health -= 1
        self.Move()
        if self.health <= 0:
            del self

    def TakeDamage(self):
        del self

    def Move(self):
        if self.isRight:
            self.x += 1
        else:
            self.x -= 1

        if BlockManager.getCollision(self._LvLManagerHandle.mapp[self.x][self.y]):
            del self