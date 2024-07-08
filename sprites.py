import pygame, time
from settings import *

""" Other functions """
def check_direction(direction):
    if direction not in ("up", "down", "left", "right"):
        raise Exception("Error: Invalid direction chosen!")

""" Classes """
class Sprite:
    def __init__(self, position: tuple, image):
        self.display_size = (32,32)
        self.current_img = image
        self.mask = pygame.mask.from_surface(self.current_img)
        self.rect = self.current_img.get_rect(topleft = position)
    
    def get_w(self):
        return self.display_size[0]
    
    def get_h(self):
        return self.display_size[1]
    
    def get_x(self):
        return self.rect[0]
    
    def get_y(self):
        return self.rect[1]
    
    def get_position(self):
        return (self.rect[0], self.rect[1])
    
    def set_position(self, position):
        self.rect.topleft = position

    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.current_img, self.display_size), self.rect)

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)

    def collide(self, other):
        if isinstance(other, Sprite):
            if other.mask.overlap(self.mask, (self.rect[0] - other.rect[0], self.rect[1] - other.rect[1])):
                return True
            else:
                return False
        else:
            raise Exception("Error: This method is only for use between Sprite objects!")

    def offscreen(self):
        return (self.rect[0] + self.get_w()) < 0 or self.rect[0] > SCREEN_WIDTH or (self.rect[1] + self.get_h()) < 0 or self.rect[1] > SCREEN_HEIGHT

class Entity(Sprite):
    def __init__(self, position: tuple, images):
        self.anim_index = 0
        self.anim_cooldown = 0.3  # Seconds
        self.last_anim_time = 0
        self.images = images[:]  # A copy so the original list isn't changed
        super().__init__(position, image=self.images[self.anim_index])

        self.display_size = (64,64)
        self.last_shot_time = 0
    
    def animate(self):
        ct = time.time()  # Current time
        if ct - self.last_anim_time >= self.anim_cooldown:
            self.anim_index = (self.anim_index + 1) % len(self.images)
            self.current_img = pygame.transform.scale(self.images[self.anim_index], self.display_size)
            self.mask = pygame.mask.from_surface(self.current_img)
            self.last_anim_time = ct
    
    def test(self, screen):
        for i in range(len(self.images)):
            screen.blit(pygame.transform.scale(self.images[i], self.display_size), (64 * i, 400))

    def shot_cooldown(self, cooldown_time):
        cur = time.time()
        if cur - self.last_shot_time >= cooldown_time:
            self.last_shot_time = cur
            return True
        else:
            return False

class Player(Entity):
    def __init__(self, position: tuple, images, health = 100):
        super().__init__(position, images)
        self.max_health = health
        self.current_health = health

    def shoot(self, laser_img):
        if self.shot_cooldown(0.5):
            for direction in ("up", "down", "left", "right"):
                to_draw.append(Laser(self.get_position(), laser_img, direction, self))

class Laser(Sprite):
    def __init__(self, position: tuple, image, direction: str, owner = None):
        super().__init__(position, image)
        check_direction(direction)
        self.direction = direction
        self.owner = owner
        if self.direction in ("up", "down"):
            self.current_img = pygame.transform.rotate(self.current_img, 90)
    
    def move(self):
        x = {"up": (0, -LASER_SPEED), "down": (0, LASER_SPEED), "left": (-LASER_SPEED, 0), "right": (LASER_SPEED, 0)}
        super().move(*x[self.direction])

""" Enemies (Movement based on player position) """

class Enemy_Ship(Entity):
    def __init__(self, position: tuple, images, direction):
        super().__init__(position, images)
        check_direction(direction)
        self.direction = direction

        # Angle to rotate ship image (is currently facing left)
        x = {"up": 270, "down": 90, "left": 0, "right": 180}
        self.images = [pygame.transform.rotate(i, x[self.direction]) for i in self.images]
            
    def move(self, player_pos):
        # Coordinates for ship to spawn lined up with the player
        spawn = {"up": (player_pos[0], SCREEN_HEIGHT), "down": (player_pos[0], 0), "left": (SCREEN_WIDTH, player_pos[1]),"right": (0, player_pos[1])}
        to = {"up": (0, -ENEMY_SHIP_SPEED), "down": (0, ENEMY_SHIP_SPEED), "left": (-ENEMY_SHIP_SPEED, 0), "right": (ENEMY_SHIP_SPEED, 0)}
        if self.offscreen():
            self.set_position(spawn[self.direction])
        super().move(*to[self.direction])
    
    def shoot(self, laser_img):
        if self.shot_cooldown(1):
            if self.direction in ("up", "down"):
                lsrs = [Laser(self.get_position(), laser_img, "left"), Laser(self.get_position(), laser_img, "right")]
                to_draw.extend(lsrs)
            elif self.direction in ("left", "right"):
                lsrs = [Laser(self.get_position(), laser_img, "up"), Laser(self.get_position(), laser_img, "down")]
                to_draw.extend(lsrs)

class Enemy_Ufo(Entity):
    def __init__(self, position: tuple, images):
        super().__init__(position, images)
        self.can_move = True
        self.last_pause_time = 0
    
    def move(self, player_pos):
        if self.can_move:
            dx, dy = 0, 0
            if self.rect[0] < player_pos[0]:  # left of player
                dx = ENEMY_UFO_SPEED
            elif self.rect[0] > player_pos[0]:  # right of player
                dx = -ENEMY_UFO_SPEED
            if self.rect[1] < player_pos[1]:  # above player
                dy = ENEMY_UFO_SPEED
            elif self.rect[1] > player_pos[1]:  # below player
                dy = -ENEMY_UFO_SPEED
            super().move(dx, dy)

    def pause(self):
        self.last_pause_time = time.time()
        self.can_move = False
    
    def try_resume(self):
        if time.time() - self.last_pause_time >= 0.2:
            self.can_move = True
    
    def shoot(self, laser_img, player_pos):
            if self.shot_cooldown(2):
                lsrs = []
                if self.rect[0] < player_pos[0]:  # left of player
                    lsrs.append(Laser(self.get_position(), laser_img, "right"))
                if self.rect[0] > player_pos[0]:  # right of player
                    lsrs.append(Laser(self.get_position(), laser_img, "left"))
                elif self.rect[1] < player_pos[1]:  # above player
                    lsrs.append(Laser(self.get_position(), laser_img, "down"))
                elif self.rect[1] > player_pos[1]:  # below player
                    lsrs.append(Laser(self.get_position(), laser_img, "up"))
                to_draw.extend(lsrs)