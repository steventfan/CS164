import socket
import sys
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

value = '1'

while 1:
    if value == '1':
        value = '0'
    else:
        value = '1'
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]

    if not data:
        break
    reply = 'OK...' + data[3:]
    
    if data[0:2] != ip_checksum(data[3:]) or data[2] != value:
        if value == '1':
            reply = '0' + reply
            value = '0'
        else:
            reply = '1' + reply
            value = '1'
    else:
        reply = value + reply
    reply = ip_checksum(reply) + reply
    s.sendto(reply, addr)
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data[3:].strip()
    s.close()