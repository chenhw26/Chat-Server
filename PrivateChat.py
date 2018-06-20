import time
import threading
import json
import Usr

"""定义处理私聊信息的函数"""

def send_private_msg(cmd, profile, sock, onlinesocket, usr_locks, usr_locks_lock):
	"""发私聊信息"""
	senderid, sendername = profile[0], profile[1]
	targetid, msg = int(cmd[:5]), cmd[5:]
	tarname = (Usr.get_profile(targetid))[0][1]
	tarblack, tarfriends = Usr.get_black(targetid), Usr.get_friends(targetid)
	cur_time = time.ctime()

	print(str(senderid), tarfriends.keys())
	if str(senderid) in tarblack.keys() or str(senderid) not in tarfriends.keys():  # 若发送者在接收者的黑名单中或不是好友
		print('send pri fail 1')
		time.sleep(0.1)
		# sock.send('1'.encode())
		return

	msg_to_client = '00' + str(senderid) + profile[1] + '\n' + str(cur_time) + '\n' + msg
	
	if targetid in onlinesocket.keys():                            #若接收者在线，直接发送
		onlinesocket[targetid].send(msg_to_client.encode('utf-8'))

		sender_rec = Usr.get_record(senderid, targetid)               #更新sender聊天记录
		sender_rec.append((sendername, tarname, str(cur_time), msg))
		Usr.update_record(senderid, targetid, sender_rec, usr_locks[senderid])

		tar_rec = Usr.get_record(targetid, senderid)               #更新发送目标聊天记录
		tar_rec.append((sendername, tarname, str(cur_time), msg))
		Usr.update_record(targetid, senderid, tar_rec, usr_locks[targetid])

		time.sleep(0.1)
		# sock.send('0'.encode('utf-8'))
	else:                                                 # 若接收者不在线
		Usr.check_lock(targetid, usr_locks, usr_locks_lock)
		
		succeed = Usr.add_unrecieved(targetid, msg_to_client, usr_locks[targetid])
		if succeed:                                                    # 加入发送目标未读消息文件成功
			sender_rec = Usr.get_record(senderid, targetid)               #更新sender聊天记录
			sender_rec.append((sendername, tarname, str(cur_time), msg))
			Usr.update_record(senderid, targetid, sender_rec, usr_locks[senderid])
	
			tar_rec = Usr.get_record(targetid, senderid)               #更新发送目标聊天记录
			tar_rec.append((sendername, tarname, str(cur_time), msg))
			Usr.update_record(targetid, senderid, tar_rec, usr_locks[targetid])

			time.sleep(0.1)
			# sock.send('0'.encode('utf-8'))				
		else:	
			print('send pri fail 2')
			time.sleep(0.1)
			# sock.send('1'.encode('utf-8'))

def get_msg_record(targetid, senderid, sock):
	"""拉取聊天记录"""
	record_str = json.dumps(Usr.get_record(senderid, targetid))
	time.sleep(0.1)
	sock.send(record_str.encode('utf-8'))

def private_chat(cmd, profile, sock, onlinesocket, usr_locks, usr_locks_lock):
	"""处理与私聊有关命令"""
	if cmd[0] == '0':
		send_private_msg(cmd[1:], profile, sock, onlinesocket, usr_locks, usr_locks_lock)
	elif cmd[0] == '1':
		get_msg_record(int(cmd[1:]), profile[0], sock)
