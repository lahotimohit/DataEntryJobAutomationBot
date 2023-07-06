import time

import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

FLAT_SEARCH_URL = "https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=2,3&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Jaipur"
ANSWER_SUBMISSION_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSdlZOjkHTAn_FKERgkzIeZlyR7RwkPZCvTXbFzWLrQXPzxf2w/viewform?usp=sf_link"
CHROME_DRIVER = "C:\Development\chromedriver.exe"

response = requests.get(url=FLAT_SEARCH_URL)
soup = bs4.BeautifulSoup(response.text, "html.parser")
available_flats = soup.find_all(name="h2", class_ ="mb-srp__card--title")
all_prices = soup.find_all(name="div", class_ = "mb-srp__card__price--amount")
all_links = soup.find_all(name="a", class_ = "mb-srp__card__developer--name")
links = [link.get("href") for link in all_links]

service = Service(executable_path=CHROME_DRIVER)
driver = webdriver.Chrome(service=service)
driver.maximize_window()

for n in range(len(links)):
    driver.get(url=ANSWER_SUBMISSION_LINK)
    time.sleep(1)

    address_answer = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_answer = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    url_answer = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_btn = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address_answer.send_keys(available_flats[n].text)
    price_answer.send_keys(all_prices[n].text)
    url_answer.send_keys(links[n])
    submit_btn.click()
driver.quit()

RESPONSE_SPREADSHEET = "https://docs.google.com/forms/d/1ToPjrLG99VLJ-0zhWVvdOu5z8Ssvir3M84YLIS-z_N4/edit"
driver.get(url=RESPONSE_SPREADSHEET)
time.sleep(3)
FORM_RESPONSE = driver.find_element(By.XPATH, '//*[@id="tJHJj"]/div[3]/div[1]/div/div[2]/span/div')
FORM_RESPONSE.click()
time.sleep(1)

GOOGLE_SHEET = driver.find_element(By.XPATH, '//*[@id="ResponsesView"]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div/span/span[2]')
GOOGLE_SHEET.click()
