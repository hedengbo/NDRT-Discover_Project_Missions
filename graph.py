import sys
from PySide import QtCore, QtGui, QtOpenGL
import numpy as np
import csv
import OpenGL.GL as gl
import os
import math
from Button import Button

class Graph(QtOpenGL.QGLWidget):
	def __init__(self, width, height):
		# Base constructor
		QtOpenGL.QGLWidget.__init__(self)
		
		# Set the attributes
		self.width = width
		self.height = height
		self.rectSize = 35.0
		self.gridCols = 0
		self.gridRows = 0
		self.grid = None
		
		# Load the fonts
		self.fontXLarge = QtGui.QFont("Verdana", 25, 1, False)
		self.fontLarge = QtGui.QFont("Verdana", 15, 1, False)
		self.fontNormal = QtGui.QFont("Verdana", 14, 1, False)
		self.fontSmall = QtGui.QFont("Verdana", 12, 1, False)
		
		# The labels
		self.ube = 0
		self.ld = 0
		#self.high = 0
		#self.medium = 0
		#self.low = 0
		self.uglance =0
		self.TotalRow =0
		
		# Create the positions

		self.brakeX= self.width * 0.078
		self.uGlanceX= self.width * 0.73
		self.lDevX= self.width * 0.37
		self.offRoadX= self.width * 0.73

		self.eventsUpY = self.height * 0.2
		self.eventsDownY = self.height * 0.6
		self.eventsWidth = self.width * 0.2
		self.eventsHeight = self.height * 0.18

		self.Title1X = self.width * 0.10
		self.Title2X = self.width * 0.10

		self.Title1Y = self.height * 0.33
		self.Title2Y = self.height * 0.68

		self.legendY = self.height * 0.06
		self.legendHeight = self.height * 0.06
		self.dsmX = self.width * 0.015
		self.dsmY = self.height * 0.090
		self.dsmWidth = self.width * 0.60
		self.dsmHeight = self.height * 0.85

		self.dsm2X = self.width * 0.635
		self.dsm2Y = self.height * 0.090
		self.dsm2Width = self.width * 0.35
		self.dsm2Height = self.height * 0.85


		self.box1X = self.width * 0.078
		self.box1Y = self.height * 0.42
		self.box1Width = self.width * 0.23
		self.box1Height = self.height * 0.475


		self.box2X = self.width * 0.1
		self.box2Y = self.height * 0.42
		self.box2Width = self.width * 0.23
		self.box2Height = self.height * 0.475


		#self.gridY = self.legendY + self.legendHeight
		#self.gridHeight = self.height * 0.50
		#self.dlX = self.width * 0.25
		#self.dlY = self.height * 0.62
		#self.highX = self.width * 0.45
		#self.mediumX = self.width * 0.55
		#self.lowX = self.width * 0.65
		#self.dpY = self.height * 0.75
		#self.siY = self.height * 0.79
		#self.siX = self.width * 0.3
		#self.safeX = self.width * 0.5
		#self.unsafeX = self.width * 0.6
		#self.sbeX = self.width * 0.1
		#self.ubeX = self.width * 0.4
		#self.ldX = self.width * 0.7
		#self.eventsY = self.height * 0.835
		#self.eventsWidth = self.width * 0.4
		#self.eventsHeight = self.height * 0.25

		#loaded data
		self.data = []
		self.ldframeno = []
		self.ldlineno = []
		self.brakeframeno= []
		self.brakelineno =[]
		self.warningframeno=[]
		self.warningframenoNET=[]
		self.histframeno=[]
		self.histframenoNET=[]
		self.offRoadframeno=[]
		self.offRoadframenoNET=[]
		
	def initializeGL(self):
		# Initialize the context
		gl.glClearColor(1.0, 1.0, 1.0, 1)
		gl.glEnable(gl.GL_LINE_STIPPLE)
		
		# Use the fixed pipeline
		# Resize the window
		self.resizeGL(self.width, self.height)
		
	def resizeGL(self, width, height):
		# Update the attributes
		self.width = width
		self.height = height
		
		# Set up the viewport
		gl.glViewport(0, 0, width, height)
		
		# Set up an orthographic view
		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glLoadIdentity()
		gl.glOrtho(0, self.width, self.height, 0, -1, 1)
		gl.glMatrixMode(gl.GL_MODELVIEW)
		
	def createGraph(self, parID, rows, cols):
		self.gridRows = rows
		self.gridCols = cols
		self.grid = [[0 for x in range(cols)] for x in range(rows)]
		self.ube = 0
		self.ld = 0
		self.high = 0
		self.medium = 0
		self.low = 0
		self.uglance = 0
		self.offRoadglance = 0
		numRows = 900

		#self.numRows = 0
		#mockData for parent
		self.Puglance= 6
		self.Pube = 3
		self.Pld = 1
		self.PoffPercentage = 20
		# Variables: Counters to keep track of values
		listValues = []
		gridValues = []
		lowCount = 0
		warnCount = 0
		dangerCount = 0
		histCount = 0
		bbTime = 0			# <1.2s
		timeCollision = 0	# <1.5s
		timeAccel = 0
		laneDepart = 0		# <-2.5
		laneDepart2 = 0     # > 5
		numCollision = 0	# >1
		accelCount = 0		# < -19.3 ft/s**2
		lineCount = 0
		isLaneDepart = False
		isLaneDepart2 = False


		isAccel = False
		isClose = False    # this is for ttc tracking
		offRoadCount= 0




		''' **********************************************************parent data DRIVEs   ********************************************************'''

		#self.Pube = int(2)
		#self.Pld = int(1)
		self.Puglance = int(0) 
		self.PoffPercentage = int(7)




		with open('../../TeenData/PostDriveSocialNormsData/%s_data.csv'%parID, 'rb') as f:
			reader = csv.reader(f, delimiter=',',quoting=csv.QUOTE_MINIMAL)
			# Use to get rid of the headers
			#headers = reader.next()
			# Going over each line of the file

			for row in reader:
				self.data.append(row)

				lineCount += 1
				# Counting for Number of Collisions
				if float(row[2]) > 1:
					numCollision += 1
				# Counting for Lane Deviation
				if float(row[4]) < -2.5 and isLaneDepart==False and float(row[1])>0 and float(row[1])<10 :
					isLaneDepart = True
					laneDepart += 1
					self.ldframeno.append(float(row[0])) 
				if isLaneDepart == True and float(row[4]) >= -2.5:
					isLaneDepart = False 

				if float(row[4]) >= 5 and isLaneDepart2 == False and float(row[1])>0 and float(row[1])<10:
					isLaneDepart2 = True
					laneDepart2 += 1
					self.ldframeno.append(float(row[0])) 					
				if isLaneDepart2 ==True and float(row[4]) <5:
					isLaneDepart2 = False

				# Counting for Bumper to Bumper Time
				#if float(row[6]) < 1.2:
				#	bbTime += 1
				# Counting for Time to Collision
			
				# Counting for Acceleration


				if (float(row[8]) < 1.5 or float(row[10])< -19.3) and isClose==False and float(row[1])>0 and float(row[1])<10:
					isClose = True
					timeCollision += 1
					self.brakeframeno.append(float(row[0]))
				if (float(row[8]) >= 1.5 and float(row[10])>= -19.3):
					isClose = False

				# if float(row[8]) < 1.5 and isClose==False:
				# 	isClose = True
				# # 	print "ttc", lineCount
				# 	timeCollision += 1
				# 	self.brakeframeno.append(float(row[0]))
				# if isClose == True and float(row[8]) >= 8:
				# 	# timeCollision += 1
				# 	# self.brakeframeno.append(float(row[0]))
				# 	isClose = False
				# 	print "ttc_",lineCount

				# if (float(row[10]) < -19.3 and float(row[8])> 8) and isClose == False and isAccel== False:
				# 	isAccel = True
				# 	print "accel", lineCount
				# 	accelCount += 1
				# 	self.brakeframeno.append(float(row[0]))
				# if float(row[10]) >=0 and isAccel == True and isClose == False:
				# 	isAccel = False
				# 	# accelCount += 1
				# 	print "accel_",lineCount
				# 	# self.brakeframeno.append(float(row[0]))


				#if float(row[10]) < -19.3 and isAccel==False:
				#	isAccel = True
				#	accelCount += 1
				#	self.brakeframeno.append(float(row[0]))

				#if isAccel == True and float(row[10]) >= -18.5:
				#	isAccel = False

				
				#if (float(row[8]) <1.5 and float(row[10])>= -19.3 and isClose == False and isAccel== False):
				#	isClose = True
				#	timeCollision += 1
				#	self.brakeframeno.append(float(row[0]))
				#if float(row[8]) >= 1.8 and isClose == True:
				#	isClose = False
					
				#if float(row[8])<1.5 and float(row[10])<-19.3 and isAccel==False and isClose == False:
				#	isAccel = True
				#	isClose = True
				#	timeAccel += 1
				#	self.brakeframeno.append (float(row[0]))

				#if float(row[8])>= 1.5 and float(row[10])>= -19.3 and isAccel==True and isClose == True:
				#	isAccel = False
				#	isClose = False

				#if isClose == False and float(row[8]) <1.5 or float(row[10]) < -19.5:
				#	isClose = True
				#	timeCollision += 1  #both time to collision and accelcount
				#	self.brakeframeno.append(float(row[0]))
				#if isClose == True and float(row[8]) >= 2 and float(row[10]) >= 19:
				#	isClose = False
					
					
				# Counting for Warning, Danger, and Low Glances
				if float(row[16]) == 1 and float(row[1])>0 and float(row[1])<10:
					warnCount += 1
					self.warningframeno.append(float(row[0]))
					self.warningframenoNET.append(float(row[11]))  
				if float(row[17]) == 1:
					histCount += 1
					self.histframeno.append(float(row[0]))
					self.histframenoNET.append(float(row[11]))  
				if float(row[19]) == 1:
					lowCount += 1
				if row[12] == 'Surface' and float(row[1])>0 and float(row[1])<10:
					offRoadCount += 1
					self.offRoadframeno.append(float(row[0]))
					self.offRoadframenoNET.append(float(row[11]))  
			
			self.TotalRow += lineCount
			self.ube = timeCollision 
			self.ld += laneDepart + laneDepart2
			self.uglance += warnCount
			self.offRoadglance += offRoadCount
			lineCount = 0
			lowCount = 0
			warnCount = 0 
			histCount = 0
			bbTime = 0
			timeCollision = 0
			laneDepart = 0
			numCollision = 0
			accelCount = 0
			offRoadCount = 0

		# Saving drives to a file
		driver = parID.split("_")
		with open('../../TeenData/PostDriveSocialNormsData/%s_TeenDrives.csv'%driver[0],'ab') as csvfile:
			toFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
			toFile.writerow(['%d'%self.ube,'%d'%self.ld,'%d'%self.uglance,'%d'%self.offRoadglance])
	



	def paintRect(self, x, y, red, green, blue):
		# Draw the background of the rectangle
		gl.glColor3f(red, green, blue)
		gl.glBegin(gl.GL_QUADS)
		gl.glVertex2f(x, y)
		gl.glVertex2f(x + self.rectSize, y)
		gl.glVertex2f(x + self.rectSize, y + self.rectSize)
		gl.glVertex2f(x, y + self.rectSize)
		gl.glEnd()
		# Draw the frame of the rectangle
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
		gl.glColor3f(0.3, 0.3, 0.3)
		gl.glBegin(gl.GL_QUADS)
		gl.glVertex2f(x, y)
		gl.glVertex2f(x + self.rectSize, y)
		gl.glVertex2f(x + self.rectSize, y + self.rectSize)
		gl.glVertex2f(x, y + self.rectSize)
		gl.glVertex2f(x + 3, y + 3)
		gl.glVertex2f(x + self.rectSize - 3, y + 3)
		gl.glVertex2f(x + self.rectSize - 3, y + self.rectSize - 3)
		gl.glVertex2f(x + 3, y + self.rectSize - 3)
		gl.glEnd()
		
		# Revert the drawing mode
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
		
	def printCentered(self, painter, str, font, x, y, width, height):
		painter.setFont(font)
		painter.drawText(x, y, width, height, QtCore.Qt.AlignCenter, str)
		
	def printCenteredHor(self, painter, str, font, y = 0):
		painter.setFont(font)
		painter.drawText(0, y, self.width, self.height, QtCore.Qt.AlignHCenter, str)
		
	def printText(self, painter, str, font, x, y, red = 0, green = 0, blue = 0):
		painter.setPen(QtGui.QColor(red, green, blue))
		painter.setFont(font)
		painter.drawText(x, y, self.width, self.height, QtCore.Qt.AlignLeft, str)
		
	def getTextBox(self, painter, str, font):
		painter.setFont(font)
		return painter.boundingRect(0, 0, 0, 0, QtCore.Qt.AlignLeft, str)
		
	def getTextCenteredBox(self, painter, str, font, x, y, width, height):
		painter.setFont(font)
		rect = painter.boundingRect(x, y, width, height, QtCore.Qt.AlignCenter, str)
		return rect
		
	def getTextCenteredHorBox(self, painter, str, font, y = 0):
		painter.setFont(font)
		rect = painter.boundingRect(0, y, self.width, self.height, QtCore.Qt.AlignHCenter, str)
		return rect
			
	def paintDSM(self):
		# Draw the border
		gl.glColor3f(0.87, 0.87, 0.87)
		#gl.glLineWidth(2.0)
		#gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
		gl.glBegin(gl.GL_QUADS);
		gl.glVertex2f(self.dsmX, self.dsmY)
		gl.glVertex2f(self.dsmX + self.dsmWidth, self.dsmY)
		gl.glVertex2f(self.dsmX + self.dsmWidth, self.dsmY + self.dsmHeight)
		gl.glVertex2f(self.dsmX, self.dsmY + self.dsmHeight)
		gl.glEnd()
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)


	def paintDSM2(self):
		# Draw the border gray on right
		gl.glColor3f(0.87, 0.87, 0.87)
		#gl.glLineWidth(2.0)
		#gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
		gl.glBegin(gl.GL_QUADS);
		gl.glVertex2f(self.dsm2X, self.dsm2Y)
		gl.glVertex2f(self.dsm2X + self.dsm2Width, self.dsm2Y)
		gl.glVertex2f(self.dsm2X + self.dsm2Width, self.dsm2Y + self.dsm2Height)
		gl.glVertex2f(self.dsm2X, self.dsm2Y + self.dsm2Height)
		gl.glEnd()
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)


	def paintTxtBox(self):
		# Draw the border gray on right
		gl.glColor3f(0.9, 0.9, 0.9)
		#gl.glLineWidth(2.0)
		#gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
		gl.glBegin(gl.GL_QUADS);
		gl.glVertex2f(self.box1X, self.box1Y)
		gl.glVertex2f(self.box1X + self.box1Width, self.box1Y)
		gl.glVertex2f(self.box1X + self.box1Width, self.box1Y + self.box1Height)
		gl.glVertex2f(self.box1X, self.box1Y + self.box1Height)
		gl.glEnd()
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

	def paintTxtBox2(self):
		# Draw the border gray on right
		gl.glColor3f(0.9, 0.9, 0.9)
		#gl.glLineWidth(2.0)
		#gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
		gl.glBegin(gl.GL_QUADS);
		gl.glVertex2f(self.box2X, self.box2Y)
		gl.glVertex2f(self.box2X + self.box2Width, self.box2Y)
		gl.glVertex2f(self.box2X + self.box2Width, self.box2Y + self.box2Height)
		gl.glVertex2f(self.box2X, self.box2Y + self.box2Height)
		gl.glEnd()
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

	def paintGrid(self):
		# Calculate the dimensions of the grid
		gridPadding = 8
		gridPaddingHalf = gridPadding/2
		gridWidth = (self.gridCols * self.rectSize) + (self.gridCols * 4) + gridPadding
		gridHeight = (self.gridRows * self.rectSize) + (self.gridRows * 4) + gridPadding
		gridX = (self.width/2) - (gridWidth/2) - (gridPadding/2)
		gridY = (self.gridY + (self.gridHeight/2)) - (gridHeight/2)
		
		# Draw the border of the grid
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
		gl.glBegin(gl.GL_QUADS);
		gl.glVertex2f(gridX - gridPaddingHalf, gridY - gridPaddingHalf)
		gl.glVertex2f(gridX + gridWidth + gridPaddingHalf, gridY - gridPaddingHalf)
		gl.glVertex2f(gridX + gridWidth + gridPaddingHalf, gridY + gridHeight + gridPaddingHalf)
		gl.glVertex2f(gridX - gridPaddingHalf, gridY + gridHeight + gridPaddingHalf)
		gl.glEnd()
		gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
		
		# Fill the grid
		for r, g in enumerate(self.grid):
			for c, v in enumerate(g):
				if v > 0:
					rectx = (gridX + gridPadding/2) + (c * self.rectSize) + (c * 4)
					recty = (gridY + gridPadding/2) + (r * self.rectSize) + (r * 4)
					if v == 1:
						self.paintRect(rectx, recty, 0.7, 0.7, 0.7)
					elif v == 2:
						self.paintRect(rectx, recty, 0.9412, 0.6784, 0.3059)
					elif v == 3:
						self.paintRect(rectx, recty, 0.851, 0.3255, 0.3099)
		return (gridX, gridY, gridWidth, gridHeight)
		
	def paintEvent(self, event):
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		gl.glLoadIdentity();
		
		# Initialize the painter
		painter = QtGui.QPainter()
		painter.begin(self)
		
		# Get the bounding rectangles
		rattdBR = self.getTextCenteredBox(painter, "represents a glance to the display", self.fontNormal, 0, self.legendY, self.width, self.legendHeight)
		startBR = self.getTextBox(painter, "START", self.fontNormal)
		endBR = self.getTextCenteredHorBox(painter, "END", self.fontNormal, 0)
		
		# Draw OpenGL stuff
		#self.paintRect(rattdBR.left() - self.rectSize - 10, rattdBR.top(), 1.0, 1.0, 1.0)
		#gridRect = self.paintGrid()
		#self.paintRect(self.highX, self.dlY + 40, 0.851, 0.3255, 0.3099)
		#self.paintRect(self.mediumX, self.dlY + 40, 0.9412, 0.6784, 0.3059)
		#self.paintRect(self.lowX, self.dlY + 40, 0.7, 0.7, 0.7)
		
		#gl.glLineWidth(20.0)

		self.paintDSM()
		self.paintDSM2()
		#self.paintTxtBox()
		#self.paintTxtBox2()
	#	Self.paintRect(self.dsmX, self.dsmY, 0.7, 0.7, 0.7)


		gl.glBegin(gl.GL_QUADS)
		#Draw hazar braking performance lines
		#teenage
		#set the clour. 0.4 willbe changed to parentsbraking

		self.maxUbe = max(float(self.ube), float(self.ube))
		#teen
		gl.glColor3f(0.851, 0.3255, 0.3099)
		gl.glVertex2f(self.brakeX, self.eventsUpY + (self.eventsHeight * 0.5))
		gl.glVertex2f(self.brakeX + ((self.eventsWidth)*(1/(self.maxUbe+5)) * (self.ube)), self.eventsUpY + (self.eventsHeight * 0.5))
		gl.glVertex2f(self.brakeX + ((self.eventsWidth)*(1/(self.maxUbe+5)) * (self.ube)), self.eventsUpY + (self.eventsHeight * 0.5) +29)
		gl.glVertex2f(self.brakeX, self.eventsUpY + (self.eventsHeight * 0.5) + 29)
		#parent
		#gl.glColor3f(0.2,0.2,0.2)
		#gl.glVertex2f(self.brakeX, self.eventsUpY + (self.eventsHeight * 0.7))
		#gl.glVertex2f(self.brakeX + self.eventsWidth* self.Pube * (1/(self.maxUbe+5)), self.eventsUpY + (self.eventsHeight * 0.7))
		#gl.glVertex2f(self.brakeX + self.eventsWidth* self.Pube * (1/(self.maxUbe+5)), self.eventsUpY + (self.eventsHeight * 0.7) + 29)
		#gl.glVertex2f(self.brakeX, self.eventsUpY + (self.eventsHeight * 0.7) + 29)
		
		#Draw lane deviation performance lines

		#teenage
		self.maxld = max(float(self.ld), float(self.ld))

		gl.glColor3f(0.851, 0.3255, 0.3099)
		gl.glVertex2f(self.lDevX, self.eventsUpY + (self.eventsHeight * 0.5))
		gl.glVertex2f(self.lDevX + ((self.eventsWidth)*(1/(self.maxld+5)) * (self.ld)) , self.eventsUpY + (self.eventsHeight * 0.5))
		gl.glVertex2f(self.lDevX + ((self.eventsWidth)*(1/(self.maxld+5)) * (self.ld)), self.eventsUpY + (self.eventsHeight * 0.5) + 29)
		gl.glVertex2f(self.lDevX, self.eventsUpY + (self.eventsHeight * 0.5) + 29)
		
		#parent
		#gl.glColor3f(0.2,0.2,0.2)
		#gl.glVertex2f(self.lDevX, self.eventsUpY + (self.eventsHeight * 0.7))
		#gl.glVertex2f(self.lDevX + self.eventsWidth* self.Pld * (1/(self.maxld+5)), self.eventsUpY + (self.eventsHeight * 0.7))
		#gl.glVertex2f(self.lDevX + self.eventsWidth* self.Pld * (1/(self.maxld+5)), self.eventsUpY + (self.eventsHeight * 0.7) + 29)
		#gl.glVertex2f(self.lDevX , self.eventsUpY + (self.eventsHeight * 0.7) + 29)


#Draw unsafe glances performance lines
		#teenage
		self.maxuglance = max(float(self.uglance), float(self.Puglance))
		#print 'maxuglance:' + str(self.maxuglance) 
		#print 'uglance' + str(self.uglance)
		#print 'Puglance' + str(self.Puglance)

		gl.glColor3f(0.851, 0.3255, 0.3099)
		gl.glVertex2f(self.uGlanceX, self.eventsUpY + (self.eventsHeight * 0.5))
		gl.glVertex2f(self.uGlanceX + ((self.eventsWidth)*(1/(self.maxuglance+5)) * (self.uglance)), self.eventsUpY + (self.eventsHeight * 0.5))
		gl.glVertex2f(self.uGlanceX + (self.eventsWidth)*(1/(self.maxuglance +5)) * (self.uglance), self.eventsUpY + (self.eventsHeight * 0.5) + 29)
		gl.glVertex2f(self.uGlanceX , self.eventsUpY + (self.eventsHeight * 0.5) + 29)
		#parent
		gl.glColor3f(0.2,0.2,0.2)
		gl.glVertex2f(self.uGlanceX, self.eventsUpY + (self.eventsHeight * 0.7))
		gl.glVertex2f(self.uGlanceX + self.eventsWidth* self.Puglance * (1/(self.maxuglance+5)), self.eventsUpY + (self.eventsHeight * 0.7))
		gl.glVertex2f(self.uGlanceX + (self.eventsWidth) * (self.Puglance) * (1/(self.maxuglance+5)), self.eventsUpY + (self.eventsHeight * 0.7) + 29)
		gl.glVertex2f(self.uGlanceX , self.eventsUpY + (self.eventsHeight * 0.7) + 29)
		

		#Draw unsafe glances performance lines
		self.offPercentage = (float(self.offRoadglance))/(float(self.TotalRow))*100 
		#print 'percentage:' + str(self.offPercentage) 
		#print 'TTC brakes:' + str(self.timeCollision) 
		#print 'Deceleration brakes:' + str(self.accelCount) 


		self.maxoff = max(float(self.offPercentage), float(self.PoffPercentage))

		#teenage
		gl.glColor3f(0.851, 0.3255, 0.3099)
		gl.glVertex2f(self.offRoadX, self.eventsDownY + (self.eventsHeight * 0.5))
		gl.glVertex2f(self.offRoadX + ((self.eventsWidth)*(1/(self.maxoff+5)) * (self.offPercentage)), self.eventsDownY + (self.eventsHeight * 0.5))
		gl.glVertex2f(self.offRoadX + ((self.eventsWidth)*(1/(self.maxoff+5)) * (self.offPercentage)), self.eventsDownY + (self.eventsHeight * 0.5) + 29)
		gl.glVertex2f(self.offRoadX , self.eventsDownY + (self.eventsHeight * 0.5) + 29)
		#parent
		gl.glColor3f(0.2,0.2,0.2)
		gl.glVertex2f(self.offRoadX, self.eventsDownY + (self.eventsHeight * 0.7))
		gl.glVertex2f(self.offRoadX + self.eventsWidth* self.PoffPercentage * (1/(self.maxoff+5)), self.eventsDownY + (self.eventsHeight * 0.7))
		gl.glVertex2f(self.offRoadX + self.eventsWidth* self.PoffPercentage * (1/(self.maxoff+5)), self.eventsDownY + (self.eventsHeight * 0.7) + 29)
		gl.glVertex2f(self.offRoadX , self.eventsDownY + (self.eventsHeight * 0.7) + 29)
		gl.glEnd()


	
		# Reset the line attributes
		gl.glLineStipple(1, 0xFFFF)		
		gl.glLineWidth(1.0)
		gl.glColor3f(0.0, 0.0, 0.0)
		
		gl.glBegin(gl.GL_LINES)


        ### Draw cordinate lines for hazardous braking graph
		gl.glVertex2f(self.brakeX, self.eventsUpY)
		gl.glVertex2f(self.brakeX, self.eventsUpY + self.eventsHeight)
		gl.glVertex2f(self.brakeX, self.eventsUpY + self.eventsHeight)
		gl.glVertex2f(self.brakeX + self.eventsWidth, self.eventsUpY + self.eventsHeight)
		

        ### Draw cordinate lines for drifs out of lane/lane deviation
		gl.glVertex2f(self.lDevX, self.eventsUpY)
		gl.glVertex2f(self.lDevX, self.eventsUpY + self.eventsHeight)
		gl.glVertex2f(self.lDevX, self.eventsUpY + self.eventsHeight)
		gl.glVertex2f(self.lDevX + self.eventsWidth, self.eventsUpY + self.eventsHeight)


        ### Draw cordinate lines for unsafe Glances graph
		gl.glVertex2f(self.uGlanceX, self.eventsUpY)
		gl.glVertex2f(self.uGlanceX, self.eventsUpY + self.eventsHeight)
		gl.glVertex2f(self.uGlanceX, self.eventsUpY + self.eventsHeight)
		gl.glVertex2f(self. uGlanceX + self.eventsWidth, self.eventsUpY + self.eventsHeight)


        ### Draw cordinate lines for %time off road glance
		gl.glVertex2f(self.offRoadX, self.eventsDownY)
		gl.glVertex2f(self.offRoadX, self.eventsDownY + self.eventsHeight)
		gl.glVertex2f(self.offRoadX, self.eventsDownY + self.eventsHeight)
		gl.glVertex2f(self. offRoadX + self.eventsWidth, self.eventsDownY + self.eventsHeight)

	
		gl.glEnd()
		
####200 for female   170 for male

		# Draw painter stuff
		self.printCentered(painter, "Drive Report", self.fontXLarge, 0, 0, self.width, self.legendHeight)
		self.printText(painter, "You", self.fontNormal, self.brakeX - 68, self.eventsUpY+ self.eventsHeight * 0.48)
		#self.printText(painter, "Parent", self.fontNormal, self.brakeX - 107, self.eventsUpY+ self.eventsHeight * 0.68)
		self.printText(painter, "You", self.fontNormal, self.lDevX - 68, self.eventsUpY+ self.eventsHeight * 0.48)
		#self.printText(painter, "Parent", self.fontNormal, self.lDevX - 107, self.eventsUpY+ self.eventsHeight * 0.68)
		self.printText(painter, "You", self.fontNormal, self.uGlanceX - 68, self.eventsUpY+ self.eventsHeight * 0.48)
		self.printText(painter, "Male Peers", self.fontNormal, self.uGlanceX - 170, self.eventsUpY+ self.eventsHeight * 0.68)
		self.printText(painter, "You", self.fontNormal, self.offRoadX - 68, self.eventsDownY+ self.eventsHeight * 0.48)
		self.printText(painter, "Male Peers", self.fontNormal, self.offRoadX - 170, self.eventsDownY+ self.eventsHeight * 0.68)
		self.printText(painter, "# of Unsafe Braking", self.fontLarge, self.brakeX - 10 , self.eventsUpY - 50)
		self.printText(painter, "# of Lane Deviation", self.fontLarge, self.lDevX - 10 , self.eventsUpY - 50)
		self.printText(painter, "# of Unsafe Glances", self.fontLarge, self.uGlanceX - 10 , self.eventsUpY - 50)
		self.printText(painter, "% of Time Not Looking at Road", self.fontLarge, self.offRoadX - 10 , self.eventsDownY - 50)
		self.printText(painter, "%i"%self.ube, self.fontNormal, self.brakeX + ((self.eventsWidth)*(1/(self.maxUbe+5)) * (self.ube)) + 3, self.eventsUpY+ self.eventsHeight * 0.48)
		#self.printText(painter, "%i"%self.Pube, self.fontNormal,self.brakeX + self.eventsWidth* self.Pube * (1/(self.maxUbe+5)) +3 , self.eventsUpY+ self.eventsHeight * 0.68)
		self.printText(painter, "%i"%self.ld, self.fontNormal, self.lDevX + ((self.eventsWidth)*(1/(self.maxld+5)) * (self.ld)) + 3, self.eventsUpY+ self.eventsHeight * 0.48)
		#self.printText(painter, "%i"%self.Pld, self.fontNormal,self.lDevX + self.eventsWidth* self.Pld * (1/(self.maxld+5)) +3 , self.eventsUpY+ self.eventsHeight * 0.68)
		
		self.printText(painter, "%i"%self.uglance, self.fontNormal, self.uGlanceX + ((self.eventsWidth)*(1/(self.maxuglance+5)) * (self.uglance)) + 3, self.eventsUpY+ self.eventsHeight * 0.48)
		self.printText(painter, "%i"%self.Puglance, self.fontNormal,self.uGlanceX + self.eventsWidth* self.Puglance * (1/(self.maxuglance+5)) +3 , self.eventsUpY+ self.eventsHeight * 0.68)
		
		self.printText(painter, "%i"%self.offPercentage, self.fontNormal, self.offRoadX + ((self.eventsWidth)*(1/(self.maxoff+5)) * (self.offPercentage)) + 3, self.eventsDownY+ self.eventsHeight * 0.48)
		self.printText(painter, "%i"%self.PoffPercentage, self.fontNormal,self.offRoadX + self.eventsWidth* self.PoffPercentage * (1/(self.maxoff+5)) +3 , self.eventsDownY+ self.eventsHeight * 0.68)
	

		#print 'Break Events:' + str(self.ube) 
		#print 'offRoadglance:' + str(self.offRoadglance) 
		#print 'rowsss' + str(self.TotalRow)
		#print 'unsafe glances' + str(self.uglance)
		#print self.ld


		#self.printCentered(painter, "represents a glance to the display", self.fontNormal, 0, self.legendY, self.width, self.legendHeight)
		#self.printText(painter, "START", self.fontNormal, gridRect[0] - (startBR.right()/2), gridRect[1] + gridRect[3] + 10)
		#self.printText(painter, "END", self.fontNormal, (gridRect[0] + gridRect[2]) - (startBR.right()/2), gridRect[1] + gridRect[3] + 10)
		#self.printText(painter, "Distraction Level:", self.fontNormal, self.dlX, self.dlY,255,0,0)
		#self.printText(painter, "High", self.fontNormal, self.highX, self.dlY)
		#self.printText(painter, "Medium", self.fontNormal, self.mediumX, self.dlY)
		#self.printText(painter, "Low", self.fontNormal, self.lowX, self.dlY)
		#self.printText(painter, str(int(self.high)) + "%", self.fontNormal, self.highX + self.rectSize + 8, self.dlY + 43)
		#self.printText(painter, str(int(self.medium)) + "%", self.fontNormal, self.mediumX + self.rectSize + 8, self.dlY + 43)
		#self.printText(painter, str(int(self.low)) + "%", self.fontNormal, self.lowX + self.rectSize + 8, self.dlY + 43)
		#self.printCenteredHor(painter, "Driving Performance", self.fontLarge, self.dpY)
		#self.printText(painter, "Safety Indicator:", self.fontNormal, self.siX, self.siY)
		#self.printText(painter, "Safe", self.fontNormal, self.safeX, self.siY, 92, 184, 92)
		#self.printText(painter, "Unsafe", self.fontNormal, self.unsafeX, self.siY, 217, 83, 79)
		#self.printText(painter, "4 safe braking events", self.fontNormal, self.sbeX + 10, self.eventsY + (self.eventsHeight*0.15))
		##self.printText(painter, "%i unsafe braking events"%self.ube, self.fontNormal, self.ubeX + 10, self.eventsY + (self.eventsHeight*0.15))
		##self.printText(painter, "%i lane deviations"%self.ld, self.fontNormal, self.ldX + 10, self.eventsY + (self.eventsHeight*0.15))



		# Draw painter stuff
		#self.printCentered(painter, "Summary of Your Drive", self.fontXLarge, 0, 0, self.width, self.legendHeight)
		#self.printCentered(painter, "represents a glance to the display", self.fontNormal, 0, self.legendY, self.width, self.legendHeight)
		#self.printText(painter, "START", self.fontNormal, gridRect[0] - (startBR.right()/2), gridRect[1] + gridRect[3] + 10)
		#self.printText(painter, "END", self.fontNormal, (gridRect[0] + gridRect[2]) - (startBR.right()/2), gridRect[1] + gridRect[3] + 10)
		#self.printText(painter, "Distraction Level:", self.fontNormal, self.dlX, self.dlY)
		#self.printText(painter, "High", self.fontNormal, self.highX, self.dlY)
		#self.printText(painter, "Medium", self.fontNormal, self.mediumX, self.dlY)
		#self.printText(painter, "Low", self.fontNormal, self.lowX, self.dlY)
		#self.printText(painter, str(int(self.high)) + "%", self.fontNormal, self.highX + self.rectSize + 8, self.dlY + 43)
		#self.printText(painter, str(int(self.medium)) + "%", self.fontNormal, self.mediumX + self.rectSize + 8, self.dlY + 43)
		#self.printText(painter, str(int(self.low)) + "%", self.fontNormal, self.lowX + self.rectSize + 8, self.dlY + 43)
		#self.printCenteredHor(painter, "Driving Performance", self.fontLarge, self.dpY)
		#self.printText(painter, "Safety Indicator:", self.fontNormal, self.siX, self.siY)
		#self.printText(painter, "Safe", self.fontNormal, self.safeX, self.siY, 92, 184, 92)
		#self.printText(painter, "Unsafe", self.fontNormal, self.unsafeX, self.siY, 217, 83, 79)
		#self.printText(painter, "4 safe braking events", self.fontNormal, self.sbeX + 10, self.eventsY + (self.eventsHeight*0.15))
		#self.printText(painter, "%i unsafe braking events"%self.ube, self.fontNormal, self.ubeX + 10, self.eventsY + (self.eventsHeight*0.15))
		#self.printText(painter, "%i lane deviations"%self.ld, self.fontNormal, self.ldX + 10, self.eventsY + (self.eventsHeight*0.15))
		



		#defining texts
		ldtxt = ''
		eventcounter = 0
		#distLevel = ''
		for fno in self.ldframeno:
			prevfno = max(fno - 300, float(self.data[0][0]))  #180= 3 seconds before
			count = 0
			count2 = 0
			distcount = 0
			eventcounter += 1
			for d in self.data:
				if float(d[0]) < prevfno:
					continue
				if float(d[0]) == fno:
					break
				if float(d[16])>0:
					count +=1
				if d[12] == 'Surface':
					count2 +=1
			distcount = float((count2/(1.0*240))*100)
			if (float(count)>0 or float(distcount)>= 40):
				distLevel = 'Distraction Detected'
				ldtxt = ldtxt + '\nDeviation' + str(eventcounter) + ': ' + str(distLevel)

			elif (float(count)==0 and float(distcount)<40) :
				distLevel =''
				ldtxt = ldtxt + '\nDeviation' + str(eventcounter) + ': ' + str(distLevel)
			#elif float((count/(1.0*(ll)))*100) <30:
			#	distLevel = ''

			#ldtxt = ldtxt + '\nEvent ' + str(eventcounter) + '(Frame ' + str(fno) + '): ' + str((count / (1.0 * (fno - prevfno)))) + '% distraction'
			#ldtxt = ldtxt + '\nDeviation' + str(eventcounter) + ': ' + str(distLevel)

		
		#self.printText(painter, ldtxt, self.fontNormal, self.brakeX, self.eventsUpY + self.eventsHeight + 30) 
		self.printText(painter, ldtxt, self.fontSmall, self.lDevX+5, self.eventsUpY + self.eventsHeight + 40) 



		#defining texts
		ubtxt = ''
		eventcounter = 0
		for fno in self.brakeframeno:
			prevfno = max(fno - 300, float(self.data[0][0]))
			count = 0
			count2 = 0
			distcount = 0
			eventcounter += 1
			for d in self.data:
				if float(d[0]) < prevfno:
					continue
				if float(d[0]) == fno:
					break
				if float(d[16])>0:
					count +=1
				if d[12] == 'Surface':
					count2 +=1
			distcount = float((count2/(1.0*240))*100)
			if (float(count)>0 or float(distcount)>= 40):
				distLevel = 'Distraction Detected'
			elif (float(count)==0 and float(distcount)<40) :
				distLevel =''
			ubtxt = ubtxt + '\nBrake' + str(eventcounter) + ': ' + str(distLevel) 
			#elif float((count/(1.0*(bl)))*100) <30:
			#	distLevel = 'Low Distraction'

			#ldtxt = ldtxt + '\nEvent ' + str(eventcounter) + '(Frame ' + str(fno) + '): ' + str((count / (1.0 * (fno - prevfno)))) + '% distraction'
			#ubtxt = ubtxt + '\nEvent ' + str(eventcounter) + ': ' + str((count / (1.0 * (fno - prevfno)))) + '% distraction'
			#ubtxt = ubtxt + '\nBrake' + str(eventcounter) + ': ' + str(distLevel) 

		self.printText(painter, ubtxt, self.fontSmall, self.brakeX+5, self.eventsUpY + self.eventsHeight + 40) 

		
		#self.printText(painter, ldtxt, self.fontNormal, self.brakeX, self.eventsUpY + self.eventsHeight + 30) 
		#self.printText(painter, ubtxt, self.fontNormal, self.ubeX, self.eventsUpY + self.eventsHeight + 30) 


		#draw pic
		#QtGui.QPicture pic;
		#pic.load("image1.png")
		#painter.drawPicture(0, 0, pic);


		# End the paguinter
'''
if __name__=='__main__':
	app = QtGui.QApplication(sys.argv)
	g = Graph(1000, 1000)
	g.createGraph('Participant01_drive01', 3, 3)
	g.show()
	sys.exit(app.exec_())'''