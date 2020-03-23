import requests
import robin_stocks
import json

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

loginRequest = robin_stocks.authentication.login(username='XXXXXXXXXX', password='XXXXXXXXXXXX', expiresIn=86400,scope='internal', by_sms=True, store_session=True)
TOKEN = loginRequest['access_token']
profileRequest = robin_stocks.profiles.load_portfolio_profile(info=None)
# print(profileRequest)

inputSymbols = ['SPY']
expirationDates = ['2020-03-25','2020-03-27','2020-03-30','2020-03-31']
amountITM = 1
volumeFloor = 50
askMax = .19            #x100
perc_change_max = 10        #of underlying
percent_gain_wanted = 100

# START OF NO TOUCHY ZONE


for expirationDate in expirationDates:
    print("STARTING OPTION SEARCH FOR " + expirationDate)
    availableOptions = robin_stocks.options.find_options_for_list_of_stocks_by_expiration_date(inputSymbols, expirationDate, optionType='both', info=None)
    # jprint(availableOptions)
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
            current_price_list = robin_stocks.stocks.get_latest_price(chain_symbol, includeExtendedHours=True)
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

# optionsRequest = robin_stocks.options.get_list_market_data('SPY', expirationDate, info=None)
# option = robin_stocks.options.get_option_market_data('SPY', expirationDate, , info=None)
# allOptions = robin_stocks.options.get_market_options(info=None)
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
