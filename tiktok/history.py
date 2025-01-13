from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import threading
from selenium.webdriver.firefox.options import Options

class Video_History(webdriver.Firefox):
    def __init__(self, driver_path=r"C:\SeleniumDrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path

        firefox_options = Options()
        firefox_options.add_argument('--disable-logging')
        firefox_options.add_argument('--log-level=3')
        firefox_options.add_argument('--disable-gpu')
        firefox_options.add_argument('--no-sandbox')
        firefox_options.add_argument('--disable-dev-shm-usage')
        # firefox_options.add_argument('--headless')
        super(Video_History, self).__init__(options=firefox_options)
        self.implicitly_wait(5)


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
        
    def convert_to_integer(self, value):
        try:
            # Periksa apakah nilai berisi akhiran K, M, atau B
            if value.endswith('K'):
                return int(float(value[:-1]) * 1_000)
            elif value.endswith('M'):
                return int(float(value[:-1]) * 1_000_000)
            elif value.endswith('B'):
                return int(float(value[:-1]) * 1_000_000_000)
            else:
                return int(value)  
        except ValueError:
            print(f"Error converting value: {value}")
            return 0
    def open_url(self, url):
        url = self.get(url)

    def update_hourly(self, cur, conn):
            cur.execute("SELECT `id`, `link` FROM `videos`;")
            existing_videos = cur.fetchall()

            start_index = 0
            while start_index < len(existing_videos):
                try:
                    # Membatasi durasi maksimum setiap iterasi dengan threading
                    result = [None]
                    video_id, link = existing_videos[start_index]

                    print(f"Opening... {link}")
                    thread = threading.Thread(target=self.process_video, args=(video_id, link, cur, conn, result))
                    thread.start()
                    thread.join(timeout=15)  # Maksimum 15 detik untuk setiap video
                    
                    if thread.is_alive():
                        # Timeout terjadi
                        print("Timeout occurred! Restarting browser...")
                        self.quit()

                        # Membuka browser baru dan melanjutkan dari video terakhir
                        with Video_History(teardown=False) as new_instance:
                            self.__dict__.update(new_instance.__dict__)
                        print("Browser restarted. Continuing from the last video...")
                        time.sleep(5)
                    else:
                        if result[0] == "success":
                            start_index += 1  # Lanjut ke video berikutnya
                        else:
                            print(f"Error on video {link}. Skipping to next.")

                except Exception as e:
                    print(f"Unexpected error: {e}")
                    print("Restarting browser...")
                    self.quit()

                    # Restart instance browser
                    with Video_History(teardown=False) as new_instance:
                        self.__dict__.update(new_instance.__dict__)
                    print("Browser restarted. Continuing from the last video...")
                    time.sleep(5)

    def process_video(self, video_id, link, cur, conn, result):
        try:
            self.open_url(link)
            duration = random.uniform(1, 2)
            time.sleep(duration)

            like_element = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="like-count"]'))
            )
            likes = self.convert_to_integer(like_element.text)
            print(f"Video ID: {video_id}, Likes: {likes}")

            # Masukkan data likes ke tabel history dengan foreign key ke video ID
            cur.execute(
                """
                INSERT INTO `video_histories` (`video_id`, `likes`)
                VALUES (%s, %s);
                """,
                (video_id, likes)
            )
            conn.commit()
            print("Data successfully saved to history.")
            result[0] = "success"

        except Exception as e:
            print(f"Error processing video {link}: {e}")
            result[0] = "error"