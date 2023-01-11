'''
Trials of Xylia
By: Jessica and Joyce
June 5, 2020

Description:
Trials of Xylia is an adventure game that centers around a girl named Poppy
climbs a tower to grant her wish of saving her grandmother.

*side note: If you are currently on a level and you return to the main
            menu it will continue where you left of (as long as you don't exit the whole game).
            This is so that the player can adjust volume and return to where they left off.
            But if you beat a level and you don't press continue you will have to restart at the previous level.
            
'''
###IMPORTS###
from pygame import *
from random import *
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "20,20"

init()

###Screen Size
size = width, height = 1366, 800
screen = display.set_mode(size)

#########################COLOURS##########################

RED=(255,0,0,255)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
AQUA = (0,255,255,255)
WHITE = (255,255,255,255)
TAR = (67,66,65,255)
LAVA = (255,60,28,255)
ASTEROIDS = (82,79,80,255)
CLOUDS = (193,218,246,255)
PINK = (254,10,187,255)
GOALSKY = (139,229,187,255)
GOALSPACE = (212,248,246,255)

#########################GAME VARIABLES##############################
#INTRO AND OUTRO ANIMATION
introLength = -10500 #length of introPic
outroLength = -8000  #length of outroPic

#ENEMY ANIMATION
frame = 0            

#INDEXES
X=0 #x-coordinate
Y=1 #y-coordinate
W=2 #width
H=3 #height
BOT = 2 #bottom (for vGROUND list)

#GROUND LEVELS
#Floor Variables
floorHeight = 30 #height of each floor
GROUND = height-floorHeight #height of ground

jumpSpeed = -15 #jump power
gravity = 1 #gravity

playerWidth = 26 #width of player (for rect)
playerHeight = 35 #height of player

          #X #Y BOT
vGround=[0,0,GROUND] #velocity for ground levels (lvl 1 and 2)

#Forest variables
count = 0 #how long the platforms and the blobs move (will change direction when count reaches a certain number)
var = 1 #variable that changes direction of the platform and enemy movement

#FLYING LEVELS

rapid  = 5 #prevents player from spamming bullets (can only shoot bullets if rapid<5

#Lists
bullets = [] #list of bullets that ship shoots
enemies = [] #list of enemies

bg = [0,-9600] #length of background for scrolling levels
v = [0,20] #horizontal and vertical speed of bullets

level = "lev1" #for tracking current level player is on

###music
volume = 0.5 #variable for volume of music

#######################LOADING IMAGES##############################
#intro and outro images
introPic = image.load("images/introPic.png") 
outroPic = image.load("images/outroPic.png")

##########Main Menu
#pics of the cover page, instructions, story outline, credits
mainMenu = ["images/cover.png","images/instructions.png","images/outline.png","images/credits.png"]
#images of text on buttons
tabs = ["images/text/start.png","images/text/instructions.png","images/text/storyoutline.png","images/text/credits.png"]
#loading the pictures with loops
tabPics = [] 
menuPics = []
for m in mainMenu:
    menuPic = image.load(m).convert()
    menuPics.append(menuPic)
for t in tabs:
    tabPic = image.load(t).convert_alpha()
    tabPics.append(tabPic)

cleared = image.load("images/levelcleared.jpg").convert() #level cleared image
cont = image.load("images/text/continue.png").convert_alpha() #continue (text) 
introText = image.load("images/text/intro.png").convert_alpha() #watch intro (text)
##music
volDown = image.load("images/voldown.png").convert_alpha() #volume down
volUp = image.load("images/volup.png").convert_alpha() #volume up
volPics = [volUp,volDown] 
volText = image.load("images/text/volume.png").convert_alpha() #text that says "volume"

###GROUND LEVELS
#player
poppyR = image.load("images/poppy.png").convert_alpha()
poppyL = image.load("images/poppyl.png").convert_alpha()

#Desert
desertBg = image.load("images/desert.bmp").convert() #background
dDoor = image.load("images/desertdoor.png").convert_alpha() #desert door
desertDoor = transform.scale(dDoor,(60,85)) #resize
desertPlat = image.load("images/platform.png").convert()#desert platform

#Forest
forestBg = image.load("images/forest.bmp").convert() #background
fDoor = image.load("images/forestdoor.png").convert_alpha() #forest door
forestDoor = transform.scale(fDoor,(60,85)) #resize
forestPlat = image.load("images/grassplat.png").convert() #forest platform

###FLYING LEVELS
shipPic=image.load('images/ship1.png').convert_alpha()
bullPic = image.load('images/bull.png').convert_alpha()
#resizing ship
shipSize = 70
shipPic=transform.scale(shipPic,(shipSize,shipSize))
#Sky 
bgSky = image.load('images/sky.bmp').convert()
bgSpace = image.load("images/space.bmp").convert()

############################LOADING MUSIC###############################
#music
music = ["music/menusoundtrack.ogg","music/desertsoundtrack.ogg","music/forestsoundtrack.ogg","music/skysoundtrack.mp3",
         "music/spacesoundtrack.ogg","music/levelcleared.ogg"]
musicRects = [Rect(1170,720,60,60),Rect(1250,720,60,60)]

GREEN = (0,255,0,255)
myClock = time.Clock()

#######################################RECTS################################################
buttons=[Rect(50,250+y*120,550,90) for y in range(4)]#creating the buttons vertically
menuCommands = ["start_play","instructions","story","cr"]
clearedRect = Rect(283,500,800,150)
#########################GAME RECTS and Lists##################################
######GROUND LEVELS#########
player = [30,735,playerWidth,playerHeight] #player list [starting X,starting Y,width,height]
emptySpace = (height - floorHeight*4)/4 #space in between each floor
floorList = [Rect(0,height-floorHeight,width,floorHeight),Rect(0,height-floorHeight*2-emptySpace,width,floorHeight),
             Rect(0,height-floorHeight*3-emptySpace*2,width,floorHeight),
             Rect(0,height-floorHeight*4-emptySpace*3,width,floorHeight),(0,0,1366,5)] #list of floors
#DOORS
doorRects = [Rect(52,685,60,85),Rect(1320,170-87,60,85)] #list of doors

####LEVEL 1 DESERT #####
#PLATFORMS
platforms1 = [Rect(400,700,130,20),Rect(850,310,130,20),Rect(350,120,160,20),Rect(670,520,130,20)] #platforms for level 1

#PORTALS for level 1 and 2
portals1 = [Rect(1346,GROUND - emptySpace-1,20,emptySpace),Rect(1346,GROUND-emptySpace*2-floorHeight-1,20,emptySpace),
            Rect(1346,GROUND-emptySpace*3-floorHeight*2-1,20,emptySpace)]
portals2 = [Rect(0,GROUND-emptySpace*2-1-floorHeight,20,emptySpace),
            Rect(0,GROUND-emptySpace*3-floorHeight*2-1,20,emptySpace),
            Rect(0,GROUND-emptySpace*4-floorHeight*3-1,20,emptySpace)]

#ENEMIES
groundEnemies = [Rect(1030,730,45,40),Rect(450,525,45,45),
           Rect(1150,330,45,40),Rect(125,125,45,43),Rect(930,125,45,43)] #enemies for level 1

####LEVEL 2 FOREST#####
platforms2 = [Rect(300, 720, 60, 20),  Rect(420, 720, 60, 20),Rect(540, 720, 60, 20), 
             Rect(660, 720, 60, 20),Rect(130,120,100,20),Rect(400,520,170,20)] #platforms for level 2
groundEnemies2 = [Rect(975,730,45,40),Rect(140,330,45,40),Rect(140,530,45,40),
           Rect(900,530,45,40),Rect(340,330,45,40),Rect(540,330,45,40),Rect(450,125,45,43)] #enemies for level 2

########FLYING LEVELS##########
####LEVEL 3 SKY#####
ship = [width/2,600,shipSize,shipSize] #ship list [starting X,Y,width,height]

####################GAME FUNCTIONS##########################
def loadEnemies(col):
    '''
    This function takes a colour as a string, loads the enemy images and returns it as a list
    enemy images are all named after colours in the images/enemy/ folder
    '''
    pics = []
    for i in range(5):
        pics.append(image.load("images/enemy/"+col+"blob00"+str(i)+".png").convert_alpha())
    return pics

def playSong(song):
    '''
    Takes in a song and loads it, and plays it at the current volume (global variable)
    '''
    global volume
    mixer.music.load(song)
    mixer.music.play(-1)
    mixer.music.set_volume(volume)

def reset():
    '''
    resets levels
    '''
    global player,playerWidth, playerHeight,width,enemies,bg,level,bullets,animationLis
    player = [30,735,playerWidth,playerHeight] #player's original position
    ship = [width/2,600,shipSize,shipSize]     #ship's original position
    enemies = [] #resets enemies list and bullets list
    bullets = []
    bg[Y] = -9600 #scrolling background reset
    
################GROUND LEVELS###########################
def drawScene(screen,background,p,plats,doors,badGuys,doorPic,platPic,pics,frame):
    '''
    draws everything
    '''
    keys = key.get_pressed()
    screen.blit(background,(0,0)) #drawing background

    for plat in plats:            #drawing platforms
        pic = transform.scale(platPic,(plat[W],plat[H])) #rescaling image
        screen.blit(pic,plat)       
        
    for d in doors:               #drawing doors
        screen.blit(doorPic,(d[X]-40,d[Y])) #doors are drawn 40 pixels to the left
        #so that when the player exits the door (doorRect) it looks like they are leaving through
        #the middle

    for guy in badGuys:           #drawing enemies
        pic = transform.scale(pics[int(frame)],(guy[W],guy[H])) #resizing current frame at enemy's position
        screen.blit(pic,guy)
        
    if keys[K_LEFT]: #if the left arrow is pressed
        screen.blit(poppyL,(p[X],p[Y])) #draws Poppy facing left
    else:
        screen.blit(poppyR,(p[X],p[Y])) #draws Poppy facing right (default standstill position is facing right
        
    display.flip()

def move(p):
    'moving the player'
    keys = key.get_pressed()
    if keys[K_UP] and p[Y] + p[H] == vGround[BOT] and vGround[Y] == 0: 
        vGround[Y] = jumpSpeed           # player must be "sitting steady" on a platform/ground in order to jump

    if keys[K_LEFT] and p[X]>=8: #moves left if player's x-coord is greater than equal to 8 (prevents player from getting off-screen)
        vGround[X] = -5 #player's x position moves left 5 pixels
    elif keys[K_RIGHT] and p[X]<=width-21: #same as left but right
        vGround[X] = 5
    else:           
        vGround[X] = 0 #player does not move if nothing is pressed
    # move p
    
    p[X] += vGround[X] #moving left/right
    
    vGround[Y] += gravity #acceleration
            
def checkPlat(p,plats):
    'check if the player "lands" on a platform'
    if (hitWalls(p[X],p[Y],plats))!= -1 or hitWalls(p[X], p[Y],floorList)!=-1: #checks if player is not touching the base of a platform or the top of a floor
        vGround[Y] = 5 #ground velocity vertical direction is 5
    for plat in plats:
        if p[X]+p[W]>plat[X] and p[X]<plat[X]+plat[W] and p[Y]+p[H]<=plat[Y] and p[Y]+p[H]+vGround[Y]>plat[Y]:
            # if p is horizontally within the plat ends, and if it is going to cross the plat (after moving):
            vGround[BOT] = plat[Y]  #bottom is wherever the platform is
            p[Y] = vGround[BOT] - p[H] #sits player on plat
            vGround[Y] =0 #stops player from falling below plat

    p[Y] += vGround[Y] #falling down

    #Switches the GROUND depending on current floor (so that player does not fall to the first floor)
    if p[Y]<floorList[0][Y]: #if the player's Y is less than the height of the first floor
        GROUND = height - floorHeight #GROUND is the height (800) minus the height of the floor (30)
    if 370<=p[Y]<570:       
        GROUND = floorList[1][Y] #second floor base
    if 170<=p[Y]<370:
        GROUND = floorList[2][Y] #third floor base
    if 0<=p[Y]<170:
        GROUND = floorList[3][Y] #fourth floor base

    if p[Y]+p[H] >= GROUND:# if the player attempts to fall below the ground
        vGround[BOT] = GROUND #bottom is the the current floor
        p[Y] = GROUND - p[H] #sets player's Y-coord so it is sitting on top of the ground
        vGround[Y] = 0 #set vertical velocity to 0 so player doesn't fall below ground

def onPlat(p,plats):
    '''
    checks if the player is currently on a platform
    returns True if player is on a platform
    '''
    check = False
    for i in range(0,len(plats)):
        if p[X]+p[W]>=plats[i][X] and p[X]<=plats[i][X]+plats[i][W] and p[Y]+p[H]<=plats[i][Y] and p[Y]+p[H]+v[Y]>=plats[i][Y]:
            check = True
            return check    

def hitWalls(x,y,walls):
    '''
    checks if player is hitting the top of the floor or the bottom of the platform
    returns -1 if there are no collisions
    used in the checkPlat() function to prevent player from jumping through platforms and the floors
    '''
    playerRect = Rect(x,y,playerWidth,playerHeight) #player's rect
    return playerRect.collidelist(walls)

def colourCollision(p,col):
    '''
    gets the colour of an obstacle and checks to see if player contacts obstacle
    if player (one of the 4 corners) contacts obstacle then return player to original position (calls reset() function)
    checks top left, top right, bottom left, bottom right corners
    '''
    p[X],p[Y] = int(p[X]),int(p[Y])
    if screen.get_at((p[X],p[Y])) == col\
       or screen.get_at((p[X]+p[W],p[Y])) == col\
       or screen.get_at((p[X],p[Y]+p[3])) == col\
       or screen.get_at((p[X]+p[W],p[Y]+p[3])) == col:
        reset()

def teleport(portal1,portal2,p):
    '''
    teleports player to corresponding portals (using corresponding lists)
    '''
    pRect = Rect(p[X],p[Y],26,35)
    for i in range(len(portal1)): #checks all portals
        if pRect.colliderect(portal1[i]): #if player collides with a portal from portal1: teleport to corresponding portal from portal2
            p[X] = portal2[i][X]+25 #adds 25 to X to prevent the player from teleporting back and forth and continously colliding with the portal)
            p[Y] = portal2[i][Y]+50 #adds 50 so player does not come out from top of portal but middle-ish
        if pRect.colliderect(portal2[i]): #similar to top explanation
            p[X] = portal1[i][X]-25
            p[Y] = portal1[i][Y]+50
  
def enemyCollide(p,badGuys):
    '''
    checks if player rect collides with enemy
    if player rect collides with enemy then send player back to its original position (using reset() function)
    '''
    for guy in badGuys: #checking every enemy
        pRect = Rect(p[X],p[Y],playerWidth,playerHeight)
        if pRect.colliderect(guy):
            reset()


############FLYING LEVELS#################
def drawSceneFly(screen,background,ship,shipPic,bullets,badGuys,enemyPics,bullPics,speed):
    screen.blit(background,(bg[X],bg[Y])) #drawing the scrolling background
    screen.blit(shipPic,(ship[X],ship[Y])) #drawing the ship (player)
    for b in bullets: #drawing all the bullets in the list
        brect=Rect(b[0],b[1],10,20) #making a bullet rect
        screen.blit(bullPic,(brect)) #blitting bullet at its current position using the brect
 
    for guy in badGuys: #drawing all the enemies at their current frame
        screen.blit(enemyPics[int(frame)],guy)
        
    bg[Y]+=speed #scrolling the background 
    
    display.flip()
    
def movePlayer(player):
    keys = key.get_pressed()
    
    if keys[K_RIGHT] and player[X]<1280: #if right key is pressed (second part prevents player from getting off-screen (sets a boundary for the player)
        player[X]+=15 #player moves right 15 pixels
        
    if keys[K_LEFT] and player[X]>8: #if the left key is pressed (second part prevents player from getting off-screen (sets a boundary for the player)
        player[X]-=15 #player moves left 15 pixels

def moveEnemies(badGuys,goodX,goodY):
    '''
    makes enemies chase player
    '''
    for guy in badGuys:
        if goodX>guy[0]: #if player's X is greater than enemies' X they will move 2 to the right
            guy[0]+=2
        if goodX<guy[0]: #opposite to above explanation
            guy[0]-=2
        if goodY-51>guy[1]: #if player's Y is greater than enemies' Y they will move down (-51 prevents enemy from going past tip of the ship)
            guy[1]+=2
        else:
            guy[1]-=120 #this is so that if the enemy moves to the same Y position as the player it moves back up a bit so the player can still dodge it
            #or else it'd be impossible for the player to dodge it when it is in the same Y position from the side
            #enemy can still attack player from above if player doesn't dodge or hit it in time

def checkHits(bull,targ):
    '''
    checks if bullet hits target
    if bullet hits target
    remove the bullet and target
    '''
    for b in bull:
        for t in targ:
            brect=Rect(b[0],b[1],10,20) #bullet rect
            if brect.colliderect(t):
                targ.remove(t)
                bull.remove(b)
                break
                
def moveBullets(bull):
    for b in bull:
        b[1]-=b[3] #the y-coordinate of the bullet moves up by the bullet velocity
        b[0]+=b[2] #the x-coordinate doesn't change since both values are 0
        if b[1]>800:#removes bullet when it goes off-screen
            bull.remove(b)


def menu(action):
    global level,volume
    while action=="menu":
        for evnt in event.get():            
            if evnt.type == QUIT: #program stops if you exit from the main menu
                action="end"
        mx,my=mouse.get_pos() #gets position of mouse
        mb=mouse.get_pressed()
        screen.blit(menuPics[0],(0,0)) #blits cover image

        #this loop draws the button rects and blits the button text
        for i in range(len(buttons)):
            draw.rect(screen,(255,255,255),buttons[i],4)
            if buttons[i].collidepoint(mx,my): #if the mouse hovers over the button 
                    draw.rect(screen,(77,56,92),buttons[i],4)#rect changes colour to indicate you are currently on that button
            screen.blit(tabPics[i],(buttons[i])) #blitting the text
        #this loop draws the music rects and blits the volume up and down buttons
        for i in range(len(musicRects)):
            draw.rect(screen,WHITE,musicRects[i],4) #draws white rect
            screen.blit(volPics[i],(musicRects[i][X]+10,musicRects[i][Y]+15)) #blits images
            if musicRects[i].collidepoint(mx,my): #if mouse hovers over
                draw.rect(screen,(77,56,92),musicRects[i],4) #draws purple rect
        
        if mb[0]==1:                    
            if buttons[0].collidepoint(mx,my): #if you click on the "start" button
                #it calls the function of the current level you are on (default is level1)
                if level == "lev1":
                    level1(level)
                elif level == "lev2":
                    level2(level)
                elif level == "lev3":
                    level3(level)
                elif level == "lev4":
                    level4(level)
            if buttons[1].collidepoint(mx,my): #if you click on instructions
                instruct("instructions")       #calls instructions function
            if buttons[2].collidepoint(mx,my): #same as above but with the story outline
                outline("story")
            if buttons[3].collidepoint(mx,my): #same as above but credits
                credit("cr")
            if musicRects[0].collidepoint(mx,my): #volume up
                if volume<=1.0:               #if the current volume is less than the maximum
                    volume+=0.01              #increases the volume by 0.01
            if musicRects[1].collidepoint(mx,my):   #same as volume up except subtract
                if volume>0:
                    volume-=0.01
            mixer.music.set_volume(volume) #sets the volume 

        screen.blit(volText,(1170,660)) #blits the text that says "VOLUME"
        display.flip()
        myClock.tick(60)


def levelCleared(action,lvl):
    '''
    this displays after a player has cleared a level
    '''
    mixer.music.stop() #stops current music from playing
    mixer.music.load(music[5]) #loads "congratulations" music
    mixer.music.play()         #plays it
    mixer.music.set_volume(volume)#sets it at the current volume
    
    while action=="level cleared":
        for evnt in event.get():            
            if evnt.type == QUIT: #if you close it, return to menu
                action="menu"
                
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        
        screen.blit(cleared,(0,0)) #blits image of "Level Cleared"
        screen.blit(cont,(clearedRect)) #blits the "Continue" text
        draw.rect(screen,(255,255,255),clearedRect,4) #draws the continue rect (clearedRect)
        if clearedRect.collidepoint(mx,my): #hovering over it turns it PINK
            draw.rect(screen,PINK,clearedRect,4)
        if mb[0] == 1 and clearedRect.collidepoint(mx,my): #if you press it
            action = "lev"+str(lvl) #lvl is a number representing the next level
            if lvl == 2:
                reset() #resets player's position
                level2(action) #calls level two function
            elif lvl == 3: #refer to above
                reset()
                level3(action)
            elif lvl == 4:
                reset()
                level4(action)
        
        display.flip()
        myClock.tick(60)

def instruct(action):
    '''
    blits the instructions and returns to menu when you exit
    '''
    while action=="instructions":
        for evnt in event.get():            
            if evnt.type == QUIT:
                action="menu"
        screen.blit(menuPics[1],(0,0))
        display.flip()
        myClock.tick(60)

def outline(action):
    '''
    blits the storyOutline and returns to menu when you exit
    '''
    outlineRect = Rect(383,680,600,90) #this rect is for rewatching the intro
    while action=="story":
        for evnt in event.get():            
            if evnt.type == QUIT:
                action="menu"
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        
        screen.blit(menuPics[2],(0,0)) #story outline
        draw.rect(screen,WHITE,outlineRect,4) #draws white rect                
        if outlineRect.collidepoint(mx,my):   #changes to purple when you hover over
            draw.rect(screen,(77,56,92),outlineRect,4)
        screen.blit(introText,(outlineRect))  #blits the text: "Watch Intro"
        
        if mb[0] == 1 and outlineRect.collidepoint(mx,my): #if you click on the rect
            animate("animation",introPic,introLength) #calls the animate() function which will play the intro
        display.flip()
        myClock.tick(60)

def credit(action):
    '''
    blits the credits and returns to menu when you exit
    '''
    while action=="cr":
        for evnt in event.get():            
            if evnt.type == QUIT:
                action="menu"
        screen.blit(menuPics[3],(0,0))
        display.flip()
        
        myClock.tick(60)

def animate(action,pic,length):
    animationList = [0,0] #list of coordinates
    playSong(music[0]) #calls playSong() (plays intro music (theme))
    while action=="animation":
        for evnt in event.get():            
            if evnt.type == QUIT:
                action="menu"
        screen.blit(pic,(animationList[X],animationList[Y])) #blits the intro at the x,y positions in the list
        animationList[Y]-= 5 #image scrolls up by 5 pixels
        if animationList[Y]< length: #if the picture is done scrolling, return to menu
            menu("menu")

        display.flip()
        myClock.tick(60)
    
###############LEVEL FUNCTIONS################################
        
def level1(action):
    global player,playerWidth,playerHeight,frame
    level = "lev1" #current level
    playSong(music[1]) #calls playSong() and plays first level's theme
    while action=="lev1":
        for evnt in event.get():            
            if evnt.type == QUIT:
                mixer.music.stop() #stops first theme
                playSong(music[0]) #plays main menu theme
                action="menu"

        ###CALLING FUNCTIONS
        
        drawScene(screen,desertBg,player,platforms1,doorRects,groundEnemies,desertDoor,desertPlat,loadEnemies("purple"),frame)
        move(player)
        checkPlat(player,platforms1)
        teleport(portals1,portals2,player)
        colourCollision(player,TAR)
        enemyCollide(player,groundEnemies)

        #enemy animation 
        frame+=0.1 #the frame increases by 0.1
        if frame >= 5: #if the frame is greater than 5 
            frame = 0  #becomes 0 

        #checking for passing the level
        playerRect = Rect(player[X],player[Y],26,35) #making a rect for the player
        if playerRect.colliderect(doorRects[1]):     #if you collide with the doorRect
            action = "level cleared"
            levelCleared(action,2) #calls levelCleared() function

                
        display.flip()
        myClock.tick(60)


def level2(action): #refer to level 1 for majority of code
    global player,count,var,frame,level
    level = "lev2"
    playSong(music[2])
    while action=="lev2":
        for evnt in event.get():            
            if evnt.type == QUIT:
                mixer.music.stop()
                playSong(music[0])
                action="menu"

        ###Calling functions
        drawScene(screen,forestBg,player,platforms2,doorRects,groundEnemies2,forestDoor,forestPlat,loadEnemies("aqua"),frame)
        move(player)
        checkPlat(player,platforms2)
        teleport(portals1,portals2,player)
        colourCollision(player,LAVA)
        enemyCollide(player,groundEnemies2)

        #enemies movement
        for e in groundEnemies2:
            e[X]+=var #enemy travels var pixels

        #turning directions
        count+=var
        if count ==  100 or count == 0: #if count == 100 or 0
            var = var*-1 #var changes signs and the enemies and plats will move in the opposite direction

        #moving platforms
        for i in range(0,len(platforms2)):
            platforms2[i][X] +=var


        if onPlat(player,platforms2) == True: #calls onPlat() to check if player is on platform
            player[X]+=var #if player is on platform it will move along with it

       #enemy animation
        frame+=0.1
        if frame >= 5:
            frame = 0

        #checking to pass the level
        playerRect = Rect(player[X],player[Y],26,35)
        if playerRect.colliderect(doorRects[1]):
            action = "level cleared"
            levelCleared(action,3)
        
        display.flip()
        myClock.tick(60)
        

def level3(action):
    global frame,rapid,enemies,level
    level = "lev3" #current level
    playSong(music[3])
    while action=="lev3":
        for evnt in event.get():            
            if evnt.type == QUIT:
                mixer.music.stop() #stops current music
                playSong(music[0]) #plays main menu theme
                action="menu"

        #CALLING FUNCTIONS        
        movePlayer(ship)
        moveBullets(bullets) 
        checkHits(bullets,enemies)
        moveEnemies(enemies,ship[X],ship[Y])
        drawSceneFly(screen,bgSky,ship,shipPic,bullets,enemies,loadEnemies("red"),bullPic,4)
        colourCollision(ship,CLOUDS)
        enemyCollide(ship,enemies)

        keys=key.get_pressed()

        #makes sure player cannot spam bullets
        if rapid<5:
            rapid+=1

        #player can only shoot bullets if rapid is 5
        if keys[32] and rapid == 5:  #if you press the spacebar and rapid is 5
            bullets.append([ship[X]+5,ship[Y],v[0],v[1]]) #add 2 bullets to the list
            bullets.append([ship[X]+50,ship[Y],v[0],v[1]])
            rapid = 0 #set rapid back to 0

        #refills enemies list with enemies at a random position near the top when all enemies are gone
        if len(enemies) == 0:
            enemies = [Rect(randint(0,1366-80),10,80,60)]

        #enemy animation
        frame+=0.1
        if frame >= 5:
            frame = 0

        ###checking for passing the level
        ship[X] = int(ship[X])
        ship[Y] = int(ship[Y])
        #if the top left or top right corner's colour is GOALSKY (end of level)
        if screen.get_at((ship[X],ship[Y])) == GOALSKY or screen.get_at((ship[X]+shipSize,ship[Y])) == GOALSKY:
            action = "level cleared"
            levelCleared(action,4) #call levelCleared()
                         
        display.flip()
        myClock.tick(60)

def level4(action):
    global frame,rapid,enemies,level
    level = "lev4"
    playSong(music[4])
    while action=="lev4":
        for evnt in event.get():            
            if evnt.type == QUIT:
                mixer.music.stop()
                playSong(music[0])
                action="menu"
        
        movePlayer(ship)
        moveBullets(bullets)
        moveEnemies(enemies,ship[X],ship[Y])
        checkHits(bullets,enemies)
        drawSceneFly(screen,bgSpace,ship,shipPic,bullets,enemies,loadEnemies("green"),bullPic,7)
        colourCollision(ship,ASTEROIDS)
        enemyCollide(ship,enemies)

        keys=key.get_pressed()

        if rapid<5:
            rapid+=1

        if keys[32] and rapid == 5:  
            bullets.append([ship[X]+5,ship[Y],v[0],v[1]])
            bullets.append([ship[X]+50,ship[Y],v[0],v[1]])

            rapid = 0
            
        if len(enemies) == 0:
            enemies = [Rect(randint(0,1366-80),10,80,60) for i in range(2)]
        
        frame+=0.1
        if frame >= 5:
            frame = 0
  
        ship[X] = int(ship[X])
        ship[Y] = int(ship[Y])
        if screen.get_at((ship[X],ship[Y])) == GOALSPACE\
           or screen.get_at((ship[X]+shipSize,ship[Y])) == GOALSPACE:
            action = "animation"
            level = "lev1"
            animate("animation",outroPic,outroLength)
        #instead of calling the next level
        #calls the animate() and plays the outro
        #sets level back to lev1
                         
        display.flip()
        myClock.tick(60)

###MAIN PROGRAM
animate("animation",introPic,introLength) #calls animate() and plays intro
menu("menu") #calls menu

quit()


