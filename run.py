from tiktok.tiktok import Tiktok
from tiktok.constants import BASE_URL
import pymysql

def mysqlconnect():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password="",
        db='project_social_media_spil',
    )
    cur = conn.cursor()

    with Tiktok() as bot:
        bot.open_landing_page(url=BASE_URL)
        result = bot.get_followers()
        print('Exiting...')

        if None not in result:
            try:
                print(f"Data: {result[0]}, {result[1]}, {result[2]}")
                cur.execute("SELECT * FROM data WHERE DATE(created_at) = CURDATE();")
                output = cur.fetchall()
                if None not in output:
                    try: 
                        cur.execute(
                            "UPDATE `data` SET `Total Follower` = %s, `Total Likes` = %s, `Total Videos`=%s WHERE DATE(created_at) = CURDATE();",
                            (result[0], result[1], result[2])
                        )
                        conn.commit()
                        print("Data Updated successfully!")
                    except:
                        print("tidak bisa update")
                else:
                    try:
                        cur.execute(
                            "INSERT INTO `data` `Total Follower`, `Total Likes`, `Total Videos`) VALUES (%s, %s, %s);",
                            (result[0], result[1], result[2])
                        )
                        conn.commit()
                        print("Data Insert successfully!")
                    except:
                        print("tidak bisa insert")
            except Exception as e:
                print(f"Error inserting data: {e}")
        else:
            print("Failed to retrieve data from TikTok. Try Again")

    conn.close()

if __name__ == "__main__":
    mysqlconnect()
