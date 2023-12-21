from sys import exit
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

class Driver:
    def create_driver(browser, GUI_MODE):
        options = ChromeOptions() if browser == 'chrome' else (FirefoxOptions() if browser == 'firefox' else EdgeOptions())
    
        if GUI_MODE == 0:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            
        if browser == "edge":
            options.use_chromium = True

            options.add_argument('--enable-javascript')
            options.add_argument('--log-level=3')
            options.add_argument('--silent')

        driver = None
        if browser == "chrome":
            driver = webdriver.Chrome(options=options)
        elif browser == "firefox":
            driver = webdriver.Firefox(options=options)
        elif browser == "edge":
            driver = webdriver.Edge(options=options)
        else:
            print("\n > Set DRIVER_OPTION di file .env menjadi DEFAULT (\"firefox\" atau \"chrome\").")
            exit(1)

        return driver
