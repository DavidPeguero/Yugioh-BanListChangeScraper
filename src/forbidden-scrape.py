import bs4 as bs
import urllib.request
from dataclasses import dataclass
import PySimpleGUI as sg
import requests as req
import re
from PIL import Image, ImageTk

api = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?name='
sg.set_options(
                font=('Arial', 12)
                )

sg.theme('black')

headers = {'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36')}



@dataclass
class card:
    type : str
    name : str
    advFormat : str
    tradFormat : str
    remarks : str

toprow = ['Type', 'Name', 'Advanced Format', 'Traditional Format', 'Remarks']
rows = []


def getCardTypes(soup, cardType, cardArray):
    count = 0
    cardContent = []
    for data in soup.select('.{}'.format(cardType)):
        count = 0
        cardContent.clear()
        for cardInfo in data.select('td'):
            cardContent.append(cardInfo.text)
            if(cardInfo.has_attr('colspan')):
                cardContent.append(cardInfo.text)
                count += 1
            count += 1
            if(count % 5 == 0 and count != 0):
                cardArray.append(card(cardContent[0], cardContent[1], cardContent[2], cardContent[3], cardContent[4]))

def populateList(url, rowArray):
    cArray = []
    rows.clear()
    try:
        sUrl = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        return e
    soup = bs.BeautifulSoup(sUrl,'lxml')
    getCardTypes(soup, 'cardlist_effect', cArray)
    getCardTypes(soup, 'cardlist_monster', cArray)
    getCardTypes(soup, 'cardlist_fusion', cArray)
    getCardTypes(soup, 'cardlist_synchro', cArray)
    getCardTypes(soup, 'cardlist_xyz', cArray)
    getCardTypes(soup, 'cardlist_link', cArray)
    getCardTypes(soup, 'cardlist_spell', cArray)
    getCardTypes(soup, 'cardlist_trap', cArray)

    for c in cArray:
        cName = re.sub('[\s]+'," ", c.name)
        cAdvFormat = re.sub('[\s]+'," ", c.advFormat)
        cTradFormat = re.sub('[\s]+'," ", c.tradFormat)
        cName = cName.replace(u"\u2013", "-")

        print(cName)
        rowArray.append([c.type, cName, cAdvFormat, cTradFormat, c.remarks])
    return 


populateList('https://www.yugioh-card.com/en/limited/list_12-01-2022/' , rows)

#Formatting the table 

#Creating the table with all the appropriate flags
tbl1 = sg.Table(values=rows, headings=toprow,
   auto_size_columns=True,
   max_col_width=40,
   display_row_numbers=False,
   justification='center', key='-TABLE-',
   background_color="black",
   selected_row_colors='white on blue',
   enable_events=True,
   enable_click_events=True,
   expand_x=True,
   expand_y=True,
)
    

#Buttons on UI
searchCard = sg.Button('Search')
updateList = sg.Button('Update')

#Set up layout of main window 
layout = [[sg.Input("Insert any official Konami Banlist. Hint: Use Wayback Machine for older banlists", size=(90, 1), key='-UPDATE-'), updateList],
    [sg.Input(size=(70, 1),key='-INPUT-'), searchCard]
    ,[tbl1]]

#Create window
window = sg.Window("Yugioh Forbidden/Limited List", layout, size=(1200, 800), resizable=True, finalize=True, icon=".\/assets\ygo_judgement.ico")
table = window['-TABLE-']
entry = window['-INPUT-']
update = window['-UPDATE-']
update.bind('<Button-1>', '+Click+')
entry.bind('<Return>', 'RETURN-')
table.bind('<Double-Button-1>', 'DOUBLE-')
table.bind('<Return>', 'RETURN-')


def openDescription(cardName):
    response = req.get(api + cardName)
    data = response.json()


    imageUrl = data['data'][0]['card_images'][0]['image_url']
    name =  data['data'][0]['name']

    urllib.request.urlretrieve(imageUrl, 'tempFile')

    img = Image.open('tempFile')

    image = ImageTk.PhotoImage(image=img)
    cardLayout = [
    [sg.Image(size=(421, 614), key='-IMAGE-')],
    ]
    cardWindow = sg.Window(name, cardLayout, resizable=True, finalize=True, icon=".\/assets\ygo_judgement.ico")
    cardWindow['-IMAGE-'].update(data = image)
    


placeHolder = True
while True:
    event, values = window.read()
    print("event:", event, "values:", values)
    if event == sg.WIN_CLOSED:
      break
   #On Update Logic
    if event in ('Update', '-UPDATE-RETURN-'):
       text = values['-UPDATE-'].lower()
       if(text == ''):
           continue
       populateList(text, rows)
       table.update(values=rows)
       
    #Searching logic
    if event in ('Search', '-INPUT-RETURN-'):
        text = values['-INPUT-'].lower()
        if text == '':
            continue
        row_colors = []
        for row, row_data in enumerate(rows):
            if text in row_data[0].lower() or text in row_data[1].lower() or  text in row_data[2].lower() or text in row_data[4].lower():
                row_colors.append((row, 'green'))
            else:
                row_colors.append((row, sg.theme_background_color()))
        table.update(row_colors=row_colors)

    #On selecting a element in the table it displays the card information
    if event == ('-TABLE-DOUBLE-') or event == ('-TABLE-RETURN-') :
       openDescription(rows[values['-TABLE-'][0]][1])

    if event == ('-UPDATE-+Click+') and placeHolder:
        placeHolder = False
        update.update('')
        
window.close()