from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from datetime import datetime, timedelta
import csv
import pandas as pd
import os

apiKey = '61hHkO6ymn0745ITLx1PbTEqbOLfpcNw9SSaufLq6rV0MRlmoHz2GH4KyCcxzRrC'
apiSecret = 'RWBnHRWraNTxF5DZgeddqNtVXhjUmqsWjJxlzdR7UG56Nee02pzNDJCfr1KvDYEi'

symbolCount = 1
client = Client(apiKey, apiSecret)

def GetSymbolList(count, quoteAsset='USDT', sort = True):
    info = client.get_exchange_info()
    symbols = []
    
    # Önceden USDT olanları bir listeye al
    usdt_symbols = [item['symbol'] for item in info['symbols'] if item['quoteAsset'] == quoteAsset]

    # Alfabetik olarak sırala
    if sort:
        usdt_symbols = sorted(usdt_symbols)
    print(f'Found {len(usdt_symbols)} symbols with quote asset {quoteAsset}.')
    wait = input('Press enter to continue.')
    for symbol in usdt_symbols:
        if len(symbols) >= count and count != -1:
            break
        symbols.append(symbol)
    
    return symbols

def GetDatas(_symbol, _interval, _start, _end):
    klines = client.get_historical_klines(_symbol, _interval, _start, _end)
    return klines

def WriteCSV(_symbol, _interval, _start, _end):
    # Yıl ve ay bilgilerini elde edin
    start = datetime.strptime(_start, '%d %B %Y')
    end = datetime.strptime(_end, '%d %B %Y')
    year = start.year
    month = end.month

    # Klasör oluşturun
    directory = f"Data/{_symbol}/{_interval}"
    os.makedirs(directory, exist_ok=True)

    # Dosya adını oluşturun
    file_name = f"{directory}/{_symbol}_{_interval}_{year}_{month}.csv"
    
    # Eğer dosya zaten varsa, dosyayı tekrar oluşturma
    if os.path.exists(file_name) and not (month == datetime.now().month and year == datetime.now().year):
        print(f"File {file_name} already exists. Skipping.")
        return
    
    klines = GetDatas(_symbol, _interval, _start, _end)
    
    for kline in klines:
        kline[0] = datetime.fromtimestamp(kline[0] / 1000)
        kline[6] = datetime.fromtimestamp(kline[6] / 1000)
    
    # CSV dosyasını oluşturun ve yazın
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
        
        for kline in klines:
            writer.writerow([kline[0].strftime('%Y-%m-%d %H:%M:%S'), *kline[1:], kline[6].strftime('%Y-%m-%d %H:%M:%S')])
    print(file_name + ' done')

def CreateDataSource(symbols,  _startDate, _endDate, _intervals = ['1m', '3m', '5m', '15m', '30m', '45m', '1h', '2h', '3h', '4h', '1d', '1w', '1w', '1M']):
    timeRange = generate_date_ranges(_startDate, _endDate)
    for symbol in symbols:
        for _interval in _intervals:
            for start, end in timeRange:
                WriteCSV(symbol, _interval, start, end)

def ReadDataSource(_symbol, _interval, _lenght = 5):
    month = datetime.now().month
    year = datetime.now().year
    directory = f"Data/{_symbol}/{_interval}"
    fileList = []
    dfList = []
    for i in range(0, _lenght):
        fileList.append(f"{directory}/{_symbol}_{_interval}_{year}_{month}.csv")
        if not os.path.exists(fileList[i]):
            continue
        else:
            month -= 1
            if month == 0:
                month = 12
                year -= 1
    
    for fileName in fileList:
        if not os.path.exists(fileName):
            continue
        dfList.append(pd.read_csv(fileName))

    df = pd.concat(dfList, ignore_index=True)
    return df

def generate_date_ranges(start_date, end_date):
    start = datetime.strptime(start_date, '%d %B %Y')
    end = datetime.strptime(end_date, '%d %B %Y')
    
    current = start
    date_ranges = []

    while current <= end:
        next_month_first_day = datetime(current.year + (current.month // 12), ((current.month % 12) + 1), 1)
        last_day_of_current_month = next_month_first_day - timedelta(days=1)
        
        if last_day_of_current_month > end:
            last_day_of_current_month = end

        date_ranges.append((current.strftime('%d %B %Y'), last_day_of_current_month.strftime('%d %B %Y')))
        
        current = next_month_first_day
    
    return date_ranges