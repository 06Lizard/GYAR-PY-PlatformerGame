from Text import Text

class BlockManager:
	# blockMasks
    ground = 'G'
    flag = 'F'
    flagPole = 'f'

    @staticmethod
    def getCollision(block):
        if block == BlockManager.ground:
            return True
        else:
            return False

    @staticmethod
    def getTexture(block):
        if block == BlockManager.ground:
            return '='
        elif block == BlockManager.flag:
            return 'F'
        elif block == BlockManager.flagPole:
            return '|'
        else:
            return ' '

    @staticmethod
    def getColour(block):
        if block == BlockManager.ground:
            return Text.Formatting.Green
        elif block == BlockManager.flag:
            return Text.Formatting.BrightRed
        elif block == BlockManager.flagPole:
            return Text.Formatting.Gray
        else:
            return Text.Formatting.ResetAll
