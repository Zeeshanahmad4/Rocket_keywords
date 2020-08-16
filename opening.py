options = webdriver.ChromeOptions()
    options.add_argument(r'user-data-dir=C:\\Users\\Abdullah\\AppData\\Local\\Google\\Chrome\\User Data')
    driver = webdriver.Chrome(chrome_options=options)