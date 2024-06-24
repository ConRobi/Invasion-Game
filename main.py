import pygame, random, time, sys, os
from sprites import Player, Enemy, Entity, Laser

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.player_speed = 7
        self.enemy_speed = 2
        self.laser_speed = 5
    
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

        self.laser_imgs = [
            pygame.image.load(os.path.join("assets", "player_laser.png")).convert_alpha()
        ]
        
    def run(self):
        self.load_imgs()

        # To start
        player = Player((self.screen_width//2, self.screen_height//2), self.player_imgs)
        to_draw = [player]
        for _ in range(3):
            to_draw.append(Enemy((random.randint(0, self.screen_width), random.randint(0, self.screen_height)), self.enemy_ufo_imgs))
        to_draw.append(Enemy((30, 30), self.enemy_spawner_imgs))

        run = True
        while run:

            # Quitting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            current_time = time.time()
            
            # Drawing and animating
            self.screen.blit(pygame.transform.scale(self.background_imgs[1], (self.screen_width, self.screen_height)), (0, 0))
            for x in to_draw:
                if isinstance(x, Entity):
                    x.draw(self.screen)
                    x.animate(current_time)
                if isinstance(x, Laser):
                    x.move(self.laser_speed)
            
            for enem in to_draw:
                if isinstance(enem, Enemy):
                    if enem.can_move:
                        enem.move(player.get_rect(), self.enemy_speed)

            # Key action handling
            keys = pygame.key.get_pressed()
            # Up
            if keys[pygame.K_UP] and player.get_y() - self.player_speed > 0:
                player.move(0, -self.player_speed)
            # Down
            if keys[pygame.K_DOWN] and player.get_y() + player.get_h() + self.player_speed < self.screen_height:
                player.move(0, self.player_speed)
            # Left
            if keys[pygame.K_LEFT] and player.get_x() - self.player_speed > 0:
                player.move(-self.player_speed, 0)
            # Right
            if keys[pygame.K_RIGHT] and player.get_x() + player.get_w() + self.player_speed < self.screen_width:
                player.move(self.player_speed, 0)
            # Space
            if keys[pygame.K_SPACE]:
                to_draw.extend(player.shoot_lasers(current_time, self.laser_imgs))
                
            self.clock.tick(self.fps)
            pygame.display.update()

        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()