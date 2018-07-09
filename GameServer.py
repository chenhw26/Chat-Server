import threading
import time
import socket

class GameServer(threading.Thread):
    '''游戏服务器'''
    def __init__(self, addr):
        super().__init__()
        self.HOST = addr
        self.PORT = 2160
        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)
        self.users = {}
        self.socks = []
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.bind(self.ADDR)
        self.tcp.listen(5)
        self.t = threading.Thread(target=self.recv_data)

    def recv_data(self):
        while True:
            for s in self.socks:
                try:
                	data = s.recv(self.BUFSIZ).decode('utf8')
                except Exception:
                	continue
                if not data:
                	self.socks.remove(s)
                	continue
                text = data.split(' ')
                print(text)
                if(text[0] == 'hello'): #登记
                	self.users[text[1]] = s
                	print('user {} loging'.format(text[1]))
                else:				    #转发
                	if self.users.__contains__(text[1]):
                		self.users[text[1]].send(data.encode('utf8'))
                		print('forward from {} to {}.'.format(text[0], text[1]))
                	else:
                		s.send("miss connect error".encode('utf8'))
                		print('return error')

				#data = '{}, {}'.format(time.ctime(), data)
				#s.send(data.encode('utf8'))

    def run(self):
        self.t.start()
        print('waiting for connecting...')
        while True:
            clientSock, addr = self.tcp.accept()
            print('connect from', addr)
            clientSock.setblocking(0)
            self.socks.append(clientSock)
        self.t.join()