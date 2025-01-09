from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
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
        
    def update_hourly(self,cur):
        cur.execute("SELECT `id`, `link` FROM `videos`;")
        existing_links = {row[1] for row in cur.fetchall()}
        for link in existing_links:
            # time.sleep(2)
            print("opening...", link)
            self.open_url(link)
            like = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="like-count"]'))
            )
            print("jumlah like: ", self.convert_to_integer(like.text))
        # return
    def update_hourly(self, cur, conn):
        cur.execute("SELECT `id`, `link` FROM `videos`;")
        existing_videos = cur.fetchall()

        for video_id, link in existing_videos:
            try:
                print("Opening...", link)
                self.open_url(link)

                like_element = WebDriverWait(self, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="like-count"]'))
                )
                likes = self.convert_to_integer(like_element.text)  
                print(f"Video ID: {video_id}, Likes: {likes}")

                # Masukkan data likes ke tabel history dengan foreign key ke video ID
                # cur.execute(
                #     """
                #     INSERT INTO `video_histories` (`video_id`, `likes`)
                #     VALUES (%s, %s);
                #     """,
                #     (video_id, likes)
                # )
                # conn.commit()
                # print("Data successfully saved to history.")

            except Exception as e:
                print(f"Error processing video {link}: {e}")