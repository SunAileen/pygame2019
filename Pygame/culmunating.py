#***********************************************************************************************************************
#Program Author: Aileen Sun and Elena Osipyan
#Revision Date: Jan 16, 2020
#Program Name: basic shooter game uwu
#Description: This program plays a two-player shooter game
#***********************************************************************************************************************
import pygame
import time
import random

pygame.init()    #Initializes pygame

#Colour constants
black = (0, 0, 0)
white = (255, 255, 255)

#Display's screen
displayWidth = 800
displayHeight = 800

#Lists that hold and manage pygame sprites
allSpritesList = pygame.sprite.Group()
bullets1List = pygame.sprite.Group()
bullets2List = pygame.sprite.Group()
powerUpsList = pygame.sprite.Group()

#Creates surface and clock
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption("basic shooter game uwu")
clock = pygame.time.Clock()

#Variables used when redirecting with buttons and using power ups
global replay, playMenu, stopMain, playGameOver, scramble1, scramble2, moreDamage1, moreDamage2, usedPower1, usedPower2, score1, score2
replay = True
playMenu = True
playGameOver = True
stopMain = False
scramble1 = False
scramble2 = False
moreDamage1 = False
moreDamage2 = False
score1 = 0
score2 = 0

#Sound effects
buttonSound = pygame.mixer.Sound('clickButton.wav')
powerUpSound = pygame.mixer.Sound('pickPowerUp.wav')
gunShotSound = pygame.mixer.Sound('gunShot.wav')
loseLifeSound = pygame.mixer.Sound('loseLife.wav')
gameOverSound = pygame.mixer.Sound('gameOverSound.wav')
countdownSound = pygame.mixer.Sound('countdown.wav')

#Loads an image, given its path
def loadImage(path):
    image = pygame.image.load(path).convert_alpha()
    return image

#Button images
global replayButtonOriginal, replayButtonHover, replayButtonClicked, quitButtonOriginal, quitButtonHover, quitButtonClicked, menuButtonOriginal, menuButtonHover, menuButtonClicked
replayButtonOriginal = loadImage('replayButton.png')
replayButtonHover = loadImage('replayButtonHover.png')
replayButtonClicked = loadImage('replayButtonClicked.png')

quitButtonOriginal = loadImage('quitButton.png')
quitButtonHover = loadImage('quitButtonHover.png')
quitButtonClicked = loadImage('quitButtonClicked.png')

menuButtonOriginal = loadImage('menuButton.png')
menuButtonHover = loadImage('menuButtonHover.png')
menuButtonClicked = loadImage('menuButtonClicked.png')

usedPower = loadImage('usedPowerUp.png')
usedPower1 = usedPower
usedPower2 = usedPower

#Making a global sound/mute button
soundButtonOriginal = loadImage('soundButton.png')
soundButtonHover = loadImage('soundButtonHover.png')
soundButtonClicked = loadImage('soundButtonClicked.png')

muteButtonOriginal = loadImage('mutedButton.png')
muteButtonHover = loadImage('mutedButtonHover.png')
muteButtonClicked = loadImage('mutedButtonClicked.png')

#Class representing a button
class Button(object):
    #Initiating the object
    def __init__(self, rect, button, buttonHover, buttonClicked):
        self.image = button
        self.image_original = button
        self.image_hover = buttonHover
        self.image_clicked = buttonClicked
        self.rect = pygame.Rect(rect)
    
    #Checks if the mouse clicks
    def checkEvent(self, event):
        boolean = False
            
        #Activates the onRelease function if the mouse is released
        if event.type == pygame.MOUSEBUTTONUP:
            boolean = self.onRelease(event.pos)        
        
        return boolean
    
    #Changes the colour of the button if it is clicked and plays the sound effect
    def onClick(self, position):
        global buttonSound
        if self.rect.collidepoint(position):
            self.image = self.image_clicked
            
            #Plays sound effect if the sound is on
            global sound
            if sound:
                pygame.mixer.Sound.play(buttonSound)
    
    #Activates the function when the button is clicked
    def onRelease(self, position):
        if self.rect.collidepoint(position):
            return True
    
    #Changes colour if the mouse is hovering over the button
    def onHover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.image_hover
        else:
            self.image = self.image_original
    
    #Draws the button on the screen
    def draw(self, text, x, y):
        gameDisplay.blit(self.image, self.rect)
        messageDisplay(text, 30, black, x, y)

#Creates sound and muted buttons
global soundButton, muteButton, sound
soundButton_rect = muteButton_rect = soundButtonOriginal.get_rect(center=(750, 50))
soundButton = Button(soundButton_rect, soundButtonOriginal, soundButtonHover, soundButtonClicked)
muteButton = Button(muteButton_rect, muteButtonOriginal, muteButtonHover, muteButtonClicked)
sound = True

#Fills screen with the background image
class Background(pygame.sprite.Sprite):
    def __init__(self, path):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = loadImage(path)
        self.rect = self.image.get_rect()

#Displays text
def textObjects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

#Continues to display text
def messageDisplay(text, size, colour, x, y):
    font = pygame.font.SysFont('comicsansms',size)
    TextSurf, TextRect = textObjects(text, font, colour)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    
#If the movement goes past the screen
def pastScreen(value, extra):
    if value + extra > displayWidth:
        value = displayWidth - extra
    elif value < 0:
        value = 0
    return value

#Program to fire a bullet
def bulletMoving(player):
    global scramble, lastDirection1, lastDirection2

    #Code for player 1
    if player == player1:
        
        #Sets bullet at the player's location
        bullet = Bullet(lastDirection1, player1)
        bullet.rect.x = player1.rect.x
        bullet.rect.y = player1.rect.y
    
        if lastDirection1 == "right":
            bullet.rect.x = player1.rect.x + 107
            bullet.rect.y = player1.rect.y + 62
        if lastDirection1 == "left":
            bullet.rect.x = player1.rect.x + 3
            bullet.rect.y = player1.rect.y + 63
        if lastDirection1 == "up":
            bullet.rect.x = player1.rect.x + 44
            bullet.rect.y = player1.rect.y + 5
        if lastDirection1 == "down":
            bullet.rect.x = player1.rect.x + 65
            bullet.rect.y = player1.rect.y + 5

        
        bullets1List.add(bullet)
        
    #Code for player 2
    elif player == player2:
        
        #Sets bullet at the player's location
        bullet = Bullet(lastDirection2, player2)
        bullet.rect.x = player2.rect.x
        bullet.rect.y = player2.rect.y
    
        if lastDirection2 == "right":
            bullet.rect.x = player2.rect.x + 63
            bullet.rect.y = player2.rect.y + 20
        if lastDirection2 == "left":
            bullet.rect.x = player2.rect.x + 47
            bullet.rect.y = player2.rect.y + 20
        if lastDirection2 == "up":
            bullet.rect.x = player2.rect.x + 78
            bullet.rect.y = player2.rect.y + 16
        if lastDirection2 == "down":
            bullet.rect.x = player2.rect.x + 26
            bullet.rect.y = player2.rect.y + 17
            
        bullets2List.add(bullet)
    
    #Adds the bullet to the list of sprites and bullets
    allSpritesList.add(bullet)

#Plays a soundtrack
def playSoundtrack(path):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(-1)  #-1 causes music to loop forever   

#Manages sound and muted buttons
def soundMute(event, background, music):
    global sound, soundButton
    #Stops music if the mouse clicks on the sound button and shows muted sprite
    if soundButton.checkEvent(event) and sound == True:
        sound = False
        pygame.mixer.music.stop()
        global muteButton
    
    #Plays music if the mouse clicks on the mute button
    elif muteButton.checkEvent(event) and sound == False:
        sound = True
        playSoundtrack(music)
        gameDisplay.blit(background.image, (725, 28), area = (725, 28, 50, 45))

#Draws the lives
def drawLives(surface, x, y, lives):
    for i in range(lives):
        heart_rect = heart.get_rect(center=(x + 30 * i, y))
        surface.blit(heart, heart_rect)

#Gives the player an extra life
def newLife(player):
    player.lives += 1

#Makes the opposite player's movements the opposite of what they press
def scrambles(player):
    global scramble1, scramble2
    if player == player1:
        scramble2 = True
    else:
        scramble1 = True

#Gives the player double damage
def overpowered(player):
    global moreDamage1, moreDamage2
    if player == player1:
        moreDamage1 = True
    else:
        moreDamage2 = True

#Spawns power ups
def powerUp(surface):
    #Generates the power up to use
    number = random.randint(1, 3)
    
    #Determines where the power up is located
    x = random.randint(23, 778)
    if x < 100 or x > 700:
        y = random.randint(23, 800)
    else:
        #Spawns on the upper or lower ledge. upOrDown determines which side, with a 50% chance for each
        upOrDown = random.randint(0, 1)
        if upOrDown == 0:
            y = random.randint(23, 100)
        else:
            y = random.randint(700, 778)

    #Determines which of the three power ups to use
    if number == 1:
        extraLife = PowerUp('extraLife.png', 'usedExtraLife.png', x, y, newLife)
        powerUpsList.add(extraLife)
        extraLife.draw(True)
    elif number == 2:
        scrambleMoves = PowerUp('scrambleMoves.png', 'usedScrambleMoves.png', x, y, scrambles)
        powerUpsList.add(scrambleMoves)
        scrambleMoves.draw(True)
    elif number == 3:
        doubleDamage = PowerUp('doubleDamage.png', 'usedDoubleDamage.png', x, y, overpowered)
        powerUpsList.add(doubleDamage)
        doubleDamage.draw(True)

#Class representing a player
class PowerUp(pygame.sprite.Sprite):
    #Constructs the player
    def __init__(self, path, used, x, y, function):
        #Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        #Creates a sprite
        self.image = loadImage(path)
        self.function = function
        self.used = loadImage(used)
        
        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect(center=(x, y))
        
    #Checks if a player activates the power-up
    def collision(self, sprite):
        global usedPower1, usedPower2, usedPower, powerUpSound
        if sprite == player1: 
            if self.rect.colliderect(sprite.rect) and usedPower1 == usedPower:
                #Replaces the empty used slot with the used power up
                usedPower1 = self.used
                
                #Activates power up
                self.kill()
                self.function(player1)
                if sound:
                    pygame.mixer.Sound.play(powerUpSound)
        else:
            if self.rect.colliderect(sprite.rect) and usedPower2 == usedPower:
                #Replaces the empty used slot with the used power up
                usedPower2 = self.used
                
                #Activates power up
                self.kill()
                self.function(player2)
                if sound:
                    pygame.mixer.Sound.play(powerUpSound)
    
    #Draws the power-up
    def draw(self, boolean):
        if boolean:
            gameDisplay.blit(self.image, self.rect)
        else:
            gameDisplay.blit(self.image, (self.rect.x, self.rect.y - 5))

#Creates a game over screen
def gameOver(winner):
    global score1, score2
    
    #Changes background depending on the player who wins
    if winner == 1:
        playerWin = Background('player1Win.png')
        gameDisplay.blit(playerWin.image, (0, 0))  
        score1 += 1
    elif winner == 2:
        playerWin = Background('player2Win.png')
        gameDisplay.blit(playerWin.image, (0, 0))  
        score2 += 1
    
    #Creates buttons
    replayButton_rect = replayButtonOriginal.get_rect(center=(400, 400))
    menuButton_rect = menuButtonOriginal.get_rect(center=(400, 500))
    quitButton_rect = quitButtonOriginal.get_rect(center=(400, 600))
    
    replayButton = Button(replayButton_rect, replayButtonOriginal, replayButtonHover, replayButtonClicked)
    menuButton = Button(menuButton_rect, menuButtonOriginal, menuButtonHover, menuButtonClicked)
    quitButton = Button(quitButton_rect, quitButtonOriginal, quitButtonHover, quitButtonClicked)
    
    global soundButton, sound
    
    global playMenu, gameOverSound
    playMenu = False
    stopLoop = False
    
    #Displays score
    messageDisplay("Player 1 Score:", 19, white, 80, 550)
    messageDisplay("Player 2 Score:", 19, white, 720, 550)    
    messageDisplay(str(score1), 69, white, 70, 600)
    messageDisplay(str(score2), 69, white, 730, 600)
    
    #Plays sound
    if sound:
        pygame.mixer.Sound.play(gameOverSound)
        playSoundtrack('gameOverSoundtrack.wav') 
    
    #Loop with buttons
    while True:
        for event in pygame.event.get():
            #Quits game if the player exits the game
            if event.type == pygame.QUIT:
                quitGame()
            
            #Replays the game if the mouse clicks on the replay button
            if replayButton.checkEvent(event):
                clearLists()
                stopLoop = True
                break
            
            #Returns to main menu if the mouse clicks on the menu button
            if menuButton.checkEvent(event):
                playMenu = True
                stopLoop = True
                break
            
            #Manages sound and mute buttons
            soundMute(event, playerWin, 'gameOverSoundtrack.wav')
            
            #Quits the game if the mouse clicks on the quit button
            if quitButton.checkEvent(event):
                quitGame()
        
        #Stops the while loop
        if stopLoop:
            break
        
        #Changes colour if the player hover overs the button
        replayButton.onHover()
        menuButton.onHover()
        quitButton.onHover()
        if sound:
            soundButton.onHover()
        else:
            muteButton.onHover()
        
        #Changes colour if the player clicks the button
        if pygame.mouse.get_pressed()[0] == 1:
            replayButton.onClick(pygame.mouse.get_pos())
            menuButton.onClick(pygame.mouse.get_pos())
            quitButton.onClick(pygame.mouse.get_pos())
            if sound:
                soundButton.onClick(pygame.mouse.get_pos())
            else:
                muteButton.onClick(pygame.mouse.get_pos())
        
        #Updates the buttons
        replayButton.draw("Play again", 400, 400)
        menuButton.draw("Return to menu", 400, 500)
        quitButton.draw("Quit game", 400, 600)
        if sound:
            soundButton.draw("", 20, 20)
        else:
            muteButton.draw("", 20, 20)
            
        pygame.display.update()
    
    pygame.mixer.music.stop()

#Clears all the lists
def clearLists():
    global scramble1, scramble2, moreDamage1, moreDamage2, usedPower1, usedPower2, usedPower
    allSpritesList.empty()
    bullets1List.empty()
    bullets2List.empty()
    powerUpsList.empty()
    scramble1 = False
    scramble2 = False
    moreDamage1 = False
    moreDamage2 = False
    usedPower1 = usedPower
    usedPower2 = usedPower

#Quits pygame
def quitGame():
    replay = False
    pygame.quit()
    quit()

#Function of the starting menu
def menu():
    #Places background
    mainMenu = Background('MainMenu.png')
    gameDisplay.blit(mainMenu.image, mainMenu.rect)
    
    #Creates buttons
    playButton_rect = replayButtonOriginal.get_rect(center=(200, 400))
    instructionButton_rect = menuButtonOriginal.get_rect(center=(200, 500))
    quitButton_rect = quitButtonOriginal.get_rect(center=(200, 600))
    
    playButton = Button(playButton_rect, replayButtonOriginal, replayButtonHover, replayButtonClicked)
    instructionButton = Button(instructionButton_rect, menuButtonOriginal, menuButtonHover, menuButtonClicked)
    quitButton = Button(quitButton_rect, quitButtonOriginal, quitButtonHover, quitButtonClicked)
    global soundButton, sound
    
    #Sets variables and plays music
    stopLoop = False
    showInstructions = False
    if sound:
        playSoundtrack('menuSoundtrack.wav')
    
    #Loop with buttons
    while True:
        for event in pygame.event.get():
            #Quits game if the player exits the game
            if event.type == pygame.QUIT:
                quitGame()
            
            #Replays the game if the mouse clicks on the replay button
            if playButton.checkEvent(event):
                clearLists()
                stopLoop = True
                break
            
            #Jumps to instruction list if the mouse clicks on the instruction button
            if instructionButton.checkEvent(event):
                stopLoop = True
                showInstructions = True
                break
            
            #Manages sound and mute buttons
            soundMute(event, mainMenu, 'menuSoundtrack.wav')
            
            #Quits the game if the mouse clicks on the quit button
            if quitButton.checkEvent(event):
                quitGame()       
        
        if stopLoop:
            break
        
        #Changes colour if the player hover overs the button
        playButton.onHover()
        instructionButton.onHover()
        quitButton.onHover()
        if sound:
            soundButton.onHover()
        else:
            muteButton.onHover()
            
        #Changes colour if the player clicks the button
        if pygame.mouse.get_pressed()[0] == 1:
            playButton.onClick(pygame.mouse.get_pos())
            instructionButton.onClick(pygame.mouse.get_pos())
            quitButton.onClick(pygame.mouse.get_pos())
            if sound:
                soundButton.onClick(pygame.mouse.get_pos())
            else:
                muteButton.onClick(pygame.mouse.get_pos())           
        
        #Updates the buttons
        playButton.draw("Play game", 200, 400)
        instructionButton.draw("Instructions", 200, 500)
        quitButton.draw("Quit game", 200, 600)
        if sound:
            soundButton.draw("", 20, 20)
        else:
            muteButton.draw("", 20, 20)
            
        pygame.display.update()
    
    if showInstructions:
        instructions()
    
    pygame.mixer.music.stop()

#Function for the pause menu
def pause():
    #Places background image
    pauseScreen = Background('pauseScreen.png')
    gameDisplay.blit(pauseScreen.image, (0, 0))
    
    #Creates buttons
    resumeButton_rect = replayButtonOriginal.get_rect(center=(400, 400))
    menuButton_rect = menuButtonOriginal.get_rect(center=(400, 500))
    quitButton_rect = quitButtonOriginal.get_rect(center=(400, 600))
    
    resumeButton = Button(resumeButton_rect, replayButtonOriginal, replayButtonHover, replayButtonClicked)
    menuButton = Button(menuButton_rect, menuButtonOriginal, menuButtonHover, menuButtonClicked)
    quitButton = Button(quitButton_rect, quitButtonOriginal, quitButtonHover, quitButtonClicked)
    global soundButton, sound
    
    if sound:
        playSoundtrack('pauseSoundtrack.wav')
    
    global stopMenu, stopMain
    stopLoop = False
    #Loop with buttons
    while True:
        for event in pygame.event.get():
            #Quits game if the player exits the game
            if event.type == pygame.QUIT:
                quitGame()
            
            #Replays the game if the mouse clicks on the replay button
            if resumeButton.checkEvent(event):
                stopMain = False
                stopLoop = True
                break
            
            #Returns to main menu if the mouse clicks on the menu button
            if menuButton.checkEvent(event):
                stopMain = True
                stopLoop = True
                break
            
            #Manages sound and mute buttons
            soundMute(event, pauseScreen, 'pauseSoundtrack.wav')
            
            #Quits the game if the mouse clicks on the quit button
            if quitButton.checkEvent(event):
                quitGame()
                    
        #Stops the while loop
        if stopLoop:
            break
        
        #Changes colour if the player hover overs the button
        resumeButton.onHover()
        menuButton.onHover()
        quitButton.onHover()
        if sound:
            soundButton.onHover()
        else:
            muteButton.onHover()
            
        #Changes colour if the player clicks the button
        if pygame.mouse.get_pressed()[0] == 1:
            resumeButton.onClick(pygame.mouse.get_pos())
            menuButton.onClick(pygame.mouse.get_pos())
            quitButton.onClick(pygame.mouse.get_pos())
            if sound:
                soundButton.onClick(pygame.mouse.get_pos())
            else:
                muteButton.onClick(pygame.mouse.get_pos())             
        
        #Updates the buttons
        resumeButton.draw("Continue", 400, 400)
        menuButton.draw("Return to menu", 400, 500)
        quitButton.draw("Quit game", 400, 600)
        if sound:
            soundButton.draw("", 20, 20)
        else:
            muteButton.draw("", 20, 20)          
        
        pygame.display.update()
    
    pygame.mixer.music.stop()
        
#Function for the instruction page
def instructions():
    #Places background image
    instructions = Background('tutorial.png')
    gameDisplay.blit(instructions.image, (0, 0))  
    
    #Creates a button to return to main menu
    backButton_rect = quitButtonOriginal.get_rect(center=(180, 750))
    backButton = Button(backButton_rect, quitButtonOriginal, quitButtonHover, quitButtonClicked)
    global soundButton, sound
    
    if sound:
        playSoundtrack('pauseSoundtrack.wav')
    
    stopLoop = False
    while True:
        for event in pygame.event.get():
            #Quits game if the player exits the game
            if event.type == pygame.QUIT:
                quitGame()
            
            #Quits the game if the mouse clicks on the quit button
            if backButton.checkEvent(event):
                stopLoop = True
            
            #Manages sound and mute button
            soundMute(event, instructions, 'pauseSoundtrack.wav')
            
            #Updates the screen
            backButton.draw("Return to menu", 180, 750)          
        
        #Stops the while loop
        if stopLoop:
            break
        
        #Changes colour if the player hover overs the button
        backButton.onHover()
        if sound:
            soundButton.onHover()
        else:
            muteButton.onHover()  
        
        #Changes colour if the player clicks the button
        if pygame.mouse.get_pressed()[0] == 1:
            backButton.onClick(pygame.mouse.get_pos())
            if sound:
                soundButton.onClick(pygame.mouse.get_pos())
            else:
                muteButton.onClick(pygame.mouse.get_pos())               
        
        #Updates the buttons
        backButton.draw("Return to menu", 180, 750)
        if sound:
            soundButton.draw("", 20, 20)
        else:
            muteButton.draw("", 20, 20)
        
        pygame.display.update()
    
    pygame.mixer.music.stop()
    
    #Returns to the main menu
    menu()

#Class representing a player
class Player(pygame.sprite.Sprite):
    #Constructs the player
    def __init__(self, playerFront, playerRight, playerLeft, playerBack, rect):
        #Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        #Creates a sprite
        self.image = playerFront
        self.image_front = playerFront
        self.image_right = playerRight
        self.image_left = playerLeft
        self.image_back = playerBack
        self.lives = 3
        
        # Fetch the rectangle object that has the dimensions of the image
        self.rect = pygame.Rect(rect)
    
    def update(self, change_x, change_y, direction, extra, scramble):
        #Moves the player
        if not scramble:
            self.rect.x += change_x
            self.rect.y += change_y
        
        #Reverses direction of the movement if the player is affected by the scramble power up
        else:
            self.rect.x -= change_x
            self.rect.y -= change_y
            
        #Uses the sprite in the direction the player is moving in   
        if direction == "right":
            self.image = self.image_right
        if direction == "left":
            self.image = self.image_left
        if direction == "up":
            self.image = self.image_back
        if direction == "down":
            self.image = self.image_front 
                
        #Prevents player from going outside of the screen
        self.rect.x = pastScreen(self.rect.x, extra)
        self.rect.y = pastScreen(self.rect.y, extra)

#Class representing the bullet
class Bullet(pygame.sprite.Sprite):
    #Initializes the bullet
    def __init__(self, direction, player):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)       
        
        #Determines the sprite of the bullet, using direction and player
        if player == player1:
            
            #Loads images
            self.image_right = loadImage('bulletRight1.png')
            self.image_left = loadImage('bulletLeft1.png')
            self.image_back = loadImage('bulletUp1.png')
            self.image_front = loadImage('bulletDown1.png')
            
            #Determines the sprite used
            if direction == "right":
                self.image = self.image_right
            elif direction == "left":
                self.image = self.image_left
            elif direction == "up":
                self.image = self.image_back
            elif direction == "down":
                self.image = self.image_front
            
        elif player == player2:
            #Loads images
            self.image_right = loadImage('bulletRight2.png')
            self.image_left = loadImage('bulletLeft2.png')
            self.image_back = loadImage('bulletUp2.png')
            self.image_front = loadImage('bulletDown2.png')
            
            #Determines the sprite used
            if direction == "right":
                self.image = self.image_right
            elif direction == "left":
                self.image = self.image_left
            elif direction == "up":
                self.image = self.image_back
            elif direction == "down":
                self.image = self.image_front
        
        self.rect = self.image.get_rect()
        
        #Plays shooting sound
        global gunShotSound
        if sound:
            pygame.mixer.Sound.play(gunShotSound)
    
    def collision(self, sprite):
        return self.rect.colliderect(sprite.rect)
    
    #Updates the bullet's movement
    def update(self, boolean):
        #Moves the bullet
        if self.image == self.image_right:
            self.rect.x += 1
        elif self.image == self.image_left:
            self.rect.x -= 1
        elif self.image == self.image_front:
            self.rect.y += 1
        elif self.image == self.image_back:
            self.rect.y -= 1              

#Main program
def main():
    #Player movement keys
    global player1, player2, lastDirection1, lastDirection2
    
    #Initializing variables
    player1_change_x = 0
    player1_change_y = 0
    player2_change_x = 0
    player2_change_y = 0
    
    lastDirection1 = "down" #Used to determine which direction sprite to use
    lastDirection2 = "down" #For player 2
    
    global playMenu, playGameOver, scramble1, scramble2, sound
    finishGame = False
    stopMenu = False
    playGameOver = True
    playMenu = True
    
    #Images
    global heart
    heart = loadImage('heart.png')
    
    player1Front = loadImage('player1Front.png')
    player1Right = loadImage('player1Right.png')
    player1Left = loadImage('player1Left.png')
    player1Back = loadImage('player1Back.png')
    player1_rect = player1Front.get_rect(center=(10, 400))
    
    player2Front = loadImage('player2Front.png')
    player2Right = loadImage('player2Right.png')
    player2Left = loadImage('player2Left.png')
    player2Back = loadImage('player2Back.png')
    player2_rect = player1Front.get_rect(center=(750, 400))
    
    #Initializes players
    player1 = Player(player1Front, player1Right, player1Left, player1Back, player1_rect)
    allSpritesList.add(player1)
    player2 = Player(player2Front, player2Right, player2Left, player2Back, player2_rect)
    allSpritesList.add(player2)
    
    #Making pause button
    pauseButtonOriginal = loadImage('pauseButton.png')
    pauseButtonHover = loadImage('pauseButtonHover.png')
    pauseButtonClicked = loadImage('pauseButtonClicked.png')
    pauseButton_rect = pauseButtonOriginal.get_rect(center=(60, 60))
    pauseButton = Button(pauseButton_rect, pauseButtonOriginal, pauseButtonHover, pauseButtonClicked)
    
    #Initial drawing of icons
    drawLives(gameDisplay, 50, 150, player1.lives)
    drawLives(gameDisplay, 700, 150, player2.lives)
    
    #Initial time to spawn a power up (between 3 to 10 seconds)
    global spawnPowerUp
    spawnPowerUp = random.randint(3000, 10000)
    
    #Creates event to animate the power ups
    animate = pygame.USEREVENT + 1
    pygame.time.set_timer(animate, 500)
    upOrDown = True
    
    #Places background image
    background = Background('background.png')
    gameDisplay.blit(background.image, (0, 0))    
    
    #Creates a "3, 2, 1, GO"
    three = loadImage('3.png')
    two = loadImage('2.png')
    one = loadImage('1.png')
    go = loadImage('Go.png')
    numList = [three, two, one, go]
    
    three_rect = three.get_rect(center=(400, 400))
    two_rect = two.get_rect(center=(400, 400))
    one_rect = one.get_rect(center=(400, 400))
    go_rect = go.get_rect(center=(400, 400))
    rectList = [three_rect, two_rect, one_rect, go_rect]
    
    for i in range(len(numList)):
        gameDisplay.blit(numList[i], rectList[i])
        if sound:
            pygame.mixer.Sound.play(countdownSound)
        pygame.display.update()
        time.sleep(1)
        gameDisplay.blit(background.image, (0, 0))
        
    if sound:
        playSoundtrack('mainSoundtrack.wav')

    #Plays the game
    while True:
        for event in pygame.event.get():  #When the program gets a keystroke command

            #Quits game if the player exits the game
            if event.type == pygame.QUIT:
                quitGame()
            
            #Movement through keys
            if event.type == pygame.KEYDOWN:
                
                #WASD for player 1
                if event.key == pygame.K_w:
                    player1_change_y = -1
                    if scramble1:
                        lastDirection1 = "down"
                    else:
                        lastDirection1 = "up"
                elif event.key == pygame.K_a:
                    player1_change_x = -1
                    if scramble1:
                        lastDirection1 = "right"
                    else:
                        lastDirection1 = "left"
                elif event.key == pygame.K_s:
                    player1_change_y = 1
                    if scramble1:
                        lastDirection1 = "up"
                    else:
                        lastDirection1 = "down"
                elif event.key == pygame.K_d:
                    player1_change_x = 1
                    if scramble1:
                        lastDirection1 = "left"
                    else:
                        lastDirection1 = "right"
                
                #Arrow keys for player 2
                elif event.key == pygame.K_LEFT:
                    player2_change_x = -1
                    if scramble2:
                        lastDirection2 = "right"
                    else:
                        lastDirection2 = "left"
                elif event.key == pygame.K_RIGHT:
                    player2_change_x = 1
                    if scramble2:
                        lastDirection2 = "left"
                    else:
                        lastDirection2 = "right"
                elif event.key == pygame.K_UP:
                    player2_change_y = -1
                    if scramble2:
                        lastDirection2 = "down"
                    else:
                        lastDirection2 = "up"
                elif event.key == pygame.K_DOWN:
                    player2_change_y = 1
                    if scramble2:
                        lastDirection2 = "up"
                    else:
                        lastDirection2 = "down"
                
                #Bullet shooting keys
                elif event.key == pygame.K_z:
                    bulletMoving(player1)
                elif event.key == pygame.K_KP0: #KP0 stands for the 0 key on the keypad
                    bulletMoving(player2)
            
            #Do nothing when the key comes up
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player1_change_x = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player1_change_y = 0
                
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player2_change_x = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player2_change_y = 0
            
            #Activates pause menu
            if pauseButton.checkEvent(event):
                pause()
                if stopMain:
                    playGameOver = False
                    finishGame = True
                    break
                if sound:
                    playSoundtrack('mainSoundtrack.wav')
            
            #Changes whether the power up is up or down
            if event.type == animate:
                upOrDown = not upOrDown
    
        #Manages the buttons
        pauseButton.onHover()
        
        if pygame.mouse.get_pressed()[0] == 1:
            pauseButton.onClick(pygame.mouse.get_pos())

        #Manages power ups
        for i in powerUpsList:
            i.collision(player1)
            i.collision(player2)
            
        # Calculate mechanics for each bullet
        global winner
        
        for i in bullets1List:
            # See if it hit a player
            if i.collision(player2):
                i.kill()
                player2.lives -= 1
                if sound:
                    pygame.mixer.Sound.play(loseLifeSound)
                
                #Player takes double damage if the opponent has a double damage power up
                if moreDamage1 == True:
                    player2.lives -= 1
                
                #Quits game if the player dies
                if player2.lives <= 0:
                    winner = 1
                    finishGame = True
                    break
                
            # Remove the bullet if it goes past the screen
            if i.rect.x < 0 or i.rect.y > displayWidth or i.rect.x > displayWidth or i.rect.y < 0:
                bullets1List.remove(i)
                allSpritesList.remove(i)            
        
        # Calculate mechanics for each bullet
        for i in bullets2List:
            # See if it hit a player
            if i.collision(player1):
                i.kill()  
                
                player1.lives -= 1
                if sound:
                    pygame.mixer.Sound.play(loseLifeSound)
                
                #Player takes double damage if the opponent has a double damage power up
                if moreDamage2 == True:
                    player1.lives -= 1
                    
                #Quits game if the player dies
                if player1.lives <= 0:
                    winner = 2
                    finishGame = True
                    break
            
            # Remove the bullet if it goes past the screen
            if i.rect.x < 0 or i.rect.y > displayWidth or i.rect.x > displayWidth or i.rect.y < 0:
                bullets2List.remove(i)
                allSpritesList.remove(i)
        
        if finishGame:
            break
        
        #Updates background
        gameDisplay.blit(background.image, background.rect)
        
        #Updates all sprites
        player1.update(player1_change_x, player1_change_y, lastDirection1, 112, scramble1)
        player2.update(player2_change_x, player2_change_y, lastDirection2, 100, scramble2)
        bullets1List.update(not scramble1)
        bullets2List.update(not scramble2)
        
        #Updates the screen display
        allSpritesList.draw(gameDisplay)
        
        #Draws how many lives each player has
        drawLives(gameDisplay, 50, 150, player1.lives)
        drawLives(gameDisplay, 700, 150, player2.lives)
        
        #Drawing power ups (and idle animation)
        if upOrDown:
            powerUpsList.draw(gameDisplay)
        else:
            for i in powerUpsList:
                i.draw(False)

        gameDisplay.blit(usedPower1, (50, 175))
        gameDisplay.blit(usedPower2, (725, 175))
        
        #Checks if it's time to spawn another power up, spawns it if it is
        if pygame.time.get_ticks() > spawnPowerUp and len(powerUpsList) < 3:
            powerUp(gameDisplay)
            spawnPowerUp = pygame.time.get_ticks() + random.randint(3000,10000)        
        clock.tick()
        
        pauseButton.draw("", 60, 60)
    
    pygame.mixer.music.stop()

#Runs program
while replay:
    if playMenu:
        menu()
    main()
    if playGameOver:
        gameOver(winner)
quitGame()