import requests
import robin_stocks
import json
import config
import robin_stocks.robinhood as r
from robin_stocks import *

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

loginRequest = r.login(config.username, config.password, expiresIn=86400,scope='internal', by_sms=True, store_session=True)
# loginRequest = r.login(config.username, config.password)

TOKEN = loginRequest['access_token']
profileRequest = r.profiles.load_portfolio_profile(info=None)
# print(profileRequest)
while 1:
    inputSymbols = input("Enter ticker (SPY):")
    if inputSymbols == "exit":
        break
    n = int(input("How many dates?: "))
    arr = str(input("Enter dates seperated by commas (2021-10-25, ...):"))   # takes the whole line of n numbers
    expirationDates = list(map(str,arr.split(','))) # split those numbers with space( becomes ['2','3','6','6','5']) and then map every element into int (becomes [2,3,6,6,5])
    # expirationDates = input('2021-10-25','2021-10-27','2021-10-30','2021-10-22']
    print(expirationDates)
    amountITM = 1
    volumeFloor = 50
    askMax = 100            #x100
    perc_change_max = 10        #of underlying
    percent_gain_wanted = 100

    # START OF NO TOUCHY ZONE


    for expirationDate in expirationDates:
        print("STARTING OPTION SEARCH FOR " + expirationDate)
        availableOptions = r.find_options_by_expiration(inputSymbols, expirationDate, optionType='both', info=None)
        jprint(availableOptions)
        if availableOptions != None:
            for d in availableOptions:
                ask_price = float(d['ask_price'])
                ask_size = int(d['ask_size'])
                break_even = float(d['break_even_price'])
                implied_volatility = d['implied_volatility']
                # last_trade_price = float(d['last_trade_price'])
                volume = int(d['volume'])
                strike_price = float(d['strike_price'])
                type = d['type']
                tradability = d['tradability']
                url = d['url']
                chain_symbol = d['chain_symbol']
                expiration_date = d['expiration_date']
                current_price_list = r.stocks.get_latest_price(chain_symbol, includeExtendedHours=True)
                current_price = float(current_price_list[0])
                if volume > volumeFloor:
                    if ask_price < askMax:
                            if type == 'call':
                                price_to_reach = strike_price + amountITM

                            if type == 'put':
                                price_to_reach = strike_price - amountITM


                            price_dif = price_to_reach - current_price
                            perc_change = price_dif/current_price
                            perc_gain = amountITM/ask_price
                            if(perc_gain > percent_gain_wanted/100):
                                if(abs(perc_change) < perc_change_max/100):
                                    print("")
                                    print(chain_symbol + " ", strike_price, " " + type + " x", ask_size, "Exp: " + expiration_date)
                                    print("Strike price:  ", strike_price)
                                    print("Current price: ", current_price)
                                    print("Ask:           ", ask_price)
                                    print("Ask Size:      ", ask_size)
                                    print("")
                                    print("Url: "+ url)
                                    print("")
                                    print("Price Difference between Strike and Actual: ", price_dif)
                                    print("Price to reach: ", price_to_reach)
                                    print("Percent change to get there", perc_change*100, "%")
                                    print("Percent gain $1 ITM", perc_gain*100, "%")
                                    print("")
                                    print("")
                                    print("")

# optionsRequest = robin_stocks.robinhood..options.get_list_market_data('SPY', expirationDate, info=None)
# option = robin_stocks.robinhood..options.get_option_market_data('SPY', expirationDate, , info=None)
# allOptions = robin_stocks.robinhood..options.get_market_options(info=None)
# jprint(allOptions)


# parameters = {  #http://api.open-notify.org/iss-pass.json?lat=40.71&lon=-74
#     "chain_id": "c277b118-58d9-4060-8dc5-a3b5898955cb", #SPY for testing
#     "issue_date": 2020-03-25
# }
# response = requests.get("https://api.robinhood.com/options/instruments/", params=parameters)
#
# jprint(response.json())
# results = response.json()
#


#alphanumeric id unique to Robinhood
# chainsymbols = []   #ticker symbols
# results = response.json()
#
# for d in results:
#     chain_ids = d['url']
#     chain_symbol = d['chain_symbol']
#     # print(chainsymbol)
#     chain_ids.append(url)
#     chainsymbols.append(chain_symbol)

# print(urls)
# print(chainsymbols)
# i = 0
# for chainSymbol in chainsymbols:
#     if chainSymbol == "SPY":
#         print("found spy")
#         print(url[i])
#     i += 1
# for newUrl in urls:
#     newResponse = requests.get(newUrl)
    # jprint(newResponse.json())
