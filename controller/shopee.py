from time import sleep
import json
from math import floor

class Shopee:
    def __init__(self, driver):
        self.driver = driver
        self.keyword = ""
        self._search_keyword = ""
        self._save_keyword = ""
        # self.data = ""

    def set_keyword(self, keyword):
        self.keyword = keyword
        self._search_keyword = keyword.lower().replace(' ', '%20')
        self._save_keyword = keyword.title()

    def get_save_keyword(self):
        return self._save_keyword

    def formula(self, max_products):
        limit = max_products if max_products < 60 else 60
        pages = 0
        lates = 0

        if max_products > limit:
            pages = floor(max_products / limit)
            lates = max_products % limit

        return  limit, pages, lates

    # FILTER: 1 = paling relevan, 2 = paling baru, 3 = paling laris, 4 = murah ke mahal, 5 = mahal ke murah
    def get_product(self, filters, max_products):
        # terkait 0, terbaru 1, terlaris 2, harga 3 (asc 0 -> rendah ke tinggi, DEFAULT: desc 1 -> tinggi ke rendah)
        filter_list = ["relevancy", "ctime", "sales", "price"]
        order_list = ["asc", "desc"]

        limit, page, limit_terakhir = self.formula(max_products)

        if max_products > limit:
            limit_terakhir = max_products % limit
            page = floor(max_products / limit)

        if 1 <= int(filters) <= 5:
            filter_mapping = {1: (filter_list[0], order_list[1]),
                              2: (filter_list[1], order_list[1]),
                              3: (filter_list[2], order_list[1]),
                              4: (filter_list[3], order_list[0]),
                              5: (filter_list[3], order_list[1])}

            filter, order = filter_mapping[int(filters)]

        product_data = []
        if page != 0:
            for i in range(0, page+1):
                print(f" > Request: page={i}")
                main_url = f"https://shopee.co.id/search?keyword={self._search_keyword}&page={i}"

                temp_newest = limit * i

                temp_limit = limit_terakhir if i == page else limit
                    
                print(f"            limit={temp_limit}&newest={temp_newest}")
                catch_produk_url = f"https://shopee.co.id/api/v4/search/search_items?by={filter}&keyword={self._save_keyword.replace(" ", "%20")}&limit={temp_limit}&newest={temp_newest}&order={order}&page_type=search&scenario=PAGE_SEO_SEARCH&version=2"
                
                self.driver.get(main_url)
                sleep(10)

                print()
                response = self.driver.execute_script(f"return fetch('{catch_produk_url}').then(response => response.text())")

                product_data.append(json.loads(response)['items'])
        else:
            main_url = f"https://shopee.co.id/search?keyword={self._search_keyword}"
            catch_produk_url = f"https://shopee.co.id/api/v4/search/search_items?by={filter}&keyword={self._save_keyword.replace(" ", "%20")}&limit={limit}&newest=0&order={order}&page_type=search&scenario=PAGE_SEO_SEARCH&version=2"
            
            print(f" > Request: page=0")
            self.driver.get(main_url)
            sleep(10)

            print(f"            limit={limit}&newest=0\n")
            response = self.driver.execute_script(f"return fetch('{catch_produk_url}').then(response => response.text())")
            product_data.append(json.loads(response)['items'])

        self.driver.quit()

        return product_data