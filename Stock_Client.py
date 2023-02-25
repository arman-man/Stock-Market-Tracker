import pymsgbox  # Alert pop-up
import zmq  # Async Messaging Library
from clint.textui import colored, progress  # CLI text
from pyfiglet import Figlet  # CLI title
import time
from threading import Thread

# == Color scheme ==
# Yellow for title
# Green for menus
# Cyan for prompts
# Red for responses
# White for loading/processes/user-input

run_loop = True

context = zmq.Context()
#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


def stock_service_request(stockTicker):
    socket.send_string(stockTicker)

    #  Get the reply.
    message = socket.recv()

    stockPrice = str(message.decode())
    return stockPrice


def trigger_alert(stockTicker, alertPrice):
    print('\r' + '                                        ')
    print(colored.red(
        'ALERT! ' + stockTicker + ' has reached $ ' + str(alertPrice)))

    pymsgbox.alert(stockTicker + ' has reached $ ' + str(alertPrice), 'Stock alert '
                                                                      'triggered!')

    print(colored.cyan('\nEnter \'3\' to return to main menu:\n>'), end='')


def stock_price_script(stockTicker, alertPrice):
    global run_loop
    stockPrice = stock_service_request(stockTicker)
    initialAlertPrice = float(alertPrice)
    initialStockPrice = float(stockPrice)

    if initialStockPrice != initialAlertPrice:
        alertStatus = True
        print('\nTracking ' + stockTicker + '...')
        while alertStatus is True and run_loop is True:
            time.sleep(3)
            stockPrice = stock_service_request(stockTicker)

            if run_loop is True:
                print('\r' + stockPrice + (' ' * 35))
                print(colored.cyan('Enter \'3\' to return to main menu >'), flush=True, end='')

            if initialStockPrice < initialAlertPrice:
                if float(stockPrice) >= float(alertPrice):
                    trigger_alert(stockTicker, alertPrice)
                    run_loop = False
                    alertStatus = False
            else:
                if float(stockPrice) <= float(alertPrice):
                    trigger_alert(stockTicker, alertPrice)
                    run_loop = False
                    alertStatus = False
    else:
        print('\nTracking ' + stockTicker + '...')
        print('\r' + stockPrice + (' ' * 35))
        print(colored.cyan('Enter \'3\' to return to main menu >'), flush=True, end='')
        if run_loop is True:
            trigger_alert(stockTicker, alertPrice)
            run_loop = False


def input_script():
    global run_loop
    while run_loop is True:
        userInput = input()
        if run_loop is True:
            if userInput == '3':
                run_loop = False
            else:
                print(colored.red('\nInvalid input.'))
                print(colored.cyan('\nEnter \'3\' to return to main menu >'), end='')


def start_scripts(stockTicker, alertPrice):
    t1 = Thread(target=stock_price_script, args=(stockTicker, alertPrice))
    t1.start()

    t2 = Thread(target=input_script)
    t2.start()

    while run_loop is True:
        pass

    t1.join()
    t2.join()


if __name__ == "__main__":
    menuInput = ''
    print('\n')
    print(colored.yellow(Figlet(font='slant').renderText('Stock Market Tracker')))
    menuSpacing = False  # Makes the first menu display closer to the Figlet banner
    while menuInput != '3':
        if menuSpacing is False:
            print(colored.green('1) Track a stock'))
        else:
            print(colored.green('\n\n\n1) Track a stock'))
        print(colored.green('2) Look up a stock'))
        print(colored.green('3) Exit'))

        print(colored.cyan('\nSelect an option:\n>'), end='')
        menuInput = input()

        if menuInput == '1':
            print(colored.cyan('\nEnter a stock to track:\n>'), end='')
            stockTicker = input().upper()

            stockPrice = stock_service_request(stockTicker)

            print()
            for i in progress.mill(range(100), label='Loading...'):
                time.sleep(3 / 100)

            # This means the stock exists
            if stockPrice != '-1':
                print('Success!')
                print(colored.red('\n' + stockTicker + ' $ ' + stockPrice))
                print(colored.cyan('\nEnter price for alert:\n>'), end='')
                alertPrice = input()

                validAlertPrice = False
                try:
                    alertPrice = float(alertPrice)
                    validAlertPrice = True
                except:
                    pass

                if validAlertPrice is True:
                    run_loop = True
                    start_scripts(stockTicker, alertPrice)

                else:
                    print(colored.red('\nInvalid price value.'))

            else:
                print(colored.red('\nInvalid stock ticker.'))

        elif menuInput == '2':
            print(colored.cyan('\nEnter a stock to look up:\n>'), end='')
            stockTicker = input().upper()

            stockPrice = stock_service_request(stockTicker)

            print()
            for i in progress.mill(range(100), label='Loading...'):
                time.sleep(3 / 100)

            # This means the stock exists
            if stockPrice != '-1':
                print('Success!')
                print(colored.red('\n' + stockTicker + ' $ ' + stockPrice))
            else:
                print(colored.red('\nInvalid stock ticker.'))

        elif menuInput != '3':
            print(colored.red('\nInvalid menu selection.'))

        else:
            print(colored.red('\nExited successfully.\n\n'))

        menuSpacing = True
