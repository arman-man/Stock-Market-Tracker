# === Web scraper microservice ===
import requests
from bs4 import BeautifulSoup
import time


def main():
    while True:
        time.sleep(1)
        line = readFile()
        price = getStockPrice(line)
        writeFile(price)


def getStockPrice(ticker: str):
    try:
        r = requests.get('https://www.marketwatch.com/investing/stock/' + ticker)
        soup = BeautifulSoup(r.text, 'html.parser')
        price = soup.select('h2 bg-quote')[0].text
        return str(price)
    except:
        return '-1'


def readFile():
    # Open the txt file in read mode
    file = open('C:\\Users\\amanu\\OneDrive\\Documents\\Programming '
                'Projects\\Stock-Market-Tracker\\stock_service_ticker.txt', 'rt')
    # Save the first line in the txt file, which should be a stock ticker
    tempVar = file.readline()
    file.close()
    return tempVar


def writeFile(price: str):
    # Re-open txt file in write mode
    file = open('C:\\Users\\amanu\\OneDrive\\Documents\\Programming '
                'Projects\\Stock-Market-Tracker\\stock_service_price.txt', 'wt')
    # Generate stock price or '-1' and save to txt file
    file.write(price)
    file.close()


main()
