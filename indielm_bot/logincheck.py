import sqlite3
import sys

with open('token.txt', 'r') as infile:
    DB = infile.readlines()[3].strip()

login, password, ip, uuid = sys.argv[1:]
if login=="" and password =="":
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('SELECT login FROM login WHERE ip = ? AND uuid = ?', (ip, uuid))
        data = c.fetchmany()
        if len(data):
            print('loginSuccess ' + data[0][0])
        else:
            print('loginFailed')
    finally:
        c.close()
        conn.close()
            
    
else:   
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('SELECT * FROM login WHERE login = ? AND password = ?', (login, password))
        if len(c.fetchmany()):
            conn.execute('UPDATE login SET ip = ? WHERE login = ? AND password = ? ',
                         (ip, login, password))
            conn.commit()
            conn.execute('UPDATE login SET uuid = ? WHERE login = ? AND password = ?',
                         (uuid, login, password))
            conn.commit()
            print('loginSuccess ' + login)
        else:
            print('loginFailed')
    finally:
        c.close()
        conn.close()
