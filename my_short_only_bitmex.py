import ccxt
import os
import sys
import numpy as np
import time
from datetime import datetime


root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

exchange = ccxt.bitmex({'apiKey':'','secret':'','enableRateLimit': True,'timeout': 60000})
if 'test' in exchange.urls:
    exchange.urls['api'] = exchange.urls['test'] # ←----- switch the base URL to testnet
print(exchange.fetch_balance())
###################################################################### Telegram

#BOT_TOKEN=''
#CHAT_ID_GC= ''

#################################################################### Functions
symbol = 'BTC/USD'
symbol_single='BTC'

timeframe = '1m'
tf=1
layer_number = 40
updis_1=10

all_order_ids=[]
all_order_id_sold = []
all_order_id_bought = []


######################## Resistance Price

res_1=9150


money_res_1=2000


####################### Support Price






ch_up1_j = np.zeros(layer_number)



############################# Profits


profit=10

############################################################################
######################## Resistance Price LEVEL1

up1_j = np.arange(res_1, res_1+layer_number*updis_1, updis_1)


money_up1_j = np.full((1, layer_number), money_res_1/layer_number)[0]




###################################################################### Constants

params = {'partial': False}

limit = 5
k=0
kp=0
index_check=0
tool=0

amount_long=0
amount_short=0

id_up1_j = np.full((1, layer_number), 0)



################################

order_up1_j = np.zeros(layer_number)



#################################################################
order_up1_j = [None] * layer_number




id_up1_j = [None] * layer_number




ch_up1_j = [1] * layer_number


################################################################# First Ordering

since = exchange.milliseconds() - limit * 60 * 1000 * tf
cl = exchange.fetch_ohlcv(symbol, timeframe, since, limit+1, params)
candles=[]
tool_can=len(cl)
online_price=cl[-1][-2]
time_start=cl[-1][0]
time_start_st=datetime.utcfromtimestamp(int(time_start/1000)).strftime('%Y-%m-%d %H:%M:%S')
print('Time Start:',time_start_st,'Time Stamp:',time_start)




################################################################################
##################################################################### SHORT LEV1
for j, x in enumerate(up1_j):
        if online_price<x:
            try:
                print(money_up1_j[j])

                order_up1_j[j] = exchange.createLimitSellOrder(symbol,money_up1_j[j],int(x))
                id_up1_j[j]=order_up1_j[j]['id']

                ch_up1_j[j]=0
                print('SHORT ORDER PLACED LEV1-',j+1,' ======> ','amount:',money_up1_j[j],'Price:',int(x))
                time.sleep(4)
            except Exception as e:
                print(e)
                print('*** ORDER SHORT LEV1-',j+1, "FETCH ERROR . . . ***")
                ch_up1_j[j]=1
                time.sleep(4)
        else:
            ch_up1_j[j]=1
            time.sleep(0.5)

time.sleep(1)



##################################################
while True:

    try:

                since = exchange.milliseconds() - limit * 60 * 1000 * tf


                try:
                    cl = exchange.fetch_ohlcv(symbol, timeframe, since, limit+1, params)

                except:
                    time.sleep(2)



                candles=[]
                tool_can=len(cl)

                online_price=cl[-1][-2]

                time.sleep(10)
                print('server on')



                fetchMyTrades_check=exchange.fetchClosedOrders(symbol,since)
                #print('fetchMyTrades_check:')
                #print(fetchMyTrades_check)
                order_id_dict= {}

                for x in fetchMyTrades_check:

                   #print(x['info']['ordStatus'])
                   #print(x['info']['side'])
                   all_order_ids.append(x['info']['orderID'])
                   #print(x['info']['orderID'])
                   #print(x)

                   if x['info']['ordStatus']=='Filled' and x['info']['side']=='Sell' and x['info']['orderID'] not in all_order_id_sold:
                       order_id = x['info']['orderID']
                       all_order_id_sold.append(order_id)
                       #print(all_order_id_sold)

                       buy_qty = x['info']['orderQty']
                       buy_price = x['info']['price']- profit
                       #print('ddddd')


                       order = exchange.createLimitBuyOrder(symbol,buy_qty,buy_price)
                       print('LONG ORDER PLACED amount:',buy_qty,'@:',buy_price)
                       #print(all_order_id_sold)



                   if x['info']['ordStatus']=='Filled' and x['info']['side']=='Buy' and x['info']['orderID'] not in all_order_id_bought:
                       buy_qty = x['info']['orderQty']
                       buy_price = x['info']['price']+ profit
                       order = exchange.createLimitSellOrder(symbol,buy_qty,buy_price)
                       order_id = x['info']['orderID']
                       all_order_id_bought.append(order_id)
                       print('SHORT ORDER PLACED amount:',buy_qty,'@:',buy_price)


    except:

        print('server offline')
