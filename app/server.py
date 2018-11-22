#from user import *
import os
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




