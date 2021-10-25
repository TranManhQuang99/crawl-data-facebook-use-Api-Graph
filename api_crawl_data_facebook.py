from requests import session
import pandas as pd
import json
from openpyxl import Workbook
import csv
import re
import cv2
from PIL import Image
import pytesseract
from pytesseract import Output


# import facebook
idGroup = '870665749718859'
# idGroup = '870665749718859'

s = session()
limit = 'limit(100)'


values_crawl1 = 'fields=feed.'+limit+'{comments}'
values_crawl2 = 'fields=feed.'+limit
values_crawl3 = 'comments?fields=comments.'+limit

token = 'EAAAAZAw4FxQIBAG3oIFhFoWmZBiStA4EDFtAofNOnjDZAeNqZCoTG24HJXclKv6tzeWqZAfycFE4FZCbgxTDakJjHGDt635pgjGuMebPjHYgKMCTTOVpbcODnF1udpUCc9Cq1IFAp5Nsqy1YB3qRLsgjrmitNsz1LzIYDhbnGVgWqR9qNlRZAKxLI7IOwv3BZCEZD'

data_fb1 = s.get('https://graph.facebook.com/' + idGroup + '?' + values_crawl1 + '&access_token=' + token)
data_fb2 = s.get('https://graph.facebook.com/' + idGroup + '?' + values_crawl2 + '&access_token=' + token)
data_fb3 = s.get('https://graph.facebook.com/' + idGroup + '?' + values_crawl3 + '&access_token=' + token)


# ------- lấy nội dung commment
def get_comments():
    for i in (data_fb1.json()["feed"]["data"]):
        if "comments" in i:
            for x in i["comments"]["data"]:
                data = {
                    "Thời gian": x.get('created_time'),
                    "Nội dung": x.get('message'),
                    "Id comment": x.get('id')
                }
                with open("comment_post1.csv", "a", encoding='utf-8') as f:
                    f.write(f"{data['Thời gian']};{data['Nội dung']};{data['Id comment']}\n")


# ------------- Lay noi dung bai viet

def conten_post_api():
    for i in (data_fb2.json()["feed"]["data"]):
        data = {
            "Thời gian": i.get('updated_time'),
            "Nội dung": i.get('message'),
            "Id bài viết": i.get('id')
        }
        with open("content_post_2.txt", "a", encoding='utf-8') as f:
            f.write(
                f"{data['Thời gian']};{data['Nội dung']};{data['Id bài viết']}\n !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n\n\n")


# -------------- loc bai viet theo keyword

# lay ra cotent list
def conten_post_keyword():
    article_keywords = []
    for i in (data_fb2.json()["feed"]["data"]):
        sub_list = []
        sub_list.append(i.get('updated_time'))
        sub_list.append(i.get('message'))
        sub_list.append(i.get('id'))

        article_keywords.append(sub_list)
    return article_keywords


article_keywords = conten_post_keyword()  # trả về giá trị article_keywords


# Lọc bài viết theo keywword

def get_content_keyword():
    conten_keyword = []
    keywords = ['Data', 'DATA ANALYST', 'DATA SCIENTIST']
    for key in keywords:
        for string in article_keywords:
            if string[1] == None:  # kiểm tra bài nội dung bài viết có None không nếu có thì bỏ qua
                continue
            for i in string:
                if key in i:
                    conten_keyword.append(string)

    for list in range(0, len(conten_keyword)):
        print(conten_keyword[list])
    with open('content_keyword.csv', 'w', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(conten_keyword)


get_content_keyword()


# filter phone number and email adress
def filter_email():
    text = pd.read_csv("content_keyword.csv")
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(text))
    return emails

def filter_phone_number():
    text = pd.read_csv("content_keyword.csv")
    phone_number = re.findall("[(][\d]{3}[)][ ]?[\d]{3}-[\d]{4}", str(text))
    return phone_number

# image to text

image_file_path = r'C:\Users\ADMIN\PycharmProjects\pythonProject\venv\Lib\data\image_name870665749718859_4464688776983187.jpg'

def image_to_string(image_file_path):
    im = Image.open(image_file_path)
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    text = pytesseract.image_to_string(im, lang = 'eng')

    return  text

