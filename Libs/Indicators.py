from DataLibrary import ReadDataSource
import numpy as np
import pandas_ta as ta

def RSI(_symbol, _interval, _lenght = 14):
    df = ReadDataSource(_symbol, _interval)
    rsiValue = ta.rsi(df['Close'], length= _lenght)
    return rsiValue

def MACD(_symbol, _interval):
    df = ReadDataSource(_symbol, _interval)
    macdValue = ta.macd(df['Close'])
    return macdValue

def SMA(_symbol, _interval, _lenght = 20):
    df = ReadDataSource(_symbol, _interval)
    smaValue = ta.sma(df['Close'], length= _lenght)
    return smaValue

def WMA(_symbol, _interval, _lenght = 20):
    df = ReadDataSource(_symbol, _interval)
    smaValue = ta.wma(df['Close'], length= _lenght)
    return smaValue

def EMA(_symbol, _interval, _lenght = 20):
    df = ReadDataSource(_symbol, _interval)
    emaValue = ta.ema(df['Close'], length= _lenght)
    return emaValue

def EMA3(_symbol, _interval, _lenght = 8, _lenght2 = 34, _lenght3 = 89):
    df = ReadDataSource(_symbol, _interval)
    emaValue = ta.ema(df['Close'], length= _lenght)
    emaValue2 = ta.ema(df['Close'], length= _lenght2)
    emaValue3 = ta.ema(df['Close'], length= _lenght3)
    if emaValue > emaValue2 and emaValue2 > emaValue3:
        return 'TrendUp'
    elif emaValue < emaValue2 and emaValue2 < emaValue3:
        return 'TrendDown'
    else:
        return 'TrendNone'

def IFTRSI(_symbol, _interval, _rsiLenght = 5, _wmaLenght = 9):
    df = ReadDataSource(_symbol, _interval)
    v1 = 0.1 * (ta.rsi(df['Close'], length= _rsiLenght) - 50)
    v2 = ta.wma(v1, length= _wmaLenght)
    inv = (np.exp(2*v2) - 1) / (np.exp(2*v2) + 1)
    return inv

def MavilimW(_symbol, _interval, _fmal = 3, _smal = 5):
    df = ReadDataSource(_symbol, _interval)
    tmal= _fmal + _smal
    Fmal= _smal + tmal
    Ftmal= tmal + Fmal
    Smal= Fmal + Ftmal

    M1 = ta.wma(df['Close'], length= _fmal)
    M2 = ta.wma(M1, length= _smal)
    M3 = ta.wma(M2, length= tmal)
    M4 = ta.wma(M3, length= Fmal)
    M5 = ta.wma(M4, length= Ftmal)
    MAVW = ta.wma(M5, length= Smal)
    isBuy = MAVW > MAVW[1]
    isSell = MAVW < MAVW[1]
    return MAVW, isBuy, isSell
    
def ATR(_symbol, _interval, _lenght = 14):
    df = ReadDataSource(_symbol, _interval)
    atrValue = ta.atr(df['High'], df['Low'], df['Close'], length= _lenght)
    return atrValue

