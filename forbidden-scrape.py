from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import bs4 as bs
import pandas as pd
import urllib.request
from dataclasses import dataclass
import PySimpleGUI as sg

sg.theme('amber')


layout = [[sg.Text("Somethin")],
          [sg.Text("Somethin else"), sg.Input()],
          [sg.Button("wut"), sg.Button("cancel")]]

window = sg.Window('Yugioh - Forbidden/Limited Cards', layout)

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

toprow = ['Type', 'Name', 'Advanced Format', 'Traditional Format', 'Remarks']
rows = []
for idx, c in enumerate(cards):
    rows.append([c.type, c.name, c.advFormat, c.tradFormat, c.remarks])



tbl1 = sg.Table(values=rows, headings=toprow,
   auto_size_columns=True,
   display_row_numbers=False,
   justification='center', key='-TABLE-',
   selected_row_colors='black on white',
   enable_events=True,
   expand_x=True,
   expand_y=True,
)
    


# for c in cards:
#     if(c.remarks.find("Was") != -1 or c.remarks.find("New") != -1):
#         print(c.type)
#         print(c.name)
#         print(c.advFormat)
#         print(c.tradFormat)
#         print(c.remarks)
#         print("\n")
        
layout = [[tbl1]]
window = sg.Window("Yugioh Forbidden/Limited List", layout, size=(715, 200), resizable=True)
while True:
   event, values = window.read()
   print("event:", event, "values:", values)
   if event == sg.WIN_CLOSED:
      break
   if '+CLICKED+' in event:
      sg.popup("You clicked row:{} Column: {}".format(event[2][0], event[2][1]))
window.close()