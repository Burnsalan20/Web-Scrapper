from functools import partial

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

from tkinter import *
from tkinter import ttk
from pandastable import Table
from PIL import Image, ImageTk
import json

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

config = {}

dataPath = "Scraper/"
def save_config():
    #Clear the config text file before writing new data to avoid double writing
    file = open(dataPath + 'config.txt', 'w').close()
    with open(dataPath + "config.txt", 'w') as file: 
        for key, value in config.items(): 
            file.write('%s:%s\n' % (key, value))

def create_or_open_config():
    with open(dataPath + "config.txt") as file:
        for line in file:
            (key, value) = line.split(':')
            config[key] = value


def isInitialLoad():
    return config['init_run']

iphoneFile = open(dataPath + "iphone_devices.txt", "r") #Loads iphone device links from txt file
iPhoneList = iphoneFile.readlines() #Reads all lines from iphone file

class iphoneDevice:
    def __init__(self, model, fair_price, good_price, excellent_price):
        self.model = model
        self.fair_price = fair_price
        self.good_price = good_price
        self.excellent_price = excellent_price
iphones = {}

class iphoneTradeIn:
    def __init__(self, model, price):
        self.model = model
        self.price = price

iphone_tradein = {}

samsungFile = open(dataPath + "samsung_devices.txt", "r") #Loads samsung device links from txt file
samsungList = samsungFile.readlines() #Reads all lines from samsung file

class samsungDevice:
    def __init__(self, model, fair_price, good_price, excellent_price):
        self.model = model
        self.fair_price = fair_price
        self.good_price = good_price
        self.excellent_price = excellent_price
samsungs = {}

class samsungTradeIn:
    def __init__(self, model, price):
        self.model = model
        self.price = price
samsung_tradein = {}

#Scrapes the website pages for device model names, and various prices of quality
def getGazelleDeviceData(url, isSamsung):
    driver.get(str(url))
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    name = soup.find('div', attrs={'class':'product-title'})
    nameChild = name.findChild("h1", href = False, recursive = False)

    fair_price = soup.find('label', attrs={'data-value':'Fair'})
    fair_price_child = fair_price.find('span', attrs={'class':'price discounted-price'})
 
    good_price = soup.find('label', attrs={'data-value':'Good'})
    good_price_child = good_price.find('span', attrs={'class':'price discounted-price'})

    excellent_price = soup.find('label', attrs={'data-value':'Excellent'})
    excellent_price_child = excellent_price.find('span', attrs={'class':'price discounted-price'})

    if isSamsung == False:
        iphones[nameChild.text.strip()] = [fair_price_child.text, good_price_child.text, excellent_price_child.text]
        #iphones.append(iphoneDevice(nameChild.text.strip(), fair_price_child.text, good_price_child.text, excellent_price_child.text))
    else:
        samsungs[nameChild.text.strip()] = [fair_price_child.text, good_price_child.text, excellent_price_child.text]
        #samsungs.append(iphoneDevice(nameChild.text.strip(), fair_price_child.text, good_price_child.text, excellent_price_child.text))
    
    print(nameChild.text.strip() + " " + fair_price_child.text + " " + good_price_child.text + " " + excellent_price_child.text)

def getAppleTradeInData(isSamsung):
    driver.get(str('https://www.apple.com/shop/trade-in?afid=p238%7Cs4wibFo6O-dc_mtid_1870765e38482_pcrid_607196296690_pgrid_80259604234_pntwk_g_pchan__pexid__&cid=aos-us-kwgo-brand--slid---product-'))
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    general_listings = soup.find_all('tbody', attrs={'class':'t-intro dd-semi'})

    if isSamsung is False:
        iphone_table_rows = general_listings[0].find_all('tr', recursive=False)
        for row in iphone_table_rows:
            cells = row.find_all(['th', 'td'], recursive=False)
            name = cells[0]
            price = cells[1]
            iphone_tradein[str(name.text)] = str(price.text).replace('Up to $', '$').strip()
            #iphone_tradein.append(iphoneTradeIn(str(name.text), str(price.text).replace('Up to $', '').strip()))
            print(str(name.text) + " $" + str(price.text).replace('Up to $', '$ ').strip())
    else:
        android_table_rows = general_listings[4].find_all('tr', recursive=False)
        for row in android_table_rows:
            cells = row.find_all(['th', 'td'], recursive=False)
            if len(cells) > 0:
                if 'Google' not in cells[0].text:
                    name = cells[0]
                    price = cells[1]
            samsung_tradein[str(name.text)] = str(price.text).replace('Up to $', '$').strip()
            #samsung_tradein.append(iphoneTradeIn(str(name.text), str(price.text).replace('Up to $', '').strip()))
            print(str(name.text) + " $" + str(price.text).replace('Up to $', '$').strip())


########## INITIALIZE DATA #################

def loadDataFromStart(canUpdate):
    global iphones, samsungs

    if canUpdate is True:
        if iphone_update:
            for index in range(len(iPhoneList)):
                getGazelleDeviceData(iPhoneList[index], False)

            json_file = json.dumps(iphones)
            file = open(dataPath + "gazelle_iphone.json","w")
            file.write(json_file)
            file.close()

        if samsung_update:
            for index in range(len(samsungList)):
                getGazelleDeviceData(samsungList[index], True)

            json_file = json.dumps(samsungs)
            file = open(dataPath + "gazelle_samsung.json","w")
            file.write(json_file)
            file.close()

        config['init_run'] = False
        save_config()
    else:
        with open(dataPath + 'gazelle_iphone.json', encoding='utf-8') as json_file:
            iphones = json.loads(json_file.read())

        with open(dataPath + 'gazelle_samsung.json', encoding='utf-8') as json_file:
            samsungs = json.loads(json_file.read())

    getAppleTradeInData(False)
    getAppleTradeInData(True)

create_or_open_config()
loadDataFromStart(config['init_run'])

root = Tk()


on = PhotoImage(file=dataPath + "on.png")
off = PhotoImage(file=dataPath + "off.png")

root.title('Device Pricing Data')
root.geometry("700x500")
root.resizable(0,0)

notebook = ttk.Notebook(root)
notebook.pack()

#Iphone toggle button Label
iphone_update = True
def toggle_iphone_update():
    global iphone_update
    if iphone_update:
        toggle_iphone_button.config(image=off)
        iphone_update_label.config(text="Iphone Data Update is disabled")
        iphone_update = False
    else:
        toggle_iphone_button.config(image=on)
        iphone_update_label.config(text="Iphone Data Update is enabled")
        iphone_update = True

#Samsung Update Toggle
samsung_update = True
def toggle_samsung_update():
    global samsung_update
    if samsung_update:
        toggle_samsung_button.config(image=off)
        samsung_update_label.config(text="Samsung Data Update is disabled")
        samsung_update = False
    else:
        toggle_samsung_button.config(image=on)
        samsung_update_label.config(text="Samsung Data Update is enabled")
        samsung_update = True

########## MAIN TAB WIDGETS BEGIN ##########
main_tab = Frame(notebook, width=700, height=500)
main_tab.pack(fill="both", expand=1)
notebook.add(main_tab, text="Main")

toggle_iphone_button = Button(main_tab, image=on, bd=0, command=toggle_iphone_update)
toggle_iphone_button.place(x=30, y=0)
iphone_update_label = Label(main_tab, text="Iphone Data Update is enabled", font=("Poppins bold", 13))
iphone_update_label.place(x=88, y=13)

toggle_samsung_button = Button(main_tab, image=on, bd=0, command=toggle_samsung_update)
toggle_samsung_button.place(x=30, y=50)
samsung_update_label = Label(main_tab, text="Samsung Data Update is enabled", font=("Poppins bold", 13))
samsung_update_label.place(x=88, y=63)

update_Button = Button(main_tab, text="Update Sheet", command=partial(loadDataFromStart, True), height=5, width=20)
update_Button.place(x=250, y=150)

########## MAIN TAB WIDGETS END ##########

########## Gazelle IPHONE TAB WIDGETS BEGIN ##########
iphone_tab = Frame(notebook, width=700, height=500)
iphone_tab.pack(fill="both", expand=1)
notebook.add(iphone_tab, text="Gazelle Iphone")

model_List = []
fair_List = []
good_List = []
excellent_List = []
for key, value in iphones.items():
    fair_price, good_price, excellent_price = value
    model_List.append(key)
    fair_List.append(fair_price)
    good_List.append(good_price)
    excellent_List.append(excellent_price)

iphoneDataFrame = pd.DataFrame({
    'Model': model_List,
    'Fair Price': fair_List,
    'Good Price': good_List,
    'Excellent Price': excellent_List,
})

iphone_tab_table = Table(iphone_tab, dataframe=iphoneDataFrame)
iphone_tab_table.show()
            
########## Gazelle IPHONE TAB WIDGETS END ##########

########## Gazelle SAMSUNG TAB WIDGETS BEGIN ##########
samsung_tab = Frame(notebook, width=700, height=500)
samsung_tab.pack(fill="both", expand=1)
notebook.add(samsung_tab, text="Gazelle Samsung")
    
model_List = []
fair_List = []
good_List = []
excellent_List = []
for key, value in samsungs.items():
    fair_price, good_price, excellent_price = value
    model_List.append(key)
    fair_List.append(fair_price)
    good_List.append(good_price)
    excellent_List.append(excellent_price)

samsungDataFrame = pd.DataFrame({
    'Model': model_List,
    'Fair Price': fair_List,
    'Good Price': good_List,
    'Excellent Price': excellent_List,
})

samsung_tab_table = Table(samsung_tab, dataframe=samsungDataFrame)
samsung_tab_table.show()

########## Gazelle SAMSUNG TAB WIDGETS END ##########

########## Iphone Tradein Tab Widget Begin ###########
iphone_tradein_tab = Frame(notebook, width=700, height=500)
iphone_tradein_tab.pack(fill="both", expand=1)
notebook.add(iphone_tradein_tab, text="Iphone Tradein")
    
model_List = []
price_List = []
for key, value in iphone_tradein.items():
    model_List.append(key)
    price_List.append(value)

iphonetradeinDataFrame = pd.DataFrame({
    'Model': model_List,
    'Price': price_List,
})

iphone_tradein_tab_table = Table(iphone_tradein_tab, dataframe=iphonetradeinDataFrame)
iphone_tradein_tab_table.show()

########## Iphone Tradein Tab Widget End #############

########## Samsung Tradein Tab Widget Begin ###########
samsung_tradein_tab = Frame(notebook, width=700, height=500)
samsung_tradein_tab.pack(fill="both", expand=1)
notebook.add(samsung_tradein_tab, text="Samsung Tradein")

model_List = []
price_List = []
for key, value in samsung_tradein.items():
    model_List.append(key)
    price_List.append(value)

samsungtradeinDataFrame = pd.DataFrame({
    'Model': model_List,
    'Price': price_List,
})

samsung_tradein_tab_table = Table(samsung_tradein_tab, dataframe=samsungtradeinDataFrame)
samsung_tradein_tab_table.show()

########## Samsung Tradein Tab Widget End #############

root.mainloop()