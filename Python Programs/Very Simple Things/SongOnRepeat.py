from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import re

pattern = re.compile('chrome not reachable')
url = 'https://www.youtube.com/watch?v=gYPX5juKBvg&t=25'

option = Options()
option.add_argument('--disable-logging')


driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
try:
    driver.get(url)
except Exception:
    successful = False
else:
    successful = True

elem = driver.find_element_by_tag_name('body')

if successful:
    while True:
        try:
            time.sleep(10)
            elem.send_keys(Keys.ARROW_LEFT)
            elem.send_keys(Keys.ARROW_LEFT)
        except WebDriverException as e:
            if pattern.search(e.msg):
                successful = False
            else:
                raise e
        finally:
            if not successful:
                driver.quit()
                break
