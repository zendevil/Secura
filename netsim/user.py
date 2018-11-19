from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256, HMAC
from Crypto.Util import Padding
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from server import Server, ChatRoom

s = Server()

userIdCounter = 0
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
		sendReq(self.id, 'c', chatroom)

	def getChatRooms():
		return chatrooms

	def sendMsg(chatroom, message):
		sendReq(self.id, 'm', 'CHATROOM='+chatroom+'BEGIN MESSAGE='+msg+'MAC='+computeMac(msg)+'SIGNATURE='+signMessage(msg))

	def recEncKey(self, key):
		receivedKey = key

	def signMsg(self, message):
		signPrivateKey = RSA.import_key(open('private.pem').read())
		h = SHA256.new(message)
		signature = pkcs1_15.new(signPrivateKey).sign(h)
		return signature

	def authenticateSign(self, message, signature):
		signPublicKey = RSA.import_key(open('public.pem').read())
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
		h.update(msg)
		return h.hexdigest()




# All users will automatically be added in the server s. 
# Check User constructor
