import DBUsr as Usr
import json
import threading
import time
import shutil

"""定义好友管理相关函数"""

def addfriend(uid, tarid, comment, onlinesocket):
    """发送添加好友请求"""
    myname = (Usr.get_profile(uid))[0][1]
    msg_to_send = '3' + '0' + str(uid) + myname + '\n' + comment

    if tarid in onlinesocket.keys():             #被请求人在线
        onlinesocket[int(tarid)].send(msg_to_send.encode('utf-8'))
        onlinesocket[int(tarid)].send(msg_to_send.encode('utf-8'))
        time.sleep(0.1)
        # sock.send('0'.encode('utf-8'))
    else:                                         #被请求人不在线
        # Usr.check_lock(tarid, usr_locks, usr_locks_lock)
        Usr.add_unreceived(tarid, msg_to_send)

def ackfriend(uid, tarid):
    """某人同意好友请求"""
    myname = (Usr.get_profile(uid))[0][1]
    tarname = (Usr.get_profile(tarid))[0][1]

    # print("tarid type:", type(tarid))
    # allfriends = Usr.get_friends(uid)                   #更新双方的好友列表
    # allfriends[str(tarid)] = tarname
    # Usr.update_friends(allfriends, uid, usr_locks[uid])
    Usr.add_friend((int(tarid), tarname), int(uid))

    # print("map keys type:", type(list(allfriends.keys())[0]))
    # Usr.check_lock(tarid, usr_locks, usr_locks_lock)
    # allfriends = Usr.get_friends(tarid)
    # allfriends[str(uid)] = myname
    # Usr.update_friends(allfriends, tarid, usr_locks[tarid])
    Usr.add_friend((int(uid), myname), int(tarid))

    time.sleep(0.1)
    # sock.send('0'.encode('utf-8'))

def defriend(uid, tarid):
    """拉黑某人"""
    profile, succeed = Usr.get_profile(tarid)
    if not succeed:               #没有这个用户
        time.sleep(0.1)
        # sock.send('1'.encode('utf-8'))
        return
    
    # allblack = Usr.get_black(uid)     # 加入拉黑名单
    # allblack[str(tarid)] = profile[1]
    # Usr.update_black(allblack, usr_locks[uid], uid)
    # time.sleep(0.1)
    # sock.send('0'.encode('utf-8'))
    Usr.add_black((int(tarid), profile[1]), int(uid))

def canceldefriend(uid, tarid):
    """取消拉黑"""
    # allblack = Usr.get_black(uid)
    # if str(tarid) in allblack.keys():
    #     del allblack[str(tarid)]
    # Usr.update_black(allblack, usr_locks[uid], uid)
    # time.sleep(0.1)
    # sock.send('0'.encode('utf-8'))
    Usr.del_black(int(tarid), int(uid))

def del_friend(uid, tarid):
    """删除好友"""
    # allfriends = Usr.get_friends(uid)        # 在双方好友列表，拉黑列表中删除对方
    # if str(tarid) in allfriends.keys():
    #     del allfriends[str(tarid)]
    # Usr.update_friends(allfriends, uid, usr_locks[uid])
    Usr.del_friend(int(tarid), int(uid))

    # allblack = Usr.get_black(uid)
    # if str(tarid) in allblack.keys():
    #     del allblack[str(tarid)]
    # Usr.update_black(allblack, usr_locks[uid], uid)
    Usr.del_black(int(tarid), int(uid))

    # Usr.check_lock(tarid, usr_locks, usr_locks_lock)

    # allfriends = Usr.get_friends(tarid)        # 在双方好友列表，拉黑列表中删除对方
    # if str(uid) in allfriends.keys():
    #     del allfriends[str(uid)]
    # Usr.update_friends(allfriends, tarid, usr_locks[tarid])
    Usr.del_friend(int(uid), int(tarid))

    # allblack = Usr.get_black(tarid)
    # if str(uid) in allblack.keys():
    #     del allblack[str(uid)]
    # Usr.update_black(allblack, usr_locks[tarid], tarid)
    Usr.del_black(int(uid), int(tarid))

    # time.sleep(0.1)
    # sock.send('0'.encode('utf-8'))

def friends_manage(cmd, uid, sock, onlinesocket):
    """处理与好友管理相关命令"""
    if cmd[0] == '0':
        addfriend(int(uid), int(cmd[1:6]), cmd[6:], onlinesocket)
    elif cmd[0] == '1':
        ackfriend(int(uid), int(cmd[1:6]))
    elif cmd[0] == '2':
        defriend(int(uid), int(cmd[1:6]))
    elif cmd[0] == '3':
        canceldefriend(int(uid), int(cmd[1:6]))
    elif cmd[0] == '4':
        del_friend(int(uid), int(cmd[1:6]))
