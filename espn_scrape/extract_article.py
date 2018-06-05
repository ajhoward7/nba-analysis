import requests
from bs4 import BeautifulSoup

url = 'http://www.espn.com/nba/story/_/id/23636649/eric-gordon-believes-houston-rockets-playing-title-chris-paul-had-played'


def extract_article(url):
    text = ""
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html5lib")
    soup.aside.decompose()
    soup.aside.decompose()  # Get rid of 'aside' tags - need to run twice for some reason

    for para in soup.find_all("p")[:-1]:
        if len(para.contents) == 1:
            text += para.contents[0]

    return text


print(extract_article(url))
