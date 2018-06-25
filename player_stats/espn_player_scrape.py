import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
This script is used to 

"""
base_url = 'http://www.espn.com/nba/statistics/player/_/stat/scoring-per-game/sort/avgPoints/seasontype/2/qualified/false/count/'

team_map = {'HOU':'Rockets','NO':'Pelicans','CLE':'Cavaliers','POR':'Blazers','MIL':'Bucks','GS':'Warriors',
            'OKC':'Thunder','BOS':'Celtics','SA':'Spurs','IND':'Pacers','LAC':'Clippers','TOR':'Raptors',
            'PHX':'Suns','WSH':'Wizards','DET':'Pistons','MIN':'Timberwolves','MEM':'Grizzlies',
            'ATL':'Hawks','DAL':'Mavericks','NY':'Knicks','DEN':'Nuggets','BKN':'Nets','ORL':'Magic',
            'MIA': 'Heat','PHI':'76ers','CHI':'Bulls','LAL':'Lakers','UTAH':'Jazz','CHA':'Hornets', 'SAC':'Kings'}  # For convenience with existing data format



output_df = pd.DataFrame()

start_ranks = []
for i in range(14):
    start_ranks.append(40*i + 1)


urls = [base_url + str(rank) for rank in start_ranks]

for url in urls:
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html5lib")

    table = soup.find("table")

    headings = [th.get_text() for th in table.find("tr").find_all("td")]

    datasets = []
    for row in table.find_all("tr")[1:]:
        dataset = (td.get_text() for td in row.find_all("td"))
        datasets.append(dataset)

    df = pd.DataFrame(datasets)

    df.columns = headings

    output_df = pd.concat([output_df,df])


output_df.index = output_df.RK

output_df = output_df.drop(['RK']).drop(['RK'],axis=1)

output_df['TEAM'] = output_df.TEAM.apply(lambda x : x.split('/')[-1])  # Take a player's last team
output_df['team'] = output_df.TEAM.apply(lambda x : team_map[x])
output_df.drop(['TEAM'],axis=1,inplace=True)
output_df['position'] = output_df.PLAYER.apply(lambda x : (x.split(',')[-1].strip()))
output_df['fname'] = output_df.PLAYER.apply(lambda x : ' '.join(x.split(',')[0].split(' ')[:-1]))
output_df['lname'] = output_df.PLAYER.apply(lambda x : x.split(',')[0].split(' ')[-1])


for col in ['FGM-FGA','3PM-3PA','FTM-FTA']:
    new_col = col.split('-')[0]
    output_df[new_col] = output_df[col].apply(lambda x : x.split('-')[0])
    output_df.drop([col],axis=1,inplace=True)

output_df.drop(['PLAYER'],axis=1,inplace=True)

output_df.to_csv('player_stats.csv',index=False)
