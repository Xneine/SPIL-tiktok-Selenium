from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
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
        self.implicitly_wait(5)


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
    
    def open_landing_page(self, url):
        print(f"Opening {url}...")
        self.get(url)
        # time.sleep(10)
        
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
        
    def scroll_page(self):
        """Scroll halaman sampai semua elemen dimuat"""
        scroll_pause_time = 2
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
            print("Fetching all videos...")
            
            time.sleep(5)
            self.scroll_page()
            time.sleep(20)
            self.scroll_page()
            time.sleep(5)
            self.scroll_page()
            time.sleep(5)
            
            
            WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="user-post-item"]'))
            )

            video_elements = self.find_elements(By.CSS_SELECTOR, '[data-e2e="user-post-item"]')
            videos = []

            for video in video_elements:
                try:
                    views = video.find_element(By.CSS_SELECTOR, '[data-e2e="video-views"]').text
                    views_int = self.convert_to_integer(views)
                    
                    like_icon = video.find_element(By.CSS_SELECTOR, '.like-icon')
                    like = like_icon.find_element(By.XPATH, './following-sibling::strong').text
                    like_int = self.convert_to_integer(like)
                    
                    link = video.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    description = video.find_element(By.TAG_NAME, 'img').get_attribute('alt')
                    
                    videos.append({
                        'views': views_int,
                        'link': link,
                        'like': like_int,
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
            
            time.sleep(10)            
            
            WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="user-post-item"]'))
            )

            video_elements = self.find_elements(By.CSS_SELECTOR, '[data-e2e="user-post-item"]')
            videos = []

            for index, video in enumerate(video_elements):
                if index >= 8:
                    break
                try:
                    views = video.find_element(By.CSS_SELECTOR, '[data-e2e="video-views"]').text
                    views_int = self.convert_to_integer(views)
                    
                    like_icon = video.find_element(By.CSS_SELECTOR, '.like-icon')
                    like = like_icon.find_element(By.XPATH, './following-sibling::strong').text
                    like_int = self.convert_to_integer(like)
                    
                    link = video.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    description = video.find_element(By.TAG_NAME, 'img').get_attribute('alt')
                    
                    videos.append({
                        'views': views_int,
                        'link': link,
                        'like': like_int,
                        'description': description
                    })
                except Exception as e:
                    print(f"Error fetching video data: {e}")

            print(f"Found {len(videos)} videos.")
            return videos

        except Exception as e:
            print(f"Error in get_all_videos: {e}")
            return []        

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import os
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# from selenium.webdriver.firefox.options import Options
# import random


# class Video(webdriver.Chrome):
#     def __init__(self, driver_path=r"C:\SeleniumDrivers", teardown=False):
#         self.driver_path = driver_path
#         self.teardown = teardown
#         os.environ['PATH'] += self.driver_path

#         firefox_options = Options()
#         firefox_options.add_argument('--disable-logging')
#         firefox_options.add_argument('--log-level=3')  # Mengurangi level log menjadi "ERROR"
#         firefox_options.add_argument('--disable-gpu')  # Mengurangi error grafis
#         firefox_options.add_argument('--no-sandbox')  # Opsional, untuk menghindari masalah hak akses
#         firefox_options.add_argument('--disable-dev-shm-usage')  # Opsional, mengurangi masalah memori
#         firefox_options.add_argument(
#             "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36"
#         )  # Simulasi browser normal
#         # firefox_options.add_argument('--headless')  # Gunakan ini jika tidak perlu tampilan browser
#         super(Video, self).__init__(options=firefox_options)
#         self.implicitly_wait(5)

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if self.teardown:
#             self.quit()

#     def open_landing_page(self, url):
#         print(f"Opening {url}...")
#         self.get(url)
#         time.sleep(5)  # Tunggu awal untuk memastikan halaman terbuka

#     def convert_to_integer(self, value):
#         try:
#             if value.endswith('K'):
#                 return int(float(value[:-1]) * 1_000)
#             elif value.endswith('M'):
#                 return int(float(value[:-1]) * 1_000_000)
#             elif value.endswith('B'):
#                 return int(float(value[:-1]) * 1_000_000_000)
#             else:
#                 return int(value)
#         except ValueError:
#             print(f"Error converting value: {value}")
#             return 0

#     def scroll_page(self, max_scroll_attempts=15):
#         """Scroll halaman dengan jeda dan aksi acak untuk menghindari CAPTCHA"""
#         scroll_pause_min = 3
#         scroll_pause_max = 5
#         last_height = self.execute_script("return document.body.scrollHeight")
#         scroll_attempts = 0

#         while scroll_attempts < max_scroll_attempts:
#             # Scroll ke bawah
#             self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(random.uniform(scroll_pause_min, scroll_pause_max))

#             # Tambahkan aksi acak (opsional)
#             self.execute_script("window.scrollBy(0, -100);")  # Scroll sedikit ke atas
#             time.sleep(random.uniform(1, 2))

#             # Periksa apakah ada elemen baru yang dimuat
#             new_height = self.execute_script("return document.body.scrollHeight")
#             if new_height == last_height:
#                 scroll_attempts += 1
#             else:
#                 scroll_attempts = 0
#             last_height = new_height

#     def get_all_videos(self):
#         try:
#             print("Fetching all videos...")

#             # Gulir halaman untuk memuat semua elemen
#             self.scroll_page(max_scroll_attempts=15)

#             # Tunggu hingga elemen video muncul
#             WebDriverWait(self, 30).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="user-post-item"]'))
#             )

#             # Ambil semua elemen video
#             video_elements = self.find_elements(By.CSS_SELECTOR, '[data-e2e="user-post-item"]')
#             videos = []

#             for video in video_elements:
#                 try:
#                     views = video.find_element(By.CSS_SELECTOR, '[data-e2e="video-views"]').text
#                     views_int = self.convert_to_integer(views)

#                     like_icon = video.find_element(By.CSS_SELECTOR, '.like-icon')
#                     like = like_icon.find_element(By.XPATH, './following-sibling::strong').text
#                     like_int = self.convert_to_integer(like)

#                     link = video.find_element(By.TAG_NAME, 'a').get_attribute('href')
#                     description = video.find_element(By.TAG_NAME, 'img').get_attribute('alt')

#                     videos.append({
#                         'views': views_int,
#                         'link': link,
#                         'like': like_int,
#                         'description': description
#                     })

#                     time.sleep(random.uniform(1, 2))  # Tunggu 1-2 detik antara iterasi
#                 except Exception as e:
#                     print(f"Error fetching video data: {e}")

#             print(f"Found {len(videos)} videos.")
#             return videos

#         except Exception as e:
#             print(f"Error in get_all_videos: {e}")
#             return []

