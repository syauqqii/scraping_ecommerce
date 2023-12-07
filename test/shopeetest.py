from selenium import webdriver
from time import sleep
from json import loads
from requests import get
import pandas as pd  # Import library pandas
from os import system

if __name__ == "__main__":
    try:
        system("clear||cls")

        keyword = input("\n > Input Keyword: ")
        _keyword = keyword.strip().title()

        # resp = get(f"https://shopee.co.id/backend/growth/canonical_search/get_url/?keyword={keyword}", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'}).json()

        # print(resp['url'])

        # Set CONFIG_DRIVER
        CONFIG_DRIVER = 1  # Ganti nilainya sesuai kebutuhan (1 untuk Firefox, 2 untuk Chrome)

        # Pilih driver sesuai dengan CONFIG_DRIVER
        if CONFIG_DRIVER == 1:
            driver = webdriver.Firefox()
        elif CONFIG_DRIVER == 2:
            driver = webdriver.Chrome()
        else:
            raise ValueError("Nilai CONFIG_DRIVER tidak valid")

        # Langkah 1: Buka URL pertama
        # url_page1 = resp['url']
        url_page1 = f"https://shopee.co.id/search?keyword={keyword.strip().lower().replace(' ', '%20')}"
        driver.get(url_page1)

        # Tunggu beberapa detik agar halaman dimuat sepenuhnya
        sleep(5)  # Sesuaikan dengan kebutuhan

        # terkait 0, terbaru 1, terlaris 2, harga 3 (asc -> rendah ke tinggi, desc -> tinggi ke rendah)
        f = ["relevancy", "ctime", "sales", "price"]
        o = ["asc", "desc"]

        # Langkah 2: Eksekusi skrip JavaScript untuk mengambil data dari URL kedua
        url_page2 = f"https://shopee.co.id/api/v4/search/search_items?by={f[2]}&keyword={_keyword.replace(" ", "%20")}&limit=60&newest=0&order={o[1]}&page_type=search&scenario=PAGE_SEO_SEARCH&version=2"
        response = driver.execute_script(f"return fetch('{url_page2}').then(response => response.text())")

        # Cetak respons
        data = loads(response)['items']

        # Simpan data dalam DataFrame
        df = pd.DataFrame([
            {
                'itemid': item['item_basic']['itemid'],
                'shopid': item['item_basic']['shopid'],
                'name': item['item_basic']['name'],
                'stock': item['item_basic']['stock'],
                'sold': item['item_basic']['sold'],
                'liked': item['item_basic']['liked_count'],
                'price': int(item['item_basic']['price']) / 100000,
                'rating_star': item['item_basic']['item_rating']['rating_star'],
                'total_rating': item['item_basic']['item_rating']['rating_count'][0],
                'rating_1': item['item_basic']['item_rating']['rating_count'][1],
                'rating_2': item['item_basic']['item_rating']['rating_count'][2],
                'rating_3': item['item_basic']['item_rating']['rating_count'][3],
                'rating_4': item['item_basic']['item_rating']['rating_count'][4],
                'rating_5': item['item_basic']['item_rating']['rating_count'][5],
                'rcount_with_context': item['item_basic']['item_rating']['rcount_with_context'],
                'rcount_with_image': item['item_basic']['item_rating']['rcount_with_image'],
                'shop_location': item['item_basic']['shop_location'],
                'shop': 'shopee'
            }
            for item in data
        ])

        # Simpan DataFrame ke dalam file Excel
        df.to_excel(f'{_keyword}.xlsx', index=False)

        # Tutup WebDriver
        driver.quit()
    except KeyboardInterrupt:
        exit()