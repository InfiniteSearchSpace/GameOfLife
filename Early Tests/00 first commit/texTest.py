import numpy as np
from scipy.misc import lena
import OpenGL.GL as gl

class Canvas():
    done_init_texture = False

    def initTexture(self):
        """
        init the texture - this has to happen after an OpenGL context
        has been created
        """

        # make the OpenGL context associated with this canvas the current one
        #self.SetCurrent()

        data = np.uint8(np.flipud(lena()))
        w,h = data.shape
        # generate a texture id, make it current
        self.texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D,self.texture)

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

    def pretendPaint(self):
        """ called when window is repainted """
        # make sure we have a texture to draw
        if not self.done_init_texture:
            self.initTexture()
            self.done_init_texture = True
        self.onDraw()
        self.onDraw2()

    def onDraw(self):
        """ draw function """

        # make the OpenGL context associated with this canvas the current one
        #self.SetCurrent()

        # set the viewport and projection       
        w,h = (256,256)
        gl.glViewport(0,0,w,h)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0,1,0,1,0,1)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glClear( gl.GL_COLOR_BUFFER_BIT )

    def onDraw2(self):
        # enable textures, bind to our texture
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D,self.texture)

        gl.glColor3f( 1, 1, 1 )

        # draw a quad
        gl.glBegin( gl.GL_QUADS )
        gl.glTexCoord2f( 0, 1 );    gl.glVertex2f( 0, 1 )
        gl.glTexCoord2f( 0, 0 );    gl.glVertex2f( 0, 0 )
        gl.glTexCoord2f( 1, 0 );    gl.glVertex2f( 1, 0 )
        gl.glTexCoord2f( 1, 1 );    gl.glVertex2f( 1, 1 )
        gl.glEnd(  )

        gl.glDisable(gl.GL_TEXTURE_2D)

        # swap the front and back buffers so that the texture is visible
        #self.SwapBuffers()

if __name__ == "__main__":
    app = Canvas()
    """app.onDraw()
    app.initTexture()
    app.onDraw2()"""
    app.pretendPaint()
    app.pretendPaint()