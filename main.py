import sys
sys.path.append('Libs')
sys.path.append('Services')
sys.path.append('Bot')
import DataLibrary as dl
import Indicators as ind
import TestBot as tb
from datetime import datetime, timedelta
import BinanceService as bs

def GetSymbolsAndIntervals():
    symbolList = []
    intervalList = []
    while True:
        symbol = input('İşleme alacağınız sembolleri girin. \nTüm sembolleri girdiğinizde boş olarak entere basın: ')
        if symbol == '':
            break
        else:
            symbolList.append(symbol)
    
    while True:
        interval = input('İşleme alacağınız intervalleri girin. \nTüm intervalleri girdiğinizde boş olarak entere basın: ')
        if interval == '':
            break
        else:
            intervalList.append(interval)
    
    return (symbolList, intervalList)

def ControlAndGenerateDataSource(_symbols, _intervals):
    for symbol in _symbols:
        for interval in _intervals:
            print(f'{symbol} için {interval} veri kaynağı kontrol ediliyor.')
            isDataOk = bs.ControlDataSource(symbol, interval)
            if isinstance(isDataOk, bool):
                if isDataOk:
                    print(f'{symbol} için {interval} veri kaynağı Ok.')
                    continue
                else :
                    print(f'{symbol} için {interval} veri kaynağı oluşturuluyor.')
                    _startDate = f'{datetime.now().day} {(datetime.now() - timedelta(days=120)).strftime("%B")} {datetime.now().year} 03:00'
                    _endDate = f'{datetime.now().day} {datetime.now().strftime("%B")} {datetime.now().year} {datetime.now().hour}:{datetime.now().minute}'
                    bs.GenerateOldDatas(symbol, [interval], _startDate, _endDate)
            else:
                print(f'{symbol} için {interval} veri kaynağı güncelleniyor.')
                _startDate = f'{isDataOk.OpenTime.day} {isDataOk.OpenTime.strftime("%B")} {isDataOk.OpenTime.year} {isDataOk.OpenTime.hour}:{isDataOk.OpenTime.minute}'
                _endDate = f'{datetime.now().day} {datetime.now().strftime("%B")} {datetime.now().year} {datetime.now().hour}:{datetime.now().minute}'
                bs.GenerateOldDatas(symbol, [interval], _startDate, _endDate)

def JoinDataSources(_symbols, _intervals):
    for symbol in _symbols:
        for interval in _intervals:
            print(f'{symbol} için {interval} veri kaynağına bağlanılıyor.')
            bs.JoinKlineSocket(symbol, interval)

(symbols, intervals) = GetSymbolsAndIntervals()
ControlAndGenerateDataSource(symbols, intervals)
JoinDataSources(symbols, intervals)
tb.BotSelector(['DCA'])

print('İşlem tamamlandı.')