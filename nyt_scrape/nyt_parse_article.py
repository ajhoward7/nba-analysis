import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

df = pd.read_csv('nyt_article_list.csv')

url = df.article_urls[0]

r = requests.get(url)

soup = BeautifulSoup(r.text, "html5lib")

paragraphs = soup.findAll("p", {"class":"css-1tyen8a e2kc3sl0"})

text = ''

for p in paragraphs:
    text += p.get_text()

print(text)