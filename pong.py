#!/usr/bin/python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation, 
follow along in the tutorial.
"""


#Import Modules
import os, pygame
from pygame.locals import *

import random
import time

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')


pygame.mixer.init(44100, 16) # 44100 KHz, 16 bit
#print (pygame.mixer.get_init())

AREA_X = 800 # 1200 #1920
AREA_Y = 400 # 700 #1920
SCREEN_X = 800 # 1200 #1920
SCREEN_Y = 500 # 800 #980  
AREA_X_MARGIN = (SCREEN_X - AREA_X) / 2  # split left and right side
AREA_Y_MARGIN = (SCREEN_Y - AREA_Y)  # top scoreboard height
PADDLE_SPEED = 10
BALL_SPEED = 9 


#functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # TODO # try:
    image = pygame.image.load(fullname)
    #except pygame.error, message:
    #    print ('Cannot load image:', fullname)
    #    raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    # TODO # try:
    sound = pygame.mixer.Sound(fullname)
    #except pygame.error, message:
    #    print ('Cannot load sound:', fullname)
    #    raise SystemExit, message
    return sound


#classes for our game objects
class Paddle(pygame.sprite.Sprite):
    """moves a paddle on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('paddle.bmp', -1)
        self.direction = 0
        self.rect.left = 10 + AREA_X_MARGIN
        self.rect.top = AREA_Y_MARGIN + (AREA_Y / 2)
        self.point = 0
        self.side = 0
        self.computer = 0

    def update(self):
        if ( self.computer == 1 ): 
            if ( self.ball.rect.centery < self.rect.top ):
                self.direction = 1 # up
            elif ( self.ball.rect.centery > self.rect.bottom ):
                self.direction = -1 # down
            else:
                self.direction = 0 # stay put 


        if ( self.direction == 1 ):  # up
            if ( self.rect.top >= PADDLE_SPEED + AREA_Y_MARGIN ):
                self.rect.top -= PADDLE_SPEED
            else:
                self.rect.top = AREA_Y_MARGIN
        elif ( self.direction == -1 ): # down
            if ( self.rect.bottom < SCREEN_Y - PADDLE_SPEED - 1 ):
                self.rect.bottom += PADDLE_SPEED
            else:
                self.rect.bottom = SCREEN_Y - 1
              
             


    def SetDirection(self, direction):
        self.direction = direction 

    def SetSide(self, side):
       # side=0 is the left side, side=1 is the right side
        self.side = side
        if ( side == 0 ):
          self.rect.left = 10 + AREA_X_MARGIN          
        else :
          self.rect.right = AREA_X - AREA_X_MARGIN - 10

    def SetComputer(self, computer):
        self.computer = computer 

    def SetBall(self, ball):
        self.ball = ball 

    def IncPoint(self):
        self.point = self.point + 1
        self.point_sound.play() 
        time.sleep(2)

    def SetPointSound(self, point_sound):
        self.point_sound = point_sound 



class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('ball.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (AREA_X/2) + AREA_X_MARGIN, (AREA_Y/2) + AREA_Y_MARGIN
        self.move_x = BALL_SPEED / 2
        self.move_y = BALL_SPEED / 2
        self.speed = BALL_SPEED
        #self.dizzy = 0

    def update(self):
        self._fly()

    def CalcVector(self, paddle):
        if ( ( ( paddle.side == 0 ) and ( self.move_x < 0 ) ) or
             ( ( paddle.side == 1 ) and ( self.move_x > 0 ) )    )  :    
            # Ball must be moving left against the left paddle, or moving right
            # against the right paddle, or the vector will not be changed.  This helps
            # 'debounce' the hits to prevent multiple changes on one hit
           
            diff_y = (self.rect.centery - paddle.rect.centery)  #  Calculate whether ball is above or below
            self.move_y = (self.speed * 4 * diff_y) / (3 * paddle.rect.height)  #  Calculate new y component of vector, which is from {-2/3 to +2/3} * speed depending on hit location
            self.move_x = self.speed - abs(self.move_y)  #  Calculate new x magnitude of vector, which is speed - move_y so that ball vector magnitude is |speed|.
            self.move_x = self.move_x * (1 - 2*paddle.side) # Calculate sign of new x component of vector (left or right movement)
            print (self.speed, self.move_x, self.move_y)
            self.hit_sound.play() 
            self.speed = self.speed + 1
                                                        
    def _fly(self):
        if self.rect.left < self.area.left: 
            self.paddle2.IncPoint()
            print ("Paddle2 point! ", self.paddle2.point)
            self.rect.topleft = (AREA_X/2) + AREA_X_MARGIN, (AREA_Y/2) + AREA_Y_MARGIN
            self.move_x = BALL_SPEED / 2
            self.move_y = BALL_SPEED / 2
            self.speed = BALL_SPEED

        if self.rect.right > self.area.right:
            self.paddle1.IncPoint()
            print ("Paddle1 point! ", self.paddle1.point)
            self.rect.topleft = (AREA_X/2) + AREA_X_MARGIN, (AREA_Y/2) + AREA_Y_MARGIN
            self.move_x = - BALL_SPEED / 2
            self.move_y = BALL_SPEED / 2
            self.speed = BALL_SPEED

        if self.rect.top < (self.area.top + AREA_Y_MARGIN): 
            self.move_y = abs(self.move_y)

        if self.rect.bottom > self.area.bottom: 
            self.move_y = - abs(self.move_y)

        if self.rect.colliderect(self.paddle1):
            self.CalcVector(self.paddle1)

        if self.rect.colliderect(self.paddle2):
            self.CalcVector(self.paddle2)


        newpos = self.rect.move((self.move_x, self.move_y))
        self.rect = newpos

    def SetPaddle1(self, paddle1):
        self.paddle1 = paddle1

    def SetPaddle2(self, paddle2):
        self.paddle2 = paddle2

    def SetHitSound(self, hit_sound):
        self.hit_sound = hit_sound 



def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption('Pong!')
    pygame.mouse.set_visible(0)

#Create The Backgound
    #background = pygame.Surface(screen.get_size())
    background = pygame.Surface( (AREA_X, AREA_Y) )
    background = background.convert()
    background.fill((0, 0, 50)) # RGB = dark blue

    scoreboard = pygame.Surface( (SCREEN_X, AREA_Y_MARGIN) )
    scoreboard = scoreboard.convert()
    scoreboard.fill((0, 0, 100)) # RGB = medium-dark blue

#Put Text On The Background, Centered
    if pygame.font:
        #font = pygame.font.Font(None, 36)

        titlefont= pygame.font.Font("data/TrueType/SFDigitalReadout-Medium.ttf", 72)
        titletext = titlefont.render("Pong!", 1, (0, 255, 0))
        titletextpos1 = titletext.get_rect(centerx=(2*scoreboard.get_width()/7))
        titletextpos2 = titletext.get_rect(centerx=(3*scoreboard.get_width()/7))
        titletextpos3 = titletext.get_rect(centerx=(4*scoreboard.get_width()/7))
        titletextpos4 = titletext.get_rect(centerx=(5*scoreboard.get_width()/7))
        scoreboard.blit(titletext, titletextpos1)
        scoreboard.blit(titletext, titletextpos2)
        scoreboard.blit(titletext, titletextpos3)
        scoreboard.blit(titletext, titletextpos4)

        playerfont = pygame.font.Font("data/TrueType/SFDigitalReadout-Medium.ttf", 36)
        player1text = playerfont.render("Player 1", 1, (0, 255, 0))
        player1textpos = player1text.get_rect(centerx=(1*scoreboard.get_width()/7))
        scoreboard.blit(player1text, player1textpos)
        player2text = playerfont.render("Player 2", 1, (0, 255, 0))
        player2textpos = player2text.get_rect(centerx=(6*scoreboard.get_width()/7))
        scoreboard.blit(player2text, player2textpos)


        scorefont = pygame.font.Font("data/TrueType/SFDigitalReadout-Medium.ttf", 108)
        score1xpos = (1*scoreboard.get_width()/7)
        score1ypos = 72
        score1text = scorefont.render("00", 1, (0, 255, 0))
        score1textpos = score1text.get_rect(centerx=score1xpos, centery=score1ypos)
        scoreboard.blit(score1text, score1textpos)
        score2xpos = (6*scoreboard.get_width()/7)
        score2ypos = 72
        score2text = scorefont.render("00", 1, (0, 255, 0))
        score2textpos = score2text.get_rect(centerx=score2xpos, centery=score2ypos)
        scoreboard.blit(score2text, score2textpos)


#Display The Background and Scoreboard
    screen.blit(background, (AREA_X_MARGIN, AREA_Y_MARGIN))
    screen.blit(scoreboard, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    #print (pygame.mixer.get_init())
    clock = pygame.time.Clock()

    joystick = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    if ( pygame.joystick.get_count() > 0 ):
      print ("Adding player 1")
      #joystick[0] = pygame.joystick.Joystick(0)
      joystick[0].init()
    else:
      #print ("This game requires a joystick.  Please plug one in and rerun.")
      print ("No joystick detected.  Only keyboard will be active for player 1")

    computer=0
    if ( pygame.joystick.get_count() > 1 ):
      print ("Adding player 2")
      #joystick[1] = pygame.joystick.Joystick(1)
      joystick[1].init()
    else:
      print ("Player 2 is a computer")
      computer=1

    hit_sound = load_sound('blip1.ogg')
    point_sound = load_sound('point.ogg')
    paddle = [Paddle() for x in range(0, 2)]
    #paddle[0] = Paddle()
    #paddle[1] = Paddle()
    paddle[0].SetSide(0) # left
    paddle[1].SetSide(1) # right
    paddle[1].SetComputer(computer)
    paddle[0].SetPointSound(point_sound)
    paddle[1].SetPointSound(point_sound)

    ball = Ball()
    ball.SetPaddle1(paddle[0])
    ball.SetPaddle2(paddle[1])
    ball.SetHitSound(hit_sound)
    allsprites = pygame.sprite.RenderPlain((paddle[0], paddle[1], ball))

    # Give computer player pointer to ball
    paddle[1].SetBall(ball)


#Main Loop
    while 1:
        clock.tick(60)

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return

            elif event.type == KEYUP: 
              if event.key == K_DOWN:
                paddle[0].SetDirection(0)
              elif event.key == K_UP:
                paddle[0].SetDirection(0)

            elif event.type == KEYDOWN: 
              if event.key == K_ESCAPE:
                return
              elif event.key == K_DOWN:
                paddle[0].SetDirection(-1)
              elif event.key == K_UP:
                paddle[0].SetDirection(1)

            elif event.type == JOYAXISMOTION:
               for i in range(0, 2 - computer): 
                   #print ("Got joystick axis event")
                   joydir = joystick[i].get_axis(1)
                   if ( joydir >= 0.5 ):
                       paddle[i].SetDirection(-1)
                   elif (joydir <= -0.5): 
                       paddle[i].SetDirection(1)
                   else:
                       paddle[i].SetDirection(0)

            #elif event.type == JOYBUTTONDOWN:
            #elif event.type == MOUSEBUTTONDOWN:
            #elif event.type is MOUSEBUTTONUP:

        allsprites.update()


      # Update scoreboard
        score1text = scorefont.render(str(paddle[0].point).zfill(2), 1, (0, 255, 0))
        score1textpos = score1text.get_rect(centerx=score1xpos, centery=score1ypos)
        scoreboard.fill((0, 0, 100), score1textpos) # RGB = med-dark blue
        scoreboard.blit(score1text, score1textpos)

        score2text = scorefont.render(str(paddle[1].point).zfill(2), 1, (0, 255, 0))
        score2textpos = score2text.get_rect(centerx=score2xpos, centery=score2ypos)
        scoreboard.fill((0, 0, 100), score2textpos) # RGB = med-dark blue
        scoreboard.blit(score2text, score2textpos)


    #Draw Everything
        #screen.blit(background, (0, 0))
        screen.blit(background, (AREA_X_MARGIN, AREA_Y_MARGIN))
        screen.blit(scoreboard, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()

