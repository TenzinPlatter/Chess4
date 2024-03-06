import pygame
import Globals as G 
from Movement import Moves
class index():
    pass

class Piece():
    def __init__(self, squares) -> None:
        self.active = Piece.init_array()
        self.squares = squares

    def render_all(self, mainApp):
        G.renderingQueue = []
        for col in self.active:
            for piece in col:
                if piece:
                    if piece.dragging:
                        mainApp.window.blit(piece.image, (piece.xCoord,piece.yCoord))
                    else:
                        mainApp.window.blit(piece.image, self.squares[piece.x][piece.y])
                if piece and piece==mainApp.selectedPiece:
                    for move in piece.validMoves:
                        G.renderingQueue.append(G.RenderCircle(*move))
                        
                        
    def update_moves(self):
        kings = []
        for col in self.active:
            for piece in col:
                if piece:
                    piece.set_moves(self.active)
                if type(piece)==King:
                    kings.append(piece)
        for king in kings:
            king.set_moves(self.active)
                
                
    def select_piece(self,mainApp, x=None,y=None):
        if not mainApp.draggingFlag:
            mainApp.selectedPiece = self.active[x][y]
        try:
            if mainApp.whiteTurn==self.active[x][y].isWhite:
                self.active[x][y].display_moves()
        except:
            return False
    
    def move(self,piece,x:index,y:index):
        if (x,y) in piece.validMoves:
            tempPiece = piece
            self.active[piece.x][piece.y] = None
            self.active[x][y] = piece
            piece.x = x
            piece.y = y
            try: piece.hasMoved = True
            except: pass
            return True
        return False  
      
    @staticmethod
    def init_array():
        final = []
        for x in range(8):
            col = []
            for y in range(8):
                col.append(None)
            final.append(col)
        for x in range(8):
            final[x][6] = Pawn(x,6,True)
            final[x][1] = Pawn(x,1,False)
        for x in range(2):
            final[x*7][7] = Rook(x*7,7,True)
            final[x*7][0] = Rook(x*7,0,False)
            final[x*5+1][7] = Knight(x*5+1,7,True) 
            final[x*5+1][0] = Knight(x*5+1,0,False)
            final[x*3+2][7] = Bishop(x*3+2,7,True) 
            final[x*3+2][0] = Bishop(x*3+2,0,False)
        final[3][7] = Queen(3,7,True) 
        final[3][0] = Queen(3,0,False)
        final[4][7] = King(4,7,True)
        final[4][0] = King(4,0,False)
        return final

class BasePiece():
    def __init__(self, x: index, y: index, isWhite:bool, type:str) -> None:
        self.isWhite = isWhite
        self.x = x
        self.y = y
        self.validMoves = []
        self.dragging = False
        self.xCoord = None
        self.yCoord = None
        if isWhite:
            self.image = G.get_image(type, "white")
        else:
            self.image = G.get_image(type, "black")
    
    def can_move_to(self,x:index,y:index,pieces:list):
        if x>=0 and x<=7 and y>=0 and y<=7 and (pieces[x][y]==None or self.isWhite!=pieces[x][y].isWhite):
                return True
        return False
    
    def is_take(self,x,y,pieces):
        try:
            if self.isWhite!=pieces[x][y].isWhite: return True
            return False
        except:
            return False
    
    def set_moves(self, pieces):
        self.validMoves = Moves(pieces).piece(self)
    
    def display_moves(self):
        for move in self.validMoves:
            G.renderingQueue.append(G.RenderCircle(*move))

        
    def drag(self):
        x,y = pygame.mouse.get_pos()
        self.xCoord, self.yCoord = x-G.SQUARE/2,y-G.SQUARE/2
        self.dragging = True
    
class Pawn(BasePiece):
    def __init__(self, x: index, y: index, isWhite: bool) -> None:
        super().__init__(x, y, isWhite, "pawn")
        self.hasMoved = False
    
    def takes(self,pieces):
        final = []
        def can_take(x,y):
            if x<0 or x>7 or y<0 or y>7: return False
            return pieces[x][y] and self.isWhite!=pieces[x][y].isWhite
        
        if self.isWhite:
            if can_take(self.x+1,self.y-1):
                final.append((self.x+1,self.y-1))
            if can_take(self.x-1,self.y-1):
                final.append((self.x-1,self.y-1))
        else:
            if can_take(self.x+1,self.y+1):
                final.append((self.x+1,self.y+1))
            if can_take(self.x-1,self.y+1):
                final.append((self.x-1,self.y+1))
        return final
        
    def set_moves(self, pieces):
        self.validMoves = Moves(pieces).pawn(self)
        
        
class Rook(BasePiece):
    def __init__(self, x: index, y: index, isWhite: bool) -> None:
        super().__init__(x, y, isWhite, "rook")
        self.dirVectors = G.dirVectors["rook"]

class Knight(BasePiece):
    def __init__(self, x: index, y: index, isWhite: bool) -> None:
        super().__init__(x, y, isWhite, "knight")
        self.dirVectors = G.dirVectors["knight"]
    
    def set_moves(self, pieces):
        self.validMoves = Moves(pieces).knight(self)
    
class Bishop(BasePiece):
    def __init__(self, x: index, y: index, isWhite: bool) -> None:
        super().__init__(x, y, isWhite, "bishop")
        self.dirVectors = G.dirVectors["bishop"]
        
class Queen(BasePiece):
    def __init__(self, x: index, y: index, isWhite: bool) -> None:
        super().__init__(x, y, isWhite, "queen")
        self.dirVectors = G.dirVectors["queen"]
        
class King(BasePiece):
    def __init__(self, x: index, y: index, isWhite: bool) -> None:
        super().__init__(x, y, isWhite, "king")
        self.dirVectors = G.dirVectors["king"]
    
    def set_moves(self, pieces):
        self.validMoves = Moves(pieces).king(self)