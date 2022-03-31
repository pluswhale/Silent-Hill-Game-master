import pygame

class Bullet(pygame.sprite.Sprite):

    def bulletInit(self):
        self.rightBullet = 'Bullets/bulletRight.png'
        self.leftBullet = 'Bullets/bulletLeft.png'
        self.upBullet = 'Bullets/bulletUp.png'
        self.downBullet = 'Bullets/bulletDown.png'

    def __init__(self, x, y, direction):
        super().__init__()
        self.bulletInit()
        self.direction = direction
        width, height = 30, 20
        if self.direction == 'right':
            self.image = pygame.transform.scale(pygame.image.load
                (self.rightBullet).convert_alpha(), (width, height))
        elif self.direction == 'left':
            self.image = pygame.transform.scale(pygame.image.load
                (self.leftBullet).convert_alpha(), (width, height))
        elif self.direction == 'up':
            self.image = pygame.transform.scale(pygame.image.load
                (self.upBullet).convert_alpha(), (width, height))
        elif self.direction == 'down':
            self.image = pygame.transform.scale(pygame.image.load
                (self.downBullet).convert_alpha(), (width, height))
        self.x, self.y = x, y
        self.bulletVel = 20
        self.updateRect()

    def updateRect(self):
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x, self.y, w, h)

    def update(self):
        if self.direction == 'right': self.x += self.bulletVel
        elif self.direction == 'left': self.x -= self.bulletVel
        elif self.direction == 'up': self.y -= self.bulletVel
        elif self.direction == 'down': self.y += self.bulletVel
        self.updateRect()
