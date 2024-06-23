import pygame, random, time, sys

class Game:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
    
    def run(self):

        to_draw = []

        run = True
        while run:

            # Quitting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
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

        
        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()