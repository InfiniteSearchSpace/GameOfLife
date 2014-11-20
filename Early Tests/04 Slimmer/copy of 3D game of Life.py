SCREEN_SIZE = (400, 400)

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from numpy import zeros
from numpy import ones
import pygame
from pygame.locals import *
from scipy.misc import lena
import OpenGL.GL as gl

class game:
	def __init__(self):
		self.grid_w = 100
		self.grid_h = 100
		np.random.seed(np.random.randint(0,100000))
		self.current_grid = zeros ((self.grid_w, self.grid_h), int)
		self.next_grid = zeros ((self.grid_w, self.grid_h), int)

	def initTexture(self):
		"""
		init the texture - this has to happen after an OpenGL context
		has been created
		"""
		data = lena()
		#data = np.where( (self.current_grid)==1, 255, 0)
		w,h = data.shape

		# generate a texture id, make it current
		self.mytexture = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D,self.mytexture)

		# texture mode and parameters controlling wrapping and scaling
		gl.glTexEnvf( gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE )
		gl.glTexParameterf( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT )
		gl.glTexParameterf( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT )
		gl.glTexParameterf( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR )
		gl.glTexParameterf( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR )


		# map the image data to the texture. note that if the input
		# type is GL_FLOAT, the values must be in the range [0..1]
		gl.glTexImage2D(gl.GL_TEXTURE_2D,0,gl.GL_RGB,w,h,0,
		    gl.GL_LUMINANCE,gl.GL_UNSIGNED_BYTE,data)

#----------------------


	def initStage(self,w,h):
		# set the viewport and projection
		gl.glViewport(0,0,w,h)
		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glLoadIdentity()

		#gluPerspective(60.0, float(w)/h, .1, 1000.) #conway
		gl.glOrtho(0,1,0,1,0,1) #tex
		

		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glLoadIdentity()

		#gl.glClear( gl.GL_COLOR_BUFFER_BIT ) #tex

		# enable textures, bind to our texture
		gl.glEnable(gl.GL_TEXTURE_2D)	#tex
		#gl.glBindTexture(gl.GL_TEXTURE_2D,self.mytexture) #tex

		#gl.glColor4f( 1, 1, 1, 1 ) #tex, needed?

#----------------------################

	def DrawCube (self, x, y, z, color, r=1):
		#glLoadIdentity()
		#glRotated (0, 0, 1, 90)
		glBegin (GL_QUADS)
		glColor4f (*color)
		glVertex3f (x-r, y-r, -z)
		glVertex3f (x+r, y-r, -z)
		glVertex3f (x+r, y+r, -z)
		glVertex3f (x-r, y+r, -z)

		"""gl.glTexCoord2f( 0, 1 );
		gl.glTexCoord2f( 0, 0 );
		gl.glTexCoord2f( 1, 0 );
		gl.glTexCoord2f( 1, 1 );"""

		glEnd()


	def doDraw(self,w,h):
		# draw a quad
		gl.glBegin( gl.GL_QUADS )
		gl.glTexCoord2f( 0, 1 );    gl.glVertex3f( 0, 1, 0 )
		gl.glTexCoord2f( 0, 0 );    gl.glVertex3f( 0, 0, 0 )
		gl.glTexCoord2f( 1, 0 );    gl.glVertex3f( 1, 0, 0 )
		gl.glTexCoord2f( 1, 1 );    gl.glVertex3f( 1, 1, 0 )
		gl.glEnd(  )

		gl.glDisable(gl.GL_TEXTURE_2D)


#----------------------################


	# Game of life stuff
	def Neighbours (self, x_, y_):
		total = 0
		for y in range (y_ - 1, y_ + 2):
		    for x in range (x_ - 1, x_ + 2):
		        if (x, y) != (x_, y_):
		            if self.current_grid [y, x] != 0:
		                total += 1
		return total



if __name__ == "__main__":
	gameDemo = game()
	pygame.init()
	screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)

	clock = pygame.time.Clock()    
	done = False

	np.random.seed(np.random.randint(0,100000))
	gameDemo.current_grid = np.where((np.random.randint(6, size=(gameDemo.grid_w, gameDemo.grid_h)))==1, 255, 0)
	
	#gameDemo.initStage(*SCREEN_SIZE)
	#gameDemo.initTexture()

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
		         
		"""if zoomVal > zoomVar+zoomMin:
		    zoomDir = -1
		if zoomVal < zoomMin:
		    zoomDir = 1
		zoomVal += zoomDir
		
		if zoomDir > 0:
		    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		    red   = (1, 0, 0, 1)
		else: 
		    red   = (0.1, 1.0, 0.1, 1)
		"""


		# Clear the screen, and z-buffer
		#glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		#if np.random.randint(0,100) == 0:
		#gameDemo.current_grid = np.where((np.random.randint(6, size=(gameDemo.grid_w, gameDemo.grid_h)))==1, 1, 0)
		

		#glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		
		
		
		"""for y in range (1, gameDemo.grid_h-1):
			for x in range (1, gameDemo.grid_w-1):
			    N = gameDemo.Neighbours (x, y)
			    if gameDemo.current_grid[y,x]:
			        if N < 2:
			            gameDemo.next_grid [y,x] = 0
			        elif 4 > N > 1:
			            gameDemo.next_grid [y,x] = 255
			        elif N > 3:
			            gameDemo.next_grid [y,x] = 0
			    else:
			        if N == 3:
			            gameDemo.next_grid [y,x] = 255
			gameDemo.current_grid = gameDemo.next_grid
			gameDemo.next_grid = zeros ((gameDemo.grid_w, gameDemo.grid_h), int) 
		"""
		
		#gameDemo.initTexture()
		#gameDemo.doDraw(*SCREEN_SIZE)
		
		pygame.display.flip()
		
		

	pygame.quit()
