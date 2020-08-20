from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime, date

csv_file1 = open("match_results.csv", "w")

csv_writer1 = csv.writer(csv_file1)
csv_writer1.writerow(["date", "team1",'result', 'team2'])

def diff_in_dates_in_days(date1, date2):
    return abs(date2-date1).days

source = requests.get("https://www.hltv.org/ranking/teams").text

soup = BeautifulSoup(source, "lxml")
teams=[]
for team in soup.find_all('div',{'class' : 'ranking-header'}):
    # rank=team.find('span').text
    # print(rank)

    teamname = team.find('span',{'class' : 'team-logo'}).find('img')['title']
    teams.append(teamname)
    if len(teams) == 10:
        break

source2=requests.get('https://www.hltv.org/results').text
soup2= BeautifulSoup(source2, "lxml")

for div in soup2.find_all("div", {'class':'big-results'}):
    div.decompose()


for result in soup2.find_all('div', {'class' : 'results-sublist'}):
    matchdate_string = result.span.text
    matchdate_simplified_string = matchdate_string[12:].replace("th", "").replace(" ", ",")
    format_str = "%B,%d,%Y"
    matchdate = datetime.strptime(matchdate_simplified_string,format_str)
    print(matchdate)
    for match_element in result.find_all('div', {'class': 'result'}):
        if diff_in_dates_in_days(matchdate, datetime.today()) <= 7:
            match_score = match_element.find('td', {'class': 'result-score'}).text.strip()
            match_team1 = match_element.find('div', {'class': 'line-align team1'}).text.strip()
            match_team2 = match_element.find('div', {'class': 'line-align team2'}).text.strip()
            full_match_info = "{} {} {}".format(match_team1,match_score,match_team2)
            # if match_team1 in teams or match_team2 in teams:
            if match_team2 in teams or match_team1 in teams:
                csv_writer1.writerow([matchdate,match_team1,match_score, match_team2])


source3=requests.get('https://www.hltv.org/results?offset=100').text
soup3= BeautifulSoup(source3, "lxml")

for result in soup3.find_all('div', {'class' : 'results-sublist'}):
    matchdate_string = result.span.text
    matchdate_simplified_string = matchdate_string[12:].replace("th", "").replace(" ", ",")
    format_str = "%B,%d,%Y"
    matchdate = datetime.strptime(matchdate_simplified_string,format_str)
    print(matchdate)
    for match_element in result.find_all('div', {'class': 'result'}):
        if diff_in_dates_in_days(matchdate, datetime.today()) <= 7:
            match_score = match_element.find('td', {'class': 'result-score'}).text.strip()
            match_team1 = match_element.find('div', {'class': 'line-align team1'}).text.strip()
            match_team2 = match_element.find('div', {'class': 'line-align team2'}).text.strip()
            full_match_info = "{} {} {}".format(match_team1,match_score,match_team2)
            # if match_team1 in teams or match_team2 in teams:
            if match_team2 in teams or match_team1 in teams:
                csv_writer1.writerow([matchdate,match_team1,match_score, match_team2])