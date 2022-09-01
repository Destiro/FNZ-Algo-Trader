## FNZ API - HELP: https://fnz-mock-market-av77i2f25a-ew.a.run.app/help
## Mock stock market: https://fnz-mock-market-av77i2f25a-ew.a.run.app/

from collections import deque

import requests

TICKERS = ['FNZ', 'NZX50', 'SNAPPER', 'XERO', 'RLAB']
URL = 'https://fnz-mock-market-av77i2f25a-ew.a.run.app/'
account_id = '2872ad75-c343-4108-810a-559b9422b224'
long_term = deque()
short_term = deque()

""" API Handlers """
def buy(ticker, amount, account_id):
    return requests.post(URL + f'/order/buy/{ticker}?id={account_id}&amount={amount}').json()


def sell(ticker, amount, account_id):
    return requests.post(URL + f'/order/sell/{ticker}?id={account_id}&amount={amount}').json()


def get_curent_prices():
    return requests.get(URL + '/get_latest_prices').json()


def create_account(name):
    return requests.post(URL + f'/account?name={name}').json()


def get_account(account_id):
    return requests.post(URL + f'/account?id={account_id}').json()


def get_current_holdings(account_id):
    return requests.get(URL + f'/holdings?id={account_id}').json()


def get_averages(list, ticker):
    average = 0

    for item in list:
        average += item['prices'][ticker]['price']
    return average / len(list)


""" Runs the Script """
if __name__ == '__main__':

    # Create an account - Uncomment to create account
    account = create_account(name='TempName')
    account_id = account['id']
    print(f'Your account Id (Do not lose this): {account_id}')

    # Buy evenly (5 stocks -> 100k bal)
    for ticker in TICKERS:
        buy(ticker, 19500, account_id)

    while True:
        prices = get_curent_prices()

        # Keep record of current stock price
        short_term.append(prices)
        if len(short_term) > 20:  # Only take last 20 reads
            short_term.popleft()

        # Keep record of intrinsic value
        long_term.append(prices)
        if len(long_term) > 200:  # Only take last 200 reads
            long_term.popleft()

        print("Curr holdings: " + str(get_current_holdings(account_id)))

        for ticker in TICKERS:
            if get_averages(long_term, ticker) < get_averages(short_term, ticker):  # Value over intrinsic -> Sell
                sell(ticker, prices['prices'][ticker]['price'] / 100, account_id)
                print("sold:" + ticker + ": " + str(prices['prices'][ticker]['price'] / 100))

            elif get_averages(short_term, ticker) < get_averages(long_term, ticker):  # Value under intrinsic -> Buy
                buy(ticker, prices['prices'][ticker]['price'] / 100, account_id)
                print("bought:" + ticker + ": " + str(prices['prices'][ticker]['price'] / 100))
