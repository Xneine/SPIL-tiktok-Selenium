import logging
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_viral():
    firefox_options = Options()
    firefox_options.add_argument('--disable-logging')
    firefox_options.add_argument('--log-level=3')
    firefox_options.add_argument('--disable-gpu')
    firefox_options.add_argument('--no-sandbox')
    firefox_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Firefox(options=firefox_options)
    driver.set_page_load_timeout(60)

    try:
        driver.get("https://slayingsocial.com/tiktok-trends-right-now/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p > strong"))
        )

        trend_elements = driver.find_elements(By.CSS_SELECTOR, "p > strong")
        top_10_trends = []

        for trend in trend_elements:
            if len(top_10_trends) >= 10:
                break

            try:
                trend_description = trend.text.strip()
                if not trend_description:
                    logging.warning("Trend description is empty. Skipping.")
                    continue

                link_element = trend.find_element(By.XPATH, "./following-sibling::a")
                trend_link = link_element.get_attribute("href") if link_element else "No link available."
                top_10_trends.append({"description": trend_description, "link": trend_link})
            except Exception as e:
                logging.error(f"Error processing trend: {e}")

        return top_10_trends
    finally:
        driver.quit()

def insert_viral_video(cur, viral_Video):
    try:
        cur.execute("DELETE FROM `viral_videos`")
        logging.info("All existing videos have been deleted from the database.")

        videos_to_insert = [video for video in viral_Video]

        insert_query = """
            INSERT INTO `viral_videos` (`link`, `Description`)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE `Description` = VALUES(`Description`);
        """
        data_to_insert = [(video['link'], video['description']) for video in videos_to_insert]

        cur.executemany(insert_query, data_to_insert)
        logging.info(f"{len(videos_to_insert)} new videos inserted into the database.")

    except Exception as e:
        logging.error(f"Error inserting or updating videos: {e}")

def mysqlconnect():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password="",
            db='project_social_media_spil',
        )
        with connection.cursor() as cur:
            viral_video = get_viral()
            if viral_video:
                insert_viral_video(cur=cur, viral_Video=viral_video)
                connection.commit()
            else:
                logging.warning("No viral videos found.")
    except Exception as e:
        logging.error(f"Database connection error: {e}")

if __name__ == "__main__":
    mysqlconnect()
