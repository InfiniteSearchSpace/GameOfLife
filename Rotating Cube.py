from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import zeros
import pygame
from os import environ
from math import sin, cos, radians
from pygame.locals import *
from numpy import zeros

white = (1.0, 1.0, 1.0, 0.5)
red   = (1.0, 0.1, 0.1, 0.5)
green = (0.0, 1.0, 0.0, 0.5)

current_grid = zeros ((10, 10, 10), int)
next_grid = zeros ((10, 10, 10), int)
# Game of life stuff
def Neighbours (x_, y_,z_):
    total = 0
    for z in range (z_ - 1, z_ + 2):
        for y in range (y_ - 1, y_ + 2):
            for x in range (x_ - 1, x_ + 2):
                if (x, y, z) != (x_, y_, z_):
                    if current_grid [y, x, z] == 1:
                        total += 1
    return total


def resize(width, height):
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width)/height, .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    
    glEnable(GL_DEPTH_TEST)
    
    glShadeModel(GL_FLAT)
    glClearColor(0.0, 0.0, 0.0, 0.0)

    glEnable(GL_COLOR_MATERIAL)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)        
    glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))
    # Enables Alpha values for colors
    glEnable (GL_BLEND);
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    
    
def DrawCube (r):
    WIDTH = 10
    glLoadIdentity()
    glTranslate (0, 0, -30)
    glRotatef (r, 0, 1, 1)
    glTranslate (-WIDTH, -WIDTH, -WIDTH)
    glColor4f (*red)
    for z in range (WIDTH):
        for y in range (WIDTH):
            for x in range (WIDTH):
                if current_grid[x, y, z]:
                    glutSolidCube (1)
                glTranslate (2, 0, 0)
            glTranslate (-WIDTH*2, 2, 0)
        glTranslate (0, -WIDTH*2, 2)
    glLoadIdentity()

pygame.init()
SCREEN_SIZE = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)

resize(*SCREEN_SIZE)
init()

clock = pygame.time.Clock()    
done = False
rotation = 0

for z in range (10):
    current_grid[5,5,z] = 1
    current_grid[5,6,z] = 1
    current_grid[5,7,z] = 1
    current_grid[6,6,z] = 1
    current_grid[4,7,z] = 1

while done==False:
    clock.tick (60)
    for event in pygame.event.get():
        if event.type == QUIT:
            done=True
        if event.type == KEYUP and event.key == K_ESCAPE:
            done=True                
    rotation += 0.5
    # Clear the screen, and z-buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    for z in range (1,9):
        for y in range (1, 9):
            for x in range (1, 9):
                N = Neighbours (x, y, z)
                if current_grid[y,x,z]:
                    if N < 2:
                        next_grid [y,x,z] = 0
                    elif 4 > N > 1:
                        next_grid [y,x,z] = 1
                    elif N > 3:
                        next_grid [y,x,z] = 0
                else:
                    if N == 3:
                        next_grid [y,x,z] = 1

    current_grid = next_grid
    next_grid = zeros ((10, 10, 10), int)  
    # Show the screen, but first draw!
    DrawCube (rotation)
    pygame.display.flip()


pygame.quit()
