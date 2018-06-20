import Usr
import Group
import json
import threading
import time
import shutil

"""定义群聊有关函数"""

def send_group_msg(senderid, groupid, sock, onlinesocket, usr_locks, usr_locks_lock, group_locks, group_locks_lock, content):
    """发送群消息"""
    sendername = (Usr.get_profile(senderid))[0][1]
    groupprofile = Group.get_profile(groupid)
    groupname = groupprofile[1]
    all_mem = Group.get_mem(groupid)
    all_pingbi = Group.get_pingbi(groupid)
    cur_time = time.ctime()

    if str(senderid) not in all_mem.keys() or groupprofile[2]:      # 若发送者不是群成员或该群被禁言
       time.sleep(0.1)
    #    sock.send('1'.encode('utf-8'))
       return

    msg_to_send = '1' + '0' + str(senderid) + str(groupid) + sendername + '\n' + groupname + '\n' + str(cur_time) + '\n' + content

    Group.check_lock(groupid, group_locks, group_locks_lock)
    Group.add_record(groupid, sendername, senderid, cur_time, content, group_locks[groupid])      #写聊天记录

    for memid in all_mem.keys():                              #向所有群成员发送消息
        if str(memid) not in all_pingbi.keys():
            if int(memid) in onlinesocket.keys():
                onlinesocket[int(memid)].send(msg_to_send.encode('utf-8'))
            else:                                               #若不在线，写未读消息
                Usr.check_lock(memid, usr_locks, usr_locks_lock)
                Usr.add_unrecieved(memid, msg_to_send, usr_locks[memid])
    
    time.sleep(0.1)
    # sock.send('0'.encode('utf-8'))

def new_group(name, founderid, sock, usr_locks):
    """创建一个群聊"""
    foundername = (Usr.get_profile(founderid))[0][1]
    groupid = Group.new_group(name, founderid, foundername)
    usr_groups = Usr.get_groups(founderid)
    usr_groups[str(groupid)] = name
    Usr.update_groups(usr_groups, founderid, usr_locks[founderid])
    time.sleep(0.1)
    # sock.send(('0' + str(groupid)).encode('utf-8'))

def invite(usrid, groupid, sock, usr_locks, usr_locks_lock, group_locks, group_locks_lock):
    """邀请某人入群"""
    usrprofile, succeed = Usr.get_profile(usrid)
    if not succeed:                        #这个用户不存在
        time.sleep(0.1)
        # sock.send('1'.encode('utf-8'))
        return
    
    usrname = usrprofile[1]
    
    Group.check_lock(groupid, group_locks, group_locks_lock)

    allmem = Group.get_mem(groupid)
    allmem[str(usrid)] = usrname                          # 更新群成员
    succeed = Group.update_mem(groupid, allmem, group_locks[groupid])
    if not succeed:                                  #这个群组不存在
        time.sleep(0.1)
        # sock.send('1'.encode('utf-8'))
        return

    Usr.check_lock(usrid, usr_locks, usr_locks_lock)

    groupname = (Group.get_profile(groupid))[1]           #更新用户群组列表
    allgroup = Usr.get_groups(usrid)
    allgroup[str(groupid)] = groupname
    Usr.update_groups(allgroup, usrid, usr_locks[usrid])

    time.sleep(0.1)
    # sock.send('0'.encode())

def pingbi(usrid, groupid, sock, group_locks, group_locks_lock):
    """某人屏蔽某个群"""
    usrname = (Usr.get_profile(usrid))[0][1]
    allpingbi = Group.get_pingbi(groupid)
    allpingbi[str(usrid)] = usrname
    Group.check_lock(groupid, group_locks, group_locks_lock)
    succeed = Group.update_pingbi(groupid, allpingbi, group_locks[groupid])
    if succeed:
        time.sleep(0.1)
        # sock.send('0'.encode('utf-8'))
    else:
        time.sleep(0.1)
        # sock.send('1'.encode('utf-8'))

def cancelpingbi(usrid, groupid, sock, group_locks, group_locks_lock):
    """取消屏蔽"""
    allpingbi = Group.get_pingbi(groupid)
    if str(usrid) in allpingbi.keys():
        del allpingbi[str(usrid)]
    Group.check_lock(groupid, group_locks, group_locks_lock)
    succeed = Group.update_pingbi(groupid, allpingbi, group_locks[groupid])
    if succeed:
        time.sleep(0.1)
        # sock.send('0'.encode('utf-8'))
    else:
        time.sleep(0.1)
        # sock.send('1'.encode('utf-8'))
# 
def del_mem(adid, usrid, groupid, sock, usr_locks, usr_locks_lock, group_locks, group_locks_lock):
    '''群管理员T人'''
    allad = Group.get_ad(groupid)
    if str(adid) not in allad.keys():
        time.sleep(0.1)
        # sock.send('1'.encode('utf-8'))              #若不是群管，不能T人
        return
    
    Group.check_lock(groupid, group_locks, group_locks_lock)
    allmem = Group.get_mem(groupid)                     #将该用户从群成员中删除
    if str(usrid) in allmem.keys():
        del allmem[str(usrid)]
    Group.update_mem(groupid, allmem, group_locks[groupid])

    allad = Group.get_ad(groupid)
    if str(usrid) in allad.keys():                          # 将该用户从群管理员中删除
        del allad[str(usrid)]
    Group.update_ad(groupid, allad, group_locks[groupid])
    
    allpingbi = Group.get_pingbi(groupid)
    if str(usrid) in allpingbi.keys():                   # 将该用户从群屏蔽成员中删除
        del allpingbi[str(usrid)]
    Group.update_pingbi(groupid, allpingbi, group_locks[groupid])

    Usr.check_lock(usrid, usr_locks, usr_locks_lock)
    allgroup = Usr.get_groups(usrid)                  #将该群从用户群列表中删除
    if str(groupid) in allgroup.keys():
        del allgroup[str(groupid)]
    succeed = Usr.update_groups(allgroup, usrid, usr_locks[usrid])
    if succeed:
        time.sleep(0.1)
        # sock.send('0'.encode('utf-8'))
    else:
        time.sleep(0.1)
        # sock.send('1'.encode('utf-8'))        

def del_group(adid, groupid, sock, usr_locks, usr_locks_lock, group_locks, group_locks_lock):
    """解散一个群"""
    allad = Group.get_ad(groupid)
    if str(adid) not in allad.keys():
        time.sleep(0.1)
        # sock.send('1'.encode('utf-8'))  # 若不是群管，不能解散群
        return

    allmem = Group.get_mem(groupid)
    for memid in allmem.keys():         #对所有群成员，删除该群
        Usr.check_lock(memid, usr_locks, usr_locks_lock)
        allgroup = Usr.get_groups(memid)
        if str(groupid) in allgroup:
            del allgroup[str(groupid)]
        Usr.update_groups(allgroup, memid, usr_locks[memid])
    
    shutil.rmtree('group\\' + str(groupid))     #删除该群文件夹
    time.sleep(0.1)
    # sock.send('0'.encode())

def get_info(groupid, sock):
    """获取该群信息"""
    profile = Group.get_profile(groupid)
    time.sleep(0.1)
    sock.send(json.dumps(profile).encode('utf-8'))
    time.sleep(0.01)

    mem = Group.get_mem(groupid)
    sock.send(json.dumps(mem).encode('utf-8'))
    time.sleep(0.01)

    ad = Group.get_ad(groupid)
    sock.send(json.dumps(ad).encode('utf-8'))
    time.sleep(0.01)

    record = Group.get_record(groupid)
    sock.send(json.dumps(record).encode('utf-8'))
    time.sleep(0.01)

def add_ad(groupid, uid, usrid, sock, group_locks, group_locks_lock):
    """将usrid用户设为管理员"""
    all_ad = Group.get_ad(groupid)
    if str(uid) not in all_ad.keys():
        time.sleep(0.1)
        # sock.send('1'.encode('utf-8'))
        return
    
    all_mem = Group.get_mem(groupid)
    if str(usrid) not in all_mem.keys():
        time.sleep(0.1)
        # sock.send('1'.encode('utf-8'))
        return
    
    all_ad = Group.get_ad(groupid)
    usrname = (Usr.get_profile(usrid))[0][1]
    all_ad[str(usrid)] = usrname

    Group.check_lock(groupid, group_locks, group_locks_lock)
    Group.update_ad(groupid, all_ad, group_locks[groupid])

    time.sleep(0.1)
    # sock.send('0'.encode('utf-8'))

def exit_group(groupid, usrid, sock, usr_locks, group_locks, group_locks_lock):
    """退出群聊"""
    all_mem, all_ad, all_black = Group.get_mem(groupid), Group.get_ad(groupid), Group.get_pingbi(groupid)
    if str(usrid) in all_mem.keys():
        del all_mem[str(usrid)]
    if str(usrid) in all_ad.keys():
        del all_ad[str(usrid)]
    if str(usrid) in all_black.keys():
        del all_black[str(usrid)]
    
    if not all_mem:
        shutil.rmtree('group\\' + str(groupid))
    else:
        Group.check_lock(groupid, group_locks, group_locks_lock)
        Group.update_mem(groupid, all_mem, group_locks[groupid])
        Group.update_ad(groupid, all_ad, group_locks[groupid])
        Group.update_pingbi(groupid, all_black, group_locks[groupid])

    all_groups = Usr.get_groups(groupid)
    if str(groupid) in all_groups.keys():
        del all_groups[str(groupid)]
    Usr.update_groups(all_groups, usrid, usr_locks[usrid])

    time.sleep(0.1)
    # sock.send('0'.encode('utf-8'))

def group_chat(cmd, uid, sock, onlinesocket, usr_locks, usr_locks_lock, group_locks, group_locks_lock):
    """处理群聊相关命令"""
    print('group chat')
    if cmd[0] == '0':
        send_group_msg(int(uid), int(cmd[1:6]), sock, onlinesocket, usr_locks, usr_locks_lock, group_locks, group_locks_lock, cmd[6:])
    elif cmd[0] == '1':
        new_group(cmd[1:], int(uid), sock, usr_locks)
    elif cmd[0] == '2':
        invite(int(cmd[1:6]), int(cmd[6:11]), sock, usr_locks, usr_locks_lock, group_locks, group_locks_lock)
    elif cmd[0] == '3':
        pingbi(int(uid), int(cmd[1:6]), sock, group_locks, group_locks_lock)
    elif cmd[0] == '4':
        cancelpingbi(int(uid), int(cmd[1:6]), sock, group_locks, group_locks_lock)
    elif cmd[0] == '5':
        del_mem(int(uid), int(cmd[6:11]), int(cmd[1:6]), sock, usr_locks, usr_locks_lock, group_locks, group_locks_lock)
    elif cmd[0] == '6':
        del_group(int(uid), int(cmd[1:6]), sock, usr_locks, usr_locks_lock, group_locks, group_locks_lock)
    elif cmd[0] == '7':
        get_info(int(cmd[1:6]), sock)
    elif cmd[0] == '8':
        add_ad(int(cmd[6:11]), int(uid), int(cmd[1:6]), sock, group_locks, group_locks_lock)
    elif cmd[0] == '9':
        exit_group(int(cmd[1:6]), int(uid), sock, usr_locks, group_locks, group_locks_lock)
