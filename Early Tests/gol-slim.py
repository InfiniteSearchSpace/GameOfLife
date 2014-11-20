import pygame
import OpenGL.GL as gl
import numpy as np
from pygame.locals import *
from scipy.misc import lena

SCREEN_SIZE = (400, 400)

class game:
	def __init__(self):
		#Set the initial size for the generative array
		self.grid_w = 2**7 
		self.grid_h = self.grid_w 
		
		#initialise both buffers to 0 in x,y
		self.current_grid = np.zeros ((self.grid_w, self.grid_h), int)
		self.next_grid = np.zeros ((self.grid_w, self.grid_h), int)

	#(x of 3), points to data, 
	def initTexture(self):
		#data = np.flipud(lena()) #insert test data
		
		#Set the data source
		data = self.current_grid
		w,h = data.shape

		# generate a texture id
		self.mytexture = gl.glGenTextures(1)
		
		#bind? the tex id and some implicit thing?
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


	def initStage(self,w,h):
		# set the viewport and projection
		gl.glViewport(0,0,w,h)
		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glLoadIdentity()

		#Perspectives/layouts
		#gluPerspective(60.0, float(w)/h, .1, 1000.)
		gl.glOrtho(0,1,0,1,0,1)
		
		#no idea what this is for
		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glLoadIdentity()

		# enable textures, bind to our texture
		gl.glEnable(gl.GL_TEXTURE_2D)


	def doDraw(self,w,h):
		# draw a quad
		gl.glBegin( gl.GL_QUADS )
		gl.glTexCoord2f( 0, 1 );    gl.glVertex3f( 0, 1, 0 )
		gl.glTexCoord2f( 0, 0 );    gl.glVertex3f( 0, 0, 0 )
		gl.glTexCoord2f( 1, 0 );    gl.glVertex3f( 1, 0, 0 )
		gl.glTexCoord2f( 1, 1 );    gl.glVertex3f( 1, 1, 0 )
		gl.glEnd(  )

#----------------------################
	# Game of life cell tester
	def Neighbours (self, x_, y_):
		total = 0
		for y in range (y_ - 1, y_ + 2):
		    for x in range (x_ - 1, x_ + 2):
		        if (x, y) != (x_, y_):
		            if self.current_grid [y, x] != 0:
		                total += 1
		return total
#----------------------################


if __name__ == "__main__":

	#Main class
	gameDemo = game()
	
	#GUI stuff	
	pygame.init()
	screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
	clock = pygame.time.Clock()    
	done = False

	#Seed the first buffer with random numbers
	np.random.seed(np.random.randint(0,100000))
	gameDemo.current_grid = np.where((np.random.randint(6, size=(gameDemo.grid_w, gameDemo.grid_h)))==1, 255, 0)

	#Set & render the initial stage
	gameDemo.initStage(*SCREEN_SIZE)
	gameDemo.initTexture()
	gameDemo.doDraw(*SCREEN_SIZE)

	#Let's do this for a while
	while done==False:
		
		clock.tick (60)

		#GUI Exits
		for event in pygame.event.get():
		    if event.type == QUIT:
		        done=True
		    if event.type == KEYUP and event.key == K_ESCAPE:
		        done=True                

		#Do the conway gruntwork
		for y in range (1, gameDemo.grid_h-1):
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

		#Swap the host's conway buffers
		gameDemo.current_grid = gameDemo.next_grid
		gameDemo.next_grid = np.zeros ((gameDemo.grid_w, gameDemo.grid_h), int) 

		#Do a full gl render cycle
		gameDemo.initStage(*SCREEN_SIZE)
		gameDemo.initTexture()
		gameDemo.doDraw(*SCREEN_SIZE)

		pygame.display.flip()
		
		

	pygame.quit()
