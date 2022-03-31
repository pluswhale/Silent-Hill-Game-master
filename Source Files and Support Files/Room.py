import pygame, random


class Collectibles(pygame.sprite.Sprite):
    # This is a parent function for all collectibles that the user is get.

    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = 2
        self.image = image
        self.updateRect()

    def updateRect(self):
        # All updateRect() methods were adapted from Lukas' asteroids example
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x, self.y, w, h)

    def update(self):
        self.updateRect()


class Health(Collectibles):

    def __init__(self, x, y):
        # health potion class inheriting from Collectibles
        healthImage = pygame.transform.scale(pygame.image.load
                                             ("roomFeatures/healthPotion.png").convert_alpha(), (15, 40))
        super().__init__(x, y, healthImage)


class Sanity(Collectibles):

    def __init__(self, x, y):
        # sanity potion class inheriting from collectibles
        width, height = 15, 40
        sanityImage = pygame.transform.scale(pygame.image.load
                                             ("roomFeatures/sanityPotion.png").convert_alpha(), (width, height))
        super().__init__(x, y, sanityImage)


class Gold(Collectibles):

    def __init__(self, x, y):
        # gold class inheriting from the collectibles class
        size = 40
        goldImage = pygame.transform.scale(pygame.image.load
                                           ('roomFeatures/gold.png').convert_alpha(), (size, size))
        super().__init__(x, y, goldImage)


class Ammo(Collectibles):

    def __init__(self, x, y):
        # ammo class inheriting from the Collectibles class
        width, height = 10, 25
        ammoImage = pygame.transform.scale(pygame.image.load
                                           ("roomFeatures/ammo.png").convert_alpha(), (width, height))
        super().__init__(x, y, ammoImage)


class Monster(pygame.sprite.Sprite):
    time = 0

    def monsterInit(self):
        # all animation pngs that will be cycled through in the update function
        self.rightEnemy = ['pyramidHead/right1.png', 'pyramidHead/right2.png',
                           'pyramidHead/right3.png', 'pyramidHead/right4.png']
        self.leftEnemy = ['pyramidHead/left1.png', 'pyramidHead/left2.png',
                          'pyramidHead/left3.png', 'pyramidHead/left4.png']
        self.upEnemy = ['pyramidHead/up1.png', 'pyramidHead/up2.png',
                        'pyramidHead/up3.png', 'pyramidHead/up4.png']
        self.downEnemy = ['pyramidHead/down1.png', 'pyramidHead/down2.png',
                          'pyramidHead/down3.png', 'pyramidHead/down4.png']

    def __init__(self, width, height, life):
        super().__init__()
        self.monsterInit()
        self.width, self.height = width, height
        self.x = self.width - 100
        self.y = random.randrange(70, self.height - 100)
        self.currDir = 'left'
        self.move = (-4, 0)
        self.radius = 10
        self.life = life
        self.leftCount, self.rightCount = 0, 0
        self.upCount, self.downCount = 0, 0
        self.leftBound, self.rightBound = 180, self.width - 51
        self.upBound, self.downBound = 20, self.height - 50
        self.sizeX, self.sizeY = 40, 50
        self.image = pygame.transform.scale(pygame.image.load
                                            (self.leftEnemy[self.leftCount % len(self.leftEnemy)]).
                                            convert_alpha(), (self.sizeX, self.sizeY))
        self.overlap = False
        self.updateRect()

    def updateRect(self):
        # constantly update the rect around the image
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x, self.y, w, h)

    def moveLeft(self):
        # cycle through the pngs moving left
        self.image = pygame.transform.scale(pygame.image.load
                                            (self.leftEnemy[self.leftCount % len(self.leftEnemy)]).
                                            convert_alpha(), (self.sizeX, self.sizeY))
        self.leftCount += 1

    def moveRight(self):
        # cycle through the pngs moving right
        self.image = pygame.transform.scale(pygame.image.load
                                            (self.rightEnemy[self.rightCount % len(self.rightEnemy)]).
                                            convert_alpha(), (self.sizeX, self.sizeY))
        self.rightCount += 1

    def moveUp(self):
        # cycle through the pngs moving up
        self.image = pygame.transform.scale(pygame.image.load
                                            (self.upEnemy[self.upCount % len(self.upEnemy)]).
                                            convert_alpha(), (self.sizeX, self.sizeY))
        self.upCount += 1

    def moveDown(self):
        # cycle through the pngs moving down
        self.image = pygame.transform.scale(pygame.image.load
                                            (self.downEnemy[self.downCount % len(self.downEnemy)]).
                                            convert_alpha(), (self.sizeX, self.sizeY))
        self.downCount += 1

    def outOfBounds(self, x, y):
        # make sure the monsters don't go out of bounds
        width, height = self.image.get_size()
        if (x < self.leftBound or x + width > self.rightBound or
                y < self.upBound or y + height > self.downBound):
            return True
        else:
            return False

    def update(self):
        # constant update movement
        if self.currDir == 'left':
            self.moveLeft()
        elif self.currDir == 'right':
            self.moveRight()
        elif self.currDir == 'up':
            self.moveUp()
        elif self.currDir == 'down':
            self.moveDown()
        dx, dy = self.move
        # make sure not overlapping with other monsters
        # or not going out of bounds
        if (self.overlap == False and
                self.outOfBounds(self.x + dx, self.y + dy) == False):
            self.x += dx
            self.y += dy
        self.updateRect()


class Room(object):
    length = 100

    def healthInit(self):
        self.healthGroup = pygame.sprite.Group()
        self.numHealth = random.randint(0, 2)  # random number of potions
        for health in range(self.numHealth):
            x = random.randrange(self.leftBound, self.rightBound)
            y = random.randrange(self.upBound, self.downBound)
            self.healthGroup.add(Health(x, y))

    def sanityInit(self):
        self.sanityGroup = pygame.sprite.Group()
        self.numSanity = random.randint(0, 1)  # random number of sanity
        for sanity in range(self.numSanity):
            x = random.randrange(self.leftBound, self.rightBound)
            y = random.randrange(self.upBound, self.downBound)
            self.sanityGroup.add(Sanity(x, y))

    def goldInit(self):
        self.goldGroup = pygame.sprite.Group()
        self.numGold = random.randint(2, 5)  # random number of gold
        for gold in range(self.numGold):
            x = random.randrange(self.leftBound, self.rightBound)
            y = random.randrange(self.upBound, self.downBound)
            self.goldGroup.add(Gold(x, y))

    def ammoInit(self):
        self.ammoGroup = pygame.sprite.Group()
        self.numAmmo = random.randint(0, 2)  # random number of ammo
        for ammo in range(self.numAmmo):
            x = random.randrange(self.leftBound, self.rightBound)
            y = random.randrange(self.upBound, self.downBound)
            self.ammoGroup.add(Ammo(x, y))

    def __init__(self, width, height, background):
        # The attributes of each room include spawning monsters, potions,
        # ammo, and gold. These objects belong to the room, not the game class.
        # Each room has its own instance of a room.
        self.width, self.height = width, height
        self.leftBound, self.rightBound = self.width // 3, self.width - 90
        self.upBound, self.downBound = 90, self.height - 90
        self.monstersGroup = pygame.sprite.Group()
        self.wallsGroup = pygame.sprite.Group()
        self.background = background
        self.leftSide = 125
        self.healthInit()
        self.sanityInit()
        self.goldInit()
        self.ammoInit()

    def drawObjs(self, screen):
        screen.blit(self.background, (self.leftSide, -1))
        # need to put -1 for top left Y because a pygame bug messed up my
        # background png for the first row of pixels
        self.healthGroup.draw(screen)
        self.sanityGroup.draw(screen)
        self.ammoGroup.draw(screen)
        self.goldGroup.draw(screen)
        self.wallsGroup.draw(screen)
