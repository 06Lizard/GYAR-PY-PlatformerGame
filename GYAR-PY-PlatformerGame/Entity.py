from GraphicBase import GraphicBase
from Position import Position

class Entity(GraphicBase, Position):
    # define position of Entity's "bools", and my 2 bit variable
    Up          = 1 << 0 # 0000 0001
    Left        = 1 << 1 # 0000 0010
    Down        = 1 << 2 # 0000 0100
    Right       = 1 << 3 # 0000 1000
    isGrounded  = 1 << 4 # 0001 0000
    isJump      = 1 << 5 # 0010 0000
    jumpTime    = 0b11000000 # 2 bit variable

    def __init__(self, health, texture, colour, collision, x, y):
        super().__init__(texture, colour, collision)
        self.health = health
        self.x = x
        self.y = y
        self.states = 0b00000000 # holds Entity's variables / flags

    def Move(self):
        raise NotImplementedError("Move method must be implemented in derived classes")

    def Update(self):
        raise NotImplementedError("Update method must be implemented in derived classes")

    def TakeDamage(self):
        raise NotImplementedError("TakeDamage method must be implemented in derived classes")

    def __str__(self):
        return f"Entity at ({self.x}, {self.y}), health: {self.health}, texture: {self.texture}, colour: {self.colour}, collision: {self.isCollision}, states: {bin(self.states)}"