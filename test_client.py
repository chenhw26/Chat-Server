import socket
import threading
import time
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 20000))

def listen():
    while True:
        try:
            print(s.recv(1024).decode('utf-8'))
            print("received")
        except:
            sys.exit(0)

t = threading.Thread(target=listen)
t.start()

while True:
    msg = input()
    for i in range(0, len(msg)):
        if msg[i] == 'n':   
            msg = msg[:i] + '\n' + msg[i+1:]
    s.send(msg.encode('utf-8'))
    if msg == '9':  break
s.close()

