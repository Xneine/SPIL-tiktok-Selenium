from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Tiktok(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\SeleniumDrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Tiktok, self).__init__()
        self.implicitly_wait(5)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
    
    def open_landing_page(self, url):
        print(f"Opening {url}...")
        self.get(url)
        time.sleep(10)
    
    def get_followers(self):
        try:
            total_followers = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'count'))
            ).text
            print("ok1")
            total_likes = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/section/section/div/section[1]/div/div/div[2]/div[1]/div/span/h5'))
            ).text
            print("ok2")
            total_videos = WebDriverWait(self, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/section/section/div/section[1]/div/div/div[2]/div[2]/div/span/h5'))
            ).text
            print("ok3")
            # time.sleep(8)
            f = int(total_followers.replace(",", ""))
            l = int(total_likes.replace(",", ""))
            v = int(total_videos.replace(",", ""))
            result = [
                # int(total_followers.replace(",", "")), 
                # int(total_likes.replace(",", "")), 
                # int(total_videos.replace(",", ""))
                # total_followers, total_likes, total_videos
                f,l,v
            ]
            print(f"Total Followers: {total_followers}")
            print(f"Total Likes: {total_likes}")
            print(f"Total Videos: {total_videos}")
            return result
        except Exception as e:
            print(f"Error getting followers: {e}")
            return [None, None, None]
