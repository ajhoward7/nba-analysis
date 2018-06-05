import requests
import time
import json
import numpy as np
import pandas as pd

base_url = 'https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/section/sports/basketball?q=&sort=newest&page={}&dom=www.nytimes.com&dedupe_hl=y'

urls = [base_url.format(i) for i in range(30)]

published_date = []
article_urls = []
article_summary = []
article_headline = []

i = 0

for url in urls:
    response = requests.get(url)
    json_blob = json.loads(response.text)
    articles = json_blob['members']['items']

    i+=1

    print("Completed: {}".format(i))

    for article in articles:
        published_date.append(article["first_published_iso_timestamp"])
        article_urls.append(article['url'])
        article_summary.append(article['summary'])
        article_headline.append(article['headline'])

    time.sleep(2 + np.random.rand())

df = pd.DataFrame()

df['published_date'] = published_date
df['article_urls'] = article_urls
df['article_summary'] = article_summary
df['article_headline'] = article_headline

df.to_csv('nyt_article_list.csv', index = False)
