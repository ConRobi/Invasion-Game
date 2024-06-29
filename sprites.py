import pygame, time
from settings import *

class Entity:
    def __init__(self, position, images):
        self.display_size = (64,64)
        self.images = images

        # For animation
        self.anim_index = 0
        self.current_image = pygame.transform.scale(self.images[self.anim_index], self.display_size)
        self.mask = pygame.mask.from_surface(self.current_image)
        self.anim_cooldown = 0.3  # seconds
        self.last_anim_time = 0

        # For collisions
        self.mask = pygame.mask.from_surface(self.current_image)

        # For movement and positioning
        self.rect = self.current_image.get_rect(topleft = position)

        # Shooting lasers
        self.last_shot = 0

    def get_w(self):
        return self.display_size[0]
    def get_h(self):
        return self.display_size[1]
    def get_rect(self):
        return self.rect
    def get_x(self):
        return self.rect[0]
    def get_y(self):
        return self.rect[1]
    
    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
    
    def get_position(self):
        return (self.rect[0], self.rect[1])
    
    def set_position(self, position):
        self.rect.topleft = position
    
    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.current_image, self.display_size), self.rect)

    def animate(self, curr_time):
        if curr_time - self.last_anim_time >= self.anim_cooldown:
            self.anim_index = (self.anim_index + 1) % len(self.images)
            self.current_image = pygame.transform.scale(self.images[self.anim_index], self.display_size)
            self.mask = pygame.mask.from_surface(self.current_image)
            self.last_anim_time = curr_time
    
    def collide(self, other):
        if isinstance(other, Entity):
            if other.mask.overlap(self.mask, (self.rect[0] - other.rect[0], self.rect[1] - other.rect[1])):
                return True
            else:
                return False
        else:
            raise Exception("Error: This method is only for use between entities!")
    
    def offscreen(self):
        return self.rect[0] < 0 or self.rect[0] > SCREEN_WIDTH or self.rect[1] < 0 or self.rect[1] > SCREEN_HEIGHT
    
    def shot_cooldown(self, cooldown_time):
        cur = time.time()
        if cur - self.last_shot >= cooldown_time:
            self.last_shot = cur
            return True
        else:
            return False

class Player(Entity):
    def __init__(self, position, images):
        super().__init__(position, images)
        self.shot_cooldown = 0.5  # Seconds
        self.last_shot_time = 0
    
    def shoot_lasers(self, curr_time, images):
        if curr_time - self.last_shot_time >= self.shot_cooldown:
            self.last_shot_time = curr_time
            lasers = [Laser(self.get_position(), images, "left"), Laser(self.get_position(), images, "right")]
            return lasers
        else:
            return []

class Enemy_Ship(Entity):
    def __init__(self, position, images, direction):
        if direction not in ("up", "down", "left", "right"):
            raise Exception("Error: Invalid ship direction chosen!")
        super().__init__(position, images)
        self.direction = direction
        self.on_screen = False
        self.images = images[:]  # Make clones of lists to not change og list?
        
        self.navigation = {
            # Pygame rotation happens counter-clockwise -> reasoning behind angle
            "up": {"angle": 270, "move": (0, -ENEMY_SHIP_SPEED)},
             "down": {"angle": 90, "move": (0, ENEMY_SHIP_SPEED)},
             "left": {"angle": 0, "move": (-ENEMY_SHIP_SPEED, 0)},
             "right": {"angle": 180, "move": (ENEMY_SHIP_SPEED, 0)}
             }

        for i in range(len(images)):
            self.images[i] = pygame.transform.rotate(self.images[i], self.navigation[direction]["angle"])
    
    def move(self, player_pos):
        # Coordinates for ship to spawn lined up with the player
        nav = {
            "up": (player_pos[0], SCREEN_HEIGHT),
            "down": (player_pos[0], 0),
            "left": (SCREEN_WIDTH, player_pos[1]),
            "right": (0, player_pos[1])
        }
        if self.on_screen == False:
            self.set_position(nav[self.direction])
            self.on_screen = True
        if self.offscreen():
            self.on_screen = False
        super().move(*self.navigation[self.direction]["move"])
    
    def shoot(self, laser_imgs):
        if self.shot_cooldown(1):
            if self.direction in ("up", "down"):
                lsrs = [Laser(self.get_position(), laser_imgs[:], "left"), Laser(self.get_position(), laser_imgs[:], "right")]
                to_draw.extend(lsrs)
            elif self.direction in ("left", "right"):
                flipped = [pygame.transform.rotate(i, 90) for i in laser_imgs[:]]
                lsrs = [Laser(self.get_position(), flipped, "up"), Laser(self.get_position(), flipped, "down")]
                to_draw.extend(lsrs)


class Enemy_UFO(Entity):
    def __init__(self, position, images, type):
        valid_types = ("ufo", "ship")
        if type not in valid_types:
            raise Exception("Error: Invalid enemy type chosen!")
        super().__init__(position, images)
        self.type = type
        self.can_move = True
        self.pause_time = 0
        if type == "ship":
            self.active = False
    
    def enemy_move(self, position):
        if self.type == "ufo":
            dx, dy = 0, 0
            if self.rect[0] < position[0]:  # left of player
                dx = ENEMY_SPEED
            elif self.rect[0] > position[0]:  # right of player
                dx = -ENEMY_SPEED
            if self.rect[1] < position[1]:  # above player
                dy = ENEMY_SPEED
            elif self.rect[1] > position[1]:  # below player
                dy = -ENEMY_SPEED
            super().move(dx, dy)
        elif self.type == "ship":
            pass

    def pause(self):
        self.pause_time = time.time()
        self.can_move = False
    
    def try_resume(self):
        if time.time() - self.pause_time >= 0.2:
            self.can_move = True
    
    def shoot(self, laser_imgs):
        pass

class Laser(Entity):
    def __init__(self, position, images, direction):
        valid_directions = ("up", "down", "left", "right")
        if direction not in valid_directions:
            raise Exception("Error: Invalid directions chosen!")
        super().__init__(position, images)
        self.display_size = (32, 32)
        self.direction = direction
    
    def move(self):
        if self.direction == "up":
            super().move(0, -LASER_SPEED)
        elif self.direction == "down":
            super().move(0, LASER_SPEED)
        elif self.direction == "left":
            super().move(-LASER_SPEED, 0)
        elif self.direction == "right":
            super().move(LASER_SPEED, 0)