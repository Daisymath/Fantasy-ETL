#merge the adp together
#import
import pandas as pd
from datetime import date
import numpy as np

adp_hist = pd.read_csv('adp_merged.csv')
adp_curr = pd.read_csv('adp_scrape.csv')
player_ids = pd.read_csv('player_ids.csv')

file_name = "adp_merged_"+ adp_hist['load_date'][0]+".csv"
#save the old hist for record keeping
adp_hist.to_csv(file_name,index=False)

#put player ids in the adp scrape
def nameCheck(player):
    player = player.replace(".","").replace(" ","").replace("'","").replace("-","")
    player = player.lower()
    return player

#lowercase temp names to compare
adp_curr['temp_name'] = adp_curr['Player'].map(nameCheck)
player_ids['temp_name'] = player_ids['Player'].map(nameCheck)

#merge and clean up columns
adp_curr_v2 = pd.merge(adp_curr,player_ids[['Player','PlayerID','temp_name']],how='left',left_on=['temp_name'],right_on=['temp_name'])
adp_curr_v2.drop(columns=['Player_x','temp_name'],inplace=True)
adp_curr_v2.rename(columns={'Player_y':'Player'},inplace=True)

#Drop all 2023 adps
adp_hist = adp_hist[~(adp_hist['Year'] == 2023)]

adp_curr_v2 = adp_curr_v2.rename(columns={"Player":"name","Team":"team","ADP":"adp","Pos":"position"})
adp_curr_v2.drop(columns='Rank',inplace=True)

adp_curr_v2['Year'] = 2023

adp_hist.drop(columns='load_date',inplace=True)

#put previous year adp with newly scraped
adp_hist_v2 = pd.concat([adp_hist,adp_curr_v2])

#clean team names
adp_hist_v2['team'] = adp_hist_v2['team'].map(lambda team: team.upper())
#add new load date
adp_hist_v2['load_date'] = (str(date.today())).replace("-","_")
#add in the adp rank by position, i.e. QB2 or RB15
adp_hist_v2['Pos_Number'] = adp_hist_v2.groupby(['position','Year'])['adp'].rank('min')


adp_hist_v2.to_csv("adp_merged.csv",index=False)


#Ranking and proj
#Updating the others
proj = pd.read_csv('proj_scrape.csv')
ranking = pd.read_csv('ranking_scrape.csv')


#lowercase temp names to compare
proj['temp_name'] = proj['Player'].map(nameCheck)
ranking['temp_name'] = ranking['player'].map(nameCheck)
player_ids['temp_name'] = player_ids['Player'].map(nameCheck)

#cleanstuff
proj.drop(columns='Team',inplace=True)
#clean up rookie missing 2022 stat values
proj = proj.replace('--',np.nan)
proj['2022 Stats'] = proj['2022 Stats'].astype(float)
ranking['team'] = ranking['team'].map(lambda team: team.upper())

#merge and clean up columns
proj_v2 = pd.merge(proj,player_ids[['Player','PlayerID','temp_name']],how='left',left_on=['temp_name'],right_on=['temp_name'])
proj_v2.drop(columns=['Player_x','temp_name'],inplace=True)
proj_v2.rename(columns={'Player_y':'Player'},inplace=True)

ranking_v2 = pd.merge(ranking,player_ids[['Player','PlayerID','temp_name']],how='left',left_on=['temp_name'],right_on=['temp_name'])
ranking_v2.drop(columns=['player','temp_name'],inplace=True)

proj_v2.to_csv('proj_merged.csv',index=False)
ranking_v2.to_csv("ranking_merged.csv",index=False)