import json
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
import time
from parse import get_captha
from selenium.common.exceptions import NoSuchElementException
from api_key import API_KEY

ua = UserAgent()
opt = Options()
opt.add_argument(f'user-agent={ua.random}')

url = 'https://otzovik.com/reviews/strahovaya_kompaniya_rosgosstrah/'

browser = webdriver.Firefox(options=opt)
browser.maximize_window()


def get_img():
    browser.find_element(By.NAME, 'captcha_url')
    with open("img.png", 'wb') as file:
        image = browser.find_element(By.TAG_NAME, 'img')
        file.write(image.screenshot_as_png)


def solve_captcha():
    get_img()
    captcha_code = get_captha('img.png', API_KEY)
    input_form = browser.find_element(By.NAME, 'llllllll')
    input_form.send_keys(captcha_code)
    browser.find_element(By.NAME, 'action_capcha_ban').click()


def page_parse(item):
    info = {}
    item_left = item.find_element(By.CLASS_NAME, 'item-left')
    item_right = item.find_element(By.CLASS_NAME, 'item-right')
    info['user_name'] = item_left.find_element(By.CLASS_NAME, 'login-line').text
    info['country'] = item_left.find_element(By.CSS_SELECTOR, 'div.item-left > div > div:nth-child(3)').text
    info['rating_score'] = item_right.find_element(By.CLASS_NAME, 'rating-score').find_element(By.TAG_NAME, 'span').text
    info['date'] = item_right.find_element(By.CLASS_NAME, 'review-postdate').text
    return info


def get_items_info():
    result = []
    while True:
        items_list = browser.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div/div[4]/div[1]/div[1]')
        items = items_list.find_elements(By.CLASS_NAME, 'item')
        for item in items:
            info = page_parse(item)
            result.append(info)
        try:
            browser.find_element(By.CLASS_NAME, 'next').click()
        except NoSuchElementException:
            try:
                solve_captcha()
            except:
                print('Парсинг прошел успешно.')
                return result


def json_write():
    with open('items_info.json', 'w') as file:
        json.dump(get_items_info(), file, indent=4, ensure_ascii=False)


try:
    browser.get(url=url)
    solve_captcha()
    time.sleep(2)
    json_write()
except:
    time.sleep(2)
    json_write()
finally:
    browser.quit()


