class User:
	id = ''
	key = b''
	def __init__(self, id):
		self.id = id
	def addCertificate(cert):
		self.certificate = cert
	def createChatRoom(chatroom):
		sendReq(self.id, 'c', chatroom)
	def sendMsg(chatroom, message):
		sendReq(self.id, 'm', 'CHATROOM'chatroom+'BEGIN MESSAGE'+message)

	def sendReq(userId, reqType, data):


class ChatRoom:
	id = ''
	inRoom = []
	def __init__(self, id, user):
		self.id = id
		self.inRoom.append(user)



class Server: 
	allUsers = []
	chatRooms = []



s = Server()

u1 = User('1223')
c1 = ChatRoom(u1)

s.allUsers.append(u1)

print (s.allUsers[0].id)
print(c1.inRoom[0].id)
