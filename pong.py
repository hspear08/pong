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
print pygame.mixer.get_init()

SCREEN_X = 1024
SCREEN_Y = 768
VERT_SPEED = 10


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
        #self.punching = 0

    def update(self):
        "move the paddle based on the mouse position"
        #pos = pygame.mouse.get_pos()
        #self.rect.top = pos[1]
        
        if ( self.direction == 1 ): 
            if ( self.rect.top >= VERT_SPEED ):
                self.rect.top -= VERT_SPEED
            else:
                self.rect.top = 0
        elif ( self.direction == -1 ):
            if ( self.rect.bottom < SCREEN_Y - VERT_SPEED - 1 ):
                self.rect.bottom += VERT_SPEED
            else:
                self.rect.bottom = SCREEN_Y - 1
             
        
        #self.rect.left = 10 

        #self.rect.midtop = pos
        #if self.punching:
        #    self.rect.move_ip(5, 10)

    def SetDirection(self, direction):
        self.direction = direction 

    def SetSide(self, side):
       # side=0 is the left side, side=1 is the right side
        if ( side == 0 ):
          self.rect.left = 10          
        else :
          self.rect.right = SCREEN_X - 10



    #def punch(self, target):
    #    "returns true if the paddle collides with the target"
    #    if not self.punching:
    #        self.punching = 1
    #        hitbox = self.rect.inflate(-5, -5)
    #        return hitbox.colliderect(target.rect)

    #def unpunch(self):
    #    "called to pull the paddle back"
    #    self.punching = 0


class Ball(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('ball.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move_x = 9
        self.move_y = 9
        #self.dizzy = 0

    def update(self):
        "fly along current vector path"
        #if self.dizzy:
        #    self._spin()
        #else:
        self._fly()

    def _fly(self):
        "move the monkey across the screen, and turn at the ends"
        if self.rect.left < self.area.left or \
            self.rect.right > self.area.right:
            self.move_x = -self.move_x
            #newpos = self.rect.move((self.move_x, self.move_y))
            #self.image = pygame.transform.flip(self.image, 1, 0)

        if self.rect.top < self.area.top or \
            self.rect.bottom > self.area.bottom:
            self.move_y = -self.move_y

        if self.rect.colliderect(self.paddle):
            self.r = random.randint(3,6)
            self.move_x = self.r
            self.move_y = 9 - self.r
            self.hit_sound.play() 
            #newpos = self.rect.move((self.move_x, self.move_y))
            #self.image = pygame.transform.flip(self.image, 1, 0)

        newpos = self.rect.move((self.move_x, self.move_y))
        self.rect = newpos

    def SetPaddle1(self, paddle1):
        self.paddle1 = paddle1

    def SetPaddle2(self, paddle2):
        self.paddle2 = paddle2

    def SetHitSound(self, hit_sound):
        self.hit_sound = hit_sound 


    #def _spin(self):
    #    "spin the monkey image"
    #    center = self.rect.center
    #    #self.dizzy = self.dizzy + 12
    #    #if self.dizzy >= 360:
    #    #    self.dizzy = 0
    #    #    self.image = self.original
    #    #else:
    #    rotate = pygame.transform.rotate
    #    self.image = rotate(self.original, 0) #self.dizzy)
    #    self.rect = self.image.get_rect(center=center)

    #def punched(self):
    #    "this will cause the monkey to start spinning"
    #    if not self.dizzy:
    #        self.dizzy = 1
    #        self.original = self.image


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
    print pygame.mixer.get_init()
    clock = pygame.time.Clock()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    #whiff_sound = load_sound('whiff.wav')
    #punch_sound = load_sound('punch.wav')
    sound = load_sound('blip1.ogg')
    paddle1 = Paddle()
    paddle2 = Paddle()
    ball = Ball()
    ball.SetPaddle1(paddle1)
    ball.SetPaddle2(paddle2)
    ball.SetHitSound(sound)
    allsprites = pygame.sprite.RenderPlain((paddle1, paddle2, ball))

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
               print "Got joystick axis event"
               joydir = joystick.get_axis(1)
               print joydir
               if ( joydir >= 0.5 ):
                   print "Set direction = -1"
                   paddle.SetDirection(-1)
               elif (joydir <= -0.5): 
                   print "Set direction = 1"
                   paddle.SetDirection(1)
               else:
                   print "Set direction = 0"
                   paddle.SetDirection(0)
            elif event.type == JOYBUTTONDOWN:
               print "Got joystick button event"

            #elif event.type == MOUSEBUTTONDOWN:
            #    if paddle.punch(ball):
            #        punch_sound.play() #punch
            #        Ball.punched()
            #    else:
            #        whiff_sound.play() #miss
            #elif event.type is MOUSEBUTTONUP:
            #    paddle.unpunch()

        allsprites.update()

    #Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()

