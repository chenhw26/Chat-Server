import DBUsr
import socket
import sqlite3

'''群组模块，定义群组操作相关函数'''

def new_group(name, founderid, foundername):
    '''创建新群组，返回新群组id'''
    conn = sqlite3.connect('AllGroups.db')
    allid = conn.execute('''SELECT ID from AllGroups''').fetchall()
    if not allid:
        curid = 10000
    else:
        curid = max(allid)[0]
    conn.execute('''INSERT into Allgroups values(?,?,?)''', (curid, name, False))
    conn.commit()
    conn.close()

    conn = sqlite3.connect('Groups/' + str(curid) + '.db')
    conn.execute('''CREATE table members(
                    ID int primary key not null, 
                    name text not null, 
                    ad bool not null, 
                    pingbi bool not null)''')
    conn.execute('''CREATE table record(
                    sendername text not null, 
                    senderid int not null, 
                    time text not null, 
                    content text not null)''')
    conn.execute('''INSERT into members values(?,?,?,?)''', 
                    (founderid, foundername, True, False))
    conn.commit()
    conn.close()

    return curid

def get_profile(uid):
    '''读取群基本信息'''
    conn = sqlite3.connect('AllGroups.db')
    profile = conn.execute('''SELECT * from Allgroups where ID=?''', (uid,))
    conn.close()
    return profile

def update_profile(uid, new_profile):
    '''更新群信息'''
    conn = sqlite3.connect('AllGroups.db')
    conn.execute('''UPDATE AllGroups set ID=?, name=?, ban=? where ID=?''', 
                 new_profile[:] + (uid, ))
    conn.commit()
    conn.close()

def get_mem(uid):
    '''读取群成员列表'''
    conn = sqlite3.connect('Groups/' + str(uid) + '.db')
    allmem = conn.execute('''SELECT * from members''').fetchall()
    conn.close()
    return allmem

def add_mem(groupid, memid, memname):
    '''新增成员'''
    conn = sqlite3.connect('Groups/' + str(groupid) + '.id')
    conn.execute('''INSERT into members values(?,?,?,?)''', 
                    (memid, memname, False, False))
    conn.commit()
    conn.close()

def del_mem(groupid, memid):
    '''删除成员'''
    conn = sqlite3.connect('Groups/' + str(groupid) + '.id')
    conn.execute('''DELETE from members where ID=?''', (memid, ))
    conn.commit()
    conn.close()

def add_ad(groupid, memid):
    '''新增管理员'''
    conn = sqlite3.connect('Groups/' + str(groupid) + '.id')
    conn.execute('''UPDATE members set ad=? where ID=?''', 
                 (True, memid))
    conn.commit()
    conn.close()

def del_ad(groupid, memid):
    '''删除管理员'''
    conn = sqlite3.connect('Groups/' + str(groupid) + '.id')
    conn.execute('''UPDATE members set ad=? where ID=?''', 
                 (False, memid))
    conn.commit()
    conn.close()

def add_pingbi(groupid, memid):
    '''某人屏蔽该群'''
    conn = sqlite3.connect('Groups/' + str(groupid) + '.id')
    conn.execute('''UPDATE members set pingbi=? where ID=?''', 
                 (True, memid))
    conn.commit()
    conn.close()

def del_pingbi(groupid, memid):
    '''取消屏蔽'''
    conn = sqlite3.connect('Groups/' + str(groupid) + '.id')
    conn.execute('''UPDATE members set pingbi=? where ID=?''', 
                 (False, memid))
    conn.commit()
    conn.close()

def get_record(groupid):
    '''读取聊天记录'''
    conn = sqlite3.connect('Groups/' + str(groupid) + '.id')
    rec = conn.execute('''SELECT * from record''').fetchall()
    conn.close()
    return rec


def add_record(groupid, sendername, senderid, time, content):
    '''添加一条聊天记录'''
    conn = sqlite3.connect('Groups/' + str(groupid) + '.id')
    conn.execute('''INSERT into record values(?,?,?,?)''',
                    (sendername, senderid, time, content))
    conn.commit()
    conn.close()
