import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

PATH_TO_CHROME_DRIVER = "C:\\Users\\chris\\Downloads\\chromedriver_win32"

def main() -> None:
    os.environ['PATH'] += os.pathsep + PATH_TO_CHROME_DRIVER
    driver = webdriver.Chrome()

if __name__ == "__main__":
    main()