import pygame
import Globals as G
class index():
    pass

class Board():
    def __init__(self) -> None:
        self.squares = Board.init_array()
    
    def render_all(self, window: pygame.surface):
        for col in self.squares:
            for square in col:
                pygame.draw.rect(window, square.COLOUR, square.rect)
    
    def unselect_all(self):
        for col in self.squares:
            for square in col:
                if square.COLOUR==G.SELECTEDCOLOUR: 
                    if (square.x+square.y)%2==0:
                        square.COLOUR = G.LIGHTCOLOUR
                    else:
                        square.COLOUR = G.DARKCOLOUR

    @staticmethod
    def init_array() -> list:
        final = []
        for x in range(8):
            col = []
            for y in range(8):
                if (x+y)%2==0:
                    col.append(Square(x,y,G.LIGHTCOLOUR))
                else:
                    col.append(Square(x,y,G.DARKCOLOUR))
            final.append(col)
        return final


class Square():
    def __init__(self, x: index, y: index, colour):
        self.COLOUR = colour
        self.size = G.SQUARE
        self.x = x
        self.y = y
        self.rect = pygame.Rect(G.add_offest(x), G.add_offest(y), G.SQUARE, G.SQUARE)
        
    def select(self):
        if self.COLOUR==G.SELECTEDCOLOUR:
            if (self.x+self.y)%2==0:
                self.COLOUR = G.LIGHTCOLOUR
            else:
                self.COLOUR = G.DARKCOLOUR
        else:
            self.COLOUR = G.SELECTEDCOLOUR
                
    def unselect(self):
        if (self.x+self.y)%2==0:
            self.COLOUR = G.LIGHTCOLOUR
        else:
            self.COLOUR = G.DARKCOLOUR