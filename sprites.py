import pygame

block_s = 25


class GameObj(pygame.sprite.Sprite):
    def __init__(self, pos, dim, color):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface(dim)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.set_pos(pos)

    def set_pos(self, pos):
        self.pos = pos
        self.rect.topleft = pos


class Player(GameObj):
    def __init__(self, pos, dim, color, objs):

        self.objs = objs
        super().__init__(pos, dim, color)
        while self.collided(self.objs):
            self.set_pos([self.pos[0] + block_s, self.pos[1]])

    def move(self, dir, mag):
        self.set_pos([self.pos[0] + dir[0] * mag, self.pos[1] + dir[1] * mag])

    def set_pos(self, pos):
        copy = self.pos[:]
        super().set_pos(pos)
        if self.collided(self.objs):
            super().set_pos(copy)

    def collided(self, objs):
        """Returns True if the player colides with an object, False otherwise"""
        for obj in objs:
            if obj.rect.colliderect(self.rect):
                return True
        return False


class Gold(GameObj):
    def __init__(self, pos, dim):
        super().__init__(pos, dim, 'yellow')

    def collision(self, group):
        return  pygame.sprite.spritecollide(self, group, False)
