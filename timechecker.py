import datetime
import sqlite3
from time import sleep


def check_time():
    while True:
        print(datetime.datetime.now())
        # sleep(60)
        db = 'db/database.db'
        con = sqlite3.connect(db)
        cur = con.cursor()
        query = "SELECT id FROM user_info"
        res = cur.execute(query).fetchall()
        for i in res:
            print(i[0])
            query = f"UPDATE user_info SET money=money + (SELECT profit FROM" \
                    f" businesses WHERE user_id = {i[0]}) WHERE id = {i[0]}"
            cur.execute(query)
            con.commit()
        sleep(60)


check_time()
