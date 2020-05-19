from numpy import cos,sin,square,sqrt,arctan2,pi
import pygame


class Ray:
    def __init__(self, screen, x1, x2, y1, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def cast(self, screen, walls):
        pots = []
        distlist = []
        for wall in walls:
                # denominator
                den = ((self.x1 - self.x2) * (wall.y1 - wall.y2)) - ((self.y1 - self.y2) * (wall.x1 - wall.x2))
                # numerator
                num = ((self.x1 - wall.x1) * (wall.y1 - wall.y2)) - ((self.y1 - wall.y1) * (wall.x1 - wall.x2))
                if den != 0:
                    t = num / den
                    u = (-((self.x1 - self.x2) * (self.y1 - wall.y1) - (self.y1 - self.y2) * (self.x1 - wall.x1))) / den
                    if t > 0 and t < 1 and u > 0 and u < 1:
                        pot= (self.x1 + t * (self.x2 - self.x1), self.y1 + t * (self.y2 - self.y1))
                        dist = sqrt(square(self.x1 - pot[0]) + square(self.y1 - pot[1]))
                        pots.append(pot)
                        distlist.append(dist)
        if len(pots) > 0:
            pt = pots[distlist.index(min(distlist))]
            #pygame.draw.line(screen, (255, 255, 255), (self.x1, self.y1), (pt[0], pt[1]), 2)
            return pt
        else:
        #elif sqrt(square(self.x1-self.x2)+square(self.y1-self.y2)) <= 300:
            #pygame.draw.line(screen, (255, 255, 255), (self.x1, self.y1), (self.x2, self.y2), 2)
            return (self.x2, self.y2)
        #else:
        #    return None
            '''opp = self.y2-self.y1
            adj = self.x2-self.x1
            if adj == 0 and self.y2 > self.y1:
                arc = pi/2
            elif adj == 0 and self.y2 < self.y1:
                arc = -pi/2
            else:
                arc = arctan2(opp,adj)
            #pygame.draw.line(screen, (255, 255, 255), (self.x1, self.y1), (self.x1+400*cos(arc), self.y1+400*sin(arc)), 2)
            return (self.x1+400*cos(arc), self.y1+400*sin(arc))'''