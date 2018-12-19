import socket
import sys
import time
from check import ip_checksum

HOST = ''
PORT = 8888
sequence = 1
count = 0

try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print 'Socket created'
except socket.error, msg:
        print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
try:
        s.bind((HOST, PORT))
except socket.error, msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
print 'Socket bind complete'

while 1:
        if count == 1 or count == 6:
                time.sleep(3)
        count = count + 1

        d = s.recvfrom(1024)
        data = d[0]
        addr = d[1]

        if not data:
                print '[Error] Server Failed To Receive Meaningful Data'
                break
        if data[0] == chr(sequence + 48) and data[1:3] == ip_checksum(data[3:]):
                reply = 'OK...' + data[3:]

                s.sendto(chr(sequence + 48) + ip_checksum(reply) + reply, addr)
                sequence = sequence + 1
        else:
                print '[Duplicate Data] Sequence : ' + data[0]
                s.sendto(chr(sequence + 47) + ip_checksum(reply) + reply, addr)
        print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data[3:].strip()
s.close()