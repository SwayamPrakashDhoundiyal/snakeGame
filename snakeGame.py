import pygame
import random

pygame.init()
pygame.mixer.pre_init()
pygame.display.set_caption('Snake Game')

SCREEN_WIDTH = 400 #screen width   
SCREEN_HEIGHT = 300 #screen height

MENU_WIDTH = 300 #menu width
MENU_HEIGHT = 200 #menu height

fontLocation = 'static\joystix monospace.otf'

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) #initializing screen
snake = pygame.Rect(200,50,10,10) #making the snake block
food = pygame.Rect(200,250,10,10) #making the food rect(/block)
selectionRect = pygame.Rect(300,200,10,10) #making the selection rect for the menu
menu = pygame.Rect(100,75,MENU_WIDTH,MENU_HEIGHT) #making menu rect for death and pause menu
menu.center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2)

run = True #condition for the game loop to run
resume_game = True #codition for the game to pause
death = False #condition for the game to be in death window

move_snake = pygame.USEREVENT +1 #custom event to map on func moveSnake
FOOD_EAT = pygame.USEREVENT +2

dir_m = [-1,0] #direction to move in current frame

font_title = pygame.font.Font('static\joystix monospace.otf',32) #intializing font for titles
text_Title = font_title.render('Game Over',True,(0,0,0))
textTitle_rect = text_Title.get_rect()
textTitle_rect.center = (SCREEN_WIDTH/2,((SCREEN_HEIGHT/2)-50))

font_options = pygame.font.Font('static\joystix monospace.otf',17) #intialising font for options
scorefont_options = pygame.font.Font('static\joystix monospace.otf',8)

font_instruction = pygame.font.Font('static\joystix monospace.otf',12) #initialsing font for instruction
text_instruction = font_instruction.render('Press A to select',True,(0,0,0))
textInstruction_rect = text_instruction.get_rect()
textInstruction_rect.center = (SCREEN_WIDTH/2,((SCREEN_HEIGHT/2)+ 50))

option_gameOver = ['Retry','Quit']
currOption_list = []

foodPos = [200,250]

snakePos:list = [310,50]
snakeBody:list = [[310,50],[320,50],[330,50],[340,50]]

usr_selection = 0

#variable used in the main menu ->
pygame.mixer.init()
main_Title = font_title.render('Snake Game',True,(255,255,255)) #main menu title
mainTitle_rect = text_Title.get_rect()
mainTitle_rect.center = (SCREEN_WIDTH/2,((SCREEN_HEIGHT/2)-50))


option_mainMenu = ['Play','Quit'] #main menu option

startGame = False

bgMusic = "static/bgMusic.mp3" #channel 0
selectSfx = 'static/Select.wav' #channel 1
foodSfx = 'static/ate.wav' #channel 2
hiscoreSfx = 'static/HighScore.wav' #channel 3
deathSfx = 'static/death.wav' #channel 4
score = 0   #score of the player 
highScore = 0 #highest score ever gone

def optionRender(optionList:list, idx:int,textColor:tuple):
    """Rendering option from the list that is passed on argument, then match the option that should be selected with the argument.

    Args:
        optionList (list): list containing the options
        idx (_type_):  index of the option that is to be selected
    """
    global selectionRect
    global usr_selection
    
    pos_y = ((SCREEN_HEIGHT/2)-50) - 10 #position on x for the initial option
    pos_x = SCREEN_WIDTH/2 #position on y for the initial option
    selectionRect = pygame.Rect(pos_x,pos_y,100,20) #re-initialsing the selection rect
    center = () #tuple for storing center position of selection rect
    
    if idx < 0: #conditions to check wheather the value is out of scope
        usr_selection = len(optionList) - 1
        idx = len(optionList) - 1
    elif idx > len(optionList) - 1:
        usr_selection = 0
        idx = 0
   
    for index ,option in enumerate(optionList): #loop through the list and render the options
        pos_y = pos_y + 30 #change y postion of option to create a space of 30 pixels
        text = option
        font = font_options
        textrender = font.render(text,True,textColor)
        text_rect = textrender.get_rect()
        text_rect.center = (pos_x,pos_y + 10)
        if index == idx: #if the option and the selection are of same index draw a box to show it is selected
            center = text_rect.center
        screen.blit(textrender,text_rect)
    selectionRect.center = center
    pygame.draw.rect(screen,textColor,selectionRect,2)

def highscore(score:int):
    """checks and load highscore from the .save file

    Args:
        score (int): current score

    Returns:
        string: highgest score by player
    """
    save = open('score.save','a+')
    save.seek(0)
    for each in save:
        if int(each) < score:
            save.close()
            save = open('score.save','w')
            save.write(str(score))
            save.close()
            return score
        else:
            save.close()
            return int(each)
    save.write(str(0))
    return 0
    

def checkScore():
    """checks and sets score and highcore variables
    """
    global score
    global highScore
    score = score + 10
    if score > highscore(score):
        highScore = score
    else:
        highScore = highscore(score)

def restart():
    """simply resetting everything to the original state
    """
    global SCREEN_WIDTH
    SCREEN_WIDTH = 400 #screen width   
    global SCREEN_HEIGHT
    SCREEN_HEIGHT = 300 #screen height
    global MENU_WIDTH
    MENU_WIDTH = 300 #menu width
    global MENU_HEIGHT
    MENU_HEIGHT = 200 #menu height
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) #initializing screen
    global snake
    snake = pygame.Rect(300,250,10,10) #making the snake block
    global food
    food = pygame.Rect(200,250,10,10) #making the food rect(/block)
    global selectionRect
    selectionRect = pygame.Rect(300,200,10,10) #making the selection rect for the menu
    global menu
    menu = pygame.Rect(100,75,MENU_WIDTH,MENU_HEIGHT) #making menu rect for death and pause menu
    menu.center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
    global run
    run = True #condition for the game loop to run
    global resume_game
    resume_game = True #codition for the game to pause
    global death
    death = False #condition for the game to be in death window
    global move_snake
    move_snake = pygame.USEREVENT +1 #custom event to map on func moveSnake
    global FOOD_EAT
    FOOD_EAT = pygame.USEREVENT +2
    global dir_m
    dir_m = [-1,0] #direction to move in current frame
    global font_title
    font_title = pygame.font.Font('static\joystix monospace.otf',32) #intializing font for titles
    global text_Title
    text_Title = font_title.render('Game Over',True,(0,0,0))
    global textTitle_rect
    textTitle_rect = text_Title.get_rect()
    textTitle_rect
    textTitle_rect.center = (SCREEN_WIDTH/2,((SCREEN_HEIGHT/2)-50))
    global font_options
    font_options = pygame.font.Font('static\joystix monospace.otf',17) #intialising font for options
    global font_instruction
    font_instruction = pygame.font.Font('static\joystix monospace.otf',12) #initialsing font for instruction
    global text_instruction
    text_instruction = font_instruction.render('Press A to select',True,(0,0,0))
    global textInstruction_rect
    textInstruction_rect = text_instruction.get_rect()
    textInstruction_rect
    textInstruction_rect.center = (SCREEN_WIDTH/2,((SCREEN_HEIGHT/2)+ 50))
    global option_gameOver
    option_gameOver = ['Retry','Quit']
    global currOption_list
    currOption_list = []
    global foodPos
    foodPos = [200,250]
    global snakePos
    snakePos = [310,50]
    global snakeBody
    snakeBody = [[310,50],[320,50],[330,50],[340,50]]
    global usr_selection
    usr_selection = 0
    global score
    score = 0

def performOption(optionList:list, idx:int):
    """matching the option with the functions that are to be ran

    Args:
        optionList (list): list of the option from which it was selected
        idx (int): the option that is selected
    """
    term = optionList[idx]
    playSound(1)
    match term:
        case 'Retry':
            restart()
        case 'Quit':
            global run
            run = False
        case 'Play':
            global startGame
            startGame = True

def resume():
    """changing the state of the game from pause to unpase and vice versa
    """
    global resume_game
    resume_game = not resume_game

def menuRender(idx,op_idx):
    """rendering the menu on the basis of what kind of menu is needed

    Args:
        idx (int): the menu that is needed to be render it's index
        op_idx (int): the index of the first option to be selected
    """
    global currOption_list
    if idx == 0:
        pygame.draw.rect(screen,(255,255,255),menu)
        screen.blit(text_Title,textTitle_rect)
        optionRender(option_gameOver,op_idx,(0,0,0))
        currOption_list = option_gameOver
        screen.blit(text_instruction,textInstruction_rect)
        
    elif idx == 1:
        screen.blit(main_Title,mainTitle_rect)
        optionRender(option_mainMenu,op_idx,(255,255,255))
        currOption_list = option_mainMenu
        screen.blit(text_instruction,textInstruction_rect)

def playSound(channel: int):
    """Play the sfx on the corresponding channel and with a set/ fixed volume

    Args:
        channel (int): the channel that has the sfx that is to pe played
    """
    match channel:
        case 0:
            if not pygame.mixer.Channel(0).get_busy():
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(bgMusic),loops=-1)
                pygame.mixer.Channel(0).set_volume(0.2)
        case 1:
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(selectSfx))
            pygame.mixer.Channel(1).set_volume(0.5)
        case 2:
            pygame.mixer.Channel(2).play(pygame.mixer.Sound(foodSfx))
            pygame.mixer.Channel(2).set_volume(0.5)
        case 3:
            pygame.mixer.Channel(3).play(pygame.mixer.Sound(hiscoreSfx))
            pygame.mixer.Channel(3).set_volume(0.6) 
        case 4:
            pygame.mixer.Channel(4).play(pygame.mixer.Sound(deathSfx))
            pygame.mixer.Channel(4).set_volume(0.7)      
        

def foodSpawn(spawn:bool):
    """Makes our food block(/ rect), and initialises it with a random postion within the window 

    Returns:
        Rect: food rect with random positon.
    """
    global foodPos
    global food
    if spawn:
        pos = [random.randrange(1, ((SCREEN_WIDTH - 20)//10)) * 10, 
                          random.randrange(1, ((SCREEN_HEIGHT - 20)//10)) * 10]
        foodPos = pos
    food = pygame.Rect(foodPos[0],foodPos[1],10,10)
    #pos = rollpos([20,100],[20,100])
    

def activeDeathWin():
    """activation the death state
    """
    global death
    death = True
    

def game_over(idx):
    """doing the rendering process for death state

    Args:
        idx (int): wheather to just quit or display the menu
    """
    if idx == 0:
        resume()
        activeDeathWin()

def redrawSnake(DrawQueue:list):
    """Clear the screen then redraw all the components needed, take the snake components needed from DrawQueue

    Args:
        DrawQueue (list): drawing queue
    """
    for pos in snakeBody:
        pygame.draw.rect(screen, (255,255,255),
                         pygame.Rect(pos[0], pos[1], 10, 10))

def snakeBodyCol():
    """checks for collision of the head with it's own body and the window collision
    """
    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            game_over(0)
            playSound(4)
    if snakePos[0] < 0 or snakePos[0] > SCREEN_WIDTH or snakePos[1] < 0 or snakePos[1] > SCREEN_HEIGHT:
            game_over(0)
            playSound(4)

def moveSnake(dir_m:list):
    """make the snake move in the direction per frame.

    Args:
        dir (1D array): to store the vector of position in which we have to move
    """
    global food
    snakePos[0] += dir_m[0] * 10
    snakePos[1] += dir_m[1] * 10
    snakeBody.insert(0, list(snakePos))
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        checkScore()
        foodSpawn(True)
        playSound(2)
    else:
        snakeBody.pop()


while run: #game loop
    screen.fill((0,0,0)) #clear screen to redraw
     
    gameClock = pygame.time.Clock()
    
    for event in pygame.event.get(): #event loop
        if event.type == pygame.QUIT: #take user inputs
            run = False
            
        if event.type == pygame.KEYDOWN: #check for which key is pressed
            if event.key == pygame.K_ESCAPE and not death and startGame:
                resume()
            if resume_game and not death and startGame:
                if event.key == pygame.K_DOWN and dir_m[1] != -1: #go down
                    dir_m = [0,1]
                elif event.key == pygame.K_UP and dir_m[1] != 1: #go up
                    dir_m = [0,-1]
                elif event.key == pygame.K_LEFT and dir_m[0] != 1: #go left
                    dir_m = [-1,0]
                elif event.key == pygame.K_RIGHT and dir_m[0] != -1: #go right
                    dir_m = [1,0]
                elif event.key == pygame.K_d:
                    game_over(0)
            elif death:
                if event.key == pygame.K_DOWN:
                    usr_selection = usr_selection + 1
                elif event.key == pygame.K_UP:
                    usr_selection = usr_selection - 1
                elif event.key == pygame.K_a:
                    performOption(currOption_list,usr_selection)

            elif not startGame:
                if event.key == pygame.K_DOWN:
                    usr_selection = usr_selection + 1
                elif event.key == pygame.K_UP:
                    usr_selection = usr_selection - 1
                elif event.key == pygame.K_a:
                    performOption(currOption_list,usr_selection)
        
    if startGame:    
        if resume_game:
            moveSnake(dir_m)
            snakeBodyCol()
    
        redrawSnake(snakeBody)
        pygame.draw.rect(screen,(0,255,0),food)
    
        if death:
            menuRender(0,usr_selection)
    else:
        menuRender(1,usr_selection)
        highScore = highscore(0)

    font = scorefont_options
    scorerender = font.render('Score: ' + str(score),True,(255,255,255))
    score_rect = scorerender.get_rect()
    score_rect.center = (40,0 + 10)
    screen.blit(scorerender,score_rect)
    
    font = scorefont_options
    hiscorerender = font.render('HighScore: '+ str(highScore),True,(255,255,255))
    hiscore_rect = hiscorerender.get_rect()
    hiscore_rect.center = (300,0 + 10)
    screen.blit(hiscorerender,hiscore_rect)
     
    playSound(0)    
    pygame.display.update() #updating the screen again    
    gameClock.tick(16)


pygame.quit() #close the window