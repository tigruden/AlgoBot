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

def TwmStart():
    twmStatus = twm.is_alive()
    if twmStatus:
        print('Twm is already started.')
        return
    twm.start()

def TwmStop():
    twmStatus = twm.is_alive()
    if not twmStatus:
        print('Twm is already stopped.')
        return
    twm.stop()

def tdcmStart():
    tdcmStatus = tdcm.is_alive()
    if tdcmStatus:
        print('Tdcm is already started.')
        return
    tdcm.start()

def tdcmStop():
    tdcmStatus = tdcm.is_alive()
    if not tdcmStatus:
        print('Tdcm is already stopped.')
        return
    tdcm.stop()

def JoinKlineSocket(symbol, interval: str):
    twm.start()
    twm.start_kline_socket(callback = handle_socket_message, symbol = symbol, interval = interval)
    twm.join()

def handle_socket_message(msg):
    global oldKline
    symbol = msg['s']
    interval = msg['k']['i']
    kline = mp.SocketKlineToBinanceKlineMapper(msg)
    
    print(kline)
    if oldKline != None:
        if oldKline.OpenTime == kline.OpenTime:
            oldKline = kline
            return
    else:
        oldKline = kline
        return

    print(f'Inserting {symbol} {interval} data.')
    kr.GenericMongoRepository(exchange, symbol, interval, bk.Kline).InsertMany(kline)
    oldKline = kline

def GenerateOldDatas(_symbol : str, _interval : list, _startDate, _endDate):
    for interval in _interval:
        dateRange = generate_date_ranges(_startDate, _endDate, timedelta(days=1))
        for start, end in dateRange:
            print(f'Getting {_symbol}-{interval} data from {start} to {end}.')
            klines = client.get_historical_klines(_symbol, interval, start, end)
            if len(klines) == 0:
                continue
            kline = mp.HistoricalKlinesToBinanceKlineMapper(klines)
            kr.GenericMongoRepository(exchange, _symbol, interval, bk.BaseModel).InsertMany(kline)

def ControlDataSource(_symbol : str, _interval : str):
    lastData = GetLastData(_symbol, _interval)
    if lastData == None:
        return False
    elif lastData.OpenTime != datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute):
        return lastData
    else:
        return True
    

def generate_date_ranges(start_date, end_date, _interval : str):
    return_as_str = False
    delta = CalculateDeltaTime(_interval)
    if isinstance(start_date, str):
        start = datetime.strptime(start_date, '%d %B %Y %H:%M')
        return_as_str = True
    else:
        start = start_date

    if isinstance(end_date, str):
        end = datetime.strptime(end_date, '%d %B %Y %H:%M')
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
                date_ranges.append((current.strftime('%d %B %Y %H:%M'), next_date.strftime('%d %B %Y %H:%M')))
            else:
                date_ranges.append((current, next_date))
            break


        if return_as_str:
            date_ranges.append((current.strftime('%d %B %Y %H:%M'), next_date.strftime('%d %B %Y %H:%M')))
        else:
            date_ranges.append((current, next_date))

        current = next_date

    return date_ranges

def GetLastData(_symbol, _interval):
    return kr.GenericMongoRepository(exchange, _symbol, _interval, bk.Kline).GetLastKline()

def GetLastDataWithDate(_symbol, _interval, _startDate, _endDate):
    return kr.GenericMongoRepository(exchange, _symbol, _interval, bk.Kline).GetDataWithDate(_startDate, _endDate)
    
def CalculateDeltaTime(_interval : str):
    if _interval == '1m':
        return timedelta(days=1)
    elif _interval == '3m':
        return timedelta(days=3)
    elif _interval == '5m':
        return timedelta(days=7)
    elif _interval == '15m':
        return timedelta(days=15)
    elif _interval == '30m':
        return timedelta(days=30)
    elif _interval == '45m':
        return timedelta(days=30)
    elif _interval == '1h':
        return timedelta(days=30)
    elif _interval == '2h':
        return timedelta(days=60)
    elif _interval == '3h':
        return timedelta(days=90)
    elif _interval == '4h':
        return timedelta(days=120)
    elif _interval == '1d':
        return timedelta(days=365)
    elif _interval == '1w':
        return timedelta(days=365)
    elif _interval == '1M':
        return timedelta(days=365)
    else:
        return timedelta(days=30)

