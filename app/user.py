from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256, HMAC
from Crypto.Util import Padding
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from server import Server, ChatRoom
import os, time, threading, re

s = Server()

userIdCounter = 0
msgSentCounter = 0
class User:
	loginId = ''
	password = ''
	signPublicKey = b''
	signPrivateKey = b''
	encPublicKey = b''
	encPrivateKey = b''
	sndSeq = 0
	rcvSeq = 0

	def __init__(self, loginId, password):
		global userIdCounter
		self.id = userIdCounter 
		userIdCounter += 1
		s.addUser(self)
		self.createSignKeyPair()
		self.createEncKeyPair()
		self.loginId = loginId
		self.password = password
		self.sendReq('u', 'loginId='+str(loginId)+'password='+password)

	def sendReq(self, messageType, msg):
		global msgSentCounter

		if messageType == 'm':
			others = self.otherUsersInChatRoom(parseChatRoom(msg.decode('utf-8')))
			#print('others in this chatroom', others)
			for o in others:
				dir = 'server/msgs/'+o+'/'+self.currChatRoom+'/toReceive/'
				if not os.path.exists(dir):
					print('path'+dir+'doesn\'t exist')
					os.makedirs(dir)
				file = open(dir+str(msgSentCounter)+'.txt', 'wb')
				file.write(msg)


		elif messageType == 'c':
			print('create message received')
			s.createChatRoom(self, msg)

		elif messageType == 'u':
			print('creating user')
			dir = 'server/userCredentials/'
			pubKey = RSA.import_key(open('keys/user/pass_public.pem').read())
			sessionKey = get_random_bytes(16)
			cipherRsa = PKCS1_OAEP.new(pubKey)
			encSessionKey = cipherRsa.encrypt(sessionKey)

			cipherAes = AES.new(sessionKey, AES.MODE_EAX)
			ciphertext, tag = cipherAes.encrypt_and_digest(msg.encode('utf-8'))

			if not os.path.exists(dir):
				os.makedirs(dir)
			file = open(dir+numUsers()+'.bin', 'wb')
			[file.write(x) for x in (encSessionKey, cipherAes.nonce, tag, ciphertext)]
			file = open('server/numUsers.txt', 'r+')
			count = file.read()
			file.seek(0)
			file.write(str(int(count) + 1))
			file.truncate()
			
	def joinChatRoom(self, chatroom):
		self.currChatRoom = chatroom
		self.sendReq('c', chatroom)

	def sendMsg(self, msg):
		self.sendReq('m', ('SENDER='+self.loginId+'CHATROOM='+self.currChatRoom+'BEGIN MESSAGE='+msg+'MAC='
			+self.computeMac(msg)+'SIGNATURE=').encode('utf-8').strip())#+self.signMsg(msg))


	def createSignKeyPair(self):
		key = RSA.generate(2048)

		signPrivateKey = key.export_key()
		file_out = open('keys/sign_private'+str(self.id)+'.pem', 'wb')
		file_out.write(signPrivateKey)

		signPublicKey = key.publickey().export_key()
		file_out = open('keys/sign_public'+str(self.id)+'.pem', 'wb')
		file_out.write(signPublicKey)

	def createEncKeyPair(self):
		key = get_random_bytes(32)

		self.encPrivateKey = key
		file_out = open('keys/enc_private'+str(self.id)+'.pem', 'wb')
		file_out.write(self.encPrivateKey)

		self.encPublicKey = key
		file_out = open('keys/enc_public'+str(self.id)+'.pem', 'wb')
		file_out.write(self.encPublicKey)
	
	def createChatRoom(self, chatroomName):
		chatroom = ChatRoom(chatroomName, self)
		print('sending request in createChatRoom')
		self.sendReq('c', chatroomName)
		self.currChatRoom = chatroom



	def receiveMsgs(self):
		rdir = 'server/msgs/'+str(self.loginId)+'/'+self.currChatRoom+'/toReceive/'
		for file in os.listdir(rdir):
			fileContent = open(rdir+file, 'rb').read().decode('utf-8')
			print(parseSender(fileContent)+': '+parseMsg(fileContent))
			os.remove(rdir+file)
		threading.Timer(5, self.receiveMsgs).start()

	def recEncKey(self, key):
		receivedKey = key

	# def signMsg(self, message):
	# 	signPrivateKey = RSA.import_key(open('keys/sign_private'+str(self.id)+'.pem').read())
	# 	h = SHA256.new((message).encode('utf-8').strip())
	# 	signature = pkcs1_15.new(signPrivateKey).sign(h)
	# 	return signature

	def authenticateSign(self, message, signature):
		signPublicKey = RSA.import_key(open('keys/sign_public'+str(self.id)+'.pem').read())
		h = SHA256.new(message)
		try:
			pkcs1_15.new(signPublicKey).verify(h,signature)
			print('Valid Signature')
		except(ValueError, TypeError):
			print('Invalid Signature')

	def encryptMsg(self, msg):
		msg = Padding.pad(msg, AES.block_size, style='iso7816')
		iv = get_random_bytes(AES.block_size)
		ENC = AES.new(self.encPrivateKey, AES.MODE_CBC, iv)
		encrypted = ENC.encrypt(msg)
		return encrypted

	def computeMac(self, msg):
		secret = b'secret'
		h = HMAC.new(secret, digestmod=SHA256)
		h.update(msg.encode('utf-8').strip())
		return h.hexdigest()

	def otherUsersInChatRoom(self, chatroomName):
		usersInChatRoom = []
		file = open('server/chatrooms/'+chatroomName+'.txt', 'r')
		for line in file:
			if not line == str(self.id) +'\n':
					usersInChatRoom.append(line[:-1])
		return usersInChatRoom

def parseMsg(payload):
	return findStrBetween(payload, 'BEGIN MESSAGE=', 'MAC=')
def parseChatRoom(payload):
	return findStrBetween(payload, 'CHATROOM=', 'BEGIN MESSAGE=')
def parseSender(payload):
	return findStrBetween(payload, 'SENDER=', 'CHATROOM=')

def findStrBetween(string, substr1, substr2):
	foundStr = re.search(substr1+'(.*)'+substr2, string)
	return(foundStr.group(1))

def numUsers():
	return open('server/numUsers.txt', 'r').read()[:-1]


