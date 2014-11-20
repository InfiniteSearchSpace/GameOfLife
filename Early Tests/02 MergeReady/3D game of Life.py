SCREEN_SIZE = (400, 400)

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from numpy import zeros
import pygame
from pygame.locals import *
from scipy.misc import lena
import OpenGL.GL as gl

class game:
	def __init__(self):
		self.grid_w = 100
		self.grid_h = 100
		self.current_grid = zeros ((self.grid_w, self.grid_h), int)
		self.next_grid = zeros ((self.grid_w, self.grid_h), int)

	def initTexture(self):
		"""
		init the texture - this has to happen after an OpenGL context
		has been created
		"""
		data = np.uint8(np.flipud(lena()))
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


	def setTexture(self,w,h):
		""" draw function """

		# set the viewport and projection
		#gl.glViewport(0,0,w,h)

		gl.glMatrixMode(gl.GL_PROJECTION) ##
		gl.glLoadIdentity()
		gl.glOrtho(0,1,0,1,0,1) #

		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glLoadIdentity()
		gl.glClear( gl.GL_COLOR_BUFFER_BIT ) #

		# enable textures, bind to our texture
		gl.glEnable(gl.GL_TEXTURE_2D)
		gl.glBindTexture(gl.GL_TEXTURE_2D,self.mytexture)

		gl.glColor4f( 1, 1, 1, 1 )

	def setConway(self, width, height):
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(60.0, float(width)/height, .1, 1000.)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()


#----------------------




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
		            if self.current_grid [y, x] == 1:
		                total += 1
		return total



if __name__ == "__main__":
	gameDemo = game()
	pygame.init()
	screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)

	gameDemo.setConway(*SCREEN_SIZE)

	clock = pygame.time.Clock()    
	done = False

	np.random.seed(np.random.randint(0,100000))
	gameDemo.current_grid = np.where((np.random.randint(6, size=(gameDemo.grid_w, gameDemo.grid_h)))==1, 1, 0)


	zoomVar = 300
	zoomMin = 1
	zoomDir = -1
	zoomVal = zoomVar

	gameDemo.initTexture()

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
		    red   = (0.1, 1.0, 0.1, 1)



		# Clear the screen, and z-buffer
		#glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		#if np.random.randint(0,100) == 0:
		#gameDemo.current_grid = np.where((np.random.randint(6, size=(gameDemo.grid_w, gameDemo.grid_h)))==1, 1, 0)
		

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

		if zoomVal%16 >= 0 and zoomVal%32 <= 16:
			gameDemo.setTexture(*SCREEN_SIZE)
			gameDemo.doDraw(*SCREEN_SIZE)
		else:
			gameDemo.setConway(*SCREEN_SIZE)
			for y in range (1, gameDemo.grid_h-1):
				for x in range (1, gameDemo.grid_w-1):
				    N = gameDemo.Neighbours (x, y)
				    if gameDemo.current_grid[y,x]:
				        if N < 2:
				            gameDemo.next_grid [y,x] = 0
				        elif 4 > N > 1:
				            gameDemo.next_grid [y,x] = 1
				        elif N > 3:
				            gameDemo.next_grid [y,x] = 0
				    else:
				        if N == 3:
				            gameDemo.next_grid [y,x] = 1
				    if gameDemo.current_grid[y,x]:
				        gameDemo.DrawCube (x-(gameDemo.grid_w/2), y-(gameDemo.grid_h/2), zoomVal, red, 0.5)
		 	# Show the screen, but first draw!
			gameDemo.current_grid = gameDemo.next_grid
			gameDemo.next_grid = zeros ((gameDemo.grid_w, gameDemo.grid_h), int) 
			
		
		pygame.display.flip()
		
		

	pygame.quit()
