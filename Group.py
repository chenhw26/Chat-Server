import Usr
import threading
import socket
import json
import os

"""群组模块，定义群组操作相关函数"""

def new_group(name, founderid, foundername):
	"""创建新群组，返回新群组id"""
	with open('curGroupID.txt') as fp:
		new_id = int(fp.read())
	with open('curGroupID.txt', 'w') as fp:
		fp.write(str(new_id + 1))

	os.makedirs('group\\' + str(new_id))
	with open('group\\' + str(new_id) + '\\profile.txt', 'w') as fp:
		json.dump((new_id, name, False), fp)

	with open('group\\' + str(new_id) + '\\members.txt', 'w') as fp:
		json.dump(dict([(founderid, foundername)]), fp)

	with open('group\\' + str(new_id) + '\\ad.txt', 'w') as fp:
		json.dump(dict([(founderid, foundername)]), fp)

	with open('group\\' + str(new_id) + '\\pingbi.txt', 'w') as fp:
		json.dump(dict(), fp)

	with open('group\\' + str(new_id) + '\\record.txt', 'w') as fp:
		json.dump(list(), fp)

	return new_id

def send(uid, onlinesocket, msg, onlinesocke, usr_locks, usr_locks_lock):
	"""群发消息，向没屏蔽该群的群成员发送消息，若在线通过socket发送，若不在线则写入未读消息文件"""
	members = get_mem(uid).keys()
	pingbi = get_pingbi(uid).keys()
	for memid in members:
		if memid not in pingbi:
			if memid in onlinesocket.keys():
				onlinesocket[memid].send(msg.encode('utf-8'))
			else:
				if memid not in usr_locks.keys():
					usr_locks_lock.acquire()
					usr_locks[memid] = threading.Lock()
					usr_locks_lock.release()
				Usr.add_unrecieved(memid, msg, usr_locks[memid])

def get_profile(uid):
	"""读取群基本信息"""
	try:
		with open('group\\' + str(uid) + '\\profile.txt') as fp:
			profile = json.load(fp)
		return profile
	except:
		return tuple()

def update_profile(uid, new_profile, lock):
	"""更新群信息"""
	try:
		lock.acquire()
		with open('group\\' + str(uid) + '\\profile.txt', 'w') as fp:
			json.dump(new_profile, fp)
		lock.release()
		return True
	except:
		return False

def get_mem(uid):
	"""读取群成员列表"""
	try:
		with open('group\\' + str(uid) + '\\members.txt') as fp:
			members = json.load(fp)
		return members
	except:
		return dict()

def update_mem(uid, new_mem, lock):
	"""更新群成员列表"""
	try:
		lock.acquire()
		with open('group\\' + str(uid) + '\\members.txt', 'w') as fp:
			json.dump(new_mem, fp)
		lock.release()
		return True
	except:
		return False

def get_ad(uid):
	"""读取管理员列表"""
	try:
		with open('group\\' + str(uid) + '\\ad.txt') as fp:
			ads = json.load(fp)
		return ads
	except:
		return dict()

def update_ad(uid, new_ad, lock):
	"""更新管理员列表"""
	try:
		lock.acquire()
		with open('group\\' + str(uid) + '\\ad.txt', 'w') as fp:
			json.dump(new_ad, fp)
		lock.release()
		return True
	except:
		return False

def get_pingbi(uid):
	"""读取屏蔽成员列表"""
	try:
		with open('group\\' + str(uid) + '\\pingbi.txt') as fp:
			pingbi = json.load(fp)
		return pingbi
	except:
		return dict()

def update_pingbi(uid, new_pingbi, lock):
	"""更新屏蔽成员列表"""
	try:
		lock.acquire()
		with open('group\\' + str(uid) + '\\pingbi.txt', 'w') as fp:
			json.dump(new_pingbi, fp)
		lock.release()
		return True
	except:
		return False

def get_record(uid):
	"""读取聊天记录"""
	try:
		with open('group\\' + str(uid) + '\\record.txt') as fp:
			record = json.load(fp)
		return record
	except:
		return list()

def add_record(uid, sendername, senderid, time, content, lock):
	"""添加一条聊天记录"""
	try:
		lock.acquire()
		with open('group\\' + str(uid) + '\\record.txt') as fp:
			record = json.load(fp)
			record.append((sendername, senderid, time, content))
		with open('group\\' + str(uid) + '\\record.txt', 'w') as fp:
			json.dump(record, fp)
		lock.release()
		return True
	except:
		return False

def check_lock(uid, group_locks, group_locks_lock):
	"""检查群组锁是否存在，若不存在，则创建"""
	if uid not in group_locks.keys():
		group_locks_lock.acquire()
		group_locks[uid] = threading.Lock()
		group_locks_lock.release()
