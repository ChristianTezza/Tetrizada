from config import *
from config import MoveD
import random

 
class Block(pg.sprite.Sprite):
    def __init__(self, tetromino,pos):
        self.tetromino = tetromino
        self.pos = vec(pos) + InitPos
        self.nextP = vec(pos) + NextPos
        self.alive = True
        
        super(). __init__(tetromino.tetris.spriteGroup)
        self.image = tetromino.image
        self.rect = self.image.get_rect()       
    
    def isAlive(self):
        if not self.alive:
            self.kill()
            
    
    def rotate(self,pivotP):
        tranlated = self.pos - pivotP
        rotated = tranlated.rotate(90)
        return rotated + pivotP
    
        
    def set_rect_pos(self):
        pos = [self.nextP, self.pos][self.tetromino.current]
        self.rect.topleft = pos * TileSize

    def update(self):
        self.isAlive()
        self.set_rect_pos()
   
    def colide(self, pos):
        x,y = int(pos.x), int(pos.y)
        if 0 <= x < FieldW and y < FieldH and (
            y < 0 or not self.tetromino.tetris.FieldA[y][x]):
            return False
        return True


class Tetromino:
    def __init__(self, tetris, current=True):
        self.tetris = tetris
        self.shape = random.choice(list(Tetros.keys()))
        self.image = random.choice(tetris.app.images)
        self.blocks = [Block(self, pos) for pos in Tetros[self.shape]]
        self.landing = False
        self.current = current
        
    def rotate(self):
        pivotP = self.blocks[0].pos
        newBP = [block.rotate(pivotP) for block in self.blocks]

        if not self.colide(newBP):
            for i, block in enumerate(self.blocks):
                block.pos = newBP[i]
        
    def colide(self, blockP):
        return any(map(Block.colide, self.blocks, blockP))
    
    def move(self, direction):
        move_direction = MoveD[direction]
        newP = [block.pos + move_direction for block in self.blocks]
        colide = self.colide(newP)
        
        if not colide:
            for block in self.blocks:
                block.pos += move_direction
        
        elif direction == 'down':
           
            self.landing = True
            
    
    def update(self):
        self.move(direction='down')
       
        
           