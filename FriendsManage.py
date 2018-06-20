import Usr
import json
import threading
import time
import shutil

"""定义好友管理相关函数"""

def addfriend(uid, tarid, sock, comment, onlinesocket, usr_locks, usr_locks_lock):
    """发送添加好友请求"""
    myname = (Usr.get_profile(uid))[0][1]
    msg_to_send = '3' + '0' + str(uid) + myname + '\n' + comment
    print(onlinesocket.keys())

    if tarid in onlinesocket.keys():             #被请求人在线
        onlinesocket[int(tarid)].send(msg_to_send.encode('utf-8'))
        onlinesocket[int(tarid)].send(msg_to_send.encode('utf-8'))
        time.sleep(0.1)
        # sock.send('0'.encode('utf-8'))
    else:                                         #被请求人不在线
        Usr.check_lock(tarid, usr_locks, usr_locks_lock)
        succeed = Usr.add_unrecieved(tarid, msg_to_send, usr_locks[tarid])
        if succeed:
            time.sleep(0.1)
            # sock.send('0'.encode('utf-8'))
        else:
            time.sleep(0.1)
            # sock.send('1'.encode('utf-8'))

def ackfriend(uid, tarid, sock, usr_locks, usr_locks_lock):
    """某人同意好友请求"""
    myname = (Usr.get_profile(uid))[0][1]
    tarname = (Usr.get_profile(tarid))[0][1]

    print("tarid type:", type(tarid))
    allfriends = Usr.get_friends(uid)                   #更新双方的好友列表
    allfriends[str(tarid)] = tarname
    Usr.update_friends(allfriends, uid, usr_locks[uid])
    
    print("map keys type:", type(list(allfriends.keys())[0]))
    Usr.check_lock(tarid, usr_locks, usr_locks_lock)
    allfriends = Usr.get_friends(tarid)
    allfriends[str(uid)] = myname
    Usr.update_friends(allfriends, tarid, usr_locks[tarid])

    time.sleep(0.1)
    # sock.send('0'.encode('utf-8'))

def defriend(uid, tarid, sock, usr_locks):
    """拉黑某人"""
    profile, succeed = Usr.get_profile(tarid)
    if not succeed:               #没有这个用户
        time.sleep(0.1)
        # sock.send('1'.encode('utf-8'))
        return
    
    allblack = Usr.get_black(uid)     # 加入拉黑名单
    allblack[str(tarid)] = profile[1]
    Usr.update_black(allblack, usr_locks[uid], uid)
    time.sleep(0.1)
    # sock.send('0'.encode('utf-8'))

def canceldefriend(uid, tarid, sock, usr_locks):
    """取消拉黑"""
    allblack = Usr.get_black(uid)
    if str(tarid) in allblack.keys():
        del allblack[str(tarid)]
    Usr.update_black(allblack, usr_locks[uid], uid)
    time.sleep(0.1)
    # sock.send('0'.encode('utf-8'))

def del_friend(uid, tarid, sock, usr_locks, usr_locks_lock):
    """删除好友"""
    allfriends = Usr.get_friends(uid)        # 在双方好友列表，拉黑列表中删除对方
    if str(tarid) in allfriends.keys():
        del allfriends[str(tarid)]
    Usr.update_friends(allfriends, uid, usr_locks[uid])

    allblack = Usr.get_black(uid)
    if str(tarid) in allblack.keys():
        del allblack[str(tarid)]
    Usr.update_black(allblack, usr_locks[uid], uid)

    Usr.check_lock(tarid, usr_locks, usr_locks_lock)

    allfriends = Usr.get_friends(tarid)        # 在双方好友列表，拉黑列表中删除对方
    if str(uid) in allfriends.keys():
        del allfriends[str(uid)]
    Usr.update_friends(allfriends, tarid, usr_locks[tarid])

    allblack = Usr.get_black(tarid)
    if str(uid) in allblack.keys():
        del allblack[str(uid)]
    Usr.update_black(allblack, usr_locks[tarid], tarid)

    time.sleep(0.1)
    sock.send('0'.encode('utf-8'))

def friends_manage(cmd, uid, sock, onlinesocket, usr_locks, usr_locks_lock):
    """处理与好友管理相关命令"""
    if cmd[0] == '0':
        addfriend(int(uid), int(cmd[1:6]), sock, cmd[6:], onlinesocket, usr_locks, usr_locks_lock)
    elif cmd[0] == '1':
        ackfriend(int(uid), int(cmd[1:6]), sock, usr_locks, usr_locks_lock)
    elif cmd[0] == '2':
        defriend(int(uid), int(cmd[1:6]), sock, usr_locks)
    elif cmd[0] == '3':
        canceldefriend(int(uid), int(cmd[1:6]), sock, usr_locks)
    elif cmd[0] == '4':
        del_friend(int(uid), int(cmd[1:6]), sock, usr_locks, usr_locks_lock)
