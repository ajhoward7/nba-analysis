import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

df = pd.read_csv('nyt_article_list.csv')

urls = df.article_urls

for url in urls:
    title = url.split('/')[-1].split('.')[0]
    print("Article: {}".format(title))
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html5lib")
    paragraphs = soup.findAll("p", {"class":"css-1tyen8a e2kc3sl0"})

    text = ''

    for p in paragraphs:
        text += p.get_text()

    with open('articles/' + title + '.txt', 'w') as f:
        f.write(text)

    time.sleep(2 + np.random.rand())