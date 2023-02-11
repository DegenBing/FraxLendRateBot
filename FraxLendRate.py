#author : DegenBing
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests

############ vars #################

bot_token = sys.argv[1]
bot_chatID = '@FraxLendRate'

def telegram_bot_sendtext(bot_message):

   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

   response = requests.get(send_text)

   return response.json()

def getNameAndLendRate(tableRow):
    return(tableRow[0].div.div.div.text, tableRow[7].div.div.span.text)

def getFraxLendRate():
    driver = webdriver.Firefox()
    driver.get('https://app.frax.finance/fraxlend/available-pairs')
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html)
    data = {}
    allTable = soup.find("div", class_="frax-Table-body").findAll("div", class_="frax-Table-row")
    for row in allTable:
        allCellinRow = row.findAll("div", class_="frax-Table-cell")
        rawData = getNameAndLendRate(allCellinRow)
        data[rawData[0]] = rawData[1]
    return data

def updateFraxLendRate():
    tgMsg = ""
    datas = getFraxLendRate()
    sort_data = sorted(datas.items(), key=lambda x: x[1], reverse=True)
    for data in sort_data:
        tgMsg += (str(data[0]+" "+str(data[1])+"\n"))
    telegram_bot_sendtext(tgMsg)

#alert when bot start
telegram_bot_sendtext("Bot Reboot")

while True:
    try:
        updateFraxLendRate()
        #30min
        time.sleep(1800) 
    except Exception as e:
        telegram_bot_sendtext(str(e))
        time.sleep(30)