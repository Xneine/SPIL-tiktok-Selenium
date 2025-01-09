from tiktok.tiktok import Tiktok
from tiktok.video import Video
from tiktok.constants import BASE_URL_ACCOUNT,BASE_URL_VIDEOS
import pymysql
                        
def mysqlconnect():
    try:
        with pymysql.connect(
            host='localhost',
            user='root',
            password="",
            db='project_social_media_spil',
        ) as conn:
            with conn.cursor() as cur:
                with Video(teardown=True) as bot_videos:
                    bot_videos.open_landing_page(url=BASE_URL_VIDEOS)
                    videos = bot_videos.get_all_videos()
                    # videos = bot_videos.get_newest_videos()
                    if all(videos):
                        # insert_videos(cur, videos)
                        conn.commit()
                    else:
                        print("Invalid data videos received from TikTok.")
    except Exception as e:
        print(f"Database connection error: {e}")

if __name__ == "__main__":
    mysqlconnect()