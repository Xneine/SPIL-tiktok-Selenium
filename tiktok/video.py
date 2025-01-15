from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.firefox.options import Options

class Video(webdriver.Firefox):
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
        super(Video, self).__init__(options=firefox_options)
        self.maximize_window()
        self.implicitly_wait(5)


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
    
    def open_landing_page(self, url):
        print(f"Opening {url}...")
        self.get(url)
        time.sleep(10)
        
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
    
    def zoom_out(self):
        # self.execute_script("document.body.style.zoom='25%'")
        actions = ActionChains(self)
        for _ in range(8):
            actions.key_down(Keys.CONTROL).send_keys(Keys.SUBTRACT).key_up(Keys.CONTROL).perform()
            time.sleep(0.5)  # Kurangi jika respons terlalu lambat

            
        
    def scroll_page(self):
        """Scroll halaman sampai semua elemen dimuat"""
        scroll_pause_time = 10
        last_height = self.execute_script("return document.body.scrollHeight")
        
        while True:
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            
            new_height = self.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_all_videos(self):
        try:
            WebDriverWait(self, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="user-post-item"]'))
            )
            print("Fetching all videos...")
            # time.sleep(5)
            # self.zoom_out()
            # time.sleep(5)
            self.scroll_page()
            # time.sleep(20)
            
            video_elements = self.find_elements(By.CSS_SELECTOR, '[data-e2e="user-post-item"]')
            videos = []

            for video in video_elements:
                try:
                    views = video.find_element(By.CSS_SELECTOR, '[data-e2e="video-views"]').text
                    views_int = self.convert_to_integer(views)
                    
                    link = video.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    description = video.find_element(By.TAG_NAME, 'img').get_attribute('alt')
                    
                    videos.append({
                        'views': views_int,
                        'link': link,
                        # 'like': like_int,
                        'description': description
                    })
                except Exception as e:
                    print(f"Error fetching video data: {e}")

            print(f"Found {len(videos)} videos.")
            return videos

        except Exception as e:
            print(f"Error in get_all_videos: {e}")
            return []
        
    def get_newest_videos(self):
        try:
            print("Fetching newest videos...")

            WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="user-post-item"]'))
            )

            video_elements = self.find_elements(By.CSS_SELECTOR, '[data-e2e="user-post-item"]')
            videos = []
            video_links = set()  # Set untuk memastikan video unik

            for index, video in enumerate(video_elements):
                if index >= 8:
                    break
                try:
                    link = video.find_element(By.TAG_NAME, 'a').get_attribute('href')

                    if link in video_links:
                        continue  # Skip jika link sudah ada

                    views = video.find_element(By.CSS_SELECTOR, '[data-e2e="video-views"]').text
                    views_int = self.convert_to_integer(views)

                    like_icon = video.find_element(By.CSS_SELECTOR, '.like-icon')
                    like = like_icon.find_element(By.XPATH, './following-sibling::strong').text
                    like_int = self.convert_to_integer(like)

                    description = video.find_element(By.TAG_NAME, 'img').get_attribute('alt')

                    videos.append({
                        'views': views_int,
                        'link': link,
                        'like': like_int,
                        'description': description
                    })

                    video_links.add(link)  # Tambahkan ke set untuk validasi berikutnya
                except Exception as e:
                    print(f"Error fetching video data: {e}")

            print(f"Found {len(videos)} unique videos.")
            return videos

        except Exception as e:
            print(f"Error in get_all_videos: {e}")
            return []
   