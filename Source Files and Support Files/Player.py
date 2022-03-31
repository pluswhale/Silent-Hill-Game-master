import pygame

class Player(pygame.sprite.Sprite):

    def imagesInit(self):
        # cycle through these animations to make it look like it's moving
        self.rightImages = ['Right/right1.png', 'Right/right2.png',
                            'Right/right3.png', 'Right/right4.png']
        self.rightCount = 0
        self.shootRight = 'Right/rightShooting.png'
        self.leftImages = ['Left/left1.png', 'Left/left2.png',
                           'Left/left3.png', 'Left/left4.png']
        self.leftCount = 0
        self.shootLeft = 'Left/leftShooting.png'
        self.upImages = ['Up/up1.png', 'Up/up2.png', 'Up/up3.png', 'Up/up4.png']
        self.upCount = 0
        self.shootUp = 'Up/upShooting.png'
        self.downImages = ['Down/down1.png', 'Down/down2.png',
                           'Down/down3.png', 'Down/down4.png']
        self.downCount = 0
        self.shootDown = 'Down/downShooting.png'

    def __init__(self, x, y, width, height):
        super().__init__()
        self.imagesInit()
        self.x = x
        self.y = y
        self.width, self.height = width, height
        self.leftBound, self.rightBound = 180, self.width - 51
        self.upBound, self.downBound = 20, self.height - 50
        self.currDir = 'right'
        self.dx, self.dy = 0, 0
        self.size = 50
        self.image = pygame.transform.scale(pygame.image.
            load(self.rightImages[self.rightCount]).convert_alpha(),
            (self.size, self.size))
        self.firing = False
        self.hit = False
        self.overlap = False
        self.updateRect()

    def firingImgs(self):
        # shooting images depending on which direction the player is looking in
        if self.currDir == 'right':
            self.image = pygame.transform.scale(pygame.image.
                load(self.shootRight).convert_alpha(), (self.size, self.size))
        elif self.currDir == 'left':
            self.image = pygame.transform.scale(pygame.image.
                load(self.shootLeft).convert_alpha(), (self.size, self.size))
        elif self.currDir == 'up':
            self.image = pygame.transform.scale(pygame.image.
                load(self.shootUp).convert_alpha(), (self.size + 10, self.size))
        elif self.currDir == 'down':
            self.image = pygame.transform.scale(pygame.image.
                load(self.shootDown).convert_alpha(), (self.size, self.size))

    def moveUp(self):
        # cycle through images moving up
        self.currDir = 'up'
        self.dx, self.dy = 0, -10
        self.image = pygame.transform.scale(pygame.image.
            load(self.upImages[self.upCount % len(self.upImages)]).
            convert_alpha(), (self.size, self.size))
        self.upCount += 1

    def moveDown(self):
        # cycle through images moving down
        self.currDir = 'down'
        self.dx, self.dy = 0, 10
        self.image = pygame.transform.scale(pygame.image.
            load(self.downImages[self.downCount % len(self.downImages)]).
            convert_alpha(), (self.size, self.size))
        self.downCount += 1

    def moveLeft(self):
        # cycle through images moving left
        self.currDir = 'left'
        self.dx, self.dy = -10, 0
        self.image = pygame.transform.scale(pygame.image.
            load(self.leftImages[self.leftCount % len(self.leftImages)]).
            convert_alpha(), (self.size, self.size))
        self.leftCount += 1

    def moveRight(self):
        # cycle through images moving right
        self.currDir = 'right'
        self.dx, self.dy = 10, 0
        self.image = pygame.transform.scale(pygame.image.
            load(self.rightImages[self.rightCount % len(self.rightImages)]).
            convert_alpha(), (self.size, self.size))
        self.rightCount += 1

    def outOfBounds(self, x, y):
        # making sure the player doesn't go out of bounds
        if (x < self.leftBound or x + self.size > self.rightBound or
            y < self.upBound or y + self.size > self.downBound):
            return True

    def updateRect(self):
        # constantly update the player's rect boundaries
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x, self.y, w, h)

    def update(self, keysDown):
        # constantly update the movement of the player
        walking = False
        if self.firing == True:
            self.firingImgs()
        else:
            if (keysDown(pygame.K_w) or keysDown(pygame.K_s) or
                keysDown(pygame.K_a) or keysDown(pygame.K_d)):
                walking = True # don't loop through pngs if player not moving
            if keysDown(pygame.K_w): self.moveUp()
            if keysDown(pygame.K_s): self.moveDown()
            if keysDown(pygame.K_a): self.moveLeft()
            if keysDown(pygame.K_d): self.moveRight()
            if walking == False: self.dx, self.dy = 0, 0
        if not self.outOfBounds(self.x + self.dx, self.y + self.dy):
            self.x += self.dx
            self.y += self.dy
        self.firing = False
        self.updateRect()
