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
                "UPDATE `data` SET `total_follower` = %s, `total_likes` = %s, `total_videos` = %s WHERE DATE(created_at) = CURDATE();",
                (result[0], result[1], result[2])
            )
            print("Data Updated successfully!")
        except Exception as e:
            print(f"Error updating data: {e}")
    else:
        try:
            cur.execute(
                "INSERT INTO `data` (`total_follower`, `total_likes`, `total_videos`) VALUES (%s, %s, %s);",
                (result[0], result[1], result[2])
            )
            print("Data Inserted successfully!")
        except Exception as e:
            print(f"Error inserting data: {e}")
            
def insert_videos(cur, videos):
    try:
        cur.execute("SELECT `link` FROM `videos`;")
        print("oke1")
        existing_links = {row[0] for row in cur.fetchall()}
        if not existing_links:
            new_videos = [video for video in videos]
        else:
            new_videos = [video for video in videos if video['link'] not in existing_links]
        print("oke2")

        if not new_videos:
            print("Semua video sudah ada di database. Tidak ada video baru untuk diinsert.")
            return
        print("oke3")

        insert_query = """
            INSERT INTO `videos` (`Views`, `link`, `Description`)
            VALUES (%s, %s, %s);
        """
        data_to_insert = [(video['views'], video['link'], video['description']) for video in new_videos]
        print("oke4")

        cur.executemany(insert_query, data_to_insert)
        print(f"{len(new_videos)} video baru berhasil diinsert ke database.")

    except Exception as e:
        print(f"Error saat menginsert video: {e}")

            
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
                    result = bot_account.get_followers_likes_videos()
                    if all(result):
                        update_or_insert_account(cur, result)
                        conn.commit()
                    else:
                        print("Invalid data account received from TikTok.")
                with Video(teardown=True) as bot_videos:
                    bot_videos.open_landing_page(url=BASE_URL_VIDEOS)
                    # videos = bot_videos.get_all_videos()
                    videos = bot_videos.get_newest_videos()
                    if all(videos):
                        insert_videos(cur, videos)
                        conn.commit()
                    else:
                        print("Invalid data videos received from TikTok.")
    except Exception as e:
        print(f"Database connection error: {e}")

if __name__ == "__main__":
    mysqlconnect()
    
# if __name__ == "__main__":
#     with Video(teardown=True) as bot:
#         bot.open_landing_page(BASE_URL_VIDEOS)
#         videos = bot.get_newest_videos()
#         print(f"Expected 8 videos, Found: {len(videos)}")
#         for video in videos:
#             print(f"Views: {video['views']}, Link: {video['link']}, Likes: {video['like']}, Description: {video['description']}")
