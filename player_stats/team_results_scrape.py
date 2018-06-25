import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import sys

"""
This script 
"""

# CHOOSE TEAM NAME VIA COMMAND LINE ARGUMENT:

team_name = sys.argv[1]

base_url = 'https://www.basketball-reference.com/teams/{}/2018_games.html'

# Choose team:
results = base_url.format(team_name)

try:
    r = requests.get(results)
    soup = BeautifulSoup(r.text,"html5lib")


    tables = soup.find_all("table")


    # REGULAR SEASON:
    table = tables[0]
    headings = [th.get_text() for th in table.find("tr").find_all("th")]

    datasets = []
    for row in table.find_all("tr")[1:]:
        dataset = (td.get_text() for td in row.find_all("td"))
        datasets.append(dataset)

    df = pd.DataFrame(datasets).dropna()

    df.columns = headings[1:]

    df = df[['Date','Opponent','Tm','Opp','W','L']]

    df.Date = pd.to_datetime(df.Date)

    df['net_wins'] = df.W.astype('int') - df.L.astype('int')
    df['win_flag'] = (df.Tm.astype('int') - df.Opp.astype('int')) > 0
    df.win_flag = df['win_flag'].apply(lambda x: 'W' if x == True else 'L')

    df['text'] = df.win_flag + ' vs ' + df.Opponent + ' (' +\
                          df.Tm.astype('int').astype('str') + '-' +\
                          df.Opp.astype('int').astype('str') + ')'

    df.to_csv("player_stats/{}_results.csv".format(team_name),index=False)

    reg_wins = list(df.net_wins)[-1]


    # POSTSEASON:
    if len(tables) > 1:
        table = tables[1]

        headings = [th.get_text() for th in table.find("tr").find_all("th")]

        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = (td.get_text() for td in row.find_all("td"))
            datasets.append(dataset)

        df = pd.DataFrame(datasets).dropna()

        df.columns = headings[1:]

        df = df[['Date','Opponent','Tm','Opp','W','L']]

        df.Date = pd.to_datetime(df.Date)

        df['net_wins'] = reg_wins + df.W.astype('int') - df.L.astype('int')
        df['win_flag'] = (df.Tm.astype('int') - df.Opp.astype('int')) > 0
        df.win_flag = df['win_flag'].apply(lambda x: 'W' if x==True else 'L')

        df['text'] = df.win_flag + ' vs ' + df.Opponent + ' (' + \
                     df.Tm.astype('int').astype('str') + '-' + \
                     df.Opp.astype('int').astype('str') + ')'


        df.to_csv("player_stats/{}_results_postseason.csv".format(team_name),index=False)

        print("Complete! Output stored in {}_results.csv and {}_results_postseason.csv. Ready to load into memory :-)".format(team_name,team_name))

    else:
        print("Complete! Output stored in {}_results.csv".format(team_name))

except:
    print("Either your internet connection is broken or you've used the wrong team acronym. Try again!")
