import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://orteil.dashnet.org/experiments/cookie//")

# Grab a cookie to click on
cookie = driver.find_element(By.ID, "cookie")

# Set time limit: Check item store every 5 seconds. Run game for 3 minute
store_check_time = time.time() + 5
timeout = time.time() + 60 * 3

# Get store item ids
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]

# Get store item prices
prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
item_prices = []
for price in prices:
    element_text = price.text
    if element_text:
        cost = int(element_text.split("-")[1].strip().replace(",", ""))
        item_prices.append(cost)

# Set dictionary of store items and prices
store_items = {item_prices[i]: item_ids[i] for i in range(len(item_prices))}


while True:
    cookie.click()

    if time.time() > store_check_time:
        money = driver.find_element(By.ID, "money").text
        if "," in money:
            money = money.replace(",", "")
        cookie_count = int(money)

        upgradable_items = {}
        for price, item_id in store_items.items():
            if cookie_count > price:
                upgradable_items[price] = item_id
        max_price = max(upgradable_items)
        max_item = upgradable_items[max_price]
        driver.find_element(By.ID, max_item).click()

        store_check_time = time.time() + 5

    if time.time() > timeout:
        cps = driver.find_element(By.ID, "cps").text
        print(f"cookies/second: {cps}")
        break
