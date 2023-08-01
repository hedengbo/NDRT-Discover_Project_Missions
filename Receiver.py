import socket
import struct
import csv
import numpy as np
from PySide.QtCore import Qt, QObject, QThread, Signal

class Receiver(QThread):
	FrameNum = Signal()
	# Receiver constructor
	def __init__(self):
		# Call the thread's constructor
		QThread.__init__(self)
		
		# Initialize the variables
		self.FrameNum = 0
		success = 0
		while not success:        
				try:
			# Create a new socket, use IPv4 and UDP
			# Then bind the socket to localhost and the port
					self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					self.socket.bind(('90.0.0.50', 1228))
					success = 1
				except socket.error as err:
			# Could not create the socket, bind it, or listen on the port.
			# Print the error message
					print "Could not create the socket:", err
					self.socket = None
	
	def setReceiverVars(self,out):
		with open('../test.csv','ab') as csvfile:
			toFile = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
			toFile.writerow(['%s'%self.FrameNum])

	# Receiver destructor
	def exitAll():
		QThread.quit() 
        
	# Runs the receiver
	def run(self):
		# Check that the socket is alive
		if self.socket is None:
			return; 

		while True:
			# Receive the data, then check that some data was returned
			packet = self.socket.recv(256)

			if not packet: break
										
			# VARIABLE: LOG STREAM
			if len(packet) == 4:
				# Unpack the data (integer type)
				data = struct.unpack('<i', packet)
				self.FrameNum = data     
               
		# Clean up
		self.socket.close()
		self.socket = None

# ---OLD CODE TO RUN RECEIVER ON ITS OWN---
# thread = Receiver();
# thread.start()

