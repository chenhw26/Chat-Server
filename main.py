import Server
import Usr
import mainUI
import threading
import socket

onlinesocket = {}                          # key为id，value为对应的socket
onlinesocket_lock = threading.Lock()       # 上面全局变量的访问锁
usr_locks, group_locks = {}, {}              # 为每个在线用户和活跃群组创建文件锁
usr_locks_lock , group_locks_lock = threading.Lock(), threading.Lock()

welcom_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcom_socket.bind(('127.0.0.1', 20000))
welcom_socket.listen(5)

mainui = mainUI.MainUI(onlinesocket, usr_locks, usr_locks_lock, group_locks, group_locks_lock)  # 管理窗口线程
mainui.start()

while True:
    sock, addr = welcom_socket.accept()
    server = Server.Server(onlinesocket, onlinesocket_lock, usr_locks, usr_locks_lock, group_locks, group_locks_lock, sock)
    server.start()
