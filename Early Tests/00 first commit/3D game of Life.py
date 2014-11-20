SCREEN_SIZE = (800, 600)

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from numpy import zeros
import pygame
from pygame.locals import *

white = (1.0, 1.0, 1.0, 0.5)
red   = (0.1, 1.0, 0.1, 0.3)

grid_w = 100
grid_h = 100

current_grid = zeros ((grid_w, grid_h), int)
next_grid = zeros ((grid_w, grid_h), int)

# Game of life stuff
def Neighbours (x_, y_):
    total = 0
    for y in range (y_ - 1, y_ + 2):
        for x in range (x_ - 1, x_ + 2):
            if (x, y) != (x_, y_):
                if current_grid [y, x] == 1:
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
    
    
def DrawCube (x, y, z, color=white, r=1):
    glLoadIdentity()
    #glRotated (0, 0, 1, 90)
    glBegin (GL_QUADS)
    glColor4f (*color)
    glVertex (x-r, y-r, -z)
    glVertex (x+r, y-r, -z)
    glVertex (x+r, y+r, -z)
    glVertex (x-r, y+r, -z)
    #glVertex3f (x-r, y-r, -z)
    #glVertex3f (x+r, y-r, -z)
    #glVertex3f (x+r, y+r, -z)
    #glVertex3f (x-r, y+r, -z)
    glEnd()


    
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)

resize(*SCREEN_SIZE)
init()

clock = pygame.time.Clock()    
done = False

np.random.seed(np.random.randint(0,100000))
current_grid = np.where((np.random.randint(6, size=(grid_w, grid_h)))==1, 1, 0)


zoomVar = 300
zoomMin = 1
zoomDir = -1
zoomVal = zoomVar

while done==False:
    clock.tick (60)
    for event in pygame.event.get():
        if event.type == QUIT:
            done=True
        if event.type == KEYUP and event.key == K_ESCAPE:
            done=True                
             
    if zoomVal > zoomVar+zoomMin:
        zoomDir = -1
    if zoomVal < zoomMin:
        zoomDir = 1
    
    zoomVal += zoomDir
    if zoomDir > 0:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        red   = (1, 0, 0, 1)
    else: 
        red   = (0.1, 1.0, 0.1, 0.3)
    # Clear the screen, and z-buffer
    #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    if np.random.randint(0,100) == 0:
        current_grid = np.where((np.random.randint(6, size=(grid_w, grid_h)))==1, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    for y in range (1, grid_h-1):
        for x in range (1, grid_w-1):
            N = Neighbours (x, y)
            if current_grid[y,x]:
                if N < 2:
                    next_grid [y,x] = 0
                elif 4 > N > 1:
                    next_grid [y,x] = 1
                elif N > 3:
                    next_grid [y,x] = 0
            else:
                if N == 3:
                    next_grid [y,x] = 1
            if current_grid[y,x]:
                DrawCube (x-(grid_w/2), y-(grid_h/2), zoomVal, red, 0.5)
 
    # Show the screen, but first draw!
    current_grid = next_grid
    next_grid = zeros ((grid_w, grid_h), int) 
    pygame.display.flip()


pygame.quit()
