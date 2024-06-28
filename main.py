import pygame, random, time, sys, os
from sprites import Player, Enemy, Entity, Laser, Ship
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
    
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

        self.enemy_ship_imgs = [
            pygame.image.load(os.path.join("assets", "enemy_ship1.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "enemy_ship2.png")).convert_alpha()
        ]

        self.enemy_spawner_imgs = [
            pygame.image.load(os.path.join("assets", "enemy_spawner1.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "enemy_spawner2.png")).convert_alpha()
        ]

        self.laser_imgs = [
            pygame.image.load(os.path.join("assets", "player_laser.png")).convert_alpha()
        ]
        
    def run(self):
        self.load_imgs()

        player = Player((SCREEN_WIDTH//2, SCREEN_HEIGHT//2), self.player_imgs)
        to_draw = [player]
        for _ in range(4):
            to_draw.append(Enemy((random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)), self.enemy_ufo_imgs, "ufo"))
        # to_draw.append(Ship((SCREEN_WIDTH - 100, SCREEN_HEIGHT//2), self.enemy_ship_imgs))
            # to_draw.append(Enemy((random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)), self.enemy_ufo_imgs),)
        # for _ in range(3):
        #     to_draw.append(Enemy((random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)), self.enemy_ship_imgs))
        
        # to_draw.append(Enemy((30, 30), self.enemy_spawner_imgs))

        lt = 0
        run = True
        while run:

            # Quitting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            current_time = time.time()
            
            # Drawing and animating
            self.screen.blit(pygame.transform.scale(self.background_imgs[0], (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
            for x in to_draw:
                if isinstance(x, Entity):
                    x.draw(self.screen)
                    x.animate(current_time)

            # Enemy Movement
            for enem in to_draw:
                if isinstance(enem, Enemy):
                    if enem.can_move:
                        enem.enemy_move(player.get_rect())
                    else:
                        enem.resume()
                if isinstance(enem, Ship):
                    enem.move()

            for x in to_draw:
                if isinstance(x, Laser):
                    x.move(LASER_SPEED)
                    x.offscreen()
            
            # Enemy collisions
            to_draw2 = to_draw[:]
            for enem1 in to_draw2:
                for enem2 in to_draw2:
                    if enem1 is not enem2 and isinstance(enem1, Enemy) and isinstance(enem2, Enemy):
                        if enem1.collide(enem2):
                            # Make one of the enemies stop moving for a second and remove the other enemy from the list clone
                            enem1.pause()
                            to_draw2.remove(enem2)
            # enemies should also explode if they contact the player

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
            # Space
            if keys[pygame.K_SPACE]:
                # to_draw.extend(player.shoot_lasers(current_time, self.laser_imgs))
                if current_time - lt >= 1:
                    to_draw.append(Ship((SCREEN_WIDTH - 100, SCREEN_HEIGHT//2), self.enemy_ship_imgs, "up"))
                    lt = current_time
                
            self.clock.tick(FPS)
            pygame.display.update()

        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()