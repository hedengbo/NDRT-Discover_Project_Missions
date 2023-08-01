import OpenGL.GL as gl
from Printer import Printer

class Button():
	def __init__(self, text, x, y, width, height):
		# Initialize the button
		self.text = text
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.mouseOver = False
		self.enabled = True

	def drawBackground(self):
		if self.enabled == True:
			gl.glBegin(gl.GL_QUADS)
			gl.glColor3f(0.7, 0.7, 0.7)
			gl.glVertex2f(self.x, self.y)
			gl.glVertex2f(self.x + self.width, self.y)
			gl.glVertex2f(self.x + self.width, self.y + self.height)
			gl.glVertex2f(self.x, self.y + self.height)
			
			gl.glColor3f(0.94, 0.94, 0.94)
			gl.glVertex2f(self.x + 2, self.y + 2)
			gl.glVertex2f(self.x + self.width - 2, self.y + 2)
			gl.glVertex2f(self.x + self.width - 2, self.y + self.height - 2)
			gl.glVertex2f(self.x + 2, self.y + self.height - 2)
			gl.glEnd()
		
			if self.mouseOver == True:
				gl.glColor3f(0.7, 0.7, 0.7)
				gl.glBegin(gl.GL_QUADS)
				gl.glVertex2f(self.x, self.y)
				gl.glVertex2f(self.x + self.width, self.y)
				gl.glVertex2f(self.x + self.width, self.y + self.height)
				gl.glVertex2f(self.x, self.y + self.height)
				gl.glEnd()
		
	def drawText(self, painter, printer, font):
		# Draw the text
		if self.enabled == True:
			printer.printCentered(painter, self.text, font, self.x, self.y, self.width, self.height, 100, 100, 100)
		
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
		