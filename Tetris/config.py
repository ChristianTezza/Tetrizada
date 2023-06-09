import pygame as pg
vec = pg.math.Vector2


Fps = 60
FieldColor = (20,40,90)
BgColor = (25,30,40)

TileSize = 34
FieldSize = FieldW, FieldH = 10,20
FieldRes = FieldW * TileSize, FieldH * TileSize

FieldScaleW, FieldScaleH = 1.7, 1

WinRes = WinW,WinH = FieldRes[0] * FieldScaleW, FieldRes[1] * FieldScaleH


SpritesC = 'assets/sprites'
FontPath = 'assets/font/VCRosdNEUE.ttf'
animT = 300 
InitPos = vec(FieldW // 2 - 1, 0)
NextPos = vec(FieldW * 1.3, FieldH * 0.3)
FastAnim = 15
MoveD = {'left': vec(-1,0), 'right': vec(1,0), 'down': vec(0,1)}

Tetros = {
    'T':[(0,0),(-1,0),(1,0),(0,-1)],
    'Q':[(0,0),(0,-1),(1,0),(1,-1)],
    'J':[(0,0),(-1,0),(0,-1),(0,-2)],
    'L':[(0,0),(1,0),(0,-1),(0,-2)],
    'I':[(0,0),(0,1),(0,-1),(0,-2)],
    'Z':[(0,0),(-1,0),(0,-1),(1,-1)],
    'S':[(0,0),(1,0),(0,-1),(-1,-1)],
    
}

