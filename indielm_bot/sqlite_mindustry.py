import sqlite3


def make_db(db):
    conn = sqlite3.connect(db)
    conn.execute('''CREATE TABLE IF NOT EXISTS login(id INTEGER,
                                                     login TEXT,
                                                     password TEXT,
                                                     ip TEXT,
                                                     uuid TEXT)''')
    conn.commit()
    conn.close()
    

def insert(db, discordid, login, password):
    try:
        conn = sqlite3.connect(db)    
        conn.execute('INSERT INTO login(id, login, password) VALUES(?,?,?)',
                     (discordid, login, password))
        conn.commit()
        succes = True
    except Exception as e:
        print(e)
        succes = False
    finally:
        conn.close()
        return succes
        
           
def check(db, discordid, login):
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('SELECT id FROM login WHERE id=? OR login=?', (discordid, login))
        num = len(c.fetchmany())
    except Exception as e:
        num = 1
    finally:
        c.close()
        conn.close()
        return num

def get_data(db, discordid):
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('SELECT login, password FROM login WHERE id=?', (discordid,))
        data = c.fetchmany()
    except Exception as e:
        data = [('error', 'error')]
    finally:
        c.close()
        conn.close()
    return data if len(data) else [('error', 'error')]


def changeLogin(db, discordid, login, password):
    try:
        conn = sqlite3.connect(db)
        conn.execute('UPDATE login SET login=?, password=? WHERE id=?',
                     (login, password, discordid))
        conn.commit()
        success = True
    except Exception as e:
        print(e)
        success = False
    finally:
        conn.close()
        return success




    