from selenium import webdriver
from time import sleep
from json import loads

class Shopee:
    def __init__(self):
        self.keyword = ""
        self._search_keyword = ""
        self._save_keyword = ""
        self.data = ""

    def set_keyword(self, keyword):
        self.keyword = keyword
        self._search_keyword = keyword.lower().replace(' ', '%20')
        self._save_keyword = keyword.title()

    def get_save_keyword(self):
        return self._save_keyword

    # FILTER: 1 = paling relevan, 2 = paling baru, 3 = paling laris, 4 = murah ke mahal, 5 = mahal ke murah
    def get_product(self, filter):
        driver = webdriver.Firefox()

        url_1 = f"https://shopee.co.id/search?keyword={self._search_keyword}"
        driver.get(url_1)

        # Tunggu beberapa detik agar halaman dimuat sepenuhnya
        sleep(5)  # Sesuaikan dengan kebutuhan

        # terkait 0, terbaru 1, terlaris 2, harga 3 (asc 0 -> rendah ke tinggi, DEFAULT: desc 1 -> tinggi ke rendah)
        f = ["relevancy", "ctime", "sales", "price"]
        o = ["asc", "desc"]
        l = 40

        # 1 = paling relevan, 2 = paling baru, 3 = paling laris, 4 = murah ke mahal, 5 = mahal ke murah
        if int(filter) == 1:
            url_2 = f"https://shopee.co.id/api/v4/search/search_items?by={f[0]}&keyword={self._save_keyword.replace(" ", "%20")}&limit={l}&newest=0&order={o[1]}&page_type=search&scenario=PAGE_SEO_SEARCH&version=2"
        elif int(filter) == 2:
            url_2 = f"https://shopee.co.id/api/v4/search/search_items?by={f[1]}&keyword={self._save_keyword.replace(" ", "%20")}&limit={l}&newest=0&order={o[1]}&page_type=search&scenario=PAGE_SEO_SEARCH&version=2"
        elif int(filter) == 3:
            url_2 = f"https://shopee.co.id/api/v4/search/search_items?by={f[2]}&keyword={self._save_keyword.replace(" ", "%20")}&limit={l}&newest=0&order={o[1]}&page_type=search&scenario=PAGE_SEO_SEARCH&version=2"
        elif int(filter) == 4:
            url_2 = f"https://shopee.co.id/api/v4/search/search_items?by={f[3]}&keyword={self._save_keyword.replace(" ", "%20")}&limit={l}&newest=0&order={o[0]}&page_type=search&scenario=PAGE_SEO_SEARCH&version=2"
        elif int(filter) == 5:
            url_2 = f"https://shopee.co.id/api/v4/search/search_items?by={f[3]}&keyword={self._save_keyword.replace(" ", "%20")}&limit={l}&newest=0&order={o[1]}&page_type=search&scenario=PAGE_SEO_SEARCH&version=2"

        response = driver.execute_script(f"return fetch('{url_2}').then(response => response.text())")

        driver.quit()

        self.data = response
        return loads(response)['items']