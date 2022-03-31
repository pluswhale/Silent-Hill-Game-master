import pygame, random, math, datetime
from PygameGame import PygameGame
from Room import Health, Sanity, Gold, Ammo, Room, Monster
from Wall import FirstWall, SecondWall, ThirdWall
from Player import Player
from Bullet import Bullet


class Game(PygameGame):
    wave = 0
    time = 0
    waveOccurring = False
    waveTime = 0
    waveOver = False
    waveOverTimer = 0
    waveStart = False
    waveStartTimer = 0

    def loadImages1(self):
        self.boxBound = 125
        self.room1PNG = pygame.transform.scale(pygame.image.load
                                               ('Backgrounds/room1.png').convert_alpha(),
                                               (self.width - self.boxBound, self.height + 1))
        self.room2PNG = pygame.transform.scale(pygame.image.load
                                               ('Backgrounds/room4.png').convert_alpha(),
                                               (self.width - self.boxBound, self.height + 1))
        self.room3PNG = pygame.transform.scale(pygame.image.load
                                               ('Backgrounds/room2.png').convert_alpha(),
                                               (self.width - self.boxBound, self.height + 1))
        self.room4PNG = pygame.transform.scale(pygame.image.load
                                               ('Backgrounds/room3.png').convert_alpha(),
                                               (self.width - self.boxBound, self.height + 1))

    def loadImages2(self):
        self.wall1 = pygame.transform.scale(pygame.image.load
                                            ('Walls/wall1.png').convert_alpha(), (60, 60))
        self.wall2 = pygame.transform.scale(pygame.image.load
                                            ('Walls/wall2.png').convert_alpha(), (60, 60))
        self.wall3 = pygame.transform.scale(pygame.image.load
                                            ('Walls/wall3.png').convert_alpha(), (60, 60))
        self.wallLeft, self.wallRight = 185, 840
        self.wallUp, self.wallDown = 60, 545
        self.cost1, self.cost2, self.cost3 = 5, 20, 40
        self.wallSize = 30
        self.wallX1, self.wallX2 = 35, 95
        self.wallAY1, self.wallAY2 = 230, 290
        self.wallBY1, self.wallBY2 = 315, 375
        self.wallCY1, self.wallCY2 = 400, 460
        self.wallLength = 60

    def colors(self):
        # store colors used in init
        self.red = (255, 0, 0)
        self.darkRed = (170, 0, 0)
        self.bgColor = (255, 255, 255)
        self.black = (0, 0, 0)
        self.yellow = (255, 255, 0)
        self.green = (0, 255, 0)
        self.gray = (70, 70, 70)
        self.white = (255, 255, 255)

    def preOtherInit(self):
        # This function initializes only once when the game is first launched
        # because it doesn't need to be unnecessarily loaded every time the game
        # is over or the game restarts. Even though it is still slow in the
        # beginning when it loads for the first time, it won't be slow whenever
        # init() needs to be called again.
        self.playerSize = 50
        self.wallWidth = 60
        # directions the monster could go in
        self.dirs = [(0, -4), (2, -2), (4, 0), (2, 2), (0, 4),
                     (-2, 2), (-4, 0), (-2, -2), (0, -4)]
        self.doorRange = 50
        self.backCenterX = self.boxBound + (self.width - self.boxBound) // 2
        self.backCenterY = self.height // 2
        self.leftDoor = self.backCenterX - self.doorRange
        self.rightDoor = self.backCenterX + self.doorRange
        self.upDoor = self.backCenterY - self.doorRange
        self.downDoor = self.backCenterY + self.doorRange

    def prePauseInit(self):
        self.pauseSize = 25
        self.pauseImg = pygame.transform.scale(pygame.image.
                                               load('pauseButton.png').convert_alpha(),
                                               (self.pauseSize, self.pauseSize))
        margin = 5
        self.pauseX = margin
        self.pauseY = self.height - (self.pauseSize + margin)
        self.pauseBoxW = 200
        self.pauseBoxH = 150
        self.pauseBoxX = self.width // 2 - self.pauseBoxW // 2
        self.pauseBoxY = self.height // 2 - self.pauseBoxH // 2

    def coordinates(self):
        self.playAX, self.playAY = 131, 37
        self.playBX, self.playBY = 250, 105
        self.howAX, self.howAY = 128, 110
        self.howBX, self.howBY = 251, 143
        self.scoreAX, self.scoreAY = 122, 147
        self.scoreBX, self.scoreBY = 249, 180
        self.creditsAX, self.creditsAY = 542, 0
        self.creditsBX, self.creditsBY = 900, 84
        self.howBackAX, self.howBackAY = 14, 413
        self.howBackBX, self.howBackBY = 140, 449
        self.credBackAX, self.credBackAY = 8, 531
        self.credBackBX, self.credBackBY = 137, 571
        self.scoreBackAX, self.scoreBackAY = 11, 534
        self.scoreBackBX, self.scoreBackBY = 140, 570

    def screens(self):
        self.menuPNG = pygame.transform.scale(pygame.image.load
                                              ('Screens/menu.png').convert_alpha(),
                                              (self.width, self.height + 2))
        self.howToPNG = pygame.transform.scale(pygame.image.load
                                               ('Screens/howToPlay.gif').convert_alpha(),
                                               (self.width, self.height + 2))
        self.highScoresPNG = pygame.transform.scale(pygame.image.load
                                                    ('Screens/highScores.gif').convert_alpha(),
                                                    (self.width, self.height + 2))
        self.creditsPNG = pygame.transform.scale(pygame.image.load
                                                 ('Screens/credits.gif').convert_alpha(),
                                                 (self.width, self.height + 2))
        self.mainMenu, self.howToPlay = 'main menu', 'how to play'
        self.credits, self.scoresDisplay = 'credits', 'high scores'
        self.gameScreen = 'game'
        self.mode = self.mainMenu
        self.nextMode = None
        self.changeDisplay = False
        self.transparency, self.switchTimer = 0, 0

    def preInit(self):
        self.loadImages1()
        self.loadImages2()
        self.colors()
        self.preOtherInit()
        self.prePauseInit()
        self.coordinates()
        self.screens()

    def roomInit(self):
        # need to add 1 to self.height because a pygame bug messed up my
        # background png for the first row of pixels
        self.room1 = Room(self.width, self.height, self.room1PNG)
        self.room2 = Room(self.width, self.height, self.room2PNG)
        self.room3 = Room(self.width, self.height, self.room3PNG)
        self.room4 = Room(self.width, self.height, self.room4PNG)
        self.rooms = [self.room1, self.room2, self.room3, self.room4]

    def sprites(self):
        self.playerGroup = pygame.sprite.Group(Player(180,
                                                      self.height // 2 - self.playerSize // 2, self.width, self.height))
        self.bulletsGroup = pygame.sprite.Group()

    def drawInit(self):
        self.paused = False
        self.barColors = [self.red, self.green]
        self.barLen = 111
        self.barMargin = 60
        self.diffScreen = False
        self.flash, self.flashTimer = False, 0
        self.blockColor, self.textColor = self.black, self.white
        self.cancelCenterX, self.cancelCenterY = 60, 540
        self.cancelRadius = 33
        self.healthRatio, self.sanityRatio = 1, 1

    def gridInit(self):
        self.gridLeft, self.gridRight = 188, 650
        self.gridUp, self.gridDown = 59, 545
        self.gridWidth = self.gridRight - self.gridLeft
        self.gridHeight = self.gridDown - self.gridUp  # 462, 486
        self.wallW, self.wallH = 22, 27  # 21 in a row and 18 in a column
        for x in range(self.gridLeft, self.gridRight, self.wallW):
            for y in range(self.gridUp, self.gridDown, self.wallH):
                self.wallGrid += [(x, y, x + self.wallW, y + self.wallH)]
                self.blockOcc += [False]

    def wallInit(self):
        self.motion1, self.motion2, self.motion3 = False, False, False
        self.wallClicked = False
        self.wallGrid, self.blockOcc = [], []
        self.currWall = None
        self.removeWall = False
        self.gridInit()

    def waveInit(self):
        self.minTime, self.maxTime = 250, 450
        self.start = random.randint(self.minTime, self.maxTime)
        self.timeSpawn = []
        for spawnTime in range(0, Room.length, 10):
            self.timeSpawn += [spawnTime]

    def otherInit(self):
        self.health, self.sanity, self.gold = 100, 100, 100
        self.ammo = 100
        self.currRoom = self.room1
        self.halfPlayer = 30
        self.nextRoom = None
        self.lastHit = 0
        self.outOfMoney = False
        self.noMoneyTimer = 0
        self.violation = False
        self.violationTimer = 0
        self.monLife = 2
        self.hurtWall = 2
        self.gameCenter = (self.width - self.boxBound) // 2 + self.boxBound

    def gameOverInit(self):
        self.gameOver = False
        self.dead = False
        self.deadImages = ['Dead/dead1.png', 'Dead/dead2.png',
                           'Dead/dead3.png', 'Dead/dead4.png']
        self.deadCount = 0
        self.deadTimer = 0
        self.gameOverX = self.width // 2 - 50
        self.gameOverY1 = 285
        self.gameOverY2 = 325
        self.gameOverW = 100
        self.gameOverH = 25

    def init(self):
        self.sprites()
        self.drawInit()
        self.roomInit()
        self.wallInit()
        self.waveInit()
        self.otherInit()
        self.gameOverInit()

    def restart(self):
        # used to restart the game
        Game.wave = 0
        Game.time = 0
        Game.waveOccurring = False
        Game.waveTime = 0
        Game.waveOver = False
        Game.waveOverTimer = 0
        Game.waveStart = False
        Game.waveStartTimer = 0

    def pausePressed(self, x, y):
        # see if pause was pressed
        if (x > self.pauseX and x < self.pauseX + self.pauseSize and
                y > self.pauseY and y < self.pauseY + self.pauseSize):
            self.paused = True
        if self.paused == True:
            boxSize = 100
            boxW, boxH = 100, 25
            boxX = self.width // 2 - boxSize // 2
            boxY1, boxY2, boxY3 = 270, 305, 340
            if (x > boxX and x < boxX + boxW):
                if (y > boxY1 and y < boxY1 + boxH):  # resume the box
                    self.paused = False
                elif (y > boxY2 and y < boxY2 + boxH):  # restart the game
                    self.restart()
                    self.init()
                    self.mode, self.paused = self.gameScreen, False
                elif (y > boxY3 and y < boxY3 + boxH):  # go to main menu
                    self.changeDisplay, self.nextMode = True, self.mainMenu
                    self.restart()
                    self.init()

    def gameOverPressed(self, x, y):
        if self.gameOver == False: return
        if (x > self.gameOverX and x < self.gameOverX + self.gameOverW):
            if (y > self.gameOverY1 and y < self.gameOverY1 + self.gameOverH):
                # restart the game
                self.restart()
                self.init()
                self.mode, self.gameOver = self.gameScreen, False
            elif (y > self.gameOverY2 and y < self.gameOverY2 + self.gameOverH):
                # go to main menu
                self.changeDisplay, self.nextMode = True, self.mainMenu
                self.restart()
                self.init()

    def wallPressed(self, x, y):
        if (x > self.wallX1 and x < self.wallX2):
            if (y > self.wallAY1 and y < self.wallAY2):  # wall1 was clicked
                self.wallClicked = True
                self.currWall = 'wall1'
            elif (y > self.wallBY1 and y < self.wallBY2):  # wall2 was clicked
                self.wallClicked = True
                self.currWall = 'wall2'
            elif (y > self.wallCY1 and y < self.wallCY2):  # wall3 was clicked
                self.wallClicked = True
                self.currWall = 'wall3'
        if (x > 5 and x < 120 and y > 467 and y < 498):  # remove a wall button
            self.removeWall = True

    def whichWall(self, block, ax, ay):
        if self.currWall == 'wall1':
            if self.gold - self.cost1 >= 0:
                self.gold -= self.cost1  # subtract from the gold
                self.currRoom.wallsGroup.add(FirstWall(ax, ay))
                self.blockOcc[block] = True
                # make sure another wall won't be placed on that current wall
                # by changing the bool in a list of the grid occupations
            else:
                self.outOfMoney = True  # can't buy if out of money
        elif self.currWall == 'wall2':
            if self.gold - self.cost2 >= 0:
                self.gold -= self.cost2
                self.currRoom.wallsGroup.add(SecondWall(ax, ay))
                self.blockOcc[block] = True
            else:
                self.outOfMoney = True
        elif self.currWall == 'wall3':
            if self.gold - self.cost3 >= 0:
                self.gold -= self.cost3
                self.currRoom.wallsGroup.add(ThirdWall(ax, ay))
                self.blockOcc[block] = True
            else:
                self.outOfMoney = True

    def addWall(self, x, y):
        if self.wallClicked:
            for block in range(len(self.wallGrid)):
                # see which block of the grid was clicked
                (ax, ay, bx, by) = self.wallGrid[block]
                if (x > ax and x < bx and y > ay and y < by):
                    if self.blockOcc[block] == True:
                        self.wallClicked = False
                        return
                    self.whichWall(block, ax, ay)

    def destroyWall(self, x, y):
        if self.removeWall == True:
            # remove the selected wall by looping through the sprites
            if (x > self.wallLeft and x < self.wallRight and
                    y > self.wallUp and y < self.wallDown):
                for wall in self.currRoom.wallsGroup.sprites():
                    if (x > wall.x and x < wall.x + wall.width and
                            y > wall.y and y < wall.y + wall.height):
                        for block in range(len(self.wallGrid)):
                            if (self.wallGrid[block] == (wall.x, wall.y,
                                                         wall.x + wall.width, wall.y + wall.height)):
                                self.blockOcc[block] = False
                                # change the current block to empty again
                        self.currRoom.wallsGroup.remove(wall)
                        self.removeWall = False

    def cancel(self, x, y):
        # used to cancel a selection
        if self.overlapDist(self.cancelCenterX, self.cancelCenterY, x, y) < 33:
            self.wallClicked = False
            self.removeWall = False

    def gameMousePressed(self, x, y):
        # mousePressed function for when the mode is the game
        self.pausePressed(x, y)
        self.gameOverPressed(x, y)
        if self.gameOver or self.paused: return
        self.wallPressed(x, y)
        self.addWall(x, y)
        self.destroyWall(x, y)
        self.cancel(x, y)

    def menuMousePressed(self, x, y):
        # mouse pressed for when mode is the main menu
        if (x > self.playAX and x < self.playBX and
                y > self.playAY and y < self.playBY):
            self.nextMode, self.changeDisplay = self.gameScreen, True
        elif (x > self.howAX and x < self.howBX and
              y > self.howAY and y < self.howBY):
            self.nextMode, self.changeDisplay = self.howToPlay, True
        elif (x > self.scoreAX and x < self.scoreBX and
              y > self.scoreAY and y < self.scoreBY):
            self.nextMode, self.changeDisplay = self.scoresDisplay, True
        elif (x > self.creditsAX and x < self.creditsBX and
              y > self.creditsAY and y < self.creditsBY):
            self.nextMode, self.changeDisplay = self.credits, True

    def howToMousePressed(self, x, y):
        # mouse pressed for when mode is the howTo screen
        if (x > self.howBackAX and x < self.howBackBX and
                y > self.howBackAY and y < self.howBackBY):
            self.nextMode, self.changeDisplay = self.mainMenu, True

    def creditsMousePressed(self, x, y):
        # mouse pressed for when mode is the credits
        if (x > self.credBackAX and x < self.credBackBX and
                y > self.credBackAY and y < self.credBackBY):
            self.nextMode, self.changeDisplay = self.mainMenu, True

    def scoresMousePressed(self, x, y):
        # mouse pressed for when the mode is the high scores screen
        if (x > self.scoreBackAX and x < self.scoreBackBX and
                y > self.scoreBackBX and y < self.scoreBackBY):
            self.nextMode, self.changeDisplay = self.mainMenu, True

    def mousePressed(self, x, y):
        if self.mode == self.gameScreen:
            self.gameMousePressed(x, y)
        elif self.mode == self.mainMenu:
            self.menuMousePressed(x, y)
        elif self.mode == self.howToPlay:
            self.howToMousePressed(x, y)
        elif self.mode == self.credits:
            self.creditsMousePressed(x, y)
        elif self.mode == self.scoresDisplay:
            self.scoresMousePressed(x, y)

    def mouseReleased(self, x, y):
        pass

    def gameMouseMotion(self, x, y):
        # put a transparent box on the wall if the mouse is hovering over it
        if (x > self.wallX1 and x < self.wallX2):
            if (y > self.wallAY1 and y < self.wallAY2):
                self.motion1, self.motion2, self.motion3 = True, False, False
            elif (y > self.wallBY1 and y < self.wallBY2):
                self.motion1, self.motion2, self.motion3 = False, True, False
            elif (y > self.wallCY1 and y < self.wallCY2):
                self.motion1, self.motion2, self.motion3 = False, False, True
        else:
            self.motion1, self.motion2, self.motion3 = False, False, False

    def mouseMotion(self, x, y):
        if self.mode == self.gameScreen:
            self.gameMouseMotion(x, y)

    def mouseDrag(self, x, y):
        pass

    def fireBullet(self, player):
        # fire the bullet depending on the player direction
        if self.ammo == 0:
            return
        elif player.currDir == 'right':
            self.bulletsGroup.add(Bullet(player.x + player.size - 10,
                                         player.y + player.size // 2 - 12, 'right'))
        elif player.currDir == "left":
            self.bulletsGroup.add(Bullet(player.x - 15, player.y +
                                         player.size // 2 - 12, 'left'))
        elif player.currDir == "up":
            self.bulletsGroup.add(Bullet(player.x + player.size // 2 - 5,
                                         player.y - 5, 'up'))
        elif player.currDir == "down":
            self.bulletsGroup.add(Bullet(player.x, player.y +
                                         player.size // 2, 'down'))

    def firstDoor(self, player):
        # open the first door and prepare the next room
        if self.currRoom == self.room1:
            self.nextRoom = self.room2
            self.diffScreen = True  # flash a switch black screen
        elif self.currRoom == self.room4:
            self.nextRoom = self.room1
            self.diffScreen = True

    def secondDoor(self, player):
        # open the second door and prepare the next room
        if self.currRoom == self.room1:
            self.nextRoom = self.room4
            self.diffScreen = True
        elif self.currRoom == self.room2:
            self.nextRoom = self.room1
            self.diffScreen = True

    def thirdDoor(self, player):
        # open the third door and prepare the next room
        if self.currRoom == self.room1:
            self.nextRoom = self.room3
            self.diffScreen = True

    def fourthDoor(self, player):
        # open the fourth door and prepare the next room
        if self.currRoom == self.room3:
            self.nextRoom = self.room1
            self.diffScreen = True

    def openDoor(self, player):
        # sees which door the player is within range of
        centerX = player.x + player.size // 2
        centerY = player.y + player.size // 2
        if (centerX > self.leftDoor and centerX < self.rightDoor and
                centerY > 20 and centerY < 80):
            self.firstDoor(player)  # up door
        elif (centerX > self.leftDoor and centerX < self.rightDoor and
              centerY > self.height - 100 and centerY < self.height - 40):
            self.secondDoor(player)  # down door
        elif (centerX > self.width - 100 and centerX < self.width - 40 and
              centerY > self.upDoor and centerY < self.downDoor):
            self.thirdDoor(player)  # right door
        elif (centerX > self.boxBound + 40 and centerX < self.boxBound + 100 and
              centerY > self.upDoor and centerY < self.downDoor):
            self.fourthDoor(player)  # left door

    def gameKeyPressed(self, keyCode, modifier):
        # key pressed for the game screen
        player = self.playerGroup.sprites()[0]
        if keyCode == pygame.K_SPACE and self.ammo != 0:
            player.firing = True
            self.fireBullet(player)
            self.ammo -= 1
        if keyCode == pygame.K_TAB and Game.waveOccurring == False:
            self.openDoor(player)

    def keyPressed(self, keyCode, modifier):
        if self.paused or self.gameOver: return
        # can't do anything if the game is paused or over
        if self.mode == self.gameScreen:
            self.gameKeyPressed(keyCode, modifier)

    def keyReleased(self, keyCode, modifier):
        pass

    def checkBullets(self):
        # if the bullets are out of bounds, remove it
        for bullet in self.bulletsGroup.sprites():
            if (bullet.x <= self.boxBound + 15 or bullet.x >= 850 or
                    bullet.y <= 28 or bullet.y >= 550):
                self.bulletsGroup.remove(bullet)

    def calculateDist(self, newX, newY):
        # calculate the distance between the monster and the player
        player = self.playerGroup.sprites()[0]
        return math.sqrt((newX - player.x) ** 2 + (newY - player.y) ** 2)

    def monCollide(self, monster, newX, newY):
        # make sure the monsters don't collide with each other when moving
        for other in self.currRoom.monstersGroup.sprites():
            if other == monster:
                continue
            elif self.overlapDist(newX, newY, other.x, other.y) <= 40:
                return True
        return False

    def moveMonsters(self, monster):
        # move the monsters according to the shortest route to the player
        shortestDist, shortestMove = None, None
        for direction in self.dirs:
            (dx, dy) = direction
            newX, newY = monster.x + dx, monster.y + dy
            if self.monCollide(monster, newX, newY) == False:
                currDist = self.calculateDist(newX, newY)
                if shortestDist == None or currDist < shortestDist:
                    shortestDist = currDist
                    shortestMove = direction
        return shortestMove

    def checkSpawn(self, monster):
        # make sure the monsters don't spawn on top of each other
        width, height = monster.image.get_size()
        monCenX = monster.x + width // 2
        monCenY = monster.y + height // 2
        for other in self.currRoom.monstersGroup.sprites():
            otherW, otherH = other.image.get_size()
            if other == monster:
                continue
            elif (monCenY > other.y and monCenY < other.y + width and
                  monCenX > other.x and monCenX < other.x + height):
                monster.y = random.randrange(70, self.height - 100)

    def monstersDir(self):
        # change the direction the monsters are facing according to which
        # direction they are moving
        for monster in self.currRoom.monstersGroup.sprites():
            self.checkSpawn(monster)
            currMove = self.moveMonsters(monster)
            if currMove == None:
                (dx, dy) = (0, 0)
            else:
                (dx, dy) = currMove
            monster.move = (dx, dy)
            if (dx, dy) == self.dirs[0]:
                monster.currDir = 'up'
            elif (dx, dy) == self.dirs[2]:
                monster.currDir = 'right'
            elif (dx, dy) == self.dirs[4]:
                monster.currDir = 'down'
            elif (dx, dy) == self.dirs[6]:
                monster.currDir = 'left'

    def playerHit(self):
        # subtract health when the player is hit BUT health has to be
        # subtracting in intervals or else the player's health will drop down
        # extremely fast so keep track of a time (self.lastHit)
        player = self.playerGroup.sprites()[0]
        self.lastHit += 1
        if self.lastHit == 1:
            if self.health - 5 <= 0:
                self.dead = True
                self.health, self.healthRatio = 0, 0
            else:
                self.health -= 5
                self.healthRatio -= 0.05
                player.hit, self.flash = True, True
        elif self.lastHit > 20:
            if self.health - 5 <= 0:
                self.dead = True
                self.health, self.healthRatio = 0, 0
            else:
                self.health -= 5
                self.healthRatio -= 0.05
                player.hit, self.flash, self.lastHit = True, True, 1

    def collide1(self):
        if pygame.sprite.groupcollide(self.playerGroup, self.currRoom.
                monstersGroup, False, False, pygame.sprite.collide_circle):
            self.playerHit()  # player and monsters collide
        for monster in pygame.sprite.groupcollide(self.currRoom.monstersGroup,
                                                  self.bulletsGroup, False, True, pygame.sprite.collide_circle):
            monster.life -= 1  # bullet and monsters collide
            if monster.life == 0: self.currRoom.monstersGroup.remove(monster)
        if pygame.sprite.groupcollide(self.currRoom.goldGroup, self.playerGroup,
                                      True, False, pygame.sprite.collide_circle):
            self.gold += 10  # gold and player collide

    def collide2(self):
        if pygame.sprite.groupcollide(self.currRoom.healthGroup,
                                      self.playerGroup, True, False, pygame.sprite.collide_circle):
            # player and health potion collide
            if self.health + 20 > 100:
                self.health, self.healthRatio = 100, 1
            else:
                self.health += 20
                self.healthRatio += 0.2
        if pygame.sprite.groupcollide(self.currRoom.sanityGroup,
                                      self.playerGroup, True, False, pygame.sprite.collide_circle):
            # player and sanity potion collide
            if self.sanity + 20 > 100:
                self.sanity, self.sanityRatio = 100, 1
            else:
                self.sanity += 10
                self.sanityRatio += 0.1
        if pygame.sprite.groupcollide(self.currRoom.ammoGroup, self.playerGroup,
                                      True, False, pygame.sprite.collide_circle):
            # player and ammo collide
            self.ammo += 20

    def collisions(self):
        self.collide1()
        self.collide2()

    def playerPos(self):
        # move the player to a certain part of the screen according to what the
        # previous room was and the next room is
        player = self.playerGroup.sprites()[0]
        if self.currRoom == self.room1 and self.nextRoom == self.room2:
            player.x, player.y = self.backCenterX - self.halfPlayer, 500
        elif self.currRoom == self.room4 and self.nextRoom == self.room1:
            player.x, player.y = self.backCenterX - self.halfPlayer, 500
        elif self.currRoom == self.room1 and self.nextRoom == self.room4:
            player.x, player.y = self.backCenterX - self.halfPlayer, 30
        elif self.currRoom == self.room2 and self.nextRoom == self.room1:
            player.x, player.y = self.backCenterX - self.halfPlayer, 30
        elif self.currRoom == self.room1 and self.nextRoom == self.room3:
            player.x = self.boxBound + 60
            player.y = (self.height - player.size) // 2
        elif self.currRoom == self.room3 and self.nextRoom == self.room1:
            player.x = self.width - 110
            player.y = (self.height - player.size) // 2

    def switch(self):
        # flash a black screen when switching rooms
        if self.diffScreen == True:
            self.switchTimer += 1
            if self.switchTimer < 4:
                self.transparency += 85
            elif self.switchTimer >= 14:
                self.playerPos()
                self.currRoom = self.nextRoom
                self.transparency -= 85
            if self.switchTimer == 16:
                self.transparency = 0
                self.diffScreen = False
                self.switchTimer = 0

    def overlapDist(self, monX, monY, otherX, otherY):
        # return distance between two objects (distance formula)
        return math.sqrt((monX - otherX) ** 2 + (monY - otherY) ** 2)

    def resetBools(self, wall):
        # make the block in the grid vacant again if a monster destroys it
        for block in range(len(self.wallGrid)):
            if (self.wallGrid[block] == (wall.x, wall.y,
                                         wall.x + wall.width, wall.y + wall.height)):
                self.blockOcc[block] = False

    def wallAndMon(self, monster, monCenX, monCenY):
        # Track the life of the wall but the wall, similar to the player, has
        # to lose life between intervals. It can't suddenly drop down really
        # fast
        for wall in self.currRoom.wallsGroup.sprites():
            centerX = wall.x + wall.width // 2
            centerY = wall.y + wall.height // 2
            if self.overlapDist(monCenX, monCenY, centerX, centerY) <= 25:
                wall.prevHit += 1
                if wall.prevHit == 1:
                    if wall.life == 0:
                        self.resetBools(wall)
                        self.currRoom.wallsGroup.remove(wall)
                    else:
                        wall.life -= self.hurtWall
                elif wall.prevHit > 20:
                    if wall.life == 0:
                        self.resetBools(wall)
                        self.currRoom.wallsGroup.remove(wall)
                    else:
                        wall.life -= self.hurtWall
                    wall.prevHit = 1
                monster.overlap = True

    def noOverlap(self):
        # make sure the wall and the monsters don't overlap and the player and
        # monsters don't overlap (but the player can still walk over monsters)
        player = self.playerGroup.sprites()[0]
        playerX = player.x + player.size // 2 + player.dx
        playerY = player.y + player.size // 2 + player.dy
        if self.currRoom == None: return
        for monster in self.currRoom.monstersGroup.sprites():
            width, height = monster.image.get_size()
            monCenX = monster.x + width // 2
            monCenY = monster.y + height // 2
            if self.overlapDist(monCenX, monCenY, playerX, playerY) <= 30:
                monster.overlap = True
            else:
                monster.overlap = False
            self.wallAndMon(monster, monCenX, monCenY)

    def hitIntervals(self):
        # keep track of the hit intervals for the player and the walls
        if self.lastHit != 0: self.lastHit += 1
        for wall in self.currRoom.wallsGroup.sprites():
            if wall.prevHit != 0:
                wall.prevHit += 1

    def flashPlayer(self):
        # flash the player if the player is hit
        if self.flash == True:
            self.flashTimer += 1
        if self.flashTimer == 2:
            self.flashTimer = 0
            self.flash = False

    def removeColor(self):
        # change color of remove wall button if it is selected
        if self.removeWall == True:
            self.blockColor, self.textColor = self.white, self.black
        else:
            self.blockColor, self.textColor = self.black, self.white

    def noMoneyCounter(self):
        # flash the insufficient funds message if the player tries to buy walls
        # when the player is out of money
        if self.outOfMoney == True:
            self.noMoneyTimer += 1
        if self.noMoneyTimer == 14:
            self.noMoneyTimer = 0
            self.outOfMoney = False

    def resetRooms(self):
        # reset rooms after each wave
        for room in self.rooms:
            room.healthInit()
            room.sanityInit()
            room.goldInit()
            room.ammoInit()

    def reset(self):
        # reset after waves
        Game.waveTime = 0
        Game.waveOccurring, Game.waveOver = False, True
        Room.length += 50  # increase the time span of spawning monsters
        self.timeSpawn = []
        self.resetMonsters()
        self.resetRooms()
        self.start = random.randint(self.minTime, self.maxTime)
        if self.sanity - 10 < 0:
            self.sanity, self.sanityRatio = 0, 0
            self.dead = True
        else:
            self.sanity -= 10
            self.sanityRatio -= 0.1

    def trackWaves(self):
        if Game.waveOccurring == False: Game.time += 1
        if Game.time == self.start:  # start wave
            Game.time = 0
            Game.wave += 1
            Game.waveOccurring, Game.waveStart = True, True
        if (len(self.currRoom.monstersGroup.sprites()) == 0 and
                Game.waveOccurring == True and Game.waveTime > 100):
            self.reset()  # reset if wave is over
        self.monLife = 2 * (Game.wave // 5) + 2
        self.hurtWall = 2 * (Game.wave // 5) + 2
        # make monsters stronger every 5 waves
        # more damage on walls

    def resetMonsters(self):
        # make a list of all the times the monsters are supposed to spawn
        for spawnTime in range(0, Room.length, 10):  # spawn at intervals
            self.timeSpawn += [spawnTime]

    def addMonsters(self):
        # loop through the times list and spawn them accordingly
        for mon in range(len(self.timeSpawn)):
            if Game.waveTime == self.timeSpawn[mon]:
                self.currRoom.monstersGroup.add(Monster(self.width,
                                                        self.height, self.monLife))

    def resetWaves(self):
        if Game.waveOccurring == True:
            Game.waveTime += 1
            # can't build during waves
            self.wallClicked, self.removeWall = False, False
            self.addMonsters()
            self.currRoom.monstersGroup.update()
        if Game.waveOver:
            Room.length = 100 + (Game.wave * 30)
            Game.waveOverTimer += 1
        if Game.waveOverTimer == 30:
            Game.waveOverTimer = 0
            Game.waveOver = False
        if Game.waveStart:
            Game.waveStartTimer += 1
        if Game.waveStartTimer == 30:
            Game.waveStartTimer = 0
            Game.waveStart = False

    @staticmethod
    def readFile(path):
        # Taken from 15-112 Strings Course Notes
        with open(path, "rt") as f:
            return f.read()

    @staticmethod
    def writeFile(path, contents):
        # Taken from 15-112 Strings Course Notes
        with open(path, "wt") as f:
            f.write(contents)

    @staticmethod
    def getWave(string):
        # get the wave number given a string
        start = 9
        end = string.find('Wave')
        waves = string[9:end].strip()
        return int(waves)

    @staticmethod
    def checkScores(currContents, newScore):
        # only get the top 5 scores so if the new score isn't bigger than the
        # previous ones, don't add it
        currScore = Game.getWave(newScore)
        scoreLines = currContents.splitlines()
        for line in range(len(scoreLines)):
            score = Game.getWave(scoreLines[line])
            if currScore > score:
                scoreLines = scoreLines[:line] + scoreLines[line + 1:]
                scoreLines += "\n" + newScore
        newString = ""
        for line in scoreLines:
            newString += line + "\n"
        return newString

    def addHighScore(self):
        currDate = str(datetime.datetime.now())  # get the current date and time
        year = currDate[:4]
        month = currDate[5:7]
        day = currDate[8:10]
        hour = currDate[11:13]
        minute = currDate[14:16]
        waves = Game.wave - 1
        if waves != 1:
            newScore = "Survived %d Waves on %s/%s/%s at %s:%s" % (waves,
                                                                   month, day, year, hour, minute)
        else:
            newScore = "Survived %d Wave on %s/%s/%s at %s:%s" % (waves,
                                                                  month, day, year, hour, minute)
        currContents = Game.readFile('highScores.txt')
        if len(currContents.splitlines()) == 5:  # only get the top 5
            newContents = Game.checkScores(currContents, newScore)
            Game.writeFile('highScores.txt', newContents)
        elif currContents == "":
            Game.writeFile('highScores.txt', newScore)
        else:
            Game.writeFile('highScores.txt', currContents + "\n" + newScore)
        # write a new file with the new contents if the file doesn't have 5
        # scores yet

    def checkGameOver(self):
        if self.dead == True: self.deadTimer += 1
        if self.dead == True and self.deadTimer % 5 == 0:
            player = self.playerGroup.sprites()[0]
            player.image = pygame.transform.scale(pygame.image.load
                                                  (self.deadImages[self.deadCount]).convert_alpha(),
                                                  (self.playerSize, self.playerSize))  # load the dead images
            self.deadCount += 1
        if self.deadCount == 4:
            self.addHighScore()  # add the new score to the text file
            self.gameOver = True

    def gameTimerFired(self, dt):
        # timer fired only for the game
        if self.paused or self.gameOver: return
        self.playerGroup.update(self.isKeyPressed)
        self.bulletsGroup.update()
        self.resetWaves()
        self.checkBullets()
        self.collisions()
        self.monstersDir()
        self.currRoom.healthGroup.update()
        self.switch()
        self.noOverlap()
        self.hitIntervals()
        self.flashPlayer()
        self.removeColor()
        self.noMoneyCounter()
        self.trackWaves()
        self.checkGameOver()

    def timerFired(self, dt):
        if self.mode == self.gameScreen:
            self.gameTimerFired(dt)
        if self.changeDisplay == True:
            # flash black screen if moving between modes
            self.switchTimer += 1
            if self.switchTimer < 4:
                self.transparency += 85
            elif self.switchTimer >= 14:
                self.transparency -= 85
                self.mode = self.nextMode
            if self.switchTimer == 16:
                self.transparency = 0
                self.changeDisplay = False
                self.switchTimer = 0

    def centerText(self, text):
        # centers the text by returning the correct x coordinate
        return self.gameCenter - text.get_rect().width // 2

    def drawBars(self, screen):
        # draw the health and sanity bars
        thickness = 5
        health = [9, self.barMargin + 2,
                  int((self.barLen - 4) * self.healthRatio), 16]
        healthBorder = [7, self.barMargin, self.barLen, 20]
        pygame.draw.rect(screen, self.black, healthBorder, thickness)
        pygame.draw.rect(screen, self.red, health)
        sanity = [9, self.barMargin + 52,
                  int((self.barLen - 4) * self.sanityRatio), 16]
        sanityBorder = [7, self.barMargin + 50, self.barLen, 20]
        pygame.draw.rect(screen, self.black, sanityBorder, thickness)
        pygame.draw.rect(screen, self.green, sanity)

    def drawText(self, screen):
        # draw the inventory text
        font = pygame.font.Font(None, 30)
        waves = font.render("Waves: %d" % Game.wave, True, self.black)
        screen.blit(waves, (7, 10))
        font = pygame.font.Font(None, 25)
        life = font.render("HEALTH", True, self.white)
        screen.blit(life, (7, self.barMargin - 22))
        lifePercent = font.render("%d %%" % self.health, True, self.black)
        screen.blit(lifePercent, (11, self.barMargin + 2))
        sanity = font.render("SANITY", True, self.white)
        screen.blit(sanity, (7, self.barMargin + 28))
        sanityPercent = font.render("%d %%" % self.sanity, True, self.black)
        screen.blit(sanityPercent, (11, self.barMargin + 52))

    def drawTransWall(self, screen, x, y):
        transparency = 100
        wallTrans = pygame.Surface((self.wallLength, self.wallLength),
                                   pygame.SRCALPHA)
        wallTrans.fill((0, 0, 0, transparency))
        screen.blit(wallTrans, (x, y))

    def transWalls(self, screen):
        if self.paused or self.gameOver: return
        if self.motion1:  # mouse hovering over wall1
            self.drawTransWall(screen, self.wallX1, self.wallAY1)
        elif self.motion2:  # mouse hovering over wall2
            self.drawTransWall(screen, self.wallX1, self.wallBY1)
        elif self.motion3:  # mouse hovering over wall3
            self.drawTransWall(screen, self.wallX1, self.wallCY1)

    def drawWalls(self, screen):
        # draw the pictures and the text for the wall selections
        font = pygame.font.Font(None, 25)
        cost1 = font.render("Cost: 5", True, self.white)
        cost2 = font.render("Cost: 20", True, self.white)
        cost3 = font.render("Cost: 40", True, self.white)
        screen.blit(cost1, (35, 210))
        screen.blit(self.wall1, (35, 230))
        screen.blit(cost2, (30, 295))
        screen.blit(self.wall2, (35, 315))
        screen.blit(cost3, (30, 380))
        screen.blit(self.wall3, (35, 400))
        pygame.draw.rect(screen, self.white, [5, 467, 115, 31])
        pygame.draw.rect(screen, self.blockColor, [8, 470, 109, 25])
        font = pygame.font.Font(None, 23)
        remove = font.render('Remove Wall', True, self.textColor)
        screen.blit(remove, (15, 475))
        self.transWalls(screen)

    def drawInven(self, screen):
        # draw the inventory
        pygame.draw.rect(screen, self.gray,
                         [0, 0, self.boxBound, self.height])
        pygame.draw.line(screen, self.black,
                         (self.boxBound, 0), (self.boxBound, self.height))
        font = pygame.font.Font(None, 35)
        inventory = font.render("Inventory", True, self.black)
        screen.blit(inventory, (7, self.barMargin + 78))
        pygame.draw.line(screen, self.black, (5, 165), (120, 165))
        font = pygame.font.Font(None, 25)
        gold = font.render("Gold: %d" % self.gold, True, self.white)
        screen.blit(gold, (7, 170))
        ammo = font.render("Ammo: %d" % self.ammo, True, self.white)
        screen.blit(ammo, (7, 190))
        self.drawWalls(screen)

    def changeScreens(self, screen):
        if self.diffScreen:
            switchScreen = pygame.Surface((self.width - self.boxBound,
                                           self.height), pygame.SRCALPHA)
            switchScreen.fill((0, 0, 0, self.transparency))
            screen.blit(switchScreen, (self.boxBound, 0))

    def drawPauseText(self, screen):
        # draw the pause box text
        font = pygame.font.Font("Times New Roman.ttf", 35)
        pauseText = font.render("Game Paused", True, self.black)
        screen.blit(pauseText, (self.pauseBoxX + 5, self.pauseBoxY + 2))
        font = pygame.font.Font("Times New Roman.ttf", 15)
        resume = font.render("RESUME", True, self.black)
        restart = font.render("RESTART", True, self.black)
        menu = font.render("MAIN MENU", True, self.black)
        screen.blit(resume, (self.width // 2 - 30, 274))
        screen.blit(restart, (self.width // 2 - 32, 309))
        screen.blit(menu, (self.width // 2 - 45, 344))

    def drawPause(self, screen):
        # draw the pause box in the middle
        screen.blit(self.pauseImg, (self.pauseX, self.pauseY))
        if self.paused == True:
            pygame.draw.rect(screen, self.darkRed, [self.pauseBoxX - 5,
                                                    self.pauseBoxY - 5, self.pauseBoxW + 10, self.pauseBoxH + 10])
            pygame.draw.rect(screen, self.gray, [self.pauseBoxX,
                                                 self.pauseBoxY, self.pauseBoxW, self.pauseBoxH])
            boxSize = 100
            boxX = self.width // 2 - boxSize // 2
            for box in range(3):
                pygame.draw.rect(screen, self.darkRed, [boxX,
                                                        270 + 35 * box, boxSize, 25])
            self.drawPauseText(screen)

    def drawGrid(self, screen):
        # draw the grid that the player uses to place the walls
        if self.wallClicked == True:
            grid = pygame.Surface((self.gridWidth, self.gridHeight),
                                  pygame.SRCALPHA)
            grid.fill((255, 255, 255, 100))
            screen.blit(grid, (self.gridLeft, self.gridUp))
            for x in range(self.gridLeft + self.wallW, self.gridRight, self.wallW):
                pygame.draw.line(screen, self.black, (x, self.gridUp),
                                 (x, self.gridDown))
            for y in range(self.gridUp + self.wallH, self.gridDown, self.wallH):
                pygame.draw.line(screen, self.black, (self.gridLeft, y),
                                 (self.gridRight, y))

    def cancelButton(self, screen):
        # draw the button the player uses to cancel a selection
        centerX, centerY, radius = 60, 540, 30
        pygame.draw.circle(screen, self.white, (centerX, centerY), radius + 3)
        pygame.draw.circle(screen, self.black, (centerX, centerY), radius)
        font = pygame.font.Font(None, 20)
        cancel = font.render("Deselect", True, self.white)
        screen.blit(cancel, (34, 532))

    def drawNoMoney(self, screen):
        # if player tries to buy something when the player has no more money,
        # flash a no money message
        if self.outOfMoney == True and self.noMoneyTimer % 2 == 0:
            font = pygame.font.Font(None, 50)
            noMoney = font.render("Insufficient Funds", True, self.black)
            screen.blit(noMoney, (self.centerText(noMoney),
                                  self.height // 2 - 20))

    def drawWaveStart(self, screen):
        # draw message everytime wave starts
        font = pygame.font.Font('Times New Roman.ttf', 80)
        waveBegin = font.render("WAVE %d" % Game.wave, True, self.black)
        screen.blit(waveBegin, (self.centerText(waveBegin),
                                self.height // 2 - 80))
        font = pygame.font.Font('Times New Roman.ttf', 30)
        restriction1 = font.render("NO BUILDING", True, self.black)
        screen.blit(restriction1, (self.centerText(restriction1),
                                   self.height // 2 + 5))
        restriction2 = font.render("DOORS LOCKED", True, self.black)
        screen.blit(restriction2, (self.centerText(restriction2),
                                   self.height // 2 + 40))
        if Game.wave != 0 and Game.wave % 5 == 0:
            difficult = font.render("STRONGER MONSTERS", True, self.black)
            screen.blit(difficult, (self.centerText(difficult),
                                    self.height // 2 + 75))

    def drawWaves(self, screen):
        # draw message when wave over
        if Game.waveOver == True:
            font = pygame.font.Font('Times New Roman.ttf', 70)
            waveOver = font.render("WAVE %d SURVIVED" % Game.wave,
                                   True, self.black)
            screen.blit(waveOver, (self.centerText(waveOver),
                                   self.height // 2 - 50))
        if Game.waveStart == True:
            self.drawWaveStart(screen)

    def drawGameOverText(self, screen):
        # draw the game over text
        font = pygame.font.Font("Times New Roman.ttf", 33)
        pauseText = font.render("GAME OVER", True, self.black)
        screen.blit(pauseText, (self.pauseBoxX + 4, self.pauseBoxY + 13))
        font = pygame.font.Font("Times New Roman.ttf", 15)
        restart = font.render("RESTART", True, self.black)
        menu = font.render("MAIN MENU", True, self.black)
        screen.blit(restart, (self.width // 2 - 33, 288))
        screen.blit(menu, (self.width // 2 - 43, 328))

    def drawGameOver(self, screen):
        # draw game over box in the middle
        if self.gameOver == True:
            pygame.draw.rect(screen, self.darkRed, [self.pauseBoxX - 5,
                                                    self.pauseBoxY + 5, self.pauseBoxW + 10, self.pauseBoxH - 10])
            pygame.draw.rect(screen, self.gray, [self.pauseBoxX,
                                                 self.pauseBoxY + 10, self.pauseBoxW, self.pauseBoxH - 20])
            boxSize = 100
            boxX = self.width // 2 - boxSize // 2
            for box in range(2):
                pygame.draw.rect(screen, self.darkRed, [boxX,
                                                        285 + 40 * box, boxSize, 25])
            self.drawGameOverText(screen)

    def gameRedrawAll(self, screen):
        # the redraw all for the game screen
        self.currRoom.drawObjs(screen)
        self.drawInven(screen)
        self.drawBars(screen)
        self.drawText(screen)
        self.cancelButton(screen)
        if self.flash == False: self.playerGroup.draw(screen)
        self.bulletsGroup.draw(screen)
        if Game.waveOccurring == True:
            self.currRoom.monstersGroup.draw(screen)
        self.changeScreens(screen)
        self.drawGrid(screen)
        self.drawNoMoney(screen)
        self.drawWaves(screen)
        self.drawPause(screen)
        self.drawGameOver(screen)

    @staticmethod
    def sortScores(content):
        # sort the scores from highest to lowest using a recursive function
        # that loops over all the strings in the text file
        if len(content) == 1:
            return content[0]
        else:
            biggest, waveLine = None, None
            for line in range(len(content)):
                currScore = Game.getWave(content[line])
                if biggest == None or currScore > biggest:
                    biggest = Game.getWave(content[line])
                    waveLine = line
            new = content[waveLine]
            content.pop(waveLine)
            return new + "\n" + Game.sortScores(content)

    def scoresRedrawAll(self, screen):
        # draw the 5 highest scores
        screen.blit(self.highScoresPNG, (0, -1))
        contents = Game.readFile('highScores.txt')
        if contents == "": return
        listOfScores = contents.splitlines()
        margin, space, left, size, counter = 120, 80, 87, 40, 1
        listOfScores = Game.sortScores(listOfScores).splitlines()
        for line in range(len(listOfScores)):
            font = pygame.font.Font("Times New Roman.ttf", size)
            text = font.render(str(counter) + ". " + listOfScores[line],
                               True, self.white)
            screen.blit(text, (left, margin + line * space))
            counter += 1

    def redrawAll(self, screen):
        if self.mode == self.gameScreen:
            self.gameRedrawAll(screen)
        elif self.mode == self.mainMenu:
            screen.blit(self.menuPNG, (0, -1))  # draw the main menu
        elif self.mode == self.howToPlay:
            screen.blit(self.howToPNG, (0, -1))  # draw the how to screen
        elif self.mode == self.credits:
            screen.blit(self.creditsPNG, (0, -1))  # draw the credits screen
        elif self.mode == self.scoresDisplay:
            self.scoresRedrawAll(screen)
        if self.changeDisplay:
            switchScreen = pygame.Surface((self.width, self.height),
                                          pygame.SRCALPHA)
            switchScreen.fill((0, 0, 0, self.transparency))
            screen.blit(switchScreen, (0, 0))


Game(900, 600).run()
