import socket
import sys
from thread import *

HOST = ''
PORT = 2571

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'

connection = []

def clientthread(conn):
	conn.send('Welcome to the server. Type something and hit enter\n')

	while True:
		data = conn.recv(1024)
		if data[:2] == '!q':
			break
		if data[:8] == '!sendall':
			if len(data) >= 10:
				for i in connection:
					i.sendall(data[9:])
			continue
		reply = 'OK...' + data
		if not data:
			break

		conn.sendall(reply)

	conn.close()

while 1:
	conn, addr = s.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	connection.append(conn)
	start_new_thread(clientthread ,(conn,))

s.close()
