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

	def createChatRoom(self, name, loginIdHash):
		chatroom = ChatRoom(name, loginIdHash)
		self.chatRooms.append(chatroom)
		dir = 'server/chatrooms/' + name + '.txt'
		if not os.path.exists(dir):
			#os.makedirs(dir)
			file = open(dir, 'w')
			file.write(loginIdHash+'\n')
		else:
			file = open(dir, 'a')
			file.write(loginIdHash+'\n')

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

	def incSndSeq(self, chatroomHash, loginIdHash):
		filepath = 'server/msgs/'+loginIdHash+'/'+chatroomHash+'/sndSeq.txt'
		incFileValBy(filepath, 1)

chatroomIdCounter = 0
class ChatRoom:
	name = ''
	inRoom = []
	def __init__(self, name, loginIdHash):
		self.name = name
		global chatroomIdCounter
		self.id = chatroomIdCounter
		chatroomIdCounter += 1
		self.inRoom.append(loginIdHash)



def incFileValBy(filepath, num):
		file = open(filepath, 'r+')
		sqn = file.read()
		file.seek(0)
		file.write(str(int(sqn) + num))
		file.truncate()