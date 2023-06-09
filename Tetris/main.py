import pygame as pg
from config import *
from tetris import Tetris, Text
import sys
import pathlib
import pygame.mixer as mixer
from moviepy.editor import VideoFileClip
import pygame.freetype as ft


class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')
        self.screen = pg.display.set_mode(WinRes)
        self.clock = pg.time.Clock()
        self.setT()
        self.images = self.loadI()
        self.tetris = Tetris(self)
        self.move_delay = 150  
        self.move_interval = 50  
        self.move_right_timer = 0
        self.move_left_timer = 0
        self.text = Text(self)

        self.blinkTimer = 0
        self.blinkInterval = 350
        self.showPause = True
        
        mixer.init()
        self.musicFiles = ["assets/song/Metal_tetris_song.mp3","assets/song/Tetris_song.mp3", "assets/song/B_type_song.mp3", "assets/song/HighScore_song.mp3"]
        self.current_music_index = 0
        self.load_music()
        self.musicPlaying = True
        self.volume = 0.5  
        self.volume_increment = 0.1
        self.paused = False
        
    def play_intro(self):
        intro_clip = VideoFileClip("assets/video/Introtristes.mp4")
        intro_clip.preview()
        pg.event.clear()
        pg.display.set_mode(WinRes)   
        
    def loadI(self):
        files = [item for item in pathlib.Path(SpritesC).rglob('*.png') if item.is_file()] 
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (TileSize,TileSize)) for image in images]
        return images
    
    def setT(self):
        self.userE = pg.USEREVENT + 0
        self.FastUser = pg.USEREVENT + 1
        self.animT = False
        self.fastT = False
        pg.time.set_timer(self.userE, animT)
        pg.time.set_timer(self.FastUser, FastAnim)
        
    def update(self):
        self.tetris.update()
        self.clock.tick(Fps)

    
    def draw(self):
        self.screen.fill(color=BgColor)
        self.screen.fill(color=FieldColor, rect=(0,0, * FieldRes))
        self.tetris.draw()
        self.text.draw()
        if self.paused:
            self.draw_pause_text()
        self.draw_music_name()    
        pg.display.flip()
        
    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            mixer.music.pause()
        else:
            mixer.music.unpause()  
                  
    def check_events(self):
        self.animT = False
        self.fastT = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    self.toggle_pause()
                elif event.key == pg.K_m:
                    self.toggle_music()
                elif event.key == pg.K_KP_PLUS:
                    self.increase_volume()
                elif event.key == pg.K_KP_MINUS:
                    self.decrease_volume()
                elif event.key == pg.K_c:
                    self.change_music()
                else:
                    self.tetris.control(pressKey=event.key)

                    if event.key == pg.K_RIGHT:
                        self.move_right_timer = pg.time.get_ticks() + self.move_delay
                    elif event.key == pg.K_LEFT:
                        self.move_left_timer = pg.time.get_ticks() + self.move_delay

            elif event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT:
                    self.move_right_timer = 0
                elif event.key == pg.K_LEFT:
                    self.move_left_timer = 0

            elif event.type == self.userE:
                self.animT = True
            elif event.type == self.FastUser:
                self.fastT = True

        
        if self.move_right_timer and pg.time.get_ticks() > self.move_right_timer:
            self.move_right_timer += self.move_interval
            self.tetris.control(pressKey=pg.K_RIGHT)

        
        if self.move_left_timer and pg.time.get_ticks() > self.move_left_timer:
            self.move_left_timer += self.move_interval
            self.tetris.control(pressKey=pg.K_LEFT)



    def increase_volume(self):
        self.volume += self.volume_increment
        if self.volume > 1.0:
            self.volume = 1.0
        mixer.music.set_volume(self.volume)

    def decrease_volume(self):
        self.volume -= self.volume_increment
        if self.volume < 0.0:
            self.volume = 0.0
        mixer.music.set_volume(self.volume)

    def toggle_music(self):
        
        if self.musicPlaying:
            mixer.music.pause()
            self.musicPlaying = False
             
        else:
            mixer.music.unpause()
            self.musicPlaying = True
            

    def load_music(self):
        musicFile = self.musicFiles[self.current_music_index]
        mixer.music.load(musicFile)

    def change_music(self):
        self.current_music_index = (self.current_music_index + 1) % len(self.musicFiles)
        musicFile = self.musicFiles[self.current_music_index]
        mixer.music.load(musicFile)
        mixer.music.play(-1)
        
    def draw_pause_text(self):
            font = ft.Font(FontPath)
            overlay_surface = pg.Surface((WinW, WinH), pg.SRCALPHA)
            overlay_surface.fill((0, 0, 0, 155))  
            self.screen.blit(overlay_surface, (0, 0))  
            self.blinkTimer += self.clock.get_rawtime()
            if self.blinkTimer >= self.blinkInterval:
                self.blinkTimer = 0
                self.showPause = not self.showPause

            if self.showPause:
                font.render_to(self.screen, (WinW // 2.5 - 90, WinH // 2.3),
                               text='PAUSED', fgcolor='white',
                               size=TileSize * 2.0, bgcolor=(20, 20, 100))     

    def draw_music_name(self):
            font = ft.Font(FontPath)
            music_name = self.musicFiles[self.current_music_index].split('/')[-1]
            font.render_to(self.screen, (WinW * 0.01, WinH * 0.01),
                       text=f"Music: {music_name}", fgcolor='white',
                       size=TileSize * 0.7, bgcolor=(20, 20, 100))

            if not self.musicPlaying:
                font.render_to(self.screen, (WinW * 0.01, WinH * 0.05),
                       text="Music Paused", fgcolor='white',
                       size=TileSize * 0.7, bgcolor=(20, 20, 100))                          
    def run(self):
        self.play_intro()
        mixer.music.play(-1)
            
        while True:
            self.check_events()
        
            if not self.paused:
                self.update()
            self.draw()

if __name__ == '__main__':
    app = App()
    app.run()
          
            
                                    
