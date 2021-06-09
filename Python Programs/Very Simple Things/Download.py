import requests
from bs4 import BeautifulSoup
import concurrent.futures


def download(img_url):
    info = requests.get(img_url).content
    img_name = img_url.split('/')[4]
    path = f"D:/Python Programs/images/{img_name}.jpg"
    with open(str(path), 'wb') as f:
        try:
            f.write(info)
        except Exception:
            return f'Error in downloading {img_name}.jpg'
        else:
            return f'{img_name} downloaded successfully!'


img_urls = []
r = requests.get('https://unsplash.com/').text
soup = BeautifulSoup(r, 'lxml')
req_div = soup.find('div', class_='_3UDio _2sCnE PrOBO _1CR66')
anchors = req_div.find_all('a')
for key, anchor in enumerate(anchors):
    if key == 48:
        break
    img_urls.append('https://unsplash.com' + anchor['href'])
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(download, img_url) for img_url in img_urls]
    for i in concurrent.futures.as_completed(results):
        print(i.result())
