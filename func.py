import sqlite3, time, asyncio, datetime, os, json
from datetime import datetime, timezone, timedelta
from collections import namedtuple

DB_path = r"./bot_alarm.db"
jsonPath = r"./keyword.json"
conn = sqlite3.connect(DB_path)
cursor = conn.cursor()

def loadJson():
    with open(jsonPath, 'r', encoding="utf-8") as f:
        data = json.load(f)
    return data

def writeJson(content):
    data = loadJson()
    for keyword in content:
        data['keyword'].append(keyword)

    with open(jsonPath, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def removeJson(content):
    data = loadJson()
    try:
        for keyword in content:
            data['keyword'].remove(keyword)
    except:
        print("部分字詞沒有, 已刪除符合字詞")

    with open(jsonPath, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def check():
    if not os.path.isfile(jsonPath):
        with open(jsonPath, "w", encoding="utf-8") as f:
            f.write(json.dumps({"keyword": []}, sort_keys=True, indent=4))

    conn.execute('''CREATE TABLE IF NOT EXISTS alarm
                (`_index`    INTEGER,
                `success`    TEXT,
                `MM`    INTEGER,
                `DD`    INTEGER,
                `HHMM`    TEXT,
                `description`    TEXT,
                `id`    TEXT,
                `name`    TEXT,
                `server_id`    INTEGER,
                `server`    TEXT,
                `channel`    INTEGER,
                `who`    TEXT);''')

    conn.execute('''CREATE TABLE IF NOT EXISTS d4channel
                (`server`    TEXT,
                `server_id`    INTEGER,
                `d4`    INTEGER
                );''')
    

def clock():
    class Date:
        now = datetime.now(timezone.utc) + timedelta(hours=8)
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
    return Date

def calculate_gpa(grades, credits):
    total_credits = sum(credits)
    weighted_scores = [grade * credit for grade, credit in zip(grades, credits)]
    gpa = sum(weighted_scores) / total_credits
    return gpa

def task(MM, DD, HHMM, description, id, name, server_id, server, channel, who, sucess = False):
    index = 1
    for i in cursor.execute("SELECT _index FROM alarm ORDER BY _index DESC limit 1"):
        index = int(i[0]) + 1 if len(i) >= 1 else i
    
    cursor.execute(f"INSERT INTO alarm VALUES('{index}', '{sucess}', '{MM}', '{DD}','{HHMM}','{description}','{id}', '{name}', '{server_id}', '{server}', '{channel}', '{who}')")
    conn.commit()
    return index

def tasklist(server_id):
    msg = ""
    i = 0
    query = """SELECT _index, success, MM, DD, HHMM, description, id, name, server_id, server, channel, who
               FROM alarm WHERE success=? AND server_id=? ORDER BY MM, DD ASC"""
    for alarm in cursor.execute(query, ("False", server_id)):
        i += 1
        msg += f"{i}. {alarm[2]}/{alarm[3]}, {alarm[4]}, {alarm[5]}, {alarm[7]} (#{alarm[0]})\n\n"
    return msg.strip() or "目前無任務"

def where(server_id):
    for _server, _server_id, d4 in cursor.execute(f"SELECT * FROM d4channel"):
        if server_id == _server_id:
            return d4

def set_channel(server, server_id, channel_id):
    query = "SELECT * FROM d4channel WHERE server_id = ?"
    result = cursor.execute(query, (server_id,)).fetchone()
    if result is not None:
        cursor.execute("UPDATE d4channel SET d4 = ? WHERE server_id = ?", (channel_id, server_id))
    else:
        cursor.execute("INSERT INTO d4channel VALUES (?, ?, ?)", (str(server), int(server_id), int(channel_id)))
    conn.commit()

def rmalarm(index, id):
    query = "SELECT * FROM alarm WHERE _index = ?"
    result = cursor.execute(query, (index,)).fetchone()
    try:
        if result != None:
            dbID = ''.join(filter(str.isdigit, result[6]))
            if str(dbID) != str(id):
                resultMsg = "欸 你又不是本人, 想亂刪?"
            elif result[1] == "True":
                resultMsg = "已經執行過的任務讓我留個紀錄好嗎?"
            else:
                message = f"{result[2]}/{result[3]}, {result[4]}, {result[5]}, {result[7]} (#{result[0]})"
                query = "UPDATE alarm SET success = ? WHERE _index = ?"
                result = cursor.execute(query, ("Cancel", index,)).fetchone()
                conn.commit()
                resultMsg = f"已刪除 {message}"
        else:
            resultMsg = "這選項是空的, 你再看看"
    except:
        resultMsg = "出了點意外:("
    return resultMsg


Alarm = namedtuple("Alarm", ["index", "check", "month", "day", "time", "description",
                             "id", "name", "server_id", "server", "channel", "who"])

async def check_task():
    nowYear = datetime.now().year
    while True:
        for alarm in cursor.execute("SELECT * FROM alarm"):
            alarm = Alarm(*alarm)
            if alarm.check == "False":
                try:
                    date = clock()
                    now_time = datetime(nowYear, date.month, date.day, date.hour, date.minute)
                    alarm_time = datetime(nowYear, int(alarm.month), int(alarm.day),
                                          int(alarm.time.split(":")[0]), int(alarm.time.split(":")[1]))
                    if now_time >= alarm_time:
                        cursor.execute(f"UPDATE alarm SET success = 'True' WHERE _index = {alarm.index}")
                        conn.commit()
                        _where = where(alarm.server_id)
                        channel = _where or alarm.channel
                        return alarm.description, alarm.id, channel, alarm.who
                except ValueError:
                    print("時間錯誤")
        await asyncio.sleep(1)