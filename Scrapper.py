from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

import gspread

import tkinter as tk
import PyPDF2
from PIL import Image, ImageTk

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

iphoneFile = open("iphone_devices.txt", "r") #Loads iphone device links from txt file
iPhoneList = iphoneFile.readlines() #Reads all lines from iphone file

class iphoneDevice:
    def __init__(self, model, fair_price, good_price, excellent_price):
        self.model = model
        self.fair_price = fair_price
        self.good_price = good_price
        self.excellent_price = fair_price
iphones = []

samsungFile = open("samsung_devices.txt", "r") #Loads samsung device links from txt file
samsungList = samsungFile.readlines() #Reads all lines from samsung file

class samsungDevice:
    def __init__(self, model, fair_price, good_price, excellent_price):
        self.model = model
        self.fair_price = fair_price
        self.good_price = good_price
        self.excellent_price = fair_price
samsungs = []

#Scrapes the website pages for device model names, and various prices of quality
def getDeviceData(url, isSamsung):
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
        iphones.append(iphoneDevice(nameChild.text.strip(), fair_price_child.text, good_price_child.text, excellent_price_child.text))
    else:
        samsungs.append(iphoneDevice(nameChild.text.strip(), fair_price_child.text, good_price_child.text, excellent_price_child.text))
    
    print(nameChild.text.strip() + " " + fair_price_child.text + " " + good_price_child.text + " " + excellent_price_child.text)

def updateSheets():
    #iterate through all the links and run getDeviceData to scrape the pages for data
    gc = gspread.service_account()
    sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1avy4rjsrkub1bpRlgeNGyQ9aCsqkSwV002T0yiKe4jg/edit#gid=0')
    
    for index in range(len(iPhoneList)):
        getDeviceData(iPhoneList[index], False)

    iphoneWorkSheet = sheet.worksheet("Iphone")
    for index in range(len(iphones)):
        iphoneWorkSheet.update('A' + str(2 + index), str(iphones[index].model)) #Device model
        iphoneWorkSheet.update('B' + str(2 + index), str(iphones[index].fair_price)) #Fair Condition Price
        iphoneWorkSheet.update('C' + str(2 + index), str(iphones[index].good_price)) #Good Condition Price
        iphoneWorkSheet.update('D' + str(2 + index), str(iphones[index].excellent_price)) #Excellent Condition Price

    for index in range(len(samsungList)):
        getDeviceData(samsungList[index], True)

    samsungWorkSheet = sheet.worksheet("Samsung")
    for index in range(len(samsungs)):
        samsungWorkSheet.update('A' + str(2 + index), str(samsungs[index].model)) #Device model
        samsungWorkSheet.update('B' + str(2 + index), str(samsungs[index].fair_price)) #Fair Condition Price
        samsungWorkSheet.update('C' + str(2 + index), str(samsungs[index].good_price)) #Good Condition Price
        samsungWorkSheet.update('D' + str(2 + index), str(samsungs[index].excellent_price)) #Excellent Condition Price

updateSheets()