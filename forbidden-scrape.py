from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import bs4 as bs
import pandas as pd
import urllib.request
from dataclasses import dataclass

@dataclass
class card:
    type : str
    name : str
    advFormat : str
    tradFormat : str
    remarks : str



source = urllib.request.urlopen('https://www.yugioh-card.com/en/limited/list_02-13-2023/').read()

soup = bs.BeautifulSoup(source,'lxml')

forbidden = soup.find_all("tr",class_="cardlist_effect")

cards = []
cardContent = []
count = 0


def getCardTypes(soup, cardType):
    count = 0
    for data in soup.select('.{}'.format(cardType)):
        count = 0
        cardContent.clear()
        for cardInfo in data.select('td'):
            print(count)
            print(cardInfo.text)
            cardContent.append(cardInfo.text)
            if(cardInfo.has_attr('colspan')):
                cardContent.append(cardInfo.text)
                count += 1
            count += 1
            if(count % 5 == 0 and count != 0):
                cards.append(card(cardContent[0], cardContent[1], cardContent[2], cardContent[3], cardContent[4]))

getCardTypes(soup, 'cardlist_effect')
getCardTypes(soup, 'cardlist_monster')
getCardTypes(soup, 'cardlist_fusion')
getCardTypes(soup, 'cardlist_synchro')
getCardTypes(soup, 'cardlist_xyz')
getCardTypes(soup, 'cardlist_link')
getCardTypes(soup, 'cardlist_spell')
getCardTypes(soup, 'cardlist_trap')
    


for c in cards:
    if(c.remarks.find("Was") != -1 or c.remarks.find("New") != -1):
        print(c.type)
        print(c.name)
        print(c.advFormat)
        print(c.tradFormat)
        print(c.remarks)
        print("\n")
        
