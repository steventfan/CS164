import socket
import sys
import time
from check import ip_checksum

HOST = ''
PORT = 8888

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

value = '0'
count = 0

while 1:
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]
    if count == 1:
        time.sleep(3)
    if not data:
        break
    reply = 'OK...' + data[3:]

    if data[0:2] != ip_checksum(data[3:]) or data[2] != value:
        if value == '0':
            reply = '1' + reply
        else:
            reply = '0' + reply
    else:
        reply = value + reply
        if value == '1':
            value = '0'
        else:
            value = '1'
    reply = ip_checksum(reply) + reply
    s.sendto(reply, addr)
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data[3:].strip()
    count += 1
s.close()