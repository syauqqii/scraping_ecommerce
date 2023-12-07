# Import library from local folder
import module.controller
import module.helper

# Import library
import pandas as pd

# Make function to return foldername
def formater_folder():
    # Set variable from other object function
    HOUR, MINUTE, SECOND, DAY, MONTH, YEAR = other.get_datetime()
    # Set Format Directory Name
    return f"{RESULT_SCRAPING}{FORMAT_FOLDER.format(HOUR, MINUTE, SECOND, DAY, MONTH, YEAR)}" # result_scraping/10.25.30_06-12-2023/

# Make funtion to return filename
def formater_file(KEYWORD, CONFIG=1):
    return FORMAT_FILE.format(KEYWORD, EXTENSION_1) if CONFIG == 1 else FORMAT_FILE.format(KEYWORD, EXTENSION_2)

# Make function to create file
def create_file(_KEYWORD, DF, CONFIG=1):
    _DIRECTORY = formater_folder()
    _FILENAME  = formater_file(_KEYWORD, CONFIG)
    export.export_file(_DIRECTORY, _FILENAME, DF) if CONFIG == 1 else export.export_file(_DIRECTORY, _FILENAME, DF, 2)

# main function
def main():
    # Clear Console from other object function
    other.clear_screen()

    # Set Keyword Variable Name
    KEYWORD = str(input("\n > Input Keyword: "))
    _KEYWORD = KEYWORD.lower().strip().replace(" ", "%20")

    shopee.set_keyword(KEYWORD)
    blibli.set_keyword(KEYWORD)

    # 1 = paling relevan, 2 = paling baru, 3 = paling laris, 4 = murah ke mahal, 5 = mahal ke murah
    data_shopee = shopee.get_product(3)
    data_blibli = blibli.get_product()

    df_shopee = pd.DataFrame([
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
            'shop_location': item['item_basic']['shop_location'],
            'shop': 'shopee'
        }
        for item in data_shopee
    ])

    df_blibli = pd.DataFrame(data_blibli)

    # Concatenate the DataFrames
    df_combined = pd.concat([df_shopee, df_blibli], ignore_index=True)

    # Call function to save file (1 = csv, 2 = xlsx)
    create_file(KEYWORD.title().strip(), df_combined, 2)    

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
        RESULT_SCRAPING = setup.get_variable("RESULT_SCRAPING") # 'result_scraping/'
        FORMAT_FOLDER   = setup.get_variable("FORMAT_FOLDER")   # '{}.{}.{}_{}-{}-{}/'
        FORMAT_FILE     = setup.get_variable("FORMAT_FILE")     # '{}.{}'
        EXTENSION_1     = setup.get_variable("EXTENSION_1")     # 'csv'
        EXTENSION_2     = setup.get_variable("EXTENSION_2")     # 'xlsx'

        # Create object from class -- controller
        shopee = module.controller.Shopee()
        blibli = module.controller.Blibli()

        main()
    except KeyboardInterrupt:
        print("\n > CTRL + C pressed.")
        exit()