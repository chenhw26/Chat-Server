import sqlite3
import os
import shutil

conn = sqlite3.connect('AllUsers.db')
conn.execute('DELETE from AllUsers')
conn.commit()
conn.close()

conn = sqlite3.connect('AllGroups.db')
conn.execute('DELETE from AllGroups')
conn.commit()
conn.close()

shutil.rmtree('Users\\')
shutil.rmtree('Groups\\')
os.mkdir('Users\\')
os.mkdir('Groups\\')
