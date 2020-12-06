from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import os
import time

from PIL import Image
import pytesseract



def recognize():
    im = Image.open("capture/image.png")
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
    text = pytesseract.image_to_string(im).strip()
    print(text)
    im.show()
    time.sleep(5)
    return text

def captchaSnatch(driver):
    try:
        wait = WebDriverWait(driver,50)
        ele = wait.until(
            EC.presence_of_element_located((By.ID,"captcha"))
        )
        imgBytes = ele.screenshot_as_png
        #print(imgBytes)
        with open("capture/image.png", "wb") as img:
            img.write(imgBytes)
    except Exception as e:
        print("\n exception in landingPage \n ",e)

def landingPage(driver,link):
    driver.get(link)
    if(driver.page_source.find("This site can’t be reached")==-1):
        captchaSnatch(driver)
        recognize()
    else:
        print("\n try Again \n")
        landingPage(driver,link)

if __name__=="__main__":
    driver_path = "layer/bin/driver_87/chromedriver"
    options = Options()
    options.binary_location = "layer/bin/chrome_87/chrome"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(executable_path=driver_path,
                          options=options) as driver:
        link = "http://www.mca.gov.in/mcafoportal/viewSignatoryDetails.do"
        landingPage(driver,link)
        driver.quit()
