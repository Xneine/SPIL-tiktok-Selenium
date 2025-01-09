from tiktok.history import Video_History
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
                with Video_History(teardown=True) as bot_videos:
                    bot_videos.update_hourly(cur=cur, conn=conn)
    except Exception as e:
        print(f"Database connection error: {e}")

if __name__ == "__main__":
    mysqlconnect()