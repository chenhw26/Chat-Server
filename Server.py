import threading
import json
import socket
import time
import Usr
import PrivateChat
import Moments
import GroupChat
import FriendsManage

class Server(threading.Thread):
	"""服务器类，继承自线程类，为每个TCP连接创建一个线程，这个线程专门处理该连接发来的消息"""
	def __init__(self, onlinesocket, onlinesocket_lock, usr_locks, usr_locks_lock, group_locks, group_locks_lock, sock):
		super().__init__()
		self.onlinesocket = onlinesocket
		self.onlinesocket_lock = onlinesocket_lock
		self.usr_locks = usr_locks
		self.usr_locks_lock = usr_locks_lock
		self.group_locks = group_locks
		self.group_locks_lock = group_locks_lock
		self.sock = sock
		print("new usr")

	def login(self, hello):
		"""登陆函数，返回是否成功与id"""
		usr_id, psw = int(hello[1:6]), hello[6:]                    # 读出请求登陆的用户id，输入的密码
		usr_profile, succeed = Usr.get_profile(usr_id)
		if not succeed or usr_profile[2] != psw:             # 用户id不存在或密码错误
			print("psw:", usr_profile[2], psw)
			time.sleep(0.1)
			self.sock.send('1'.encode('utf-8'))
			return (False, None)
		elif usr_profile[3]:								#该用户目前处于被封禁状态
			time.sleep(0.1)
			self.sock.send('1'.encode('utf-8'))               
		else:                                                  #id和密码都无误
			time.sleep(0.1)
			self.sock.send('0'.encode('utf-8'))
			return (True, usr_id)
	
	def run(self):
		"""服务器主进程"""
		while True:	
			try:
				hello = self.sock.recv(2048).decode('utf-8')        # 客户端的首个消息，必须是登陆或注册请求
				print("hello", hello)
			except:
				print("usr quit1")
				self.sock.close()
				return

			if hello[0] == '0' and hello[1:6] == '00000':      # 客户放弃登陆，关闭连接
				self.sock.close()
				print("usr quit2")
				return	
			if hello[0] == '0':                                 #用户登陆	
				succeed, self.id = self.login(hello)
				if succeed:	break                              #登陆成功
				else:	continue                               #登陆失败
			elif hello[0] == '1':                               #用户注册
				sep = hello.find('\n')
				self.id = int(Usr.new_usr(hello[1:sep], hello[sep + 1: ]))
				time.sleep(0.1)
				self.sock.send(('0' + str(self.id)).encode('utf-8'))       #向客户端反馈成功信息
				break
			else:                                               #客户端首个消息不合规范，退出连接
				self.sock.close()
				print("usr quit3")
				return 

		self.profile = (Usr.get_profile(self.id))[0]          # 保存当前用户基本信息

		self.onlinesocket_lock.acquire()
		self.onlinesocket[self.id] = self.sock                 #更新在线用户sock
		self.onlinesocket_lock.release()
		
		Usr.check_lock(self.id, self.usr_locks, self.usr_locks_lock)

		unrecieved = Usr.get_and_clear_unrecieved(self.id, self.usr_locks[self.id])
		for msg in unrecieved:
			print('send unreceived')
			time.sleep(0.1)
			self.sock.send(msg.encode('utf-8'))                      #将客户下线时未接受的消息发送给客户
		time.sleep(0.1)
		self.sock.send('0'.encode('utf-8'))

		try:
			while True:                                             #接受客户消息
				cmd = self.sock.recv(4096).decode('utf-8')
				print('rec:', cmd)
				if cmd[0] == '0':
					PrivateChat.private_chat(cmd[1:], self.profile, self.sock, self.onlinesocket, self.usr_locks, self.usr_locks_lock)
				elif cmd[0] == '1':
					GroupChat.group_chat(cmd[1:], self.id, self.sock, self.onlinesocket, self.usr_locks, self.usr_locks_lock, self.group_locks, self.group_locks_lock)
				elif cmd[0] == '2':
					Moments.moments(cmd[1:], self.id, self.sock, self.usr_locks)
				elif cmd[0] == '3':
					FriendsManage.friends_manage(cmd[1:], self.id, self.sock, self.onlinesocket, self.usr_locks, self.usr_locks_lock)
				elif cmd[0] == '4':      # 拉取个人信息
					profile = (Usr.get_profile(self.id))[0]
					allfriends = Usr.get_friends(self.id)
					allblack = Usr.get_black(self.id)
					allgroups = Usr.get_groups(self.id)
					time.sleep(0.1)
					self.sock.send(json.dumps(profile).encode('utf-8'))
					time.sleep(0.1)
					self.sock.send(json.dumps(allfriends).encode('utf-8'))
					time.sleep(0.1)
					self.sock.send(json.dumps(allblack).encode('utf-8'))
					time.sleep(0.1)
					self.sock.send(json.dumps(allgroups).encode('utf-8'))
					time.sleep(0.1)
				elif cmd[0] == '9':
					break
				else:
					self.sock.send('0'.encode('utf-8'))
		except: pass                                                #出现异常，退出循环，关闭线程	
		self.onlinesocket_lock.acquire()
		del self.onlinesocket[self.id]                                  # 删除该用户的sock
		self.onlinesocket_lock.release()

		self.usr_locks_lock.acquire()
		del self.usr_locks[self.id]                                      # 删除文件锁
		self.usr_locks_lock.release()

		self.sock.close()
		print("usr quit4")
		return                                               # 退出线程
