from curl_cffi import requests
from bs4 import BeautifulSoup
import pandas
import time
import random
import multiprocessing
from fake_useragent import UserAgent
from itertools import cycle

def get_page(pi):
    url = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={0}&region=1'

    proxy_list = [
        #список прокси
    ]
    login = 'gV53aN9C:amW3wumk@'
    accept_list = ['*/*', 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8']
    encoding = 'gzip, deflate, br, zstd'
    language_list = ['ru-RU', 'ru;q=0.9', 'en-US;q=0.8', 'en', 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7']
    referer_list = ['https://www.google.com', 'https://ya.ru', 'https://www.cian.ru',
            'https://www.cian.ru/kupit-kvartiru/', url.format(pi),
            'https://ya.ru/search/?text=cian&lr=11315&search_source=yaru_desktop_common&search_domain=yaru']

    proxy_pool = cycle(proxy_list)
    browsers_dict = {"chrome": "chrome124", "safari": "safari17_0", "edge": "edge101"}
    browsers_list = ['chrome', 'safari', 'edge']
    accept_pool = cycle(accept_list)
    language_pool = cycle(language_list)
    random.shuffle(referer_list)
    referer_pool = cycle(referer_list)

    ua = UserAgent(min_version=120.0, platforms='pc', browsers=browsers_list)
    ua_dict = ua.getRandom
    proxy = next(proxy_pool)
    sess = new_sess(browsers_dict[ua_dict['browser']], login + proxy, ua_dict, next(referer_pool),
        next(accept_pool), encoding, next(language_pool))
    r = sess.get(url.format(pi))
    while r.status_code == 429:
        print('Error 429. URL: {0}'.format(url.format(pi)))
        time.sleep(random.uniform(5.0, 10.0))
        ua_dict = ua.getRandom
        sess = new_sess(browsers_dict[ua_dict['browser']], login + proxy, ua_dict, next(referer_pool),
            next(accept_pool), encoding, next(language_pool))
        r = sess.get(url.format(pi))
    if r.status_code == 200:
        cookies = r.cookies
        sess.cookies.update(cookies)

        soup = BeautifulSoup(r.text, 'html.parser')
        links = []
        for l in soup.findAll('a', class_='_93444fe79c--link--VtWj6'):
            links.append(l['href'])
        count = 0
        for link in links:
            start = time.time()
            r = sess.get(link)
            i = 1
            while r.status_code == 429:
                print('Error 429. URL: {0}'.format(link))
                count = 0
                time.sleep(random.uniform(5.0 * i, 10.0 * i))
                i += 1
                ua_dict = ua.getRandom
                sess = new_sess(browsers_dict[ua_dict['browser']], login + proxy, ua_dict, next(referer_pool),
                    next(accept_pool), encoding, next(language_pool))
                r = sess.get(link)
            if r.status_code == 200:
                print('Successful request! Browser: {0}'.format(ua_dict['browser']))
                cookies = r.cookies
                sess.cookies.update(cookies)
                get_info(r.text, link)
                count += 1
                if count == 3:
                    sess = new_sess(browsers_dict[ua_dict['browser']], login + proxy, ua_dict, next(referer_pool),
                        next(accept_pool), encoding, next(language_pool))
            else:
                print('Error: {0}.'.format(r.status_code))
            print("Parsing time: {0}".format(time.time() - start))
            print('---------------------------------------')
            time.sleep(random.uniform(2.0, 4.0))
            sess.get(url.format(pi))
            time.sleep(random.uniform(2.0, 4.0))
    else:
        print("Page Request error. Status code: {0}".format(r.status_code))

def new_sess(browser, proxy, ua_dict, referer, accept, encoding, language):
    headers = {'User-Agent': ua_dict['useragent'], 'Referer': referer,
               'Accept': accept, 'Accept-Encoding': encoding, 'Accept-Language': language}
    proxies = {'http': proxy}
    s = requests.Session(impersonate=browser)
    s.headers.update(headers)
    s.proxies.update(proxies)
    return s
def get_info(html, link):
    offer_str = 'None'
    place_str = 'None'
    address_str = 'None'
    price_str = 'None'

    s = BeautifulSoup(html, 'html.parser')
    offer = s.find('h1', class_='a10a3f92e9--title--vlZwT')
    if offer is not None:
        offer_str = offer.text

    place = s.find('a', class_='a10a3f92e9--link--A5SdC')
    if place is not None:
        place_str = place.text

    address = s.find('div', {'data-name': 'AddressContainer'})
    if address is not None:
        i = address.text.find('На карте')
        address_str = address.text[:i]

    price = s.find('div', {'data-testid': 'price-amount'})
    if price is not None:
        price_str = price.text
    try:
        df = pandas.DataFrame({'Offer': offer_str, 'Place': place_str,
                               'Address': address_str, 'Price': price_str, 'Link': link}, index=[0])
        w = pandas.ExcelWriter('./real_state.xlsx', engine='openpyxl', mode='a', if_sheet_exists="overlay")
        df.to_excel(w, sheet_name='Flats', startrow=w.sheets['Flats'].max_row, index=False, header=False)
        w.close()
        print('Data successfully added')
    except Exception as e:
        print('Zip file error: {0}'.format(e))

if __name__ == '__main__':
    df = pandas.DataFrame({'Offer': [], 'Place': [], 'Address': [], 'Price': [],
                           'Link': []})
    writer = pandas.ExcelWriter('./real_state.xlsx', engine='openpyxl')
    df.to_excel(writer, sheet_name='Flats', index=False)
    writer.close()

    page_list = list(range(1, 54))
    random.shuffle(page_list)

    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        p.map(get_page, page_list)
