class GraphicBase:
    def __init__(self, texture=' ', colour=0, collision=False):
        self.texture = texture
        self.colour = colour
        self.isCollision = collision

    def getCollision(self):
        return self.isCollision

    def getTexture(self):
        return self.texture

    def getColour(self):
        return self.colour
