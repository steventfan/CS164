import socket
import sys
from check import ip_checksum

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
host = 'localhost'
port = '8888'
value = '1'

while 1:
    if value == '1':
        value = '0'
    else:
        value = '1'

    msg = raw_input('Enter message to send : ')

    try:
        resend = 1
        while resend:
            print 'Sending Packet : ' + value
            if raw_input('----- TEST : ENTER 1 TO CORRUPT DATA ----- : ') == '1':
                check = ip_checksum(msg + 'corrupt')
            else:
                check = ip_checksum(msg)
            s.sendto(check + value + msg, (host, port))

            d = s.recvfrom(1024)
            reply = d[0]
            addr = d[1]

            if reply[0:2] == ip_checksum(reply[2:]) and value == reply[2]:
                print 'Server reply : ' + 'ACK: ' + reply[2] + ' ' + reply[3:]
                resend = 0
            else:
                print 'Server reply : ' + 'ACK: ' + reply[2] + ' Error : Conflicting ACK'
    except socket.error, msg:
            print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()