import DataLibrary as dl
import Indicators as ind
import pandas_ta as ta
import pandas as pd

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

    print('Coin Adı: ' + str(toplamCoin))
    print('Toplam Yapılan İşlem: ' + str(toplamCoin))
    print('Toplam Alınan Coin: ' + str(toplamCoin))
    print('Toplam Verilen Komisyon: ' + str(verilenKomisyon))
    print('Toplam Kazanç: ' + str(islemBasiDolar - 100))
    print('Toplam Kazanç Oranı: ' + str((islemBasiDolar - 100) / 100))
    print('Toplam Kazanç Oranı (Yıllık): ' + str(((islemBasiDolar - 100) / 100) * 365))

def BurakStrategy_1(model):
    df = dl.ReadDataSource(model.symbol, model.interval)
    open = df['Open']
    close = df['Close']
    high = df['High']
    low = df['Low']
    acilisZamani = df['Open time']
    print('Coin Adı: ' + model.symbol)
    print('İşlem Aralığı: ' + model.interval)

class BurakStrategy_1_Model:
    def __init__(self, _symbol, _interval):
        self.symbol = _symbol
        self.interval = _interval