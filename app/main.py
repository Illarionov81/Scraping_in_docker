import os
import subprocess
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = 'https://finance.yahoo.com/'
COMPANIES = ['PD', 'ZUO', 'PINS', 'ZM', 'PVTL', 'DOCU', 'CLDR', 'RUN']


def get_company_data(companies):
    save_dir = os.path.abspath('downloads')
    try:
        os.mkdir(save_dir)
        print('create dir')
    except OSError:
        print('dir already has ')
        pass
    folder = [save_dir]
    subprocess.call(['chmod', "guo+rwx"] + folder)
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
    #                      ' Chrome/90.0.4430.93 Safari/537.36')
    prefs = {'download.default_directory': f'/home/seluser/Downloads',
             'prompt_for_download': False,
             "directory_upgrade": True,
             }
    options.add_experimental_option('prefs', prefs)
    path_to_driver = os.path.abspath('chromedriver')
    capabilities = {
        "browserName": "chrome",
        "version": "90.0.4430.85",
        "platform": "LINUX"
    }
    driver = webdriver.Remote('http://selenium:4444/wd/hub', desired_capabilities=capabilities, options=options)
    # driver = webdriver.Remote('http://selenium:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME, options=options)
    # driver = webdriver.Chrome(executable_path=path_to_driver, options=options)

    for company in companies:
        print('#' * 10)
        print(company)
        print('#' * 10)
        get_data(URL, company, driver)
    try:
        print('Start parsing . . . ')
        files = os.listdir(save_dir)
        print(files)
        for f in files:
            filename = os.path.basename(os.path.join(save_dir + os.path.relpath(f)))
            name = os.path.splitext(filename)[0]
            print(save_dir)
            print(name)
    except FileNotFoundError:
        print(f'No such file or directory: {save_dir}')


def get_data(url, company, driver):
    try:
        driver.get(url)
        print('search company')
        driver.find_element_by_id('yfin-usr-qry').send_keys(f'{company}')
        driver.find_element_by_id('header-desktop-search-button').click()
        print('find link - historical_data ')
        link = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//li[@data-test='HISTORICAL_DATA']"))
        )
        link.find_element_by_css_selector("a").click()
        print('find date choice')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "dateRangeBtn"))).click()
        print('find button - MAX')
        driver.find_element_by_xpath("//button[@data-value='MAX']").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@download]"))).click()
        print('download file')
        time.sleep(10)
        print('ready')
    except Exception as e:
        print(e)
        print('! ' * 20, company, 'not find')
    # finally:
    #     driver.close()
    #     driver.quit()


if __name__ == '__main__':
    get_company_data(COMPANIES)
