import socket
import sys
from check import ip_checksum

try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
        print 'Failed to create socket'
        sys.exit()
s.settimeout(2)

host = 'localhost';
port = 8888;
base = 1
sequence = 1
N = 4
message = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight']

while sequence < base + N:
        print 'Sending Message : Sequence ' + chr(sequence + 48) + ' : ' + message[sequence - 1]
        s.sendto(chr(sequence + 48) + ip_checksum(message[sequence - 1]) + message[sequence - 1], (host, port))
        if base == sequence:
                s.settimeout(2)
        sequence = sequence + 1

try:
        while 1:
                try:
                        d = s.recvfrom(1024)
                        reply = d[0]
                        addr = d[1]

                        if reply[0] == chr(base + 48) and reply[1:3] == ip_checksum(reply[3:]):
                                print 'Message Received : ACK ' + reply[0] + ' : ' + reply[3:]
                                base = base + 1
                                if base == sequence:
                                        break
                                else:
                                        s.settimeout(2)
                                if sequence <= 8:
                                        print 'Sending Message : Sequence ' + chr(sequence + 48) + ' : ' + message[sequence - 1]
                                        s.sendto(chr(sequence + 48) + ip_checksum(message[sequence - 1]) + message[sequence - 1], (host, port))
                                        sequence = sequence + 1
                        else:
                                print '[Error] Sequence : ' + reply[0] + ' ' + reply[3:]
                except socket.timeout:
                        print 'Timeout'
                        for i in range(0, N):
                                if base + i <= 8:
                                        print 'Resending Message Sequence ' + chr(base + i + 48) + ' : ' + message[base + i - 1]
                                        s.sendto((chr(base + i + 48)) + ip_checksum(message[base + i - 1]) + message[base + i - 1], (host, port))
                        continue
except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()