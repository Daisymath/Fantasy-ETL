#import stuff
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

#relevant URLS
#top 150 ppr rankings field yates
URL_rankings = "https://www.espn.com/fantasy/football/story/_/id/37683451/2023-fantasy-football-rankings-ppr-field-yates-qb-rb-wr-te"
URL_adp = "https://fantasy.espn.com/football/livedraftresults"
URL_proj = "https://fantasy.espn.com/football/players/projections"

options = Options()
options.page_load_strategy = 'none'
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get(URL_adp)
time.sleep(2)

#Scrape ADP
pages = [0,1,2,3]
adp = []
for i in pages:
    print("Running "+str(i))
    rows = driver.find_elements(By.TAG_NAME,"tr")
    for j in range(2,50):
        temp = rows[j].text
        #The injury tag changes the format of the text in the tag
        if temp.split('\n')[2] in ['Q','SSPD','O']:
            temp_data = temp.split('\n')[:2]
            temp_data.extend(temp.split('\n')[3:6])
        else:
            temp_data = temp.split('\n')[:5]
        adp.append(temp_data)
    #find and define the 'next' button
    path = "//button[@data-nav-item='"+str(i+2)+"']"
    buttons = driver.find_elements(By.XPATH,path )
    #press the button to go to the next page
    buttons[0].click()
    #wait for loading
    time.sleep(3)

df_adp = pd.DataFrame(adp,columns=['Rank','Player','Team','Pos','ADP'])
df_adp = df_adp[~df_adp['Pos'].isin(['K','D/ST'])]
df_adp.to_csv('adp_scrape.csv',index=False)
driver.close()

#Scrape Rankings

#Rankings scrape
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'}
page=requests.get(URL_rankings,headers=agent)
soup=BeautifulSoup(page.content,"html.parser")
rank_table = soup.table

#update date - make a column in the df
date = soup.find_all('p')[3].text.split(':')[1][1:]
print(date)
player_tbl = soup.find_all('p')[4:]
players = player_tbl[0].text.split('\n')

rankings = []
for player in players:
    temp_player = player
    temp_rank = {'rank':temp_player.split('.',1)[0],'player':(temp_player.split('.',1)[1][1:]).split(',')[0],'team':((temp_player.split('.',1)[1][1:]).split(',')[1][1:]).split(" ")[0],'pos':(((temp_player.split('.',1)[1][1:]).split(',')[1][1:]).split(" ")[1])[1:3],'pos_rank':(((temp_player.split('.',1)[1][1:]).split(',')[1][1:]).split(" ")[1])[3:-1]}
    rankings.append(temp_rank)

df_rankings = pd.DataFrame(rankings)
df_rankings.to_csv('ranking_scrape.csv',index=False)


#Projections Scrape
options = Options()
options.page_load_strategy = 'none'
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get(URL_proj)
time.sleep(2)



pages = [0,1,2,3,4,5]
proj = []
for i in pages:
    print("Running "+str(i))
    rows = driver.find_elements(By.TAG_NAME,"tr")
    for j in range(0,50):
        temp_player = rows[j*5+1].text
        print(temp_player)
        stats_2022 = rows[j*5+3].text
        proj_2023 = rows[j*5+4].text
        #Don't do kickers or defense
        if temp_player.split('\n')[1][-4:] == 'D/ST':
            pass
        elif temp_player.split('\n')[2][-1] == 'K':
            pass
        else:
            player = temp_player.split('\n')[:2]
            player.append(temp_player.split('\n')[2][-2:])
            player.append(temp_player.split('\n')[2][:-2])
            player.append(stats_2022.split('\n')[-1])
            player.append(proj_2023.split('\n')[-1])
            proj.append(player)
    #Example output
    #['1', 'Justin Jefferson', 'WR', 'Vikings', '368.66', '322.33']
    #Find, define, and click the next page button
    path = "//button[@data-nav-item='"+str(i+2)+"']"
    buttons = driver.find_elements(By.XPATH,path )
    buttons[0].click()
    time.sleep(3)

df_proj = pd.DataFrame(proj,columns=['Rank','Player','Pos','Team','2022 Stats','2023 Proj'])
df_proj.to_csv('proj_scrape.csv',index=False)
driver.close()
