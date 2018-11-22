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

if not user:
	exit()

print('Chatrooms.')
count = 0 
chatrooms = s.getChatRooms(user)
for c in chatrooms:
	print(count, c)
	count += 1
print('Pick a chatroom number:')
i = input()
if not i == 'j':
	chatroom = chatrooms[int(i)]
	
else:
	chatroom = input('Name of the chatroom you would like to join:')
user.joinChatRoom(chatroom)


if platform == 'linux' or platform == 'linux 2' or platform == 'darwin':
	os.system('clear')
elif platform == 'win64' or platform == 'win32':
	os.system('cls')


print('Entered chatroom', chatroom)
print(time.ctime())
while(True):
	msg = input()
	CURSOR_UP_ONE = '\x1b[1A'
	ERASE_LINE = '\x1b[2K'
	print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
	print(end='\r')
	user.sendMsg(msg)
	user.receiveMsgs()


# tests
