import sys
import os
from PySide import QtCore, QtGui, QtOpenGL
from PySide.QtGui import QMainWindow, QPushButton, QApplication, QDesktopWidget
from mainwindow import Ui_MainWindow
from graph import Graph
import csv
import numpy as np
from Receiver import *
    
def writecsv(self):
    with open('/Users/hedengbo/Desktop/%s/%s.csv'%(self.parID,self.fileName),'ab') as csvfile:
        toFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
        if np.isnan(self.response):
            PhaseSelect = "NaN"
            IsCorrect = "NaN"
        else:
            PhaseSelect = self.allList[self.response,0]
            IsCorrect = self.allList[self.response,1]
        InterectNum = self.interact;
        toFile.writerow(['%d'%self.trialNum,'%s'%PhaseSelect,'%s'%IsCorrect,'%d'%InterectNum,'%d'%self.receiver.FrameNum,'%s'%self.Press])

class MainWindow(QMainWindow, Ui_MainWindow):	
        
	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Escape:
			self.close()
			self.receiver.socket.close()
			self.receiver.socket = None
			self.receiver.exitAll
            

	def __init__(self, parent = None):
		# Initialize the constructor
		super(MainWindow, self).__init__(parent)

		
		# Define variables
		self.initAll = False
		#self.FrameNum = 123456789
		self.receiver = Receiver()
		self.receiver.start()
		#self.endDrive = False
		txtList = np.genfromtxt('largeSet.txt',dtype='str',delimiter='\n')
		ansList = np.genfromtxt('largeAnsSet.txt',dtype='int',delimiter='\n')
		# Creates the list of words with corresponding answer keys
		self.responseList = np.vstack((txtList,ansList)).T
		self.rnd = 0
		self.allList = self.responseList[self.rnd*10:self.rnd*10+10,:]
		
		self.counter = 0 # Defines the counter to go over list of phrases and answers
		self.response = np.nan # Keeps track of the response
		self.trialNum = 0 # Keeps track of the trial number
		self.interact = 0 # Keeps track of the number of interactions

		# Set up the GUI
		self.setupUi(self)

		# Show the application in fullscreen
		self.showFullScreen()
		
		# Setting the frames to be full screen
		width = 1920
    #desktop.geometry().width()
		height = 1080
    #desktop.geometry().height()

		# Create the graph object
		self.graph = Graph(width, height)

		# Hide all the frames except the initial
		self.introframe.show()
		self.readyframe.hide()
		self.feedbackframe.hide()
		self.gameframe.hide()
		self.endframe.hide()

		# Position and resize the frames.
		self.introframe.move(0,0)
		self.introframe.resize(width, height)
		self.readyframe.move(0,0)		
		self.readyframe.resize(width, height)
		self.feedbackframe.move(0,0)
		self.feedbackframe.resize(width, height)
		self.gameframe.move(0,0)
		self.gameframe.resize(width, height)
		self.endframe.move(0,0)
		self.endframe.resize(width, height)

		''' BUTTONS '''
		# Button "DONE" on click
		QtCore.QObject.connect(self.btnDone, QtCore.SIGNAL("clicked()"), self.showReadyFrame)
		# Moving UP/DOWN buttons
		QtCore.QObject.connect(self.btnUp, QtCore.SIGNAL("clicked()"), self.moveUp)
		QtCore.QObject.connect(self.btnDown, QtCore.SIGNAL("clicked()"), self.moveDown)
		self.btnUp.setEnabled(False)
		self.btnUp.setStyleSheet("QPushButton{background-color:#B0B0B0;}")
		# Selecting buttons
		QtCore.QObject.connect(self.btnLabelUp, QtCore.SIGNAL("clicked()"), self.Uphighlight)
		QtCore.QObject.connect(self.btnLabelDown, QtCore.SIGNAL("clicked()"), self.Downhighlight)
		# Button "SUBMIT" on click
		QtCore.QObject.connect(self.btnSubmit, QtCore.SIGNAL("clicked()"), self.submitFun)
		# Button "START" on click
		QtCore.QObject.connect(self.btnStart, QtCore.SIGNAL("clicked()"), self.showGameFrame)

	''' HIGHLIGHTING BUTTONS '''
	# This modifies the highligh sequence of the labels
	def Uphighlight(self):
		self.btnLabelUp.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:white;background-color:blue;text-align:left;}")
		self.btnLabelDown.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;text-align:left;}")
		self.response = self.counter
		# Increase counter for interactions with screen
		self.interact += 1
		self.Press = 'UpChoose'
		writecsv(self)
		
	def Downhighlight(self):
		self.btnLabelDown.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:white;background-color:blue;text-align:left;}")
		self.btnLabelUp.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;text-align:left;}")
		tmp = self.counter
		self.response = tmp+1
		# Increase counter for interactions with screen
		self.interact += 1
		self.Press = 'DownChoose'
		writecsv(self)

	''' UP/DOWN BUTTONS '''
	# Functions for moving up or down in the text file
	def moveUp(self):
		if self.counter == 0:
			self.counter = 0
		else:
			self.counter = self.counter - 2
			if self.counter == 0:
				self.btnUp.setEnabled(False)
				self.btnUp.setStyleSheet("QPushButton{background-color:#B0B0B0;}")
		self.btnDown.setEnabled(True)
		self.btnDown.setStyleSheet("QPushButton{background-color:"";}")
		# Modifying labels from buttons
		self.response = np.nan
		self.btnLabelUp.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;text-align:left;}")
		self.btnLabelDown.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;text-align:left;}")
		# Setting up labels
		counter = self.counter
		self.btnLabelUp.setText(QtGui.QApplication.translate("MainWindow",self.allList[counter,0] , None, QtGui.QApplication.UnicodeUTF8))
		self.btnLabelDown.setText(QtGui.QApplication.translate("MainWindow",self.allList[counter+1,0] , None, QtGui.QApplication.UnicodeUTF8))
		# Increase counter for interactions with screen
		self.interact += 1
		self.Press = 'UpArrow'
		writecsv(self)

	def moveDown(self):
		if self.counter == len(self.allList)-2:
			self.counter = len(self.allList)-2
		else:
			self.counter = self.counter + 2
			if self.counter == len(self.allList)-2:
				self.btnDown.setEnabled(False)
				self.btnDown.setStyleSheet("QPushButton{background-color:#B0B0B0;}")
		self.btnUp.setEnabled(True)
		self.btnUp.setStyleSheet("QPushButton{background-color:"";}")
		# Modifying labels from buttons
		self.response = np.nan
		self.btnLabelUp.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;text-align:left;}")
		self.btnLabelDown.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;text-align:left;}")
		# Setting up labels
		counter = self.counter
		self.btnLabelUp.setText(QtGui.QApplication.translate("MainWindow",self.allList[counter,0] , None, QtGui.QApplication.UnicodeUTF8))
		self.btnLabelDown.setText(QtGui.QApplication.translate("MainWindow",self.allList[counter+1,0] , None, QtGui.QApplication.UnicodeUTF8))
		# Increase counter for interactions with screen
		self.interact += 1
		self.Press = 'DownArrow'
		writecsv(self)

	''' SHOW/HIDE FRAMES '''
	# Showing all required frames
	def showReadyFrame(self):
		self.parID = self.editParticipantID.text()
        # The format should be Participant_XX
		self.fileName= "Sce1 "+self.parID.split(" ")[0]+"_"+self.parID.split(" ")[1]

		if self.initAll == False:
			self.initAll = True
        
		# GUI part
		self.introframe.hide()
		self.feedbackframe.hide()
		self.gameframe.hide()
		self.endframe.hide()
		self.readyframe.show()
		
		if not os.path.exists('/Users/hedengbo/Desktop/Results/%s'%self.parID):
			os.makedirs('/Users/hedengbo/Desktop/Results/%s'%self.parID)
		# Only create the file if it does not exist
		if not os.path.exists('/Users/hedengbo/Desktop/Results/%s/%s.csv'%(self.parID,self.fileName)):
			with open('/Users/hedengbo/Desktop/Results/%s/%s.csv'%(self.parID,self.fileName),'wb') as csvfile:
				toFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
				toFile.writerow(['Trial#','Phrase Selected','isCorrect','InteractNum','FrameNum','Content'])


	def showGameFrame(self):
		self.btnUp.setStyleSheet("QPushButton{background-color:#B0B0B0;}")
		self.btnDown.setStyleSheet("QPushButton{background-color:"";}")
		self.btnUp.setEnabled(False)
		self.btnDown.setEnabled(True)
		# Set up the initial words
		counter = self.counter
		self.btnLabelUp.setText(QtGui.QApplication.translate("MainWindow",self.allList[counter,0] , None, QtGui.QApplication.UnicodeUTF8))
		self.btnLabelDown.setText(QtGui.QApplication.translate("MainWindow",self.allList[counter+1,0] , None, QtGui.QApplication.UnicodeUTF8))
		self.response = np.nan
		self.btnLabelUp.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;text-align:left;}")
		self.btnLabelDown.setStyleSheet("QPushButton{border:0px;margin:0px;padding:0px;color:black;background-color:white;text-align:left;}")
		self.introframe.hide()
		self.readyframe.hide()
		self.feedbackframe.hide()
		self.endframe.hide()
		self.gameframe.show()
		self.trialNum += 1
		self.interact += 1
		self.Press = 'Start'
		writecsv(self)
		


	def submitFun(self):
		if np.isnan(self.response):
			self.interact += 1 #increase counter for interactions with screen
			self.Press = 'SubmitEmpty'
			writecsv(self)
		if not np.isnan(self.response):
				# Incorrect response - Keeps on playing the game
			if int(self.allList[self.response,1]) == 0:
				self.lblFeedback.setText(QtGui.QApplication.translate("MainWindow", "Incorrect", None, QtGui.QApplication.UnicodeUTF8))
              # Correct response - Goes back to "Task Is Ready" Screen
			if int(self.allList[self.response,1]) == 1:
				self.lblFeedback.setText(QtGui.QApplication.translate("MainWindow", "Correct", None, QtGui.QApplication.UnicodeUTF8))
			self.gameframe.hide()
			self.feedbackframe.show()
			self.interact += 1 # Increase counter for interactions with screen
			timer = QtCore.QTimer()
			timer.singleShot(1000, self.showReadyFrame)

			# Writing results to file
			self.Press = 'SubmitChosen'
			writecsv(self)

			# Randomizing the next trial
			self.rnd = self.rnd+1
			self.allList = self.responseList[self.rnd*10:self.rnd*10+10,:]
            
          # Resets counter for interactions with screen
			self.interact = 0

		self.counter = 0 # Resets counter for answers
        				
if __name__=='__main__':
	app = QtGui.QApplication(sys.argv)
	app.aboutToQuit.connect(app.deleteLater)
	frame = MainWindow()
	frame.show()
	app.exec_() 	
	
