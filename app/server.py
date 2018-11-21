#from user import *
import os
class Server: 
	allUsers = []
	chatRooms = []

	def addUser(self, user):
		self.allUsers.append(user)

	def getChatRooms(self, user):
		userChatrooms = []
		for c in self.chatRooms:
			if user.id in c.inRoom:
				userChatrooms.append(c)
		return userChatrooms

	def createChatRoom(self, user, name):
		chatroom = ChatRoom(name, user)
		self.chatRooms.append(chatroom)
		dir = 'server/chatrooms/' + name + '.txt'
		if not os.path.exists(dir):
			os.makedirs(dir)
			file = open(dir, 'w')
			file.write(str(user.id)+'\n')



chatroomIdCounter = 0
class ChatRoom:
	name = ''
	inRoom = []
	def __init__(self, name, user):
		self.name = name
		global chatroomIdCounter
		self.id = chatroomIdCounter
		chatroomIdCounter += 1
		self.inRoom.append(user.id)



