import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

df = pd.read_csv('nyt_article_list.csv')

urls = df.article_urls
i=0

for url in urls:
    i+=1
    title = url.replace("/","").replace(".","")
    print("Article: {}".format(title))
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html5lib")
        paragraphs = soup.findAll("p", {"class":"css-1i0edl6 e2kc3sl0"})

        text = []

        for p in paragraphs:
            text.append(p.get_text())


        with open('new_articles/{}.txt'.format(title), 'w') as f:
            text = '\n'.join(text)
            f.write(text)

    except:
        print("Unable to fetch: {}".format(url))

    time.sleep(2 + np.random.rand())