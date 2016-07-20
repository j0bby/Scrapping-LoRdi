from bs4 import BeautifulSoup

import requests
import re


r= requests.get("https://www.leboncoin.fr/informatique/995687831.htm?ca=6_s")

data = r.text

soup = BeautifulSoup(data)

annonce = soup.find('section',{'id':'adview'})

titre = annonce.find_all('h1')
print(titre[0].get_text())

descriptionTag = soup.find('div',{'class':re.compile('description$')})
description = descriptionTag.find('p',{'itemprop':'description'})
print(description.get_text())