import pygame
import Globals as G

class Moves():
    def __init__(self, pieces: list) -> None:
        self.pieces = pieces
        
    def piece(self, piece):
        finalMoves = []
        for dir in piece.dirVectors:
            currX = piece.x+dir[0]
            currY = piece.y+dir[1]
            cont = True
            while piece.can_move_to(currX, currY, self.pieces) and cont:
                if piece.is_take(currX,currY,self.pieces): cont=False
                finalMoves.append((currX,currY))
                currX+=dir[0]
                currY+=dir[1]
        return finalMoves

    def knight(self, piece):
        finalMoves=[]
        for dir in piece.dirVectors:
            currX = piece.x+dir[0]
            currY = piece.y+dir[1]
            if piece.can_move_to(currX,currY,self.pieces):
                finalMoves.append((currX,currY))
        return finalMoves
                
    def pawn(self, piece):
        finalMoves=[]
        if piece.isWhite:
            if piece.can_move_to(piece.x,piece.y-1, self.pieces):
                finalMoves.append((piece.x,piece.y-1))
            if piece.can_move_to(piece.x,piece.y-2,self.pieces) and not piece.hasMoved:
                finalMoves.append((piece.x,piece.y-2))
        else:
            if piece.can_move_to(piece.x,piece.y+1,self.pieces):
                finalMoves.append((piece.x,piece.y+1))
            if piece.can_move_to(piece.x,piece.y+2, self.pieces) and not piece.hasMoved:
                finalMoves.append((piece.x,piece.y+2))
        for move in piece.takes(self.pieces):
            finalMoves.append(move)
        return finalMoves
    
    def king(self, piece):
        finalMoves=[]
        for dir in piece.dirVectors:
            currX = piece.x+dir[0]
            currY = piece.y+dir[1]
            if piece.can_move_to(currX,currY,self.pieces):
                finalMoves.append((currX,currY))
        moveSet = set()
        for col in self.pieces:
            for thing in col:
                if thing!=None and thing.isWhite!=piece.isWhite:
                    for move in thing.validMoves:
                        moveSet.add(move)
        def in_set():
            res = []
            for move in finalMoves:
                if move not in moveSet:
                    res.append(move)
            return res
        return in_set()