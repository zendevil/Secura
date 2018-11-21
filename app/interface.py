from user import *
import os
from sys import platform
print('Secura. Copyright 2018.')
loginId = input('Login Id:')
password = input('Password:')

def getValidUser(loginId, password):
	user = User(loginId, password)
	return user

user = getValidUser(loginId, password)

c1 = user.createChatRoom('secret')
c2 = user.createChatRoom('sauce')
c3 = user.createChatRoom('space')

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
user.joinChatRoom(chatroom)


if platform == 'linux' or platform == 'linux 2' or platform == 'darwin':
	os.system('clear')
elif platform == 'win64' or platform == 'win32':
	os.system('cls')


print('Entered chatroom', chatroom.name)
print(time.ctime())
while(True):
	msg = input()
	user.sendMsg(msg)
	user.receiveMsgs()


# tests
