from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256, HMAC
from Crypto.Util import Padding
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from server import *
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
		print('password', password)
		self.sendReq('u', 'loginId='+loginId+'password='+password)

	def sendReq(self, messageType, msg):
		global msgSentCounter

		if messageType == 'm':

			chatroom = parseChatRoom(msg)
			
			hashedloginId = createHash(self.loginId)
			hashedChatroom = createHash(chatroom)
			sndSeqDir = 'server/msgs/'+hashedloginId+'/'+hashedChatroom+'/sndSeq.txt'
			file = open(sndSeqDir, 'r')
			msg = 'SEND SEQ='+file.read()+msg	
			pubKey = RSA.import_key(open('keys/user/enc_public.pem').read())
			sessionKey = get_random_bytes(16)
			
			# encrypt session key 
			cipherRsa = PKCS1_OAEP.new(pubKey)
			encSessionKey = cipherRsa.encrypt(sessionKey)
			
			# encrypt data
			cipherAes = AES.new(sessionKey, AES.MODE_EAX)
			ciphertext, tag = cipherAes.encrypt_and_digest(msg.encode('utf-8'))
			
			others = self.usersInChatRoom(chatroom)
			for o in others:
				dir = 'server/msgs/'+o+'/'+createHash(chatroom)+'/toReceive/'
				if not os.path.exists(dir):
					#print('path'+dir+'doesn\'t exist')
					os.makedirs(dir)
				file = open(dir+str(msgSentCounter)+'.bin', 'wb')
				[file.write(x) for x in (encSessionKey, cipherAes.nonce, tag, ciphertext)]
			s.incSndSeq(createHash(chatroom), hashedloginId)

		elif messageType == 'c':
			print('create message received')
			s.createChatRoom(msg, createHash(self.loginId))

		elif messageType == 'u':
			dir = 'server/userCredentials/'
			hashedCredentials = createHash(msg)
			if not os.path.exists(dir):
				os.makedirs(dir)
			file = open(dir+numUsers()+'.txt', 'w')
			file.write(hashedCredentials)
			incFileValBy('server/numUsers.txt', 1)
			print('User created')

	def decryptUserCredentials(file):
		priKey = RSA.import_key(open('keys/user/pass_private.pem').read())
		return decrypt(file, priKey)

	def decryptMsg(self, filename):
		priKey = RSA.import_key(open('keys/user/enc_private.pem').read())
		return decrypt(filename, priKey)


	def joinChatRoom(self, chatroom):
		self.currChatRoom = chatroom
		self.sendReq('c', chatroom)
		
		dir = 'server/msgs/' + createHash(self.loginId)+'/'+createHash(self.currChatRoom)
		if not os.path.exists(dir):
			os.makedirs(dir)
		file = open(dir + '/sndSeq.txt', 'w+')
		file.write('0')

	def sendMsg(self, msg):
		msg = 'SENDER='+self.loginId+'CHATROOM='+self.currChatRoom+'BEGIN MESSAGE='+msg+'MAC='+\
		self.computeMac(msg)+'SIGNATURE='#+self.signMsg(msg))
		
		self.sendReq('m', msg)

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
		loginIdHash = createHash(self.loginId)
		currChatRoomHash = createHash(self.currChatRoom)
		rdir = 'server/msgs/'+loginIdHash+'/'+currChatRoomHash+'/toReceive/'
		count = 0
		for file in os.listdir(rdir):
			count += 1
			#if not file == 'sendSeq.txt':
			fileContent = self.decryptMsg(rdir+file)
			#fileContent = open(rdir+file, 'rb').read().decode('utf-8')
			print(parseSender(fileContent)+': '+parseMsg(fileContent))
			os.remove(rdir+file)
		if count > 0:
			filepath = 'server/msgs/'+loginIdHash+'/'+currChatRoomHash+'/recSqn.txt'
			if os.path.isfile(filepath):
				incFileValBy(filepath, count)
			else:
				file = open(filepath, 'w+')
				file.write('0')


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

	def computeMac(self, msg):
		secret = b'secret'
		h = HMAC.new(secret, digestmod=SHA256)
		h.update(msg.encode('utf-8').strip())
		return h.hexdigest()

	def usersInChatRoom(self, chatroomName):
		usersInChatRoom = []
		file = open('server/chatrooms/'+chatroomName+'.txt', 'r')
		for line in file:
			#if not line == str(self.id) +'\n':
			usersInChatRoom.append(line[:-1])
		return usersInChatRoom

def decrypt(filename, key):
	file = open(filename, 'rb')
	encSessionKey, nonce, tag, ciphertext = \
	[file.read(x) for x in (key.size_in_bytes(), 16, 16, -1)]
	# decrypt session key
	cipherRsa = PKCS1_OAEP.new(key)
	sessionKey = cipherRsa.decrypt(encSessionKey)
	# decrypt data 
	cipherAes = AES.new(sessionKey, AES.MODE_EAX, nonce)
	data = cipherAes.decrypt_and_verify(ciphertext, tag)
	return data.decode('utf-8')

# def encryptMsg(self, msg):
# 	print('encoded', msg.encode('utf-8'))
# 	msg = Padding.pad(msg.encode('utf-8'), AES.block_size, style='iso7816')
# 	print('after padding', msg)
# 	iv = get_random_bytes(AES.block_size)
# 	ENC = AES.new(self.encPrivateKey, AES.MODE_CBC, iv)
# 	encrypted = ENC.encrypt(msg)
# 	print(type(encrypted))
# 	return encrypted

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
	return open('server/numUsers.txt', 'r').read()

def incFileValBy(filepath, num):
		file = open(filepath, 'r+')
		sqn = file.read()
		file.seek(0)
		file.write(str(int(sqn) + num))
		file.truncate()


