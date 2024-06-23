import pygame

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

    def get_w(self):
        return self.display_size[0]
    def get_h(self):
        return self.display_size[1]
    def get_rect(self):
        return self.rect
    
    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
    
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

class Player(Entity):
    def __init__(self, position, images):
        super().__init__(position, images)

class Enemy(Entity):
    def __init__(self, position, images):
        super().__init__(position, images)
        self.last = 0
        self.can_move = True
    
    def move(self, position, speed):
        dx, dy = 0, 0
        if self.rect[0] < position[0]:  # left of player
            dx = speed
        elif self.rect[0] > position[0]:  # right of player
            dx = -speed
        if self.rect[1] < position[1]:  # above player
            dy = speed
        elif self.rect[1] > position[1]:  # below player
            dy = -speed
        super().move(dx, dy)
    
    # String representation of object for debugging
    def __repr__(self) -> str:
        return "Enemy object"