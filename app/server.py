#from user import *
from Crypto.Hash import SHA256
import os

def createHash(data):
	hashObj = SHA256.new(data.encode('utf-8'))
	return hashObj.hexdigest()

class Server: 
	allUsers = []
	chatRooms = []

	def addUser(self, user):
		self.allUsers.append(user)

	def getChatRooms(self, user):
		userChatrooms = []

		dir = 'server/chatrooms/'
		for filename in os.listdir(dir):
			if filename.endswith('.txt'):
				file = open(dir+filename, 'r')
				if user.loginId in file.read():
					userChatrooms.append(filename[:-4])
		return userChatrooms

	def createChatRoom(self, user, name):
		chatroom = ChatRoom(name, user)
		self.chatRooms.append(chatroom)
		dir = 'server/chatrooms/' + name + '.txt'
		if not os.path.exists(dir):
			#os.makedirs(dir)
			file = open(dir, 'w')
			file.write(str(user.loginId)+'\n')
		else:
			file = open(dir, 'a')
			file.write(str(user.loginId)+'\n')

	def userExists(self, username):
		usernameHash = createHash(username)
		dir = 'server/msgs/'
		for filename in os.listdir(dir):
			if filename == usernameHash:
				return True
		return False

	def userPassCorrect(self, loginId, password):
		dir = 'server/userCredentials/'
		hashedCredentials = createHash('loginId='+str(loginId)+'password='+password)
		for filename in os.listdir(dir):
			file = open(dir+filename, 'r')
			print(dir+filename)
			if file.read() == hashedCredentials:
				return True
		return False

chatroomIdCounter = 0
class ChatRoom:
	name = ''
	inRoom = []
	def __init__(self, name, user):
		self.name = name
		global chatroomIdCounter
		self.id = chatroomIdCounter
		chatroomIdCounter += 1
		self.inRoom.append(user.loginId)




