from tiktok.tiktok import Tiktok
from tiktok.video import Video
from tiktok.history import Video_History
from tiktok.constants import BASE_URL_ACCOUNT,BASE_URL_VIDEOS
import pymysql
import threading
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def fill_missing_created_at(cur, conn):
    try:
        cur.execute("SELECT `id`, `link` FROM `videos` WHERE `created_at` IS NULL;")
        videos_missing_date = cur.fetchall()

        if not videos_missing_date:
            print("Tidak ada video dengan kolom created_at kosong.")
            return

        print(f"Found {len(videos_missing_date)} videos with missing upload date.")

        # Gunakan browser yang sama untuk semua link
        with Video_History(teardown=False) as bot:
            start_index = 0
            while start_index < len(videos_missing_date):
                video_id, link = videos_missing_date[start_index]
                result = {}

                def process_video(video_id, link, result):
                    """
                    Proses untuk membuka link video, mengambil tanggal upload, dan mengupdate database.
                    """
                    try:
                        print(f"Opening {link}...")
                        bot.open_url(link)
                        upload_date_element = WebDriverWait(bot, 20).until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, '[data-e2e="browser-nickname"] span:nth-child(3)')
                            )
                        )
                        upload_date = upload_date_element.text
                        formatted_date = time.strptime(upload_date, "%Y-%m-%d")

                        result["status"] = "success"
                        result["formatted_date"] = formatted_date
                    except Exception as e:
                        print(f"Error processing video {link}: {e}")
                        result["status"] = "error"
                        result["error"] = str(e)

                # Proses video dengan threading dan timeout
                thread = threading.Thread(target=process_video, args=(video_id, link, result))
                thread.start()
                thread.join(timeout=15)

                if thread.is_alive():
                    print(f"Timeout occurred for video {link}. Restarting browser...")
                    bot.quit()

                    # Restart browser dan lanjutkan dari video yang sama
                    with Video_History(teardown=False) as new_bot:
                        bot.__dict__.update(new_bot.__dict__)
                    time.sleep(5)
                    continue  # Ulangi proses untuk video yang sama

                if result.get("status") == "success":
                    # Update database dengan tanggal yang didapat
                    cur.execute(
                        """
                        UPDATE `videos` 
                        SET `created_at` = %s 
                        WHERE `id` = %s;
                        """,
                        (result["formatted_date"], video_id)
                    )
                    conn.commit()
                    print(f"Updated upload date for video ID {video_id}.")
                    start_index += 1  # Lanjut ke video berikutnya
                else:
                    print(f"Failed to process video {link}: {result.get('error')}")
                    bot.quit()

                    # Restart browser dan lanjutkan dari video yang sama
                    with Video_History(teardown=False) as new_bot:
                        bot.__dict__.update(new_bot.__dict__)
                    time.sleep(5)

    except Exception as e:
        print(f"Error during filling missing created_at: {e}")
            
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
        existing_videos = {row[0] for row in cur.fetchall()}
        print("Data video di database berhasil diambil.")

        videos_to_update = [video for video in videos if video['link'] in existing_videos]
        videos_to_insert = [video for video in videos if video['link'] not in existing_videos]

        if videos_to_update:
            update_query = """
                UPDATE `videos` 
                SET `Views` = %s
                WHERE `link` = %s;
            """
            data_to_update = [
                (video['views'], video['link']) 
                for video in videos_to_update
            ]
            cur.executemany(update_query, data_to_update)
            print(f"{len(videos_to_update)} video berhasil diupdate.")

        if videos_to_insert:
            insert_query = """
                INSERT INTO `videos` (`Views`, `link`, `Description`)
                VALUES (%s, %s, %s);
            """
            data_to_insert = [
                (video['views'], video['link'], video['description']) 
                for video in videos_to_insert
            ]
            cur.executemany(insert_query, data_to_insert)
            print(f"{len(videos_to_insert)} video baru berhasil diinsert ke database.")

        if not videos_to_insert and not videos_to_update:
            print("Tidak ada perubahan pada database.")

    except Exception as e:
        print(f"Error saat menginsert atau mengupdate video: {e}")

            
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
                    videos = bot_videos.get_all_videos()
                    # videos = bot_videos.get_newest_videos()
                    if all(videos):
                        insert_videos(cur, videos)
                        conn.commit()
                    else:
                        print("Invalid data videos received from TikTok.")
                    fill_missing_created_at(cur, conn)
    except Exception as e:
        print(f"Database connection error: {e}")

if __name__ == "__main__":
    mysqlconnect()
