# Import library from local folder
import module.controller
import module.helper

# Import library
import pandas as pd
from math import floor

# Make function to return foldername
def formater_folder():
    # Set variable from other object function
    # HOUR, MINUTE, SECOND, DAY, MONTH, YEAR = other.get_datetime()
    DAY, MONTH, YEAR = other.get_datetime()
    # Set Format Directory Name
    # return f"{RESULT_SCRAPING}{FORMAT_FOLDER.format(HOUR, MINUTE, SECOND, DAY, MONTH, YEAR)}" # result_scraping/10.25.30_06-12-2023/
    return f"{RESULT_SCRAPING}{FORMAT_FOLDER.format(DAY, MONTH, YEAR)}" # result_scraping/10.25.30_06-12-2023/

# Make funtion to return filename
def formater_file(KEYWORD, CONFIG=1):
    return FORMAT_FILE.format(KEYWORD, EXTENSION_1) if CONFIG == 1 else FORMAT_FILE.format(KEYWORD, EXTENSION_2)

# Make function to create file
def create_file(_DIRECTORY, _KEYWORD, DF, CONFIG=1):
    _FILENAME  = formater_file(_KEYWORD, CONFIG)
    export.export_file(_DIRECTORY, _FILENAME, DF) if CONFIG == 1 else export.export_file(_DIRECTORY, _FILENAME, DF, 2)

# main function
def main():
    # Clear Console from other object function
    other.clear_screen()

    other.get_banner()

    # Set Keyword Variable Name
    KEYWORD = str(input("\n > Input Keyword       : "))
    
    if KEYWORD.strip() == "":
        main()
    elif KEYWORD.strip() == "-1":
        exit(0)
    
    _KEYWORD = KEYWORD.lower().strip().replace(" ", "%20")

    _DIRECTORY = formater_folder()

    if export.is_file_exists(_DIRECTORY, f"{KEYWORD.title().strip()}.csv") or export.is_file_exists(_DIRECTORY, f"{KEYWORD.title().strip()}.xlsx"):
        choice = input(f"\n > File ({_DIRECTORY}{KEYWORD.title().strip()} [.csv / .xlsx]) SUDAH ADA\n   apakah anda yakin ingin scrapping dengan keyword itu lagi? (y/n) ")
        if choice.lower() != 'y':
            main()
            
    JUMLAH_PRODUK = int(input("\n > Input Jumlah Produk : (max. 1000) "))

    # Mengecek apakah JUMLAH_PRODUK lebih dari 1500
    if JUMLAH_PRODUK >= 1000:
        JUMLAH_PRODUK = 1000
        print("   Jumlah Produk = 1000")
    # Mengecek apakah JUMLAH_PRODUK kurang dari 1
    elif JUMLAH_PRODUK <= 1:
        JUMLAH_PRODUK = 1
        print("   Jumlah Produk = 1")
    else:
        print(f"   Jumlah Produk = {JUMLAH_PRODUK}")

    print("\n # Sorting Produk:\n   1. paling relevan [DEFAULT]\n   2. paling baru\n   3. paling laris\n   4. harga: murah -> mahal\n   5. harga: mahal -> murah")

    SORTING = int(input("\n   > Input Pilihan : "))
    SORTING = int(1) if SORTING not in [1, 2, 3, 4, 5] else SORTING

    # print("\n # Simpan File:\n   1. csv\n   2. xlsx [DEFAULT]")

    # OPT_SAVING_FILE = int(input("\n   > Input Pilihan : "))
    # OPT_SAVING_FILE = int(2) if OPT_SAVING_FILE not in [1, 2] else OPT_SAVING_FILE

    total_detik = (TIMEOUT + TOLERANT) if JUMLAH_PRODUK < 60 else ((floor(JUMLAH_PRODUK / 60) + 1) * TIMEOUT) + (TOLERANT * (floor(JUMLAH_PRODUK / 60) + 1))
    menit = total_detik // 60
    detik_sisa = total_detik % 60

    print(f"\n [!] Perkiraan selesai: {menit} Menit {detik_sisa} Detik ({total_detik} detik)\n")

    # Create driver
    driver = module.controller.Driver.create_driver(DRIVER_OPTION, int(GUI_MODE))

    # Create object from class -- controller
    # blibli = module.controller.Blibli(driver)
    shopee = module.controller.Shopee(driver, TIMEOUT)

    shopee.set_keyword(KEYWORD)
    # blibli.set_keyword(KEYWORD)

    # @params get_products(..)
    #   1 = paling relevan
    #   2 = paling baru
    #   3 = paling laris
    #   4 = murah ke mahal
    #   5 = mahal ke murah
    #   6 = terpopuler (params: khusus blibli)
    data_shopee = shopee.get_product(SORTING, JUMLAH_PRODUK)
    # data_blibli = blibli.get_product(3)

    # Menggabungkan semua item dalam satu list
    all_items = [item for sublist in data_shopee for item in sublist]

    # Membuat DataFrame dari list produk_data
    df_shopee = pd.DataFrame({
        'itemid': [item['item_basic']['itemid'] for item in all_items],
        'shopid': [item['item_basic']['shopid'] for item in all_items],
        'name': [item['item_basic']['name'] for item in all_items],
        'stock': [item['item_basic']['stock'] for item in all_items],
        'sold': [item['item_basic']['sold'] for item in all_items],
        'liked': [item['item_basic']['liked_count'] for item in all_items],
        'price': [int(item['item_basic']['price']) / 100000 for item in all_items],
        'rating_star': [item['item_basic']['item_rating']['rating_star'] for item in all_items],
        'total_rating': [item['item_basic']['item_rating']['rating_count'][0] for item in all_items],
        'rating_1': [item['item_basic']['item_rating']['rating_count'][1] for item in all_items],
        'rating_2': [item['item_basic']['item_rating']['rating_count'][2] for item in all_items],
        'rating_3': [item['item_basic']['item_rating']['rating_count'][3] for item in all_items],
        'rating_4': [item['item_basic']['item_rating']['rating_count'][4] for item in all_items],
        'rating_5': [item['item_basic']['item_rating']['rating_count'][5] for item in all_items],
        'shop_location': [item['item_basic']['shop_location'] for item in all_items],
        'shop': 'shopee'
    })

    # Hapus data yang memiliki sold 0 dan rating start 0
    df_shopee = df_shopee.loc[(df_shopee['sold'] != 0) & (df_shopee['rating_star'] != 0)]

    # Hapus Duplicated data
    df_shopee = df_shopee.drop_duplicates(subset='itemid', keep='first')

    # Sorting Produk dengan sold paling banyak -> paling dikit
    df_shopee = df_shopee.sort_values(by='sold', ascending=False)

    jumlah_baris = len(df_shopee)

    if jumlah_baris < JUMLAH_PRODUK:
        print(f" > WARNING: Hasil  dari scraping {JUMLAH_PRODUK} produk, hanya mendapatkan {jumlah_baris} produk saja.\n")
    else:
        df_shopee = df_shopee.head(JUMLAH_PRODUK)
        print(f" > SUCCESS: Berhasil scraping {JUMLAH_PRODUK} produk.\n")

    # df_blibli = pd.DataFrame(data_blibli)

    # Concatenate the DataFrames
    # df_combined = pd.concat([df_shopee, df_blibli], ignore_index=True)

    # Call function to save file (1 = csv, 2 = xlsx)
    print(f" > Proses Membuat File: {KEYWORD.title().strip()}.csv")
    create_file(_DIRECTORY, KEYWORD.title().strip(), df_shopee, 1)

    print(f" > Proses Membuat File: {KEYWORD.title().strip()}.xlsx")
    create_file(_DIRECTORY, KEYWORD.title().strip(), df_shopee, 2)

    print("\n -- Selamat tinggal --")  

# main block
if __name__ == "__main__":
    try:
        # Create object from class -- helper
        export = module.helper.Export()
        other = module.helper.Other
        setup = module.helper.Setup()

        # Load environment from setup object function
        setup.load_env()

        # Read environment -- general
        USER_AGENT      = setup.get_variable("USER_AGENT")
        RESULT_SCRAPING = setup.get_variable("RESULT_SCRAPING") # 'result/'
        FORMAT_FOLDER   = setup.get_variable("FORMAT_FOLDER")   # '{}-{}-{}/'
        FORMAT_FILE     = setup.get_variable("FORMAT_FILE")     # '{}.{}'
        EXTENSION_1     = setup.get_variable("EXTENSION_1")     # 'csv'
        EXTENSION_2     = setup.get_variable("EXTENSION_2")     # 'xlsx'
        TIMEOUT         = int(setup.get_variable("TIMEOUT"))
        TOLERANT        = int(setup.get_variable("TOLERANT"))

        # Read environment -- driver
        GUI_MODE = setup.get_variable("GUI_MODE")
        DRIVER_OPTION = setup.get_variable("DRIVER_OPTION")

        main()
    except KeyboardInterrupt:
        print("\n > CTRL + C pressed.")
        exit()