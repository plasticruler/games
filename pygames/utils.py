from random import randrange, choice

class COLOURS:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    GREY = (200, 200, 200)
    ORANGE = (255, 128, 0)
    SKY_BLUE = (135, 206, 235)
    INDIGO = (70, 0, 130)
    YELLOW = (255, 255, 0)    

    @staticmethod
    def GetRandomColour(select=True):
        if not select:
            return (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        else:
            return random.choice([COLOURS.WHITE, COLOURS.YELLOW, COLOURS.RED, COLOURS.INDIGO, COLOURS.GREEN, COLOURS.ORANGE, COLOURS.SKY_BLUE])

class POS:
    def __init__(self, r, c):
        self.r = r
        self.c = c
    def c(self):
        return self.c
    def r(self):
        return self.r

    def __add__(self, o):
        return POS(self.r + o.r, self.c + o.c)
    
    def __sub__(self, o):
        return POS(self.r - o.r, self.c - o.c)
    
    def __mul__(self, o):
        if type(o) is POS:
            return POS(self.r * o.r, self.c * o.c)
        
        if type(o) is int:
            return POS(self.r * o, self.c * o)
            
        raise ArithmeticError()
        
    def __rmul__(self, o):
        if type(o) is POS:
            return POS(self.r * o.r, self.c * o.c)
        
        if type(o) is int:
            return POS(self.r * o, self.c * o)
        
        raise ArithmeticError()

    
    def __repr__(self):
        return f"<POS:{self.r},{self.c}>"

class DIRECTIONS:
    UP = POS(-1, 0)
    DOWN = POS(1, 0)
    SAME = POS(0, 0)
    LEFT = POS(0, -1)
    RIGHT = POS(0, 1)
    TOP_LEFT = POS(-1, -1)
    TOP_RIGHT = POS(-1, 1)
    BOTTOM_LEFT = POS(1, -1)
    BOTTOM_RIGHT = POS(1,1)