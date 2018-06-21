import sqlite3

'''用户模块，操作用户数据库'''

def new_usr(name, psw):
    '''创建新用户，返回新用户id'''
    conn = sqlite3.connect('AllUsers.db')
    allid = conn.execute('''SELECT ID from AllUsers''').fetchall()
    if not allid:
        curid = 10000
    else:
        curid = max(allid)[0] + 1
    conn.execute('''INSERT into AllUsers values(?,?,?,?)''',
                 (curid, name, psw, False))
    conn.commit()
    conn.close()

    # print('create table:' + str(curid))
    conn = sqlite3.connect('Users\\' + str(curid) + '.db')
    conn.execute('''CREATE table friends (
                    ID int primary key not null, 
                    name text not null)''')
    conn.execute('''CREATE table black (
                    ID int primary key not null, 
                    name text not null)''')
    conn.execute('''CREATE table groups (
                    ID int primary key not null, 
                    name text not null)''')
    conn.execute('''CREATE table moments (
                    ID int primary key not null, 
                    time text not null, 
                    content text not null)''')
    conn.execute('''CREATE table unreceived (
                    msg text not null)''')
    conn.commit()
    conn.close()

    return curid

def get_profile(uid):
    '''读取用户信息'''
    conn = sqlite3.connect('AllUsers.db')
    cur = conn.execute('''SELECT * from AllUsers WHERE ID=?''', 
                          (int(uid), ))
    profile = cur.fetchone()
    if not profile:
        return (None, False)
    else:
        return (profile, True)

def update_profile(new_profile, uid):
    '''更新用户信息'''
    conn = sqlite3.connect('AllUsers.db')
    conn.execute('''UPDATE AllUsers set
                    ID=?, name=?, psw=?, ban=? 
                    WHERE ID=?''', new_profile + (int(uid), ))
    conn.commit()
    conn.close()

def get_friends(uid):
    '''读取好友列表'''
    conn = sqlite3.connect('Users\\' + str(uid) + '.db')
    friends = conn.execute('''SELECT * from friends''').fetchall()
    conn.close()
    return dict(friends)

def add_friend(new_friend, uid):
    '''添加好友'''
    conn = sqlite3.connect('Users\\' + str(uid) + '.db')
    conn.execute('''INSERT into friends values (?,?)''', new_friend)
    conn.execute('''CREATE table %s (
                    sendername text not null, 
                    rec_name text not null, 
                    time text not null, 
                    content text not null) ''' % ('rec' + str(new_friend[0])))
    conn.commit()
    conn.close()

def del_friend(friendsid, uid):
    '''删除好友'''
    conn = sqlite3.connect('Users\\' + str(uid) + '.db')
    conn.execute('''DELETE from friends where ID=?''', (friendsid, ))
    conn.commit()
    conn.close()

def get_black(uid):
    '''读取黑名单列表'''
    conn = sqlite3.connect('Users\\' + str(uid) + '.db')
    black = conn.execute('''SELECT * from black''').fetchall()
    conn.close()
    return dict(black)

def add_black(new_black, uid):
    '''添加某人进黑名单'''
    conn = sqlite3.connect('Users\\' + str(uid) + '.db')
    conn.execute('''INSERT into black values (?,?)''', new_black)
    conn.commit()
    conn.close()

def del_black(blacksid, uid):
    '''将某人从黑名单中删除'''
    conn = sqlite3.connect('Users\\' + str(uid) + '.db')
    conn.execute('''DELETE from black where ID=?''', (blacksid, ))
    conn.commit()
    conn.close()

def get_groups(uid):
    '''读取群组列表'''
    conn = sqlite3.connect('Users\\' + str(uid) + '.db')
    groups = conn.execute('''SELECT * from groups''').fetchall()
    conn.close()
    return dict(groups)

def join_group(new_group, uid):
    '''加入一个群组'''
    conn = sqlite3.connect('Users\\' + str(uid) + '.db')
    conn.execute('''INSERT into groups values (?,?)''', new_group)
    conn.commit()
    conn.close()


def del_group(groupsid, uid):
    '''退出一个群组'''
    conn = sqlite3.connect('Users\\' + str(uid) + '.db')
    conn.execute('''DELETE from groups where ID=?''', (groupsid, ))
    conn.commit()
    conn.close()

def get_moments(uid):
    '''读取说说列表'''
    conn = sqlite3.connect('Users\\' + str(uid) + '.db')
    all_moments = conn.execute('''SELECT * from moments''').fetchall()
    for i in range(0, len(all_moments)):
        all_moments[i] = (all_moments[i][0], all_moments[i][1:])
    conn.close()
    return dict(all_moments)

def add_moments(new_moment, uid):
    '''添加一条说说'''
    conn = sqlite3.connect('Users\\' + str(uid) + '.db')
    conn.execute('''INSERT into moments values (?,?,?)''', new_moment)
    conn.commit()
    conn.close()

def get_record(uid, tarid):
    '''读取两人之间的聊天记录'''
    conn = sqlite3.connect('Users\\' + str(uid) + '.db')
    records = conn.execute('''SELECT * from %s''' % ('rec' + str(tarid))).fetchall()
    conn.close()
    return records

def add_record(record, uid, tarid):
    '''添加一条聊天记录'''
    conn = sqlite3.connect('Users\\' + str(uid) + '.db')
    conn.execute('''INSERT into %s values (?,?,?,?)''' % ('rec' + str(tarid)), record)
    conn.commit()
    conn.close()

def get_and_clear_unreceived(uid):
    '''读取未读消息列表并清空'''
    conn = sqlite3.connect('Users\\' + str(uid) + '.db')
    all = conn.execute('''SELECT * from unreceived''').fetchall()
    conn.execute('''DELETE from unreceived''')
    conn.commit()
    conn.close()
    all = [item[0] for item in all]
    return all    
    
def add_unreceived(uid, new_msg):
    '''添加一条未读消息列表'''   
    conn = sqlite3.connect('Users\\' + str(uid) + '.db')
    conn.execute('''INSERT into unreceived values (?)''', (new_msg, ))
    conn.commit()
    conn.close()
