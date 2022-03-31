import pygame

class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, image, life, wallType):
        super().__init__()
        # parent wall class for building walls
        self.x, self.y = x, y
        self.width, self.height = 22, 27
        self.image = image
        self.life = life
        self.radius = self.width // 2
        self.wallType = wallType
        self.prevHit = 0
        self.updateRect()

    def updateRect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class FirstWall(Wall):

    def __init__(self, x, y):
        # inherits from the main wall Parent class
        # this is the cheapest wall
        sizeX, sizeY = 22, 27
        wall1 = pygame.transform.scale(pygame.image.load
            ('Walls/wall1.png').convert_alpha(), (sizeX, sizeY))
        life1 = 10
        super().__init__(x, y, wall1, life1, 'wall1')

class SecondWall(Wall):

    def __init__(self, x, y):
        # inherits from the main wall Parent class
        # this is the second cheapest wall
        sizeX, sizeY = 22, 27
        wall2 = pygame.transform.scale(pygame.image.load
            ('Walls/wall2.png').convert_alpha(), (sizeX, sizeY))
        life2 = 20
        super().__init__(x, y, wall2, life2, 'wall2')

class ThirdWall(Wall):

    def __init__(self, x, y):
        # inherits from the main wall Parent class
        # this is the most expensive wall
        sizeX, sizeY = 22, 27
        wall3 = pygame.transform.scale(pygame.image.load
            ('Walls/wall3.png').convert_alpha(), (sizeX, sizeY))
        life3 = 50
        super().__init__(x, y, wall3, life3, 'wall3')
