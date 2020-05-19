from player import *
from level import *
from enemy import *
from prox import *
import os

START_X = 30
START_Y = 590
WIDTH = 1120
HEIGHT = 630
SCREEN = (WIDTH, HEIGHT)
class Display:
    def __init__(self):
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = '0,20'
        self.screen = pygame.display.set_mode(SCREEN)
        pygame.display.set_caption("Tiny Object Simulator","TOS")
        self.level_map = Level(self.screen,WIDTH,HEIGHT,START_X,START_Y)
        self.enemies = []
        self.enemies.append(Enemy(self.screen, self.level_map.tile_rects, self.level_map, 760,600, self.level_map.hazardrects, self.level_map.boostrects))
        self.enemies.append(Enemy(self.screen, self.level_map.tile_rects, self.level_map, 80, 150, self.level_map.hazardrects,self.level_map.boostrects))
        self.enemies.append(Enemy(self.screen, self.level_map.tile_rects, self.level_map, 700, 20, self.level_map.hazardrects,self.level_map.boostrects))
        self.player = Player(self.screen,self.level_map.tile_rects,self.level_map,START_X,START_Y,self.level_map.winrect,self.level_map.hazardrects,self.level_map.boostrects,self.enemies)
        self.stopgame = False
        self.clock = pygame.time.Clock()
        pygame.mixer.music.load('music/falling_sun.mp3')
        pygame.mixer.music.play(-1)
        self.prox = Prox()
    def draw(self,screen):
        self.level_map.draw()
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        self.level_map.draw_light()
        font = pygame.font.SysFont(None, 20)
        img = font.render("Units Traveled:", True, (255, 0, 0))
        units_traveled = self.player.getunits()
        screen.blit(img, (110, 570))
        img2 = font.render(str(int(units_traveled)) + " Units", True, (255, 255, 255))
        screen.blit(img2, (110, 590))

    def run(self):
        while not self.stopgame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stopgame = True
            key = pygame.key.get_pressed()  # checking pressed keys
            self.player.runmovement(key)
            for enemy in self.enemies:
                enemy.runmovement()
            self.draw(self.screen)
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                font = pygame.font.SysFont(None, 24)
                img = font.render('x:' + str(pos[0]) + ',y:' + str(pos[1]), True, (255, 200, 120))
                self.screen.blit(img, (pos[0], pos[1]))
            self.clock.tick(60)
            self.level_map.hasWon(self.player.wongame)
            self.prox.get_pos(self.player.player_rect.center)
            self.prox.get_info(self.enemies)
            pygame.display.update()


if __name__ == '__main__':
    D = Display()
    D.run()