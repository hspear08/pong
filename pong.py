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

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


pygame.mixer.init(44100, 16) # 44100 KHz, 16 bit
#print pygame.mixer.get_init()

SCREEN_X = 1920
SCREEN_Y = 980  
PADDLE_SPEED = 10
BALL_SPEED = 9 


#functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
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
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound


#classes for our game objects
class Paddle(pygame.sprite.Sprite):
    """moves a paddle on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('paddle.bmp', -1)
        self.direction = 0
        self.rect.left = 10
        self.point = 0
        #self.punching = 0

    def update(self):
        "move the paddle based on the mouse position"
        #pos = pygame.mouse.get_pos()
        #self.rect.top = pos[1]
        
        if ( self.direction == 1 ): 
            if ( self.rect.top >= PADDLE_SPEED ):
                self.rect.top -= PADDLE_SPEED
            else:
                self.rect.top = 0
        elif ( self.direction == -1 ):
            if ( self.rect.bottom < SCREEN_Y - PADDLE_SPEED - 1 ):
                self.rect.bottom += PADDLE_SPEED
            else:
                self.rect.bottom = SCREEN_Y - 1
             


    def SetDirection(self, direction):
        self.direction = direction 

    def SetSide(self, side):
       # side=0 is the left side, side=1 is the right side
        if ( side == 0 ):
          self.rect.left = 10          
        else :
          self.rect.right = SCREEN_X - 10

    def IncPoint(self):
        self.point = self.point + 1



class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('ball.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = SCREEN_X/2, SCREEN_Y/2
        self.move_x = BALL_SPEED / 2
        self.move_y = BALL_SPEED / 2
        self.speed = BALL_SPEED
        #self.dizzy = 0

    def update(self):
        self._fly()

    def _fly(self):
        if self.rect.left < self.area.left: 
            print "Paddle1 point!"
            self.paddle1.IncPoint()

        if self.rect.right > self.area.right:
            print "Paddle2 point!"
            self.paddle2.IncPoint()

        if self.rect.top < self.area.top or \
            self.rect.bottom > self.area.bottom:
            self.move_y = -self.move_y

        if self.rect.colliderect(self.paddle1):
            #self.r = random.randint(BALL_SPEED / 3, 2 * BALL_SPEED / 3)
            self.r = (self.rect.top + self.rect.height/2 - self.paddle1.rect.top - self.paddle1.rect.height/2) * 2 * self.speed / (self.paddle1.rect.height * 3 / 2)
            print self.rect.top, self.rect.height/2, self.paddle1.rect.top, self.paddle1.rect.height/2, self.r
            self.move_y = self.r
            self.move_x = self.speed - abs(self.r)
            print self.speed, self.move_x, self.move_y
            self.hit_sound.play() 
            self.speed = self.speed + 1

        if self.rect.colliderect(self.paddle2):
            #self.r = random.randint(BALL_SPEED / 3, 2 * BALL_SPEED / 3)
            self.r = (self.rect.top + self.rect.height/2 - self.paddle2.rect.top - self.paddle2.rect.height/2) * 2 * self.speed / (self.paddle1.rect.height * 3 / 2)
            print self.rect.top, self.rect.height/2, self.paddle2.rect.top, self.paddle2.rect.height/2, self.r
            self.move_y = self.r
            self.move_x = - self.speed + abs(self.move_y)
            print self.speed, self.move_x, self.move_y
            self.hit_sound.play() 
            self.speed = self.speed + 1

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
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 50)) # RGB = dark blue

#Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Pong!", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    #print pygame.mixer.get_init()
    clock = pygame.time.Clock()

    joystick = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    if ( pygame.joystick.get_count() > 0 ):
      print "Adding player 1"
      #joystick[0] = pygame.joystick.Joystick(0)
      joystick[0].init()
    else:
      print "This game requires a joystick.  Please plug one in and rerun."
      return

    if ( pygame.joystick.get_count() > 1 ):
      print "Adding player 2"
      #joystick[1] = pygame.joystick.Joystick(1)
      joystick[1].init()

    sound = load_sound('blip1.ogg')
    paddle = [Paddle() for x in range(0, 2)]
    #paddle[0] = Paddle()
    #paddle[1] = Paddle()
    paddle[0].SetSide(0) # left
    paddle[1].SetSide(1) # right
    ball = Ball()
    ball.SetPaddle1(paddle[0])
    ball.SetPaddle2(paddle[1])
    ball.SetHitSound(sound)
    allsprites = pygame.sprite.RenderPlain((paddle[0], paddle[1], ball))

#Main Loop
    while 1:
        clock.tick(60)

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == JOYAXISMOTION:
               for i in range(0, 2): 
                   #print "Got joystick axis event"
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

    #Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()

