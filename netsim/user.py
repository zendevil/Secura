from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256, HMAC
from Crypto.Util import Padding
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from server import Server, ChatRoom
import os, time, threading, re

s = Server()

userIdCounter = 0
msgSentCounter = 0
class User:
	signPublicKey = b''
	signPrivateKey = b''
	encPublicKey = b''
	encPrivateKey = b''
	sndSeq = 0
	rcvSeq = 0

	def __init__(self):
		global userIdCounter
		self.id = userIdCounter 
		userIdCounter += 1
		s.addUser(self)
		self.createSignKeyPair()
		self.createEncKeyPair()

	
	def sendReq(self, userId, messageType, msg):
		global msgSentCounter
		chatroom = re.search('CHATROOM=(.*)BEGIN MESSAGE=', msg.decode('utf-8'))
		print(result.group(1))
		directory = 'server/msgs/'+''+str(userId)+'/toSend/'
		if not os.path.exists(directory):
			print('path'+directory+'doesn\'t exist')
			os.makedirs(directory)
		file = open(directory+str(msgSentCounter)+'.txt', 'wb')
		file.write(msg)
		print('request sent')


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
	
	def createChatRoom(chatroom):
		self.sendReq(self.id, 'c', chatroom)

	def sendMsg(self, chatroom, msg):
		self.sendReq(self.id, 'm', ('CHATROOM='+chatroom.name+'BEGIN MESSAGE='+msg+'MAC='+self.computeMac(msg)+'SIGNATURE=').encode('utf-8').strip()+self.signMsg(msg))

	def receiveMsgs(self, chatroom):
		for file in os.listdir('server/'+c.name+'toReceive/'):
			print(file.read().decode('utf-8'))
			os.remove(file)
		threading.Timer(5, self.receiveMsgs).start()

	def recEncKey(self, key):
		receivedKey = key

	def signMsg(self, message):
		signPrivateKey = RSA.import_key(open('keys/sign_private'+str(self.id)+'.pem').read())
		h = SHA256.new((message).encode('utf-8').strip())
		signature = pkcs1_15.new(signPrivateKey).sign(h)
		return signature

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