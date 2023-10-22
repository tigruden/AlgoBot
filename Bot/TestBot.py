import DataLibrary as dl
import Indicators as ind
import pandas_ta as ta
import pandas as pd

def BotSelector(botNames : list, model : BurakStrategy_1_Model):
    for botName in botNames:
        if botName == 'BurakStrategy_1':
            BurakStrategy_1(model)

def DCA(_symbol, _interval):
    islemBasiDolar = 100
    alimSayisi = 0
    toplamCoin = 0
    komisyon = 0.001
    verilenKomisyon = 0

    df = dl.ReadDataSource(_symbol, _interval)
    open = df['Open']
    close = df['Close']
    high = df['High']
    low = df['Low']
    acilisZamani = df['Open time']
    sma50 = ta.sma(close, length=50)

    for i in range(0, len(close)):
        if pd.isna(sma50[i]) is False:
            if close[i] > sma50[i] and close[i-1] < sma50[i-1]:
                alimSayisi += 1
                toplamCoin += islemBasiDolar / close[i]
                verilenKomisyon += islemBasiDolar * komisyon
                islemBasiDolar -= islemBasiDolar * komisyon
                print('Alış yapıldı: ' + str(close[i]) + ' ' + str(acilisZamani[i]))
            elif close[i] < sma50[i] and close[i-1] > sma50[i-1]:
                islemBasiDolar += toplamCoin * close[i]
                toplamCoin = 0
                verilenKomisyon += islemBasiDolar * komisyon
                islemBasiDolar -= islemBasiDolar * komisyon
                print('Satış yapıldı: ' + str(close[i]) + ' ' + str(acilisZamani[i]))


def BurakStrategy_1(model):
    print(f'BurakStrategy_1 çalıştırılıyor. Başlangıç Tarihi: {model.start} Bitiş Tarihi: {model.end}')
    print('Coin Adı: ' + model.symbol)
    print('İşlem Aralığı: ' + model.interval)

    df = dl.ReadDataSource(model.symbol, model.interval, 100)
    close = df['Close']
    df1d = dl.ReadDataSource(model.symbol, '1d')
    close1d = df['Close']

    for i in range(0, len(close)):
        trend = ind.EMA3(model.symbol, '1d', 8, 34, 89)
        mavilimW = ind.MavilimW(model.symbol, model.interval, 3, 5)
        iftRSI = ind.IFTRSI(model.symbol, model.interval, 5, 9)
        atr = ta.atr(df['High'], df['Low'], df['Close'], length=14)
        CalcSL = df['Close'] - atr
        CalcTP = df['Close'] + atr
        longCondition = df['Close'] > mavilimW[0] and mavilimW[1] and trend == 'TrendUp' and iftRSI > 0.5
        shortCondition = df['Close'] < mavilimW[0] and mavilimW[2] and trend == 'TrendDown' and iftRSI < -0.5
        if longCondition:
            print('Long: ' + str(df['Close'][i]))
        elif shortCondition:
            print('Short: ' + str(df['Close'][i]))
        else:
            print('None: ' + str(df['Close'][i]))
    

    

    

class BurakStrategy_1_Model:
    def __init__(self, _symbol, _interval, _start, _end):
        self.symbol = _symbol
        self.interval = _interval
        self.start = _start
        self.end = _end