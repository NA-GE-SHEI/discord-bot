import os, sqlite3

DB_path = r"./bot_alarm.db"
conn = sqlite3.connect(DB_path)
cursor = conn.cursor()

def check():
    # if not os.path.isfile(DB_path):
    a = cursor.execute("SELECT _index FROM alarm ORDER BY _index DESC limit 1")
    for i in a:
        if len(i[0]) == 0:
            print("is space")
        print(i)
    conn.close()

check()