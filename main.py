import pygame, random, time, sys, os
# from images import *
from sprites import Player, Enemy, Entity

class Game:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.fps = 60
    
    def load_imgs(self):
        self.background_imgs = [
            pygame.image.load(os.path.join("assets", "spacebg.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "black_spacebg.png")).convert_alpha()
            ]

        self.player_imgs = [
            pygame.image.load(os.path.join("assets", "player_ufo1.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "player_ufo2.png")).convert_alpha()
        ]

        self.enemy_ufo_imgs = [
            pygame.image.load(os.path.join("assets", "enemy_ufo1.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "enemy_ufo2.png")).convert_alpha()
        ]

        self.enemy_spawner_imgs = [
            pygame.image.load(os.path.join("assets", "enemy_spawner1.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "enemy_spawner2.png")).convert_alpha()
        ]
        

    def run(self):
        self.load_imgs()

        # To start
        level = 1
        to_draw = []
        for _ in range(3):
            to_draw.append(Enemy((0, 0), self.enemy_ufo_imgs))

        run = True
        while run:

            # Quitting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            # Drawing and animating
            self.screen.blit(pygame.transform.scale(self.background_imgs[1], (self.screen_width, self.screen_height)), (0, 0))
            for x in to_draw:
                pass
            
            # Key action handling
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                pass
            if keys[pygame.K_DOWN]:
                pass
            if keys[pygame.K_LEFT]:
                pass
            if keys[pygame.K_RIGHT]:
                pass
            
            self.clock.tick(self.fps)
            pygame.display.update()

        
        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()