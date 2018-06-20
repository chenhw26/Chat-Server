import Usr
import json
import time

"""定义处理说说信息的函数"""

def add_moment(content, uid, sock, usr_locks):
	"""添加一条说说"""
	allmoments = Usr.get_moments(uid)
	if not allmoments:
		cur_moment_key = 10000
	else:
		cur_moment_key = max(allmoments.keys()) + 1
	cur_time = time.ctime()
	allmoments[str(cur_moment_key)] = (cur_time, content)
	
	Usr.update_moments(allmoments, uid, usr_locks[uid])
	time.sleep(0.1)
	# sock.send('0'.encode('utf-8'))

def del_moment(uid, momentid, sock, usr_locks):
	"""删除一条说说"""
	allmoments = Usr.get_moments(uid)
	if str(momentid) in allmoments.keys():
		del allmoments[str(momentid)]
		Usr.update_moments(allmoments, uid, usr_locks[uid])
		time.sleep(0.1)
		# sock.send('0'.encode('utf-8'))
	else:
		time.sleep(0.1)
		# sock.send('1'.encode('utf-8'))

def get_someone_moments(tarid, sock):
	"""获取某人说说"""
	someone_moments = Usr.get_moments(tarid)
	moments_str = json.dumps(someone_moments)
	time.sleep(0.1)
	sock.send(moments_str.encode('utf-8'))

def cmp_moments(a):
	return a[1]

def get_all_moments(uid, sock):
	'''获取某人所有好友的说说'''
	allfriends = Usr.get_friends(uid)
	allmoments = list()
	
	mymoments = list(Usr.get_moments(uid).values())
	myname = (Usr.get_profile(uid))[0][1]
	for i in range(0, len(mymoments)):
		mymoments[i] = [myname] + mymoments[i]
	allmoments += mymoments

	for friendid in allfriends.keys():
		friendmoments = list(Usr.get_moments(friendid).values())
		for i in range(0, len(friendmoments)):
			friendmoments[i] = [allfriends[friendid]] + friendmoments[i]
		allmoments += friendmoments

	allmoments.sort(key = cmp_moments)
	allmoments_str = json.dumps(allmoments)
	time.sleep(0.1)
	sock.send(allmoments_str.encode('utf-8'))

def moments(cmd, uid, sock, usr_locks):
	"""处理与说说有关的命令"""
	if cmd[0] == '0':
		add_moment(cmd[1:], int(uid), sock, usr_locks)
	elif cmd[0] == '1':
		del_moment(int(uid), int(cmd[1:]), sock, usr_locks)
	elif cmd[0] == '2':
		get_all_moments(uid, sock)
	elif cmd[0] == '3':
		get_someone_moments(int(cmd[1:]), sock)
		