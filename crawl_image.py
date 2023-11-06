from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import re
import json
import string
import random
import datetime
import requests
import pandas as pd

driver = webdriver.Chrome()
driver.maximize_window()
url = "https://www.shopify.com/stock-photos/coffee"
driver.get(url)

soupMain = BeautifulSoup(driver.page_source, "html.parser")

def process_image(str):
    split_str = str.split("/")
    str_tmp = split_str[-1]
    str_tmp = str_tmp.split("?")[0]
    return str_tmp

def download_image(url, file_path):
    response = requests.get(url)
    print(response.status_code)

    if response.status_code == 200:
        # Tạo đường dẫn đầy đủ đến thư mục đích
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("Hình ảnh đã được tải xuống thành công.")
    else:
        print("Lỗi trong quá trình tải xuống hình ảnh.")


data = pd.DataFrame(columns=["path", "description_image"])

sleep(15)
div_list_class_image = soupMain.find("div", {"class":"js-masonry-grid"})
list_class_image = div_list_class_image.find_all("div", {"class": "grid__item grid__item--desktop-up-third"})
print("len ", len(list_class_image))

for item in list_class_image:
    div_class_photo_title = item.find("div", {"class":"photo-tile"})
    title = div_class_photo_title.find("p",{"class":"photo-tile__title"})
    print("title :", title.text)
    div_a_image = div_class_photo_title.find("a",{"class":"photo-tile__image-wrapper"})
    div_class_ratio_box = div_a_image.find("div",{"class":"ratio-box"})
    image_div = div_class_ratio_box.find("img")
    image = image_div["src"]
    image_text = process_image(image)
    print("image :",image_text)
    # Thêm dữ liệu vào DataFrame
    new_data = pd.DataFrame({"path": [image_text], "description_image": [title.text]})
    data = pd.concat([data, new_data], ignore_index=True)
    # download_image(image, image_text)
    
data.to_csv("oke.csv", index=False)
    
sleep(9999)