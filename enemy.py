import pygame
from numpy import exp
import random
SIZE=20
class Enemy():
    def __init__(self,screen,tile_rects,level_map,START_X,START_Y,hazardrects,boostrects):
        self.groundbing_sound = False
        self.groundbing_coords = (0,0)
        self.wasAir = False
        self.image_library = {}
        self.waitloop = 0
        self.move_t = 1
        self.old_pos = (START_X,START_Y)
        self.boosttime = 0
        self.boostrects = boostrects
        self.hazardrects = hazardrects
        self.START_X = START_X
        self.START_Y = START_Y
        self.level_map = level_map
        self.tile_rects = tile_rects
        self.imgstate = 1
        self.vy = 0
        self.vx_const = 4
        self.screen = screen
        self.vx = 1
        self.font = pygame.font.SysFont(None, 24)
        self.img = self.font.render('vx:' + str(self.vx_const), True, (84, 255, 0))
        self.img2 = self.font.render('vy:' + str(self.vy), True, (84, 255, 0))
        self.enemy_img = pygame.image.load('images/slime_r.png').convert_alpha()
        self.enemy_img = pygame.transform.smoothscale(self.enemy_img, (SIZE, SIZE))
        self.enemy_rect = pygame.Rect(START_X, START_Y, SIZE,SIZE)
        image = pygame.image.load("images/slime_r.png")
        self.image_library["images/slime_r.png"] = pygame.transform.smoothscale(image,(SIZE,SIZE))
        image = pygame.image.load("images/slime_l.png")
        self.image_library["images/slime_l.png"] = pygame.transform.smoothscale(image, (SIZE, SIZE))
    def get_image(self,path):
        image = self.image_library.get(path)
        return image
    def rollRight(self,isRight):
        if isRight:
            self.enemy_img = self.get_image('images/slime_r.png')
        else:
            self.enemy_img = self.get_image('images/slime_l.png')
    def runmovement(self):
        enemy_v_xy = [0, 0]
        if self.vx > 0:
            self.vx = .5*self.move_t * (1 - self.move_t / 20)
            self.move_t += 1
            if self.move_t > 19:
                self.move_t = 1
            self.rollRight(True)
        elif self.vx < 0:
            self.vx = -.5*self.move_t * (1 - self.move_t / 20)
            self.move_t += 1
            if self.move_t > 19:
                self.move_t = 1
            self.rollRight(False)
        enemy_v_xy[1] += self.vy
        if self.waitloop==10:
            self.waitloop=0
            if random.randint(0,29)==0:
                self.vx = -self.vx
        else:
            self.waitloop += 1
        enemy_v_xy[0] += self.vx
        self.vy += .2
        if self.vy > 5:
            self.vy = 5
        collisions = self.move(enemy_v_xy, self.tile_rects)
        if collisions['bottom'] == True:
            self.vy = 0
        elif collisions['top'] == True:
            self.vy = -self.vy
        self.check_boosts()
        self.check_hazards()
    def draw(self):
        self.screen.blit(self.enemy_img, (self.enemy_rect.x, self.enemy_rect.y))
    def check_hazards(self):
        for hazard in self.hazardrects:
            if self.enemy_rect.colliderect(hazard):
                self.enemy_rect.center=(self.START_X,self.START_Y)
    def check_boosts(self):
        for boost in self.boostrects:
            if self.enemy_rect.colliderect(boost):
                boosttime = self.enemy_rect.bottom - boost.top
                self.vy -= 1.5 * exp(.01 * (boosttime - 300))
    def collision_test(self,tiles):
        hit_list = []
        for tile in tiles:
            if self.enemy_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self,enemy_v_xy, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.enemy_rect.x += enemy_v_xy[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if enemy_v_xy[0] > 0:
                self.enemy_rect.right = tile.left
                collision_types['right'] = True
                self.vx = -self.vx
            elif enemy_v_xy[0] < 0:
                self.enemy_rect.left = tile.right
                collision_types['left'] = True
                self.vx = -self.vx
        self.enemy_rect.y += enemy_v_xy[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if enemy_v_xy[1] > 0:
                self.enemy_rect.bottom = tile.top
                collision_types['bottom'] = True
            elif enemy_v_xy[1] < 0:
                self.enemy_rect.top = tile.bottom
                collision_types['top'] = True
        self.img = self.font.render('vx:' + str(round(enemy_v_xy[0],3)), True,(84, 255, 0))
        self.img2 = self.font.render('vy:' + str(round(enemy_v_xy[1], 3)), True,(84, 255, 0))
        return collision_types