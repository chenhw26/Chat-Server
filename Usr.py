import json
import threading
import os
"""用户模块，处理用户文件等函数"""

def new_usr(name, psw):
	"""创建新用户，返回新用户id"""
	with open('curUsrID.txt') as fp:
		new_id = int(fp.read())
	
	with open('curUsrID.txt', 'w') as fp:
		fp.write(str(new_id + 1))

	os.makedirs('usr\\' + str(new_id))
	with open('usr\\' + str(new_id) + '\\profile.txt', 'w') as fp:
		json.dump((new_id, name, psw, False), fp)
	
	with open('usr\\' + str(new_id) + '\\friends.txt', 'w') as fp:
		json.dump(dict(), fp)
	
	with open('usr\\' + str(new_id) + '\\black.txt', 'w') as fp:
		json.dump(dict(), fp)
	
	with open('usr\\' + str(new_id) + '\\groups.txt', 'w') as fp:
		json.dump(dict(), fp)

	with open('usr\\' + str(new_id) + '\\moments.txt', 'w') as fp:
		json.dump(dict(), fp)

	with open('usr\\' + str(new_id) + '\\unrecieved.txt', 'w') as fp:
		json.dump(list(), fp)

	os.makedirs('usr\\' + str(new_id) + '\\record')
	return new_id

def get_profile(uid):
	"""从文件中读取用户信息"""
	try:
		with open('usr\\' + str(uid) + '\\profile.txt') as fp:
			pro = json.load(fp)
		return (pro, True)
	except:
		return (None, False)

def update_profile(new_profile, uid, lock):
	"""更新文件中的用户信息"""
	lock.acquire()
	with open('usr\\' + str(uid) + '\\profile.txt', 'w') as fp:
		json.dump(new_profile, fp)
	lock.release()

def get_friends(uid):
	"""读取好友列表"""
	with open('usr\\' + str(uid) + '\\friends.txt') as fp:
		friends = json.load(fp)
	return friends

def update_friends(friends, uid, lock):
	"""更新文件中好友列表"""
	lock.acquire()
	with open('usr\\' + str(uid) + '\\friends.txt', 'w') as fp:
		json.dump(friends, fp)
	lock.release()

def get_black(uid):
	"""读取黑名单列表"""
	with open('usr\\' + str(uid) + '\\black.txt') as fp:
		black = json.load(fp)
	return black

def update_black(black, lock, uid):
	"""更新文件中黑名单列表"""
	lock.acquire()
	with open('usr\\' + str(uid) + '\\black.txt', 'w') as fp:
		json.dump(black, fp)
	lock.release()

def get_groups(uid):
	"""读取群组列表"""
	with open('usr\\' + str(uid) + '\\groups.txt') as fp:
		groups = json.load(fp)
	return groups

def update_groups(groups, uid, lock):
	"""更新文件中群组列表"""
	try:
		lock.acquire()
		with open('usr\\' + str(uid) + '\\groups.txt', 'w') as fp:
			json.dump(groups, fp)
		lock.release()
		return True
	except:
		return False

def get_moments(uid):
	"""读取说说列表"""
	try:
		with open('usr\\' + str(uid) + '\\moments.txt') as fp:
			moments = json.load(fp)
		return moments
	except:
		return dict()

def update_moments(moments, uid, lock):
	"""更新文件中说说列表"""
	lock.acquire()
	with open('usr\\' + str(uid) + '\\moments.txt', 'w') as fp:
		json.dump(moments, fp)
	lock.release()

def get_record(senderid, tarid):
	"""读取聊天记录"""
	try:
		with open('usr\\' + str(senderid) + '\\record\\' + str(tarid) + '.txt') as fp:
			record = json.load(fp)
		return record
	except:
		return list()

def update_record(senderid, tarid, new_rec, lock):
	"""更新聊天记录"""
	lock.acquire()
	with open('usr\\' + str(senderid) + '\\record\\' + str(tarid) + '.txt', 'w') as fp:
		json.dump(new_rec, fp)
	lock.release()

def get_and_clear_unrecieved(uid, lock):
	"""读取未读消息列表并清空"""
	lock.acquire()
	with open('usr\\' + str(uid) + '\\unrecieved.txt') as fp:
		unrecieved = json.load(fp)
	with open('usr\\' + str(uid) + '\\unrecieved.txt', 'w') as fp:
		json.dump(list(), fp)
	lock.release()
	return unrecieved

def add_unrecieved(uid, new_msg, lock):
	"""添加文件中未读消息列表"""
	try:
		lock.acquire()
		with open('usr\\' + str(uid) + '\\unrecieved.txt') as fp:
			unrecieved = json.load(fp)
			unrecieved.append(new_msg)

		with open('usr\\' + str(uid) + '\\unrecieved.txt', 'w') as fp:
			json.dump(unrecieved, fp)
		lock.release()
		return True
	except:
		return False

def check_lock(uid, usr_locks, usr_locks_lock):
	"""检查用户锁是否存在，若不存在，则创建"""
	if uid not in usr_locks.keys():
		usr_locks_lock.acquire()
		usr_locks[uid] = threading.Lock()
		usr_locks_lock.release()
