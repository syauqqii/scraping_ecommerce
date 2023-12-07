from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from json import loads
import pandas as pd

class Blibli:
    def __init__(self, driver):
        self.driver = driver
        self.keyword = ""
        self._search_keyword = ""
        self._save_keyword = ""
        self.data = ""

    def set_keyword(self, keyword):
        self.keyword = keyword
        self._search_keyword = keyword.strip().title()
        self._save_keyword = keyword.title()

    def get_save_keyword(self):
        return self._save_keyword

    def get_product(self, filter):
        try:
            print(" > proses ! [5]")

            # terkait 1, terbaru 2, terlaris 3, harga termurah 4, harga termahal 5
            if filter == 1:
                url_page1_blibli = f"https://www.blibli.com/backend/search/products?sort=0&page=1&start=0&searchTerm={self._search_keyword}"
            elif filter == 2:
                url_page1_blibli = f"https://www.blibli.com/backend/search/products?sort=1&page=1&start=0&searchTerm={self._search_keyword}"
            elif filter == 3:
                url_page1_blibli = f"https://www.blibli.com/backend/search/products?sort=16&page=1&start=0&searchTerm={self._search_keyword}"
            elif filter == 4:
                url_page1_blibli = f"https://www.blibli.com/backend/search/products?sort=3&page=1&start=0&searchTerm={self._search_keyword}"
            elif filter == 5:
                url_page1_blibli = f"https://www.blibli.com/backend/search/products?sort=4&page=1&start=0&searchTerm={self._search_keyword}"
            elif filter == 6:
                url_page1_blibli = f"https://www.blibli.com/backend/search/products?sort=7&page=1&start=0&searchTerm={self._search_keyword}"

            self.driver.get(url_page1_blibli)

            print(" > proses ! [6]")

            json_element = WebDriverWait(self.driver, 300).until(
                EC.presence_of_element_located((By.ID, "json"))
            )
            data = loads(json_element.text)

            print(" > proses ! [7]")

            product_data = []
            for product in data.get('data', {}).get('products', []):
                product_id = product.get('sku', '')
                shop_id = product.get('merchantCode', '')
                name = product.get('name', '')
                sold = product.get('soldRangeCount', {}).get('id', '')
                price = product.get('price', {}).get('minPrice', '')

                product_data.append({
                    'itemid': product_id,
                    'shopid': shop_id,
                    'name': name,
                    'stock': 0,
                    'sold': int(sold) if sold and sold.isdigit() else 0,
                    'liked': 0, 
                    'price': price,
                    'rating_star': 0,
                    'total_rating': 0,
                    'rating_1': 0,
                    'rating_2': 0,
                    'rating_3': 0,
                    'rating_4': 0,
                    'rating_5': 0,
                    'shop_location': '',
                    'shop': 'blibli'
                })

            df_blibli = pd.DataFrame(product_data)

            product_list = []
            for index, row in df_blibli.iterrows():
                product_id = row['itemid']

                sleep(1)

                url_page2_blibli = f"https://www.blibli.com/backend/product-detail/products/is--{product_id}-00001/_summary"
                self.driver.get(url_page2_blibli)

                json_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "json"))
                )
                data = loads(json_element.text)

                stock = data['data']['stock']
                location = data['data']['merchant']['location']

                sleep(1)

                url_page3_blibli = f"https://www.blibli.com/backend/product-review/public-reviews?productSku={product_id}"
                self.driver.get(url_page3_blibli)

                json_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "json"))
                )
                data = loads(json_element.text)

                total_reviews = data['summary']['count']
                average_rating = data['summary']['rating']['average']

                product_list.append({
                    'itemid': product_id,
                    'shopid': row['shopid'],
                    'name': row['name'],
                    'stock': int(stock),
                    'sold': row['sold'],
                    'liked': 0,
                    'price': row['price'],
                    'rating_star': average_rating,
                    'total_rating': total_reviews,
                    'rating_1': int(data['summary']['rating']['counts']['1']),
                    'rating_2': int(data['summary']['rating']['counts']['2']),
                    'rating_3': int(data['summary']['rating']['counts']['3']),
                    'rating_4': int(data['summary']['rating']['counts']['4']),
                    'rating_5': int(data['summary']['rating']['counts']['5']),
                    'shop_location': location,
                    'shop': 'blibli'
                })

            self.driver.quit()

            return product_list
        except Exception as e:
            print(f"Error: {str(e)}")
            return None