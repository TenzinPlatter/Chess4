import pygame
class forTime():
    pass

WINSIZE = WIDTH, HEIGHT = (900,900)
BORDER = 50
SQUARE = 100
LMB, RMB = 1,3
LIGHTCOLOUR = (245, 179, 113)
DARKCOLOUR = (168, 94, 20)
SELECTEDCOLOUR = (255, 51, 51)
VALIDCOLOUR = (160,160,160)
DELAY = 300
lastTime = 0
renderingQueue = []

dirVectors = {
    "rook":[[1,0],[-1,0],[0,1],[0,-1]],
    "bishop":[[1,1],[1,-1],[-1,1],[-1,-1]],
    "queen":[[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]],
    "king":[[1,0],[1,1],[1,-1],[-1,0],[-1,1],[-1,-1],[0,1],[0,-1]],
    "knight":[[2,1],[-2,-1],[2,-1],[-2,1],[1,2],[1,-2],[-1,-2],[-1,2]]
}

def can_select() -> forTime:
    global lastTime
    if lastTime+DELAY>pygame.time.get_ticks():
        return False
    lastTime = pygame.time.get_ticks()
    return True

def to_coords(coords):
    x,y = coords
    x,y = int((x-BORDER)/SQUARE), int((y-BORDER)/SQUARE)
    if x<0 or x>7 or y<0 or y>7:
        return False
    return x,y

def add_offest(val):
    return val*SQUARE + BORDER

def render_queue(surface):
    for item in renderingQueue:
        item.draw(surface)

def get_image(name: str, colour: str):
    return pygame.transform.scale(pygame.image.load(f"Chess4/Pieces/{name}_{colour}.png"), (SQUARE, SQUARE))

class RenderCircle():
    def __init__(self,x,y):
        self.center = (x+.5)*SQUARE+BORDER, (y+.5)*SQUARE+BORDER
    
    def draw(self, surf: pygame.surface):
        pygame.draw.circle(surf, VALIDCOLOUR, self.center, SQUARE*.2)
        
