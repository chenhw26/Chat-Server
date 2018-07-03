import DBUsr
import time

def sendAGameRequest(uid, tarid, sock, onlinesockets):
    myname = DBUsr.get_profile(uid)[0][1]
    tarname = DBUsr.get_profile(tarid)[0][1]
    if tarid not in onlinesockets.keys():        #对方不在线
        msg = '52' + str(tarid) + tarname
        time.sleep(0.05)
        sock.send(msg.encode('utf-8'))
    else:
        msg = '50' + str(uid) + myname
        onlinesockets[tarid].send(msg.encode('utf-8'))

def ackAGameRequest(uid, tarid, onlinesockets):
    myname = DBUsr.get_profile(uid)[0][1]
    if tarid in onlinesockets.keys():
        msg = '51' + str(uid) + myname
        onlinesockets[tarid].send(msg.encode('utf-8'))
    
def dclAGameRequest(uid, tarid, onlinesockets):
    myname = DBUsr.get_profile(uid)[0][1]
    if tarid in onlinesockets.keys():
        msg = '52' + str(uid) + myname
        onlinesockets[tarid].send(msg.encode('utf-8'))

def gameRequest(cmd, uid, sock, onlinesockets):
    if cmd[0] == '0':
        sendAGameRequest(int(uid), int(cmd[1:6]), sock, onlinesockets)
    elif cmd[0] == '1':
        ackAGameRequest(int(uid), int(cmd[1:6]), onlinesockets)
    elif cmd[0] == '2':
        dclAGameRequest(int(uid), int(cmd[1:6]), onlinesockets)