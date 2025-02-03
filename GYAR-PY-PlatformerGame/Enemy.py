from Entity import Entity

class Enemy(Entity):
    def __init__(self, HP, texture, colour, collision, x, y, faceRight, _LvLManagerHandle):
        super().__init__(HP, texture, colour, collision, x, y)
        self._LvLManagerHandle = _LvLManagerHandle
        if faceRight:
            self.states |= Entity.Right

    def Update(self):
        raise NotImplementedError("Update method must be implemented in derived classes")

    def Move(self):
        raise NotImplementedError("Move method must be implemented in derived classes")