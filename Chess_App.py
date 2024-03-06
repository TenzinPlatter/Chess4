import pygame
from pygame.locals import *
from Board import Board
from Piece import Piece
import Globals as G

class Chess_App():
    def __init__(self):
        self.on_init()
        self.on_start()
    
    def on_init(self):
        pygame.init()
        self.running = True
        self.window = pygame.display.set_mode(G.WINSIZE)
        pygame.display.set_caption("Chess 4.0 (please fucking work)")
        self.board = Board()
        self.pieces = Piece(self.board.squares)
        self.boardUpdated = True
        self.selectedPiece = None
        self.whiteTurn = True
        self.mouseDown = False
        self.draggingPiece = None
        self.draggingFlag = False
        
    def on_quit(self):
        pygame.quit()

    def render(self):
        self.window.fill((0,0,0))
        self.board.render_all(self.window)
        self.pieces.render_all(self)
        G.render_queue(self.window)
        if self.mouseDown:
            self.drag_piece()
        pygame.display.update()
    
    def on_lClick(self):
        self.board.unselect_all()
        if not G.to_coords(pygame.mouse.get_pos()): return
        x,y = G.to_coords(pygame.mouse.get_pos())
        if self.draggingFlag: return
        if not self.pieces.active[x][y] or self.pieces.active[x][y].isWhite != self.whiteTurn: return
        if self.pieces.move(self.selectedPiece,x,y):
            self.selectedPiece = None
            return
        self.selectedPiece = self.pieces.active[x][y]
        
    
    def on_rClick(self):
        if not G.to_coords(pygame.mouse.get_pos()): return
        x,y = G.to_coords(pygame.mouse.get_pos())
        if G.can_select():
            self.board.squares[x][y].select()
            
    def on_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == G.LMB:
                self.draggingFlag = True
                self.mouseDown = True
            elif event.type == MOUSEBUTTONUP and event.button == G.RMB:
                self.on_rClick()
            elif event.type == MOUSEBUTTONUP and event.button == G.LMB:
                if self.mouseDown:
                    self.unselect_drag()
                self.on_lClick()
    
    def drag_piece(self):
        x,y = pygame.mouse.get_pos()
        if x<G.BORDER or x>G.BORDER+G.SQUARE*8 or y<G.BORDER or y>G.BORDER+G.SQUARE*8:
            self.unselect_drag()
            return
        x,y = G.to_coords((x,y))
        if self.draggingPiece==None:
            if self.pieces.active[x][y] and self.whiteTurn == self.pieces.active[x][y].isWhite:
                self.draggingPiece = self.pieces.active[x][y]
                self.selectedPiece = self.pieces.active[x][y]
            return
        self.draggingPiece.drag()
    
    def unselect_drag(self):
        x,y = G.to_coords(pygame.mouse.get_pos())
        self.pieces.move(self.selectedPiece,x,y)
        self.mouseDown = False
        self.draggingFlag = None
        if self.draggingPiece:
            self.draggingPiece.dragging = False
            self.draggingPiece = None
    
    def on_start(self):
        while self.running:
            if self.boardUpdated:
                self.pieces.update_moves()
                self.boardUpdated = False
            self.on_event()
            self.render()
        self.on_quit()

app = Chess_App()