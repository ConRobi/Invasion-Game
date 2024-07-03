import pygame, random, time, sys, os
from sprites import *
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.data = {'level': 2, 'map': 0}
    
    def load_imgs(self):
        self.background_imgs = [
            pygame.image.load(os.path.join("assets", "spacebg.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "black_spacebg.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "new_spacebg.png")).convert_alpha()
            ]

        self.player_imgs = [
            pygame.image.load(os.path.join("assets", "player_ufo1.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "player_ufo2.png")).convert_alpha()
        ]

        self.enemy_ufo_imgs = [
            pygame.image.load(os.path.join("assets", "enemy_ufo1.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "enemy_ufo2.png")).convert_alpha()
        ]

        self.enemy_ship_imgs = [
            pygame.image.load(os.path.join("assets", "enemy_ship1.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "enemy_ship2.png")).convert_alpha()
        ]

        self.laser_imgs = {
            "player": pygame.image.load(os.path.join("assets", "player_laser.png")).convert_alpha(),
            "enemy": pygame.image.load(os.path.join("assets", "enemy_laser.png")).convert_alpha()}
        
    
    def draw_bg(self):
        self.screen.blit(pygame.transform.scale(self.background_imgs[self.data['map']], (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
    
    def spawn_enemies(self):
        for _ in range(self.data['level'] * 2):
            to_draw.append(Enemy_Ufo((random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)), self.enemy_ufo_imgs))

        for _ in range(self.data['level']//2):
            to_draw.append(Enemy_Ship((random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)), 
                                      self.enemy_ship_imgs, random.choice(["up", "down", "left", "right"])))

    def run(self):
        """
        Game Logic: 
        - For every level there will be (2 * level) ufos and (level//2) ships.
        """

        self.load_imgs()
        self.spawn_enemies()

        player = Player(MIDDLE, self.player_imgs)
        to_draw.append(player)

        self.data['map'] = random.randint(0, 2)

        
        run = True
        while run:

            # Drawing
            self.draw_bg()
            for item in to_draw:
                if isinstance(item, Sprite):
                    item.draw(self.screen)
                    # Maybe use a lambda function to sort to_draw to handle the layers

            # Enemy Movement
            for enem in to_draw:
                if isinstance(enem, Enemy_Ufo) or isinstance(enem, Enemy_Ship):
                    enem.move(player.get_position())
            
            # Enemy shooting
            for enem in to_draw:
                if isinstance(enem, Enemy_Ship) or isinstance(enem, Enemy_Ufo):
                    enem.shoot(self.laser_imgs['enemy'])
            
            # Lasers
            for lsr in to_draw:
                if isinstance(lsr, Laser):
                    lsr.move()
                    if lsr.offscreen():
                        to_draw.remove(lsr)
            
            # Enemy_UFO collisions
            # to_draw2 = to_draw[:]
            # for enem1 in to_draw2:
            #     for enem2 in to_draw2:
            #         if enem1 is not enem2 and isinstance(enem1, Enemy_UFO) and isinstance(enem2, Enemy_UFO):
            #             if enem1.collide(enem2):
            #                 # Make one of the enemies stop moving for a second and remove the other enemy from the list clone
            #                 enem1.pause()
            #                 to_draw2.remove(enem2)
            # enemies should also explode if they contact the player

            # Laser collisions
            for lsr in to_draw:
                for x in to_draw:
                    if isinstance(lsr, Laser) and lsr.owner == player and (isinstance(x, Enemy_Ship) or isinstance(x, Enemy_Ufo)) and lsr.collide(x):
                        to_draw.remove(x)
                        to_draw.remove(lsr)
                        break

            # Key action handling
            keys = pygame.key.get_pressed()
            # Up
            if keys[pygame.K_UP] and player.get_y() - PLAYER_SPEED > 0:
                player.move(0, -PLAYER_SPEED)
            # Down
            if keys[pygame.K_DOWN] and player.get_y() + player.get_h() + PLAYER_SPEED < SCREEN_HEIGHT:
                player.move(0, PLAYER_SPEED)
            # Left
            if keys[pygame.K_LEFT] and player.get_x() - PLAYER_SPEED > 0:
                player.move(-PLAYER_SPEED, 0)
            # Right
            if keys[pygame.K_RIGHT] and player.get_x() + player.get_w() + PLAYER_SPEED < SCREEN_WIDTH:
                player.move(PLAYER_SPEED, 0)
            
            if keys[pygame.K_s]:
                player.shoot(self.laser_imgs['player'])
            if keys[pygame.K_t]:
                print(to_draw)
            
            # Quitting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
            self.clock.tick(FPS)
            pygame.display.update()

        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()