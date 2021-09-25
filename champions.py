
import requests
import re
from bs4 import BeautifulSoup

def extractChampionName(string):
    return re.search('/lol/champions/(.*)/build', string).group(1) 

def writeChampionsListToCsv(soup):
    champions = {}
    ids = []
    championDivs = soup.find_all('a', {'class': 'champion-link'})
    championImages = soup.find_all('div', {'class': 'image-wrapper'})
    
    for champDiv in championDivs:
        name = extractChampionName(champDiv['href'])
        image = champDiv.find_all('div', {'class': 'image-wrapper'})[0].find('img')['src']
        champions[name] = image    

    with open('champions.csv', 'w') as csvfile:
        for champ in champions.keys():
             csvfile.write(champ+'\t'+champions[champ]+"\n")
       

def getRequestChampions(): # gather and parse all champions from champion.gg
    url = 'https://u.gg/lol/champions'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    writeChampionsListToCsv(soup)

getRequestChampions()