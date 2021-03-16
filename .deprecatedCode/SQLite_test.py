import sqlite3

# 創表格
conn = sqlite3.connect('iot.db')
c = conn.cursor()
c.execute('''CREATE TABLE STATUS
       (KEY    TEXT    NOT NULL,
       VALUE   TEXT    NOT NULL,
       PRIMARY KEY (KEY));
       ''')
conn.commit()
conn.close()

# 新增紀錄
conn = sqlite3.connect('iot.db')
c = conn.cursor()
c.execute("INSERT INTO STATUS (KEY,VALUE) \
            VALUES ('Locked', 'yes' )")
conn.commit()
conn.close()

# 查詢紀錄
conn = sqlite3.connect('iot.db')
c = conn.cursor()
cc = c.execute("SELECT VALUE FROM STATUS WHERE KEY = 'Locked'")
print(cc.fetchone()[0])
conn.commit()
conn.close()

# 更新紀錄
conn = sqlite3.connect('iot.db')
c = conn.cursor()
c.execute("UPDATE STATUS SET \
            VALUE = 'no' where KEY = 'Locked'")
conn.commit()
conn.close()