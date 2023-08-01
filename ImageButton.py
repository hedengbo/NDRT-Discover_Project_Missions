import OpenGL.GL as gl
from Printer import Printer

class ImageButton():
	def __init__(self, image, texture, x, y):
		self.text = ""
		self.image = image
		self.texture = texture
		self.x = x
		self.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.mouseOver = False
		self.enabled = True

	def drawBackground(self):
		gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
		gl.glBegin(gl.GL_QUADS)
		gl.glColor3f(0.0, 0.7, 0.7)
		borderVal = 0
		gl.glVertex2f(self.x-borderVal, self.y-borderVal)
		gl.glVertex2f(self.x+borderVal + self.width, self.y-borderVal)
		gl.glVertex2f(self.x+borderVal + self.width, self.y + self.height+borderVal)
		gl.glVertex2f(self.x-borderVal, self.y + self.height+borderVal)
		
		gl.glColor3f(0.94, 0.94, 0.94)
		gl.glVertex2f(self.x + 2, self.y + 2)
		gl.glVertex2f(self.x + self.width - 2, self.y + 2)
		gl.glVertex2f(self.x + self.width - 2, self.y + self.height - 2)
		gl.glVertex2f(self.x + 2, self.y + self.height - 2)
		gl.glEnd()
		
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
		gl.glBegin(gl.GL_QUADS)
		# Changing the background color
		if self.mouseOver == True:
			gl.glColor3f(0.7, 0.7, 0.7)
		gl.glTexCoord2f(0.0, 1.0)
		gl.glVertex2f(self.x, self.y)
		
		gl.glTexCoord2f(1.0, 1.0)
		gl.glVertex2f(self.x + self.image.get_width(), self.y)
		
		gl.glTexCoord2f(1.0, 0.0)
		gl.glVertex2f(self.x + self.image.get_width(), self.y + self.image.get_height())
		
		gl.glTexCoord2f(0.0, 0.0)
		gl.glVertex2f(self.x, self.y + self.image.get_height())
		gl.glEnd()
		gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
		
		
	def update(self, mouse_x, mouse_y):
		# Check if the mouse is over the button
		if( self.enabled == True and
			mouse_x >= self.x and mouse_x <= self.x + self.width and
			mouse_y >= self.y and mouse_y <= self.y + self.height ):
			self.mouseOver = True
		else:
			self.mouseOver = False
	
	def isMouseOver(self):
		return self.enabled and self.mouseOver;
		
	def disable(self):
		self.enabled = False
		
	def enable(self):
		self.enabled = True
		