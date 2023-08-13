import pygame, sys
from utils.colors import *

class Paint:

    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.pos = list()

        self.click = False
        self.drawing_started = False
        self.linePos = list()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.click = False

    def logics(self):
        self.mpos = pygame.mouse.get_pos()
        # Si el usuario hace clic por primera vez, agrega (0,0) a la lista
        if self.click:
            self.linePos.append(self.mpos)
        else:
            self.linePos = list()
        
        if self.linePos: self.pos.append(self.linePos)
        

    def draw(self):
        self.screen.fill(WHITE)
        for line in self.pos:
            for i,p in enumerate(line):
                #pygame.draw.circle(self.screen, RED, p, 3)
                if i+1 < len(line):


                    pygame.draw.line(self.screen, GREEN, p, line[i+1], 3)

    def run(self):
        while True:
            self.events()

            self.logics()

            self.draw()

            pygame.display.flip()
            self.clock.tick(60)


Paint().run()