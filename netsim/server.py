from user import *
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
		


