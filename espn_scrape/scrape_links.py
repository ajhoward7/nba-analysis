import requests
from bs4 import BeautifulSoup
import numpy as np
import time
import progessbar
import pandas as pd

titles = []
web_links = []

base_url = 'http://www.espn.com/nba/news/archive/_/month/{}/year/{}'
months = [('may','2018'),('april','2018'),('march','2018'),('february','2018'),('january','2018'),
          ('december','2017'),('november','2017'),('october','2017')]
urls = [base_url.format(month[0],month[1]) for month in months]

i = 0

bar = progessbar.ProgressBar(maxval=len(urls),widgets=[progessbar.Bar('=','[',']'),' ', progessbar.Percentage()])
bar.start()

for url in urls:
    i+=1
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html5lib")
    links = soup.find_all("ul", {"class": "inline-list indent"})
    soup2 = BeautifulSoup(str(links[0]))
    for link in soup2.find_all("a"):
        titles.append(link['title'])
        web_links.append(link["href"])
    time.sleep(np.random.randint(1,3))
    bar.update(i+1)

bar.finish()

df = pd.DataFrame()
df['links'] = web_links
df['titles'] = titles

df.to_csv('article_links.csv')
