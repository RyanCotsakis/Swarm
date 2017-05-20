import pygame
from socket import *
import time
import sys
import threading
from Tkinter import *

import serverGame
import clientGame

SENTINEL = -100
timeoutAfter = 1
killThreads = False

clients = []

class Client():
	def __init__(self, sock, IP):
		self.sock = sock
		self.IP = IP
		self.received = []
		self.listenThread = threading.Thread(target = self.listen)
		self.listenThread.start()
		self.isAlive = True

	"""
	Don't call this! Used only in a new thread
	"""
	def listen(self):
		while True:
			if killThreads:
				self.isAlive = False
				break
			try:
				message = str(self.sock.recv(1024)).split('_')
				if len(message) > 1:
					self.received += message[1:]
			except timeout:
				pass


	def send(self, message):
		self.sock.send(message)

	"""
	Does not block. Returns list of recently sent
	"""
	
	def get(self):
		"""if len(self.received) == 0:
			return SENTINEL
		toReturn = self.received[0]
		del self.received[0]
		return toReturn"""

		toReturn = self.received
		self.received = []
		return toReturn


# --- MAIN PROCESS ---
class UserInterface(Frame):
	processes = 0 #not including self. Number of CA's being read.

	#TKinter tutorials will tell more a bout this than I can.
	def __init__(self,parent):
		self.waitingForClients = False
		self.waitingForHost = False
		self.numberOfClients = 0

		self.wasAGame = False

		Frame.__init__(self,parent)
		self.parent = parent
		self.parent.title("Swarm")

		"""Button(text = "Load Progress", command = self.loadProgress).grid(row = 0, column = 0, rowspan = 2, pady = 10)
		self.progress = StringVar()
		self.progress.set("No Progress Loaded")
		Label(textvariable = self.progress).grid(row = 0, column = 1, rowspan = 2)"""


		Label(text = "Type IP address of host to join their game").grid(row = 2, column = 0, columnspan = 2)

		Label(text = "IP Address:").grid(row = 4, rowspan = 2, column = 0)
		self.addrEntry = Entry()
		self.addrEntry.grid(row = 4, column = 1)

		Button(text = "Join Game", command = self.join).grid(row = 4, column = 2, rowspan = 2, padx = 10)
		self.connected = StringVar()
		self.connected.set("Not Connected")
		Label(textvariable = self.connected).grid(row = 4, column = 3, rowspan = 2, padx = 10)

		Button(text = "Host Server", command = self.hostServer).grid(row = 7, column = 0, rowspan = 2, pady = 20)
		self.waitLabel = StringVar()
		self.waitLabel.set("")
		Label(textvariable = self.waitLabel).grid(row = 7, column = 1, columnspan = 2, rowspan = 2, padx = 10)

		Button(text = "Start Game", command = self.startGame, padx = 50).grid(row = 9, column = 0, columnspan = 2, rowspan = 2)


	"""def loadProgress(self):
		fname = tkFileDialog.askopenfilename(filetypes = (("Text Document","*.txt"),("All Files","*.*")))
		try:
			f = open(fname, mode = 'r')
			data = f.read()
			f.close()
			fname = fname.split("/")
			self.progress.set(fname[len(fname)-1])
		except:
			print "ERROR: could not open <" + fname + ">"
			sys.stdout.flush()"""


	def join(self):
		if not self.waitingForClients and not self.waitingForHost:
			addr = self.addrEntry.get()
			port = 5000
			s = socket()

			try:
				s.connect((addr,port))
				s.settimeout(timeoutAfter)
				server = Client(s,addr)
			except:
				print "ERROR: could not connect to <" + addr + ">"
				sys.stdout.flush()
				s.close()
				return
			self.connected.set("Connected! Waiting for host to start game")
			self.waitingForHost = True
			print "Waiting for host...\nPlease do not close this window"
			"""sys.stdout.flush()
			t = threading.Thread(target = clientGame.start, args = (server,))
			t.start()"""
			self.parent.destroy()
			clientGame.start(server)
		else:
			print "ERROR: Cannot join at this time. Reopen window and try again"
			sys.stdout.flush()


	def hostServer(self):
		if not self.waitingForHost and not self.waitingForClients:
			#hostIP = "127.0.0.1"
			hostIP = gethostbyname(gethostname())
			port = 5000
			try:
				s = socket()
				s.bind((hostIP,port))
				s.listen(5)
				s.settimeout(timeoutAfter)
				acceptThread = threading.Thread(target = self.acceptClients, args = (s,hostIP)) #want to start the accept clients function at the top. this is were we update numberOfClients
				acceptThread.start()
				self.waitingForClients = True
				self.waitLabel.set("Host IP: " + hostIP + "    Number of Clients: " + str(self.numberOfClients))
				print "Server Enabled. Host IP: <" + hostIP + ">"
				sys.stdout.flush()
			except:
				print "ERROR: could not host game on <" + hostIP + ">"
				sy.stdout.flush()
		else:
			print "ERROR: Cannot host at this time. Reopen window and try again"
			sys.stdout.flush()


	def acceptClients(self, serv, hostIP): #this will be called by a new thread
		while True:
			if killThreads:
				break
			try:
				c, addr = serv.accept()
				self.numberOfClients += 1
				self.waitLabel.set("Host IP: " + hostIP + "    Number of Clients: " + str(self.numberOfClients))
				print "Client connected on <" + str(addr) + ">"
				sys.stdout.flush()
				c.settimeout(timeoutAfter)
				client = Client(c, addr)
				clients.append(client)
			except timeout:
				"Keep Listening"



	def startGame(self):
		if not (self.waitingForHost or self.wasAGame):
			print "Loading Game..."
			sys.stdout.flush()
			"""t = threading.Thread(target = serverGame.start, args = (clients,))
			t.start()
			self.wasAGame = True"""
			self.parent.destroy()
			serverGame.start(clients)

		elif self.waitingForHost:
			print "ERROR: Host must start the game"
			sys.stdout.flush()
		else:
			self.waitLabel.set("Sorry, please reopen this window to start a new game")

		

if __name__ == '__main__':
	root = Tk()
	root.geometry("600x200+100+100")
	UserInterface(root)
	root.mainloop()
	print "Bye Bye"
	sys.stdout.flush()
	killThreads = True