from PySide import QtCore, QtGui

class Printer():
	def __init__(self):	
		# Load the fonts
		self.fontXLarge = QtGui.QFont("Helvetica", 32, QtGui.QFont.Bold, False)
		self.fontLarge = QtGui.QFont("Helvetica", 24, QtGui.QFont.Bold, False)
		self.fontNormal = QtGui.QFont("Helvetica", 20, 1, False)
		self.fontNormal_2 = QtGui.QFont("Helvetica", 20, QtGui.QFont.Bold, False)
		self.fontSmall  = QtGui.QFont("Helvetica", 16, 1, False)
		
	def printCentered(self, painter, str, font, x, y, width, height, red = 0, green = 0, blue = 0):
		painter.setPen(QtGui.QColor(red, green, blue))
		painter.setFont(font)
		painter.drawText(x, y, width, height, QtCore.Qt.AlignCenter, str)
		
	def getTextCenteredBox(self, painter, str, font, x, y, width, height):
		painter.setFont(font)
		return painter.boundingRect(x, y, width, height, QtCore.Qt.AlignCenter, str)
		
	def printCenteredHor(self, painter, str, font, x, y, width, height, red = 0, green = 0, blue = 0):
		painter.setPen(QtGui.QColor(red, green, blue))
		painter.setFont(font)
		painter.drawText(x, y, width, height, QtCore.Qt.AlignHCenter, str)
		
	def getTextCenteredHorBox(self, painter, str, font, x, y, width, height):
		painter.setFont(font)
		return painter.boundingRect(x, y, width, height, QtCore.Qt.AlignCenter, str)		
		
	def printText(self, painter, str, font, x, y, width, height, red = 0, green = 0, blue = 0):
		painter.setPen(QtGui.QColor(red, green, blue))
		painter.setFont(font)
		painter.drawText(x, y, width, height, QtCore.Qt.AlignLeft, str)
		
	def getTextBox(self, painter, str, font):
		painter.setFont(font);
		return painter.boundingRect(0, 0, 0, 0, QtCore.Qt.AlignLeft, str)
		
	def printTextWrap(self, painter, str, font, x, y, width, height, red = 0, green = 0, blue = 0):
		painter.setPen(QtGui.QColor(red, green, blue))
		painter.setFont(font)
		painter.drawText(x, y, width, height, QtCore.Qt.TextWordWrap, str)
		