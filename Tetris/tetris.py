import pygame as pg
from config import *
from tetromino import Tetromino
import pygame.freetype as ft


class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FontPath)

    def draw(self):
        self.font.render_to(self.app.screen, (WinW * 0.60, WinH * 0.04),
            text='TRISTRES', fgcolor='white',
            size=TileSize * 1.60, bgcolor=(20, 20, 100))

        self.font.render_to(self.app.screen, (WinW * 0.72, WinH * 0.15),
            text='NEXT', fgcolor='white',
            size=TileSize * 1, bgcolor=(20, 20, 100))

        self.font.render_to(self.app.screen, (WinW * 0.62, WinH * 0.55),
            text='HighScore', fgcolor='white',
            size=TileSize * 1.2, bgcolor=(20, 20, 100))

        self.font.render_to(self.app.screen, (WinW * 0.73, WinH * 0.65),
            text=f'{self.app.tetris.max_score}', fgcolor='white',
            size=TileSize * 1.4, bgcolor=(20, 20, 100))

        self.font.render_to(self.app.screen, (WinW * 0.67, WinH * 0.75),
            text='Score', fgcolor='white',
            size=TileSize * 1.4, bgcolor=(20, 20, 100))

        self.font.render_to(self.app.screen, (WinW * 0.76, WinH * 0.85),
            text=f'{self.app.tetris.score}', fgcolor='white',
            size=TileSize * 1.60, bgcolor=(20, 20, 100))
        

class Tetris:
    def __init__(self, app):
        self.app = app
        self.spriteGroup = pg.sprite.Group()
        self.FieldA = self.GetFieldA()
        self.tetromino = Tetromino(self)
        self.nextTetro = Tetromino(self, current=False)
        self.SpeedUp = False
        self.max_score = self.load_max_score()
        self.score = 0
        self.fullLines = 0
        self.pointsLine = {0: 0, 1: 100, 2: 300, 3: 500, 4: 700, 5: 900}
        self.game_over = False
        
       
        self.blinkTimer = 0
        self.blinkInterval = 500
        self.showText = True
    
    def GetScore(self):
        self.score += self.pointsLine[self.fullLines]
        self.fullLines = 0

        if self.score > self.max_score:
            self.max_score = self.score
            self.save_max_score(self.max_score)

    def save_max_score(self, max_score):
        with open('max_score.txt', 'w') as file:
            file.write(str(max_score))

    def load_max_score(self):
        try:
            with open('max_score.txt', 'r') as file:
                max_score = int(file.read())
        except FileNotFoundError:
            max_score = 0
        return max_score

    def checkLine(self):
        row = FieldH - 1
        for y in range(FieldH - 1, -1, -1):
            for x in range(FieldW):
                self.FieldA[row][x] = self.FieldA[y][x]

                if self.FieldA[y][x]:
                    self.FieldA[row][x].pos = vec(x, y)

            if sum(map(bool, self.FieldA[y])) < FieldW:
                row -= 1
            else:
                for x in range(FieldW):
                    self.FieldA[row][x].alive = False
                    self.FieldA[row][x] = 0

                self.fullLines += 1

    def PutT(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.FieldA[y][x] = block

    def GetFieldA(self):
        return [[0 for x in range(FieldW)] for y in range(FieldH)]

    def GameOver(self):
        if self.tetromino.blocks[0].pos.y == InitPos[1]:
            pg.time.wait(500)
            self.game_over = True

    def checkTL(self):
        if self.tetromino.landing:
            if self.GameOver():
                self.__init__(self.app)
            else:
                self.SpeedUp = False
                self.PutT()
                self.nextTetro.current = True
                self.tetromino = self.nextTetro
                self.nextTetro = Tetromino(self, current=False)

    def control(self, pressKey):
        if self.game_over:
            if pressKey == pg.K_SPACE:
                self.__init__(self.app)
        if pressKey == pg.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressKey == pg.K_RIGHT:
            self.tetromino.move(direction='right')
        elif pressKey == pg.K_UP:
            self.tetromino.rotate()
        elif pressKey == pg.K_DOWN and pg.K_SPACE:
            self.SpeedUp = True
            self.score += 10
            if self.score > self.max_score:
                self.max_score = self.score
                self.save_max_score(self.max_score)

    def drawGrid(self):
        for x in range(FieldW):
            for y in range(FieldH):
                pg.draw.rect(self.app.screen, 'black',
                             (x * TileSize, y * TileSize, TileSize, TileSize), 1)

    def update(self):
            trigger = [self.app.animT, self.app.fastT][self.SpeedUp]
            if trigger:
                self.checkLine()
                self.tetromino.update()
                self.checkTL()
                self.GetScore()
            self.spriteGroup.update()
    
    def draw(self):
        self.drawGrid()
        self.spriteGroup.draw(self.app.screen)
        
        if self.game_over:
            overlay_surface = pg.Surface((WinW, WinH), pg.SRCALPHA)
            overlay_surface.fill((0, 0, 0, 155))  
            self.app.screen.blit(overlay_surface, (0, 0))  

            font = ft.Font(FontPath)
            font.render_to(self.app.screen, (WinW // 6 - 90, WinH // 3),
                text='Game Over', fgcolor='white',
                size=TileSize * 1.8, bgcolor=(20, 20, 100))            
            
            self.blinkTimer += self.app.clock.get_rawtime()
            if self.blinkTimer >= self.blinkInterval:
                self.blinkTimer = 0
                self.showText = not self.showText

            if self.showText:
                font.render_to(self.app.screen, (WinW // 5.5 - 90, WinH // 2),
                               text='Press "SPACE" to Restart', fgcolor='white',
                               size=TileSize * 0.7, bgcolor=(20, 20, 100))
        
