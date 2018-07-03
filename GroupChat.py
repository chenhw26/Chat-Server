import DBUsr as Usr
import DBGroup as Group
import json
import threading
import time
import shutil

"""定义群聊有关函数"""

def send_group_msg(senderid, groupid, onlinesocket, content):
    """发送群消息"""
    sendername = (Usr.get_profile(senderid))[0][1]
    groupprofile = Group.get_profile(groupid)
    groupname = groupprofile[1]
    all_mem = Group.get_mem(groupid)
    cur_time = time.ctime()

    if groupprofile[2]:      # 若该群被禁言
       return

    msg_to_send = '1' + '0' + str(senderid) + str(groupid) + sendername + '\n' + groupname + '\n' + str(cur_time) + '\n' + content

    Group.add_record(groupid, sendername, senderid, cur_time, content)      #写聊天记录

    for mem in all_mem:                              #向所有群成员发送消息
        if not mem[3]:
            if mem[0] in onlinesocket.keys():
                onlinesocket[mem[0]].send(msg_to_send.encode('utf-8'))
            else:                                               #若不在线，写未读消息
                Usr.add_unreceived(mem[0], msg_to_send)
    
    time.sleep(0.1)
    # sock.send('0'.encode('utf-8'))

def new_group(name, founderid, sock):
    """创建一个群聊"""
    foundername = (Usr.get_profile(founderid))[0][1]
    groupid = Group.new_group(name, founderid, foundername)
    # usr_groups = Usr.get_groups(founderid)
    # usr_groups[str(groupid)] = name
    # Usr.update_groups(usr_groups, founderid, usr_locks[founderid])
    time.sleep(0.1)
    sock.send(('0' + str(groupid)).encode('utf-8'))
    Usr.join_group((groupid, name), founderid)

def invite(usrid, groupid):
    """邀请某人入群"""
    usrprofile, succeed = Usr.get_profile(usrid)
    if not succeed:                        #这个用户不存在
        time.sleep(0.1)
        # sock.send('1'.encode('utf-8'))
        return
    
    usrname = usrprofile[1]
    
    # allmem = Group.get_mem(groupid)
    # allmem[str(usrid)] = usrname                          # 更新群成员
    # succeed = Group.update_mem(groupid, allmem, group_locks[groupid])
    # if not succeed:                                  #这个群组不存在
    #     time.sleep(0.1)
    #     # sock.send('1'.encode('utf-8'))
    #     return
    groupProfile = Group.get_profile(groupid)
    if not groupProfile:
        return
    Group.add_mem(groupid, usrid, usrname)

    # groupname = (Group.get_profile(groupid))[1]           #更新用户群组列表
    # allgroup = Usr.get_groups(usrid)
    # allgroup[str(groupid)] = groupname
    # Usr.update_groups(allgroup, usrid, usr_locks[usrid])
    Usr.join_group(groupProfile[:2], usrid)

def pingbi(usrid, groupid):
    """某人屏蔽某个群"""
    # usrname = (Usr.get_profile(usrid))[0][1]
    # allpingbi = Group.get_pingbi(groupid)
    # allpingbi[str(usrid)] = usrname
    # Group.check_lock(groupid, group_locks, group_locks_lock)
    # succeed = Group.update_pingbi(groupid, allpingbi, group_locks[groupid])
    if not Group.get_profile(groupid):
        return
    Group.add_pingbi(groupid, usrid)

def cancelpingbi(usrid, groupid):
    """取消屏蔽"""
    # allpingbi = Group.get_pingbi(groupid)
    # if str(usrid) in allpingbi.keys():
    #     del allpingbi[str(usrid)]
    # Group.check_lock(groupid, group_locks, group_locks_lock)
    # succeed = Group.update_pingbi(groupid, allpingbi, group_locks[groupid])
    if not Group.get_profile(groupid):
        return
    Group.del_pingbi(groupid, usrid)


def del_mem(adid, usrid, groupid):
    '''群管理员T人'''
    # allad = Group.get_ad(groupid)
    # if str(adid) not in allad.keys():
    #     time.sleep(0.1)
    #     # sock.send('1'.encode('utf-8'))              #若不是群管，不能T人
    #     return
    allmem = Group.get_mem(groupid)
    for mem in allmem:
        if mem[0] == adid:
            if not mem[2]:
                return
            else:
                break

    if not Group.get_profile(groupid):                  # 没有这个群
        return

    # allmem = Group.get_mem(groupid)                     #将该用户从群成员中删除
    # if str(usrid) in allmem.keys():
    #     del allmem[str(usrid)]
    # Group.update_mem(groupid, allmem, group_locks[groupid])
    Group.del_mem(groupid, usrid)

    # Usr.check_lock(usrid, usr_locks, usr_locks_lock)
    # allgroup = Usr.get_groups(usrid)                  #将该群从用户群列表中删除
    # if str(groupid) in allgroup.keys():
    #     del allgroup[str(groupid)]
    # succeed = Usr.update_groups(allgroup, usrid, usr_locks[usrid])
    Usr.del_group(groupid, usrid)

def del_group(adid, groupid):
    """解散一个群"""
    # allad = Group.get_ad(groupid)
    # if str(adid) not in allad.keys():
    #     time.sleep(0.1)
    #     # sock.send('1'.encode('utf-8'))  # 若不是群管，不能解散群
    #     return
    allmem = Group.get_mem(groupid)
    for mem in allmem:
        if mem[0] == adid:
            if not mem[2]:
                return
            else:
                break

    # allmem = Group.get_mem(groupid)
    # for memid in allmem.keys():         #对所有群成员，删除该群
    #     Usr.check_lock(memid, usr_locks, usr_locks_lock)
    #     allgroup = Usr.get_groups(memid)
    #     if str(groupid) in allgroup:
    #         del allgroup[str(groupid)]
    #     Usr.update_groups(allgroup, memid, usr_locks[memid])
    for mem in allmem:
        Usr.del_group(groupid, mem[0])

    # shutil.rmtree('group\\' + str(groupid))     #删除该群文件夹
    Group.del_group(groupid)

def get_info(groupid, sock):
    """获取该群信息"""
    profile = Group.get_profile(groupid)
    time.sleep(0.1)
    sock.send(json.dumps(profile).encode('utf-8'))
    time.sleep(0.01)

    allmem = Group.get_mem(groupid)
    mem, ad = {}, {}
    for m in allmem:
        mem[m[0]] = m[1]
        if m[2]:
            ad[m[0]] = m[1]

    print(mem)
    sock.send(json.dumps(mem).encode('utf-8'))
    time.sleep(0.01)

    print(ad)
    sock.send(json.dumps(ad).encode('utf-8'))
    time.sleep(0.01)

    record = Group.get_record(groupid)
    sock.send(json.dumps(record).encode('utf-8'))
    time.sleep(0.01)

def add_ad(groupid, uid, usrid):
    """将usrid用户设为管理员"""
    # all_ad = Group.get_ad(groupid)
    # if str(uid) not in all_ad.keys():
    #     time.sleep(0.1)
    #     # sock.send('1'.encode('utf-8'))
    #     return
    allmem = Group.get_mem(groupid)
    for mem in allmem:
        if mem[0] == uid:
            if not mem[2]:   return
            else:   break
    
    # all_ad[str(usrid)] = usrname
    # Group.check_lock(groupid, group_locks, group_locks_lock)
    # Group.update_ad(groupid, all_ad, group_locks[groupid])
    Group.add_ad(groupid, usrid)

def exit_group(groupid, usrid):
    """退出群聊"""
    # all_mem, all_ad, all_black = Group.get_mem(groupid), Group.get_ad(groupid), Group.get_pingbi(groupid)
    # if str(usrid) in all_mem.keys():
    #     del all_mem[str(usrid)]
    # if str(usrid) in all_ad.keys():
    #     del all_ad[str(usrid)]
    # if str(usrid) in all_black.keys():
    #     del all_black[str(usrid)]
    Group.del_mem(groupid, usrid)

    # all_groups = Usr.get_groups(usrid)
    # if str(groupid) in all_groups.keys():
    #     del all_groups[str(groupid)]
    # Usr.update_groups(all_groups, usrid, usr_locks[usrid])
    Usr.del_group(groupid, usrid)

    # if not all_mem:
    #     shutil.rmtree('group\\' + str(groupid))
    # else:
    #     Group.check_lock(groupid, group_locks, group_locks_lock)
    #     Group.update_mem(groupid, all_mem, group_locks[groupid])
    #     Group.update_ad(groupid, all_ad, group_locks[groupid])
    #     Group.update_pingbi(groupid, all_black, group_locks[groupid])
    if not Group.get_mem(groupid):
        Group.del_group(groupid)

def group_chat(cmd, uid, sock, onlinesocket):
    """处理群聊相关命令"""
    print('group chat')
    if cmd[0] == '0':
        send_group_msg(int(uid), int(cmd[1:6]), onlinesocket, cmd[6:])
    elif cmd[0] == '1':
        new_group(cmd[1:], int(uid), sock)
    elif cmd[0] == '2':
        invite(int(cmd[1:6]), int(cmd[6:11]))
    elif cmd[0] == '3':
        pingbi(int(uid), int(cmd[1:6]))
    elif cmd[0] == '4':
        cancelpingbi(int(uid), int(cmd[1:6]))
    elif cmd[0] == '5':
        del_mem(int(uid), int(cmd[6:11]), int(cmd[1:6]))
    elif cmd[0] == '6':
        del_group(int(uid), int(cmd[1:6]))
    elif cmd[0] == '7':
        get_info(int(cmd[1:6]), sock)
    elif cmd[0] == '8':
        add_ad(int(cmd[6:11]), int(uid), int(cmd[1:6]))
    elif cmd[0] == '9':
        exit_group(int(cmd[1:6]), int(uid))
