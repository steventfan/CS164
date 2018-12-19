import socket
import sys


host = ''
port = 8888
accounts = [['sfan', 'testing123', 0], ['bliou', 'tienrenboba', 0], ['kazi', 'curryrice', 0]]
addresses = []
buffers = []
messages = []

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error, msg:
	print '[ERROR] Failed to create socket'
	sys.exit()
try:
	s.bind((host, port))
except socket.error:
	print '[ERROR] Failed to bind socket'
	sys.exit()
while 1:
	reply = ''
	d = s.recvfrom(1024)
	data = d[0]
	addr = d[1]
	sequence = -1
	for i in range(len(addresses)):
		if addresses[i][0] == addr:
			sequence = addresses[i][1]
	if not data:
		print '[ERROR] Failed to read data'
		break
	if data[0] == '0':
		for i in range(len(accounts)):
			if accounts[i][0] == data[1:]:
				if accounts[i][2] == 0:
					addresses.append([addr, i])
					reply = '0'
				else:
					j = len(addresses) - 1
					while j >= 0:
						if addresses[j][0] == addr:
							addresses.pop(j)
						j = j - 1	
					reply = '1'
				break
		if len(reply) == 0:
			reply = '2'
	elif data[0] == '1':
		if data[1:] == accounts[sequence][1]:
			if accounts[sequence][2] == 0:
				accounts[sequence][2] = 1
				reply = '0'
			else:
				reply = '1'
		else:
			reply = '2'
	elif data[0] == '2':
		accounts[sequence][1] = data[1:]
		reply = '0'
	elif data[0] == '3':
		accounts[sequence][2] = 0
		i = len(addresses) - 1
		while i >= 0:
			if addresses[i][0] == addr:
				addresses.pop(i)
			i = i - 1
		reply = '0'
	elif data[0] == '4':
		for i in range(len(accounts)):
			if accounts[i][0] == data[1:]:
				buffers.append([addr, data[1:]])
				reply = '0'
				break
		if i >= len(accounts):
			reply = '1'
	elif data[0] == '5':
		for i in range(len(buffers)):
			if buffers[i][0] == addr:
				for j in range(len(accounts)):
					if buffers[i][1] == accounts[j][0]:
						buffers.pop(i)
						messages.append([j, data[1:]])
						break
				if j >= len(accounts):
					reply = '1'
				break
		if i >= len(buffers):
			reply = '1'
	elif data[0] == '6':
		for i in range(len(accounts)):
			if accounts[i][2] == 1:
				for j in range(len(addresses)):
					if i != addresses[j][1]:
						messages.append([i, data[1:]])
		reply = '0'
	elif data[0] == '7':
		for i in range(len(addresses)):
			if addresses[i][0] == addr:
				reply = ''
				j = len(messages) - 1
				while j >= 0:
					if addresses[i][1] == messages[j][0]:
						reply = messages[j][1] + '\n' + reply
						messages.pop(j)
					j = j - 1
				if len(reply) == 0:
					reply = '1'
				else:
					reply = '0' + reply
	elif data[0] == '8':
		for i in range(len(addresses)):
			if addresses[i][0] == addr:
				count = 0
				for j in range(len(messages)):
					if addresses[i][1] == messages[j][0]:
						count = count + 1
		reply = str(count)
	s.sendto(reply, addr)
