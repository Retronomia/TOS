from numpy import arctan2
import pygame
from ray import *
from wall import *

class Level():
    def __init__(self,screen,WIDTH,HEIGHT,START_X,START_Y):
        self.won = False
        self.focus_pos_x = 0
        self.focus_pos_y = 0
        self.screen = screen
        self.rays = []
        self.walls = []
        self.START_X = START_X
        self.START_Y = START_Y
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.create_platforms()
        self.create_hazards()
        self.create_boosts()
        self.lightimg = pygame.image.load("images/light.png").convert_alpha()
        self.lightimg = pygame.transform.smoothscale(self.lightimg, (600,600))
        self.bgimg = pygame.image.load("images/bg.png")
        self.bgimg = pygame.transform.smoothscale(self.bgimg, (self.WIDTH, self.HEIGHT))
        self.winimg = pygame.image.load("images/triforce.png")
        self.winimg = pygame.transform.smoothscale(self.winimg, (100,100))
        self.winrect = self.winimg.get_rect()
        self.winrect.x = 300
        self.winrect.y = 310
        self.tile_rects = []
        self.tile_rects_draw = []
        for i in range(len(self.rectcoords)):
            self.tile_rects.append(pygame.Rect((self.rectcoords[i][0],self.rectcoords[i][1], self.rectwh[i][0],self.rectwh[i][1])))
            self.tile_rects_draw.append((self.rectcoords[i][0],self.rectcoords[i][1], self.rectwh[i][0],self.rectwh[i][1]))
    def create_boosts(self):
        self.boostcoords = [(900,200),(580,300)]
        self.boostwh = [(100,420),(30,180)]
        self.boostrects = []
        self.boostrects_draw = []
        for i in range(len(self.boostcoords)):
            self.boostrects.append(pygame.Rect((self.boostcoords[i][0],self.boostcoords[i][1], self.boostwh[i][0],self.boostwh[i][1])))
            self.boostrects_draw.append((self.boostcoords[i][0],self.boostcoords[i][1], self.boostwh[i][0],self.boostwh[i][1]))
    def create_hazards(self):
        self.hazardcoords = [(510,600),(380,600),(220,600),(330,479),(10,450)]
        self.hazardwh = [(130,20),(80,20),(110,20),(50,10),(80,30)]
        self.hazardrects = []
        self.hazardrects_draw = []
        for i in range(len(self.hazardcoords)):
            self.hazardrects.append(pygame.Rect((self.hazardcoords[i][0],self.hazardcoords[i][1], self.hazardwh[i][0],self.hazardwh[i][1])))
            self.hazardrects_draw.append((self.hazardcoords[i][0],self.hazardcoords[i][1], self.hazardwh[i][0],self.hazardwh[i][1]))
    def create_platforms(self):
        self.rectcoords = [(0,0),(0,620),(0,10),(1110,0),
                           (100,560),(10,480),(210,300),(90,300),(160,300),(160,370),(240,480),(280,300),(280,400),(280,280),(560,250),
                           (400,60),(60,40),(10,100),(10,170),(420,180),(420,120),(800,180),(470,230),(330,590),(460,590),(640,590),(720,200),(820,300),(1060,150),
                           (460,10),(600,70),(480,70),(600,50),(654,100),(610,330),(670,280)]
        self.rectwh = [(1110,10),(1120,10),(10,610),(10,620),
                       (120,60),(150,20),(30,200),(20,180),(50,20),(50,20),(400,20),(20,100),(300,20),(240,20),(20,150),
                       (20,220),(360,20),(320,20),(320,20),(340,20),(200,20),(20,400),(200,20),(50,30),(50,30),(80,30),(40,200),(50,20),(50,20),
                       (20,80),(20,50),(120,20),(400,20),(300,40),(50,20),(50,20)]
        self.shapemap = []
        for i in range(0,len(self.rectcoords)):
            self.shapemap.append((self.rectcoords[i][0], self.rectcoords[i][1] + self.rectwh[i][1]))
            self.shapemap.append(self.rectcoords[i])
            self.shapemap.append((self.rectcoords[i][0]+self.rectwh[i][0],self.rectcoords[i][1]))
            self.shapemap.append((self.rectcoords[i][0] + self.rectwh[i][0], self.rectcoords[i][1] + self.rectwh[i][1]))
        for i in range(0,len(self.shapemap),4):
            x1 = self.shapemap[i][0]
            y1 = self.shapemap[i][1]
            x2 = self.shapemap[i+1][0]
            y2 = self.shapemap[i+1][1]
            x3 = self.shapemap[i+2][0]
            y3 = self.shapemap[i+2][1]
            x4 = self.shapemap[i+3][0]
            y4 = self.shapemap[i+3][1]
            #if(x1 > 0 and x1 < self.WIDTH and x2 > 0 and x2 < self.WIDTH)and(y1 > 0 and y1 < self.HEIGHT and y2 > 0 and y2 < self.HEIGHT):
            self.walls.append(Wall(self.screen, x1, x2, y1, y2))
            self.rays.append(Ray(self.screen, self.START_X, x1, self.START_Y, y1))
            #if(x2 > 0 and x2 < self.WIDTH and x3 > 0 and x3 < self.WIDTH)and(y3 > 0 and y3 < self.HEIGHT and y2 > 0 and y2 < self.HEIGHT):
            self.walls.append(Wall(self.screen, x2, x3, y2, y3))
            self.rays.append(Ray(self.screen, self.START_X, x2, self.START_Y, y2))
            #if (x4 > 0 and x4 < self.WIDTH and x3 > 0 and x3 < self.WIDTH)and(y3 > 0 and y3 < self.HEIGHT and y4 > 0 and y4 < self.HEIGHT):
            self.walls.append(Wall(self.screen, x3, x4, y3, y4))
            self.rays.append(Ray(self.screen, self.START_X, x3, self.START_Y, y3))
            #if (x1 > 0 and x1 < self.WIDTH and x4 > 0 and x4 < self.WIDTH)and(y1 > 0 and y1 < self.HEIGHT and y4 > 0 and y4 < self.HEIGHT):
            self.walls.append(Wall(self.screen, x4, x1, y4, y1))
            self.rays.append(Ray(self.screen, self.START_X, x4, self.START_Y, y4))
        #self.rays.append(Ray(self.screen, self.START_X, 0, self.START_Y, 0))
        #self.rays.append(Ray(self.screen, self.START_X, 0, self.START_Y, self.HEIGHT))
        #self.rays.append(Ray(self.screen, self.START_X, self.WIDTH, self.START_Y, 0))
        #self.rays.append(Ray(self.screen, self.START_X, self.WIDTH, self.START_Y, self.HEIGHT))
    def draw(self):
        self.screen.blit(self.bgimg, (0, 0))
        self.screen.blit(self.winimg, (300,310))
        for drawrect in self.tile_rects_draw:
            pygame.draw.rect(self.screen,(0,0,0),drawrect)
        for hazardrect in self.hazardrects_draw:
            pygame.draw.rect(self.screen,(0,0,255),hazardrect)
        for boostrect in self.boostrects_draw:
            pygame.draw.rect(self.screen,(0,255,0),boostrect)
    def update_pos(self,x,y):
        self.focus_pos_x = x
        self.focus_pos_y = y
        for ray in self.rays:
            ray.x1 = self.focus_pos_x
            ray.y1 = self.focus_pos_y
    def draw_light(self):
        poly = []
        for ray in self.rays:
            res = ray.cast(self.screen, self.walls)
            if res is not None:
                poly.append(res)
        poly = list(filter((self.focus_pos_x, self.focus_pos_y).__ne__, poly))
        if len(poly)>2:
            self.surf = pygame.Surface((self.WIDTH, self.HEIGHT))
            poly.sort(key=lambda p: arctan2(p[1] - self.focus_pos_y, p[0] - self.focus_pos_x))
            LUM = (255,0,255)
            #self.surf.set_alpha(50) #makes light an overlay
            pygame.draw.polygon(self.surf, (255, 0, 255), poly)
            if(self.won == False):
                pygame.draw.rect(self.screen,(0,0,0),(0,0,self.WIDTH,self.focus_pos_y-300))
                pygame.draw.rect(self.screen, (0, 0, 0), (0, self.focus_pos_y+300, self.WIDTH,self.HEIGHT-self.focus_pos_y-300))
                pygame.draw.rect(self.screen, (0, 0, 0), (self.focus_pos_x+300,self.focus_pos_y-300, self.WIDTH-self.focus_pos_x-300, self.HEIGHT-self.focus_pos_y+300))
                pygame.draw.rect(self.screen, (0, 0, 0), (0, self.focus_pos_y-300, self.focus_pos_x-300,self.HEIGHT-self.focus_pos_y+300))
                self.screen.blit(self.lightimg, (self.focus_pos_x-300, self.focus_pos_y-300))
                self.surf.set_colorkey(LUM)  # makes light invis
            else:
                self.surf.set_alpha(50)
            self.screen.blit(self.surf,(0,0))
    def hasWon(self,win):
        self.won = win
