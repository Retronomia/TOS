import pygame
from numpy import sqrt,square
class Prox():
    def __init__(self):
        self.pos = (0,0)
        self.groundnoise = pygame.mixer.Sound('music/bounce.wav')
    def get_pos(self,player):
        self.pos = player
    def get_info(self,enemies):
        for enemy in enemies:
            coord = enemy.groundbing_coords
            noise = enemy.groundbing_sound
            if noise == True:
                self.play_ground(coord)
    def play_ground(self,coord):
        dist = sqrt(square(self.pos[1]-coord[1])+square(self.pos[0]-coord[0]))
        if dist <= 300:
            vol = (300-dist)/300
            self.groundnoise.set_volume(vol)
            self.groundnoise.play()