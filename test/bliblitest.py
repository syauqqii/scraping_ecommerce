from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from json import loads
import pandas as pd

def scrape_blibli(keyword):
    try:
        # Set CONFIG_DRIVER
        CONFIG_DRIVER = 1  # Ganti nilainya sesuai kebutuhan (1 untuk Firefox, 2 untuk Chrome)

        # Pilih driver sesuai dengan CONFIG_DRIVER
        if CONFIG_DRIVER == 1:
            driver = webdriver.Firefox()
        elif CONFIG_DRIVER == 2:
            driver = webdriver.Chrome()
        else:
            raise ValueError("Nilai CONFIG_DRIVER tidak valid")

        # Langkah 1: Buka URL pertama Blibli
        url_page1_blibli = f"https://www.blibli.com/backend/search/products?sort=16&page=1&start=0&searchTerm={keyword}"
        driver.get(url_page1_blibli)

        # Tunggu hingga elemen dengan id "json" muncul
        json_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "json"))
        )
        data = loads(json_element.text)

        # Ekstraksi data yang diinginkan dari respons JSON
        product_data = []
        for product in data.get('data', {}).get('products', []):
            product_id = product.get('sku', '')
            shop_id = product.get('merchantCode', '')
            name = product.get('name', '')
            sold = product.get('soldRangeCount', {}).get('id', '')
            price = product.get('price', {}).get('minPrice', '')

            # Tambahkan data ke list
            product_data.append({
                'itemid': product_id,
                'shopid': shop_id,
                'name': name,
                'stock': 0,  # Fix: Set default value for stock
                'sold': int(sold) if sold and sold.isdigit() else 0,
                'liked': 0,  # Assuming like count is not available
                'price': price,
                'rating_star': 0,  # Fix: Set default value for rating_star
                'total_rating': 0,  # Fix: Set default value for total_rating
                'rating_1': 0,  # Fix: Set default value for rating_1
                'rating_2': 0,  # Fix: Set default value for rating_2
                'rating_3': 0,  # Fix: Set default value for rating_3
                'rating_4': 0,  # Fix: Set default value for rating_4
                'rating_5': 0,  # Fix: Set default value for rating_5
                'shop_location': '',  # Fix: Set default value for shop_location
                'shop': 'blibli'
            })

        # Simpan data pertama dalam DataFrame
        df_blibli = pd.DataFrame(product_data)

        # Inisialisasi product_list
        product_list = []

        # Langkah 2: Eksekusi skrip JavaScript untuk mengambil data dari URL kedua Blibli
        for index, row in df_blibli.iterrows():
            product_id = row['itemid']

            sleep(1)

            url_page2_blibli = f"https://www.blibli.com/backend/product-detail/products/is--{product_id}-00001/_summary"
            driver.get(url_page2_blibli)

            # Tunggu hingga elemen dengan id "json" muncul
            json_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "json"))
            )
            data = loads(json_element.text)

            # Ekstraksi data dari endpoint kedua
            stock = data['data']['stock']
            location = data['data']['merchant']['location']

            sleep(1)

            # Langkah 3: Eksekusi skrip JavaScript untuk mengambil data dari URL ketiga Blibli
            url_page3_blibli = f"https://www.blibli.com/backend/product-review/public-reviews?productSku={product_id}"
            driver.get(url_page3_blibli)

            # Tunggu hingga elemen dengan id "json" muncul
            json_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "json"))
            )
            data = loads(json_element.text)

            # Ekstraksi data dari endpoint ketiga
            total_reviews = data['summary']['count']
            average_rating = data['summary']['rating']['average']

            # Simpan data Blibli dalam bentuk array produk
            product_list.append({
                'itemid': product_id,
                'shopid': row['shopid'],
                'name': row['name'],
                'stock': int(stock),
                'sold': row['sold'],
                'liked': 0,  # Assuming like count is not available
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

        # Tutup WebDriver Blibli
        driver.quit()

        return product_list

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Contoh penggunaan
keyword = 'sandal slop'
result = scrape_blibli(keyword.strip().title())
print(result)
