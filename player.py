import pygame
from numpy import sqrt,square,exp

SIZE =30
class Player():
    def __init__(self,screen,tile_rects,level_map,START_X,START_Y,winrect,hazardrects,boostrects,enemies):
        self.enemies = enemies
        self.image_library = {}
        self.old_pos = (START_X,START_Y)
        self.boostrects = boostrects
        self.winrect = winrect
        self.wongame = False
        self.hazardrects = hazardrects
        self.winnoise = pygame.mixer.Sound('music/tada.wav')
        self.winnoise.set_volume(1)
        self.START_X = START_X
        self.START_Y = START_Y
        self.units_traveled = 0
        self.level_map = level_map
        self.tile_rects = tile_rects
        self.imgstate = 1
        self.vy = 0
        self.vx_const = 4
        self.air_timer = 0
        self.screen = screen
        self.groundnoise = pygame.mixer.Sound('music/bounce.wav')
        self.camelaimg = pygame.image.load("images/camela.png")
        self.camelaimg = pygame.transform.smoothscale(self.camelaimg, (60,60))
        self.cavernimg = pygame.image.load("images/cavern.png")
        self.cavernimg = pygame.transform.smoothscale(self.cavernimg, (40, 40))
        self.player_img = pygame.image.load('images/orb1.png').convert_alpha()
        self.player_img = pygame.transform.smoothscale(self.player_img, (SIZE, SIZE))
        self.player_rect = pygame.Rect(START_X, START_Y, SIZE,SIZE)
        for i in range(1,13):
            image = pygame.image.load("images/orb"+str(i)+".png")
            self.image_library["images/orb"+str(i)+".png"] = pygame.transform.smoothscale(image,(SIZE,SIZE))
    def get_image(self,path):
        image = self.image_library.get(path)
        return image
    def rollRight(self,isRight):
        if isRight:
            if(self.imgstate<12):
                self.imgstate+=1
            else:
                self.imgstate=1
        else:
            if(self.imgstate>1):
                self.imgstate-=1
            else:
                self.imgstate=12
        self.player_img = self.get_image("images/orb" + str(self.imgstate) + ".png")
    def runmovement(self,key):
        player_v_xy = [0, 0]
        if key[pygame.K_RIGHT]:
            player_v_xy[0] += self.vx_const
            self.rollRight(True)
        if key[pygame.K_LEFT]:
            player_v_xy[0] -= self.vx_const
            self.rollRight(False)
        if key[pygame.K_UP]:
            if self.air_timer < 4:
                self.vy += -2
                self.air_timer += 1
        player_v_xy[1] += self.vy
        self.vy += .2
        if self.vy > 5:
            self.vy = 5
        collisions = self.move(player_v_xy, self.tile_rects)
        if collisions['bottom'] == True:
            self.air_timer = 0
            self.vy = 0
        elif collisions['top'] == True:
            self.air_timer = 0
            self.vy = -self.vy
        self.check_boosts()
        self.check_enemies()
        self.check_hazards()
        self.check_win()
        self.level_map.update_pos(self.player_rect.x + SIZE / 2, self.player_rect.y + SIZE / 2)
        self.units_traveled += sqrt(square(self.old_pos[0]-(self.player_rect.x))+square(self.old_pos[1]-(self.player_rect.y)))
        self.old_pos=((self.player_rect.x,self.player_rect.y))
    def draw(self):
        self.screen.blit(self.player_img, (self.player_rect.x, self.player_rect.y))
        self.accessories = pygame.Surface((1120,630), pygame.SRCALPHA)
        self.accessories.blit(self.camelaimg, (420, 420))
        self.accessories.blit(self.cavernimg, (690, 10))
        self.screen.blit(self.accessories, (0, 0))
    def check_win(self):
        if self.player_rect.colliderect(self.winrect):
            self.winnoise.play()
            self.player_rect.center=(self.START_X,self.START_Y)
            self.wongame=True
    def check_enemies(self):
        for enemy in self.enemies:
            if self.player_rect.colliderect(enemy.enemy_rect):
                self.player_rect.center=(self.START_X,self.START_Y)
    def check_hazards(self):
        for hazard in self.hazardrects:
            if self.player_rect.colliderect(hazard):
                self.player_rect.center=(self.START_X,self.START_Y)
    def getunits(self):
        return self.units_traveled
    def check_boosts(self):
        for boost in self.boostrects:
            if self.player_rect.colliderect(boost):
                boosttime=self.player_rect.bottom-boost.top
                self.vy -= 1.5*exp(.01*(boosttime-300))
    def collision_test(self,tiles):
        hit_list = []
        for tile in tiles:
            if self.player_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self,player_v_xy, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.player_rect.x += player_v_xy[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if player_v_xy[0] > 0:
                self.player_rect.right = tile.left
                collision_types['right'] = True
            elif player_v_xy[0] < 0:
                self.player_rect.left = tile.right
                collision_types['left'] = True
        self.player_rect.y += player_v_xy[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if player_v_xy[1] > 0:
                self.player_rect.bottom = tile.top
                collision_types['bottom'] = True
            elif player_v_xy[1] < 0:
                self.player_rect.top = tile.bottom
                collision_types['top'] = True
        return collision_types