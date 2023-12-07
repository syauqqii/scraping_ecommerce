from sys import exit
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

class Driver:
	def create_driver(browser, GUI_MODE):
	    if GUI_MODE == 1:
	        options = None
	    elif GUI_MODE == 0:
	        options = ChromeOptions() if browser == 'chrome' else FirefoxOptions()
	        options.add_argument('--headless')
	    else:
	    	print(f"\n > Set GUI_MODE di file .env menjadi DEFAULT (0 atau 1).")
	    	exit(1)

	    driver = None
	    if browser == "chrome":
	        driver = webdriver.Chrome(options=options)
	    elif browser == "firefox":
	        driver = webdriver.Firefox(options=options)
	    else:
	        print("\n > Set DRIVER_OPTION di file .env menjadi DEFAULT (\"firefox\" atau \"chrome\").")
	        exit(1)
	    
	    return driver