import pygame
import OpenGL.GL as gl
import numpy as np
from pygame.locals import *
from scipy.misc import lena

SCREEN_SIZE = (800, 800)

class game:
	def __init__(self):
		#Set the initial size for the generative array
		self.grid_w = 2**12 #12 = 4k, 13 = 8k
		self.grid_h = self.grid_w 
		
		#initialise both buffers to 0 in x,y
		self.current_grid = np.zeros ((self.grid_w, self.grid_h), int)
		self.next_grid = np.zeros ((self.grid_w, self.grid_h), int)

	def initTexture(self):
		#data = np.flipud(lena()) #insert test data
		
		#Set the data source
		data = self.current_grid
		w,h = data.shape

		# generate a texture id
		self.mytexture = gl.glGenTextures(1)
		
		#bind? the tex id and some implicit thing?
		gl.glBindTexture(gl.GL_TEXTURE_3D,self.mytexture)

		# texture mode and parameters controlling wrapping and scaling
		#gl.glTexEnvf( gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE )
		#gl.glTexParameterf( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT )
		#gl.glTexParameterf( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT )
		gl.glTexParameterf( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST ) #close up
		gl.glTexParameterf( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST ) #Far away
		#gl.GL_LINEAR
		#gl.GL_NEAREST

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
		#L,R,B,T,?,?
		#gl.glOrtho(-0.1, 1.1,	-0.1, 1.1,	 0,1)
				
		"""offset = 0.5
		x1 = offset+1
		x2 = (x1 - 1) *-1
		y1 = offset+1
		y2 = (x1 - 1) *-1
		gl.glOrtho(x2,x1,y2,y1, 0,1)"""

		#no idea what this is for
		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glLoadIdentity()

		# enable textures, bind to our texture
		gl.glEnable(gl.GL_TEXTURE_2D)


	def changeOrtho(self, offset):
		x1 = offset+1
		x2 = (x1 - 1) *-1
		y1 = offset+1
		y2 = (x1 - 1) *-1
		gl.glOrtho(x2,x1,y2,y1, 0,1)


	def doDraw(self,w,h):
		# draw a quad
		gl.glBegin( gl.GL_QUADS )
		gl.glTexCoord2f( 0, 1 );    gl.glVertex3f( 0, 1, self.z )
		gl.glTexCoord2f( 0, 0 );    gl.glVertex3f( 0, 0, self.z )
		gl.glTexCoord2f( 1, 0 );    gl.glVertex3f( 1, 0, self.z )
		gl.glTexCoord2f( 1, 1 );    gl.glVertex3f( 1, 1, self.z )
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
	gameDemo.z = 0
	gameDemo.initStage(*SCREEN_SIZE)
	gameDemo.changeOrtho(1)
	gameDemo.initTexture()
	gameDemo.doDraw(*SCREEN_SIZE)

	myOrtho = 0
	orthDir = 0.05

	#Let's do this for a while
	while done==False:
		
		#Min, max zoom
		if myOrtho > 3:
			orthDir = -0.05
		if myOrtho < -0.4999:
			orthDir = 0.0001

		#Controlled inward zooms
		if orthDir < 0 and myOrtho < -0.3:
			orthDir = -0.001
		if orthDir < 0 and myOrtho < -0.475:
			orthDir = -0.0001
		if orthDir < 0 and myOrtho < -0.495:
			orthDir = -0.00005

		if orthDir > 0 and myOrtho > -0.495:
			orthDir = 0.001
		if orthDir > 0 and myOrtho > -0.475:
			orthDir = 0.01
		if orthDir > 0 and myOrtho > -0.3:
			orthDir = 0.05

		
		myOrtho += orthDir		
		print "Zoom:", myOrtho
		

		clock.tick (60)

		#GUI Exits
		for event in pygame.event.get():
		    if event.type == QUIT:
		        done=True
		    if event.type == KEYUP and event.key == K_ESCAPE:
		        done=True                

		"""#Do the conway gruntwork
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
		gameDemo.next_grid = np.zeros ((gameDemo.grid_w, gameDemo.grid_h), int)"""

		

		#Do a full gl render cycle
		gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
		gameDemo.initStage(*SCREEN_SIZE)
		gameDemo.changeOrtho(myOrtho)
		gameDemo.initTexture()
		gameDemo.doDraw(*SCREEN_SIZE)

		pygame.display.flip()
		
		

	pygame.quit()
