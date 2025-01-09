from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time

class Tiktok(webdriver.Firefox):
    def __init__(self, driver_path=r"C:\SeleniumDrivers", teardown=True):
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
        super(Tiktok, self).__init__(options=firefox_options)
        self.implicitly_wait(5)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
    
    def open_landing_page(self, url):
        print(f"Opening {url}...")
        self.get(url)
        time.sleep(5)
        # self.save_screenshot("page_screenshot.png")
    
    # def get_followers(self):
    #     try:
    #         total_followers = WebDriverWait(self, 20).until(
    #             EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="followers-count"]'))
    #         ).text
    #         print("ok1")
    #         total_likes = WebDriverWait(self, 20).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH, "//div[h3[text()='Live Likes Count']]/div/span/h5")
    #             )
    #         ).text
    #         print("ok2")
    #         total_videos = WebDriverWait(self, 20).until(
    #             EC.presence_of_element_located(
    #                 (By.XPATH, "//div[h3[text()='Total TikTok Videos']]/div/span/h5")
    #             )
    #         ).text
    #         print("ok3")
    #         # time.sleep(8)
    #         f = int(total_followers.replace(",", ""))
    #         l = int(total_likes.replace(",", ""))
    #         v = int(total_videos.replace(",", ""))
    #         result = [
    #             f,l,v
    #         ]
    #         print(f"Total Followers: {total_followers}")
    #         print(f"Total Likes: {total_likes}")
    #         print(f"Total Videos: {total_videos}")
    #         return result
    #     except Exception as e:
    #         print(f"Error getting followers: {e}")
    #         return [None, None, None]
    def get_followers_likes_videos(self):
        try:
            print("Loading page source...")

            total_followers = WebDriverWait(self, 30).until(
                EC.presence_of_element_located((By.XPATH, "//h5[@class='count']"))
            ).text

            total_likes = WebDriverWait(self, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[h3[text()='Live Likes Count']]/div/span/h5")
                )
            ).text

            total_videos = WebDriverWait(self, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[h3[text()='Total TikTok Videos']]/div/span/h5")
                )
            ).text

            followers = int(total_followers.replace(",", ""))
            likes = int(total_likes.replace(",", ""))
            videos = int(total_videos.replace(",", ""))

            print(f"Followers: {followers}, Likes: {likes}, Videos: {videos}")
            return [followers, likes, videos]

        except Exception as e:
            print(f"Error fetching data: {e}")
            return [None, None, None]

