import sys
sys.path.append('Libs')
sys.path.append('Repository')
sys.path.append('Models')

import json
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from datetime import datetime, timedelta
import KlineRepository as kr
import Mapper as mp
import BinanceKline as bk

with open('Config/config.json', 'r') as f:
    config = json.load(f)

apiKey = config['Exchange']['Binance']['ApiKey']
apiSecret = config['Exchange']['Binance']['ApiSecret']
client = Client(apiKey, apiSecret)
twm = ThreadedWebsocketManager(apiKey, apiSecret)
twm.start()
tdcm = ThreadedDepthCacheManager(apiKey, apiSecret)
exchange = 'Binance'
oldKline = None

def GetSymbolList(count, quoteAsset='USDT', sort = True):
    info = client.get_exchange_info()
    symbols = []
    
    # Önceden USDT olanları bir listeye al
    usdt_symbols = [item['symbol'] for item in info['symbols'] if item['quoteAsset'] == quoteAsset]

    # Alfabetik olarak sırala
    if sort:
        usdt_symbols = sorted(usdt_symbols)

    for symbol in usdt_symbols:
        if len(symbols) >= count and count != -1:
            break
        symbols.append(symbol)
    
    return symbols

def JoinKlineSocket(symbol, interval: str):
    twm.start_kline_socket(callback = handle_socket_message, symbol = symbol, interval = interval)
    twm.join()

def handle_socket_message(msg):
    symbol = msg['s']
    interval = msg['k']['i']
    kline = mp.SocketKlineToBinanceKlineMapper(msg)
    
    print(kline)
    if oldKline != None:
        if oldKline.OpenTime == kline.OpenTime:
            oldKline = kline
            return

    print(f'Inserting {symbol} {interval} data.')
    #kr.GenericMongoRepository(exchange, symbol, interval, bk.Kline).InsertMany(kline)

def GenerateOldDatas(_symbol : str, _interval : list, _startDate : str, _endDate : str):
    dateRange = generate_date_ranges(_startDate, _endDate)
    for start, end in dateRange:
        print(f'Getting {_symbol} data from {start} to {end}.')
        for index, interval in enumerate(_interval):
            print(f'Getting {len(_interval)} of {index + 1} data.')
            klines = client.get_historical_klines(_symbol, interval, start, end)
            if len(klines) == 0:
                continue
            kline = mp.HistoricalKlinesToBinanceKlineMapper(klines, _symbol, interval, exchange)
            kr.GenericMongoRepository(exchange, _symbol, interval, bk.BaseModel).InsertMany(kline)

def generate_date_ranges(start_date, end_date, delta=timedelta(days=30)):
    return_as_str = False

    if isinstance(start_date, str):
        start = datetime.strptime(start_date, '%d %B %Y')
        return_as_str = True
    else:
        start = start_date

    if isinstance(end_date, str):
        end = datetime.strptime(end_date, '%d %B %Y')
        return_as_str = True
    else:
        end = end_date

    current = start
    date_ranges = []

    while current <= end:
        next_date = current + delta
        if next_date > end:
            next_date = end
            if return_as_str:
                date_ranges.append((current.strftime('%d %B %Y'), next_date.strftime('%d %B %Y')))
            else:
                date_ranges.append((current, next_date))
            break


        if return_as_str:
            date_ranges.append((current.strftime('%d %B %Y'), next_date.strftime('%d %B %Y')))
        else:
            date_ranges.append((current, next_date))

        current = next_date

    return date_ranges

def GetLastData(_symbol, _interval):
    return kr.GenericMongoRepository(exchange, _symbol, _interval, bk.Kline).GetLastKline()

def GetLastDataWithDate(_symbol, _interval, _startDate, _endDate):
    return kr.GenericMongoRepository(exchange, _symbol, _interval, bk.Kline).GetDataWithDate(_startDate, _endDate)
    


