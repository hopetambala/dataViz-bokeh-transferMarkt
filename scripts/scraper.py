import requests
import json
from bs4 import BeautifulSoup
import csv


BASEURL = 'https://www.transfermarkt.com/'

def loadJson(name):
    CACHE_FNAME = str(name) + '.json'
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {}
    return CACHE_DICTION

def getWhoScoredDataSoup(cacheName, specifier):
    baseurl = BASEURL

    page_url = baseurl + str(specifier)
    header = {'User-Agent': 'hope'}

    CACHE_DICTION = loadJson(str(cacheName))

    unique_ident = page_url

    if unique_ident in CACHE_DICTION:
        page_text = CACHE_DICTION[unique_ident]
    else:
        page_text = requests.get(page_url,headers=header).text #original
        CACHE_DICTION[unique_ident] = page_text
        dumped_json_cache = json.dumps(CACHE_DICTION,indent=4)
        fw = open(str(cacheName)+'.json',"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file


    page_soup = BeautifulSoup(page_text, 'html.parser')
    return page_soup

def getTeamsAndPlayers():

    leagues = [
        ('premierleague','premier-league/startseite/wettbewerb/GB1/saison_id/2018'),
        ('bundesliga','bundesliga/startseite/wettbewerb/L1/plus/?saison_id=2018'),
        ('laliga','laliga/startseite/wettbewerb/ES1/plus/?saison_id=2018'),
        ('ligue1','ligue-1/startseite/wettbewerb/FR1/plus/?saison_id=2018'),
        ('serieA',"serie-a/startseite/wettbewerb/IT1/plus/?saison_id=2018"),
        ('mls','major-league-soccer/startseite/wettbewerb/MLS1/plus/?saison_id=2017')

    ]
    #League Information loop
    list_of_leagues = []
    list_of_teams = []
    list_of_players = []
    for league in leagues:
        stats_soup = getWhoScoredDataSoup('leagues',league[1])
        
        league_info = stats_soup.find('div', class_='box-personeninfos')

        table_elements = league_info.find_all('td')

        '''
        Sample Data Structure
        First Tier -  United States
        23 teams
        672
        369 Players  54,9%
        773 Th. €
        Los Angeles Galaxy  7 time(s)
        26,5 Years
        New York Red Bulls
        Alphonso Davies  10,00 Mill. €
        '''

        league = []
        for table in table_elements: #Create table for leagues
            table_string = table.text
            table_stripped = table_string.strip(' \t\n\r')
            latin_stripped = table_stripped.replace(u'\xa0', u' ')
            league.append(latin_stripped)
            #print(table_stripped)
        list_of_leagues.append(league)   
        
        divs = stats_soup.find("div", id="yw1").find('tbody') #gets me the teams table so I can crawl further
        rows = divs.find_all('tr') #Team table rows on league page
        
        #Team Information Loop
        for row in rows:
            #Club Name
            img = row.find('img',alt=True)
            #club_name = img['alt']

            teams_info = row.find_all('td')


            team = []
            club_name = teams_info[1].text.strip(' \t\n\r\xa0') #for the player model
            team.append(teams_info[1].text.strip(' \t\n\r\xa0'))
            team.append(teams_info[2].text.strip(' \t\n\r\xa0'))
            team.append(teams_info[3].text.strip(' \t\n\r\xa0'))
            team.append(teams_info[4].text.strip(' \t\n\r\xa0'))
            team.append(teams_info[5].text.strip(' \t\n\r\xa0'))
            team.append(teams_info[6].text.strip(' \t\n\r\xa0'))
            team.append(teams_info[7].text.strip(' \t\n\r\xa0'))
            list_of_teams.append(team)
            '''
            for teams in teams_info:
                print(teams.text)
            '''

            #Club URL
            row_of_a= row.find_all('a', href = True,class_='vereinprofil_tooltip')
            first_element = row_of_a[0]
            
            urlExtension = first_element.get('href')


            #Search Through Each URL in the row of Teams to get Player Information
            clubs_soup = getWhoScoredDataSoup('teams',urlExtension[1:]) #removes extra comma
        
            team_divs = clubs_soup.find("div", id="yw1").find('tbody')

            team_rows_odd = team_divs.find_all('tr',class_='odd')
            team_rows_even = team_divs.find_all('tr',class_='even')
            team_rows = team_rows_even + team_rows_odd
            
            
            '''
            25
            Wilfred Ndidi
            Defensive Midfield
            Dec 16, 1996 (21)
            Nigeria
            Leicester City
            '''
            #Player Information Loop
            for row in team_rows: #player table rows on team page
                #print(row.find("td")) //prints some goodies
                player = []
                
                #Player Number
                #print(row.find('div',class_='rn_nummer').text)
                player.append(row.find('div',class_='rn_nummer').text)
                
                #Player Name
                #print(row.find('td',class_='hide').text)
                player.append(row.find('td',class_='hide').text)
                
                #Position
                all_trs = row.find('table',class_='inline-table').find_all('tr')
                position = all_trs[1].text
                #print(position)
                player.append(position)
                
                #Birthday
                #print(row.find_all('td',class_='zentriert')[1].text) 
                player.append(row.find_all('td',class_='zentriert')[1].text) 
                
                #Nationality
                #print(row.find('img',class_='flaggenrahmen')['alt'])
                player.append(row.find('img',class_='flaggenrahmen')['alt'])

                #Club
                #print(club_name)
                player.append(club_name)

                #Market Value
                player.append(row.find('td',class_='rechts hauptlink').text)

                list_of_players.append(player)
    
    return(list_of_leagues,list_of_players,list_of_teams)         
                
            
            
print('Start Crawl and Scrape')
leagues, players, teams = getTeamsAndPlayers()
print('Create CSV')
try:
    with open("leagues.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(leagues)
except KeyboardInterrupt:
    print('Exit')
except:
    print('Error')
    pass



try:
    with open("players.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(players)
except KeyboardInterrupt:
    print('Exit')
except:
    print('Error')

try:
    with open("teams.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(teams)
except KeyboardInterrupt:
    print('Exit')
except:
    print('Error')

print('Finish Creating CSV')