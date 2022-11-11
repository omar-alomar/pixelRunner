import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.playerWalk1 = pygame.image.load(
            'graphics/player/player_walk_1.png').convert_alpha()
        self.playerWalk2 = pygame.image.load(
            'graphics/player/player_walk_2.png').convert_alpha()
        self.playerWalk = [self.playerWalk1, self.playerWalk2]
        self.playerIndex = 0
        self.playerJump = pygame.image.load(
            'graphics/player/jump.png').convert_alpha()

        self.image = self.playerWalk[self.playerIndex]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def applyGravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animationState(self):
        if self.rect.bottom < 300:
            self.image = self.playerJump
        else:
            self.playerIndex += 0.1
            if self.playerIndex >= len(self.playerWalk):
                self.playerIndex = 0
            self.image = self.playerWalk[int(self.playerIndex)]

    def update(self):
        self.playerInput()
        self.applyGravity()
        self.animationState()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly1, fly2]
            yPos = 210
        else:
            snailFrame1 = pygame.image.load(
                'graphics/snail/snail1.png').convert_alpha()
            snailFrame2 = pygame.image.load(
                'graphics/snail/snail2.png').convert_alpha()
            self.frames = [snailFrame1, snailFrame2]
            yPos = 300
        self.animationIndex = 0
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(
            midbottom=(randint(900, 1100), yPos))

    def animationState(self):
        self.animationIndex += 0.1
        if self.animationIndex >= len(self.frames):
            self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]

    def update(self):
        self.animationState()
        self.rect.x -= -6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


# Constants
WIDTH = 800
HEIGHT = 400
FPS_LIMIT = 60


def displayScore():
    currentTime = int(pygame.time.get_ticks() / 1000) - startTime
    scoreSurf = testFont.render(f'Score: {currentTime}', False, (64, 64, 64))
    scoreRect = scoreSurf.get_rect(center=(400, 50))
    screen.blit(scoreSurf, scoreRect)
    return currentTime


def obstacleMovement(obstacleList):
    if obstacleList:
        for obstacleRect in obstacleList:
            obstacleRect.x -= 5

            if obstacleRect.bottom == 300:
                screen.blit(snailSurf, obstacleRect)
            else:
                screen.blit(flySurf, obstacleRect)

        obstacleList = [
            obstacle for obstacle in obstacleList if obstacle.x > -100]
        return obstacleList
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacleRect in obstacles:
            if player.colliderect(obstacleRect):
                return False
    return True


def playerAnimation():
    global playerSurf, playerIndex

    if playerRect.bottom < 300:
        playerSurf = playerJump
    else:
        playerIndex += 0.1
        if playerIndex >= len(playerWalk):
            playerIndex = 0
        playerSurf = playerWalk[int(playerIndex)]


# Initial setup
pygame.init()
pygame.display.set_caption("Natural Selection Test")
testFont = pygame.font.Font('font/Pixeltype.ttf', 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # display surface
clock = pygame.time.Clock()
gameActive = False
startTime = 0
score = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacleGroup = pygame.sprite.Group()

# Surfaces
skySurface = pygame.image.load('graphics/Sky.png').convert()
groundSurface = pygame.image.load('graphics/ground.png').convert()
textSurface = testFont.render('Natural Selection Test', False, 'Black')

snailFrame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snailFrame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snailFrames = [snailFrame1, snailFrame2]
snailFrameIndex = 0
snailSurf = snailFrames[snailFrameIndex]
snailRect = snailSurf.get_rect(bottomright=(600, 300))

flyFrame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
flyFrame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
flyFrames = [flyFrame1, flyFrame2]
flyFrameIndex = 0
flySurf = flyFrames[flyFrameIndex]
obstacleRectList = []

playerWalk1 = pygame.image.load(
    'graphics/player/player_walk_1.png').convert_alpha()
playerWalk2 = pygame.image.load(
    'graphics/player/player_walk_2.png').convert_alpha()
playerWalk = [playerWalk1, playerWalk2]
playerIndex = 0
playerJump = pygame.image.load(
    'graphics/player/jump.png').convert_alpha()
playerSurf = playerWalk[playerIndex]

playerRect = playerSurf.get_rect(midbottom=(80, 300))
playerGravity = 0

# intro screen
playerStand = pygame.image.load(
    'graphics/player/player_stand.png').convert_alpha()
playerStand = pygame.transform.scale2x(playerStand)
playerStandRect = playerStand.get_rect(center=(400, 200))

gameName = testFont.render('Pixel Runner', False, (111, 196, 169))
gameNameRect = gameName.get_rect(center=(400, 80))

gameMessage = testFont.render('Press space to run', False, (111, 196, 169))
gameMessageRect = gameMessage.get_rect(center=(400, 320))

# timer
obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer, 1500)

snailAnimationTimer = pygame.USEREVENT + 2
pygame.time.set_timer(snailAnimationTimer, 500)

flyAnimationTimer = pygame.USEREVENT + 3
pygame.time.set_timer(flyAnimationTimer, 200)

while True:  # game loop

    for event in pygame.event.get():  # event loop
        if event.type == pygame.QUIT:
            pygame.quit()  # kills pygame instance
            exit()  # stops game loop
        if gameActive:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and playerRect.bottom == 300:
                    playerGravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gameActive = True

                startTime = int(pygame.time.get_ticks() / 1000)
        if gameActive:
            if event.type == obstacleTimer:
                obstacleGroup.add(
                    Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                #     obstacleRectList.append(snailSurf.get_rect(
                #         bottomright=(randint(900, 1100), 300)))
                # else:
                #     obstacleRectList.append(flySurf.get_rect(
                #         bottomright=(randint(900, 1100), 210)))

            if event.type == snailAnimationTimer:
                if snailFrameIndex == 0:
                    snailFrameIndex = 1
                else:
                    snailFrameIndex = 0
                snailSurf = snailFrames[snailFrameIndex]

            if event.type == flyAnimationTimer:
                if flyFrameIndex == 0:
                    flyFrameIndex = 1
                else:
                    flyFrameIndex = 0
                flySurf = flyFrames[flyFrameIndex]

    if gameActive:
        # Rendering surfaces
        # blit = block image transfer. just puts one surface onto another.
        screen.blit(skySurface, (0, 0))
        screen.blit(groundSurface, (0, 300))
        # Drawing score rectangle
        # We need to draw 2 rectangles because pygame removes center when specifying a border
        score = displayScore()

        # snailRect.x -= 4
        # if snailRect.right <= 0:
        #     snailRect.left = 800
        # screen.blit(snailSurf, snailRect)

        # # Gravity, player
        # playerGravity += 1
        # playerRect.y += playerGravity
        # if playerRect.bottom >= 300:
        #     playerRect.bottom = 300
        # playerAnimation()
        # screen.blit(playerSurf, playerRect)
        # player
        player.draw(screen)
        player.update()
        # obstacles
        obstacleGroup.draw(screen)
        obstacleGroup.update()

        # obstacleRectList = obstacleMovement(obstacleRectList)

        # collisions
        # gameActive = collisions(playerRect, obstacleRectList)

    else:
        screen.fill((94, 129, 162))
        screen.blit(playerStand, playerStandRect)
        obstacleRectList.clear()
        playerRect.midbottom = (80, 300)
        playerGravity = 0

        scoreMessage = testFont.render(
            f'Your score: {score}', False, (111, 196, 169))
        scoreMessageRect = scoreMessage.get_rect(center=(400, 330))
        screen.blit(gameName, gameNameRect)

        if score == 0:
            screen.blit(gameMessage, gameMessageRect)
        else:
            screen.blit(scoreMessage, scoreMessageRect)
    pygame.display.update()
    clock.tick(FPS_LIMIT)
