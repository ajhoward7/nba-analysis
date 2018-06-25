import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

df = pd.read_csv('nyt_article_list.csv')

urls = df.article_urls
i=0

for url in urls:
    text = []
    i += 1

    title = url.replace("/","").replace(".","")
    try:
        print(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html5lib")
        paragraphs = soup.findAll("p", {"class":"css-1i0edl6 e2kc3sl0"})  # Format 1
        paragraphs += soup.findAll("p", {"class":"story-body-text story-content"})  # Format 2
        paragraphs += soup.findAll("p", {"class": "g-body"})  # Format 3

        text = []

        for p in paragraphs:
            text.append(p.get_text())

        if len(text) == 0:
            print(r)


        with open('final_articles/{}.txt'.format(title), 'w') as f:
            text = '\n'.join(text)
            f.write(text)

    except:
        print("Unable to fetch: {}".format(url))

    time.sleep(2 + np.random.rand())