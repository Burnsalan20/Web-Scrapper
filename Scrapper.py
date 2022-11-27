from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

import json

import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SHEETS_READ_WRITE_SCOPE = 'https://www.googleapis.com/auth/spreadsheets'
SCOPES = [SHEETS_READ_WRITE_SCOPE]

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

iphoneFile = open("iphone_devices.txt", "r") #Loads iphone device links from txt file
samsungFile = open("samsung_devices.txt", "r") #Loads samsung device links from txt file

iPhoneList = iphoneFile.readlines() #Reads all lines from iphone file
samsungList = samsungFile.readlines() #Reads all lines from samsung file

products=[] #List to store name of the product
fair_prices=[] #List to store fair price of the product
good_prices=[] #List to store good price of the product
excellent_prices=[] #List to store excellent price of the product

def getDeviceData(url):
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

    products.append(nameChild.text.strip())
    fair_prices.append(fair_price_child.text)
    good_prices.append(good_price_child.text)
    excellent_prices.append(excellent_price_child.text)

    print(nameChild.text.strip() + " " + fair_price_child.text + " " + good_price_child.text + " " + excellent_price_child.text)

for x in range(len(iPhoneList)):
    getDeviceData(iPhoneList[x])

def main():
    spreadsheet_id = '1avy4rjsrkub1bpRlgeNGyQ9aCsqkSwV002T0yiKe4jg'  # this is part of the url of google
    rows = [
        ["IPhone Device", "Fair Price", "Good Price", "Excellent Price"],
    ]

    for index in range(len(iPhoneList)):
        device = [str(products[index]), str(fair_prices[index]), str(good_prices[index]), str(excellent_prices[index])]
        rows.append(device)

    # -----------

    credentials = get_or_create_credentials(scopes=SCOPES)  # or use GoogleCredentials.get_application_default()
    service = build('sheets', 'v4', credentials=credentials)
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="Sheet1!A:Z",
        body={
            "majorDimension": "ROWS",
            "values": rows
        },
        valueInputOption="USER_ENTERED"
    ).execute()

# Source: https://developers.google.com/sheets/api/quickstart/python
def get_or_create_credentials(scopes):
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
            credentials = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    return credentials


if __name__ == '__main__':
    main()