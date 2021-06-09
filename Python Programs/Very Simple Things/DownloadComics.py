from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import requests
import concurrent.futures
import os
import time
from itertools import count


def download(info):
    chapter_name, url = info
    name = url.split('/')[11]
    response = requests.get(url)
    content = response.content
    with open(f'Comics/{chapter_name}/{name}', 'wb') as f:
        try:
            f.write(content)
        except Exception:
            print(f'Error in downloading {name}')
        else:
            print(f'{name} downloaded successfully')


pattern = re.compile(r'([\d]+)$')

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
option = Options()
option.add_argument('--headless')
# option.add_argument('log-level=3')
option.add_argument("--disable-logging")
option.add_argument(f'user-agent={user_agent}')

k = count(0)
main_url = f'https://reaperscans.com/comics/535459-mercenary-enrollment/1/{next(k)}'

while True:
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
        driver.get(main_url)
    except Exception:
        break

    time.sleep(0.5)

    for i in range(2):
        driver.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    chapter_name = main_url[-1]
    os.mkdir(f'D:/Python Programs/Comics/{chapter_name}')
    # print(soup.prettify())

    container = soup.find('div', {'id': 'pages-container'})
    # print(container.prettify())
    imgs = container.find_all('img')
    img_info = []
    for img in imgs:
        img_info.append((chapter_name, img['src']))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download, img_info)

    print(f"I think we're done with chapter {chapter_name}")

    main_url = main_url[:-1] + f'{next(k)}'
    print(main_url)

print('YAY, We did it!')
