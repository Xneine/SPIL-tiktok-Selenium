from tiktok.tiktok import Tiktok
from tiktok.video import Video
from tiktok.constants import BASE_URL_ACCOUNT,BASE_URL_VIDEOS
import pymysql

def update_or_insert_account(cur, result):
    cur.execute("SELECT * FROM data WHERE DATE(created_at) = CURDATE();")
    output = cur.fetchall()
    if output:
        try:
            cur.execute(
                "UPDATE `data` SET `Total Follower` = %s, `Total Likes` = %s, `Total Videos` = %s WHERE DATE(created_at) = CURDATE();",
                (result[0], result[1], result[2])
            )
            print("Data Updated successfully!")
        except Exception as e:
            print(f"Error updating data: {e}")
    else:
        try:
            cur.execute(
                "INSERT INTO `data` (`Total Follower`, `Total Likes`, `Total Videos`) VALUES (%s, %s, %s);",
                (result[0], result[1], result[2])
            )
            print("Data Inserted successfully!")
        except Exception as e:
            print(f"Error inserting data: {e}")
            
def insert_videos(cur, videos):
    cur.execute("SELECT * FROM data WHERE DATE(created_at) = CURDATE();")

            
def mysqlconnect():
    try:
        with pymysql.connect(
            host='localhost',
            user='root',
            password="",
            db='project_social_media_spil',
        ) as conn:
            with conn.cursor() as cur:
                with Tiktok() as bot_account:
                    bot_account.open_landing_page(url=BASE_URL_ACCOUNT)
                    result = bot_account.get_followers()
                    if all(result):
                        update_or_insert_account(cur, result)
                        conn.commit()
                    else:
                        print("Invalid data account received from TikTok.")
                with Video(teardown=True) as bot_videos:
                    bot_videos.open_landing_page(url=BASE_URL_VIDEOS)
                    videos = bot_videos.get_all_videos()
                    # videos = bot_videos.get_newest_videos()
                    if all(videos):
                        insert_videos(cur, videos)
                        conn.commit()
                    else:
                        print("Invalid data videos received from TikTok.")
    except Exception as e:
        print(f"Database connection error: {e}")

if __name__ == "__main__":
    mysqlconnect()