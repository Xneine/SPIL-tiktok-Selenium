from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inisialisasi driver
driver = webdriver.Firefox()

try:
    # Buka halaman target
    driver.get("https://slayingsocial.com/tiktok-trends-right-now/")

    # Tunggu elemen tren dimuat
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p > strong"))
    )

    # Ambil elemen tren
    trend_elements = driver.find_elements(By.CSS_SELECTOR, "p > strong")
    top_10_trends = []

    for trend in trend_elements:
        if len(top_10_trends) >= 10:
            break

        try:
            # Ambil deskripsi utama tren
            trend_description = trend.text

            # Cari tautan tren
            link_element = trend.find_element(By.XPATH, "./following-sibling::a")
            trend_link = link_element.get_attribute("href") if link_element else "No link available."

            # Tambahkan ke list
            top_10_trends.append({
                "description": trend_description,
                "link": trend_link,
            })

        except Exception as e:
            print(f"Error processing trend: {e}")

    # Cetak 10 tren teratas
    for i, trend in enumerate(top_10_trends, start=1):
        print(f"{i}. Description: {trend['description']}")
        print(f"   Link: {trend['link']}")

finally:
    driver.quit()
