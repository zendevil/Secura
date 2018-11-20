from user import *

print('Secura. Copyright 2018.')
#loginId = input('Login Id:')
#password = input('Password:')

def getValidUser(loginId, password):
	user = User()
	return user

user = getValidUser(loginId=1, password=1)

c1 = s.createChatRoom(user, 'secret')
c2 = s.createChatRoom(user, 'sauce')
c3 = s.createChatRoom(user, 'space')

if not user:
	exit()

print('Chatrooms.')
count = 0 
chatrooms = s.getChatRooms(user)
for c in chatrooms:
	print(count, c.name)
	count += 1
print('Pick a chatroom number:')
chatroom = chatrooms[int(input())]
print('Entered chatroom', chatroom.name)



print(time.ctime())
while(True):
	msg = input('>')
	user.sendMsg(chatroom, msg)
	user.receiveMsgs(chatroom)



# tests

encrypted = user.encryptMsg(b'298134712389')
signature = user.signMsg(encrypted)



print('mac', user.computeMac(encrypted))

