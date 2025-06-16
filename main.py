from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

driver.get("https://www.google.com/maps")
search_input = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
search_input.send_keys("Restaurants in New York")
search_input.send_keys(Keys.ENTER)
time.sleep(5)

scrollable_div_xpath = '//div[@role="feed"]'
scrollable_div = wait.until(EC.presence_of_element_located((By.XPATH, scrollable_div_xpath)))

for _ in range(10):
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
    time.sleep(random.uniform(2, 4))

business_cards = driver.find_elements(By.XPATH, '//a[contains(@href, "/place/")]')
business_urls = list({card.get_attribute("href") for card in business_cards})

results = []

for url in business_urls:
    driver.get(url)
    time.sleep(random.uniform(3, 5))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    name_tag = soup.find('h1')
    name = name_tag.text.strip() if name_tag else ''
    phone = ''
    spans = soup.find_all('span')
    for span in spans:
        text = span.get_text(strip=True)
        if text.startswith('+1') and len(text) > 10:
            phone = text
            break
    results.append({'name': name, 'phone': phone, 'email': ''})

df = pd.DataFrame(results)
df.to_csv('google_maps_scraped_data.csv', index=False)

driver.quit()
