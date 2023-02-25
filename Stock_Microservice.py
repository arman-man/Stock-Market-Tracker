# === Web scraper microservice ===
import requests
from bs4 import BeautifulSoup
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


def getStockPrice(ticker: str):
    try:
        r = requests.get('https://www.marketwatch.com/investing/stock/' + ticker)
        soup = BeautifulSoup(r.text, 'html.parser')
        price = soup.select('h2 bg-quote')[0].text
        return str(price)
    except:
        return '-1'


if __name__ == '__main__':
    print('Microservice running...')
    while True:
        time.sleep(1)
        #  Wait for next request from client
        message = socket.recv()
        stockTicker = str(message.decode())

        #  Do some 'work'
        stockPrice = getStockPrice(stockTicker)

        #  Send reply to client
        socket.send_string(stockPrice)
