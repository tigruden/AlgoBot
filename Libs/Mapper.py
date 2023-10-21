import sys
sys.path.append('Models')

import BinanceKline
from datetime import datetime


def HistoricalKlinesToBinanceKlineMapper(historicalKlines):
    binanceKlines = []
    for historicalKline in historicalKlines:
        binanceKline = BinanceKline.Kline(CreationTime=datetime.now(), OpenTime=datetime.fromtimestamp(historicalKline[0] / 1000), Open=historicalKline[1], High=historicalKline[2], Low=historicalKline[3], Close=historicalKline[4], Volume=historicalKline[5], CloseTime=datetime.fromtimestamp(historicalKline[6] / 1000), QuoteAssetVolume=historicalKline[7], NumberOfTrades=historicalKline[8], TakerBuyBaseAssetVolume=historicalKline[9], TakerBuyQuoteAssetVolume=historicalKline[10], Ignore=historicalKline[11])
        binanceKlines.append(binanceKline)
    return binanceKlines

def SocketKlineToBinanceKlineMapper(socketKline):
    kline = BinanceKline.Kline(CreationTime=datetime.now(), OpenTime=datetime.fromtimestamp(socketKline['k']['t'] / 1000), Open=socketKline['k']['o'], High=socketKline['k']['h'], Low=socketKline['k']['l'], Close=socketKline['k']['c'], Volume=socketKline['k']['v'], CloseTime=datetime.fromtimestamp(socketKline['k']['T'] / 1000), QuoteAssetVolume=socketKline['k']['q'], NumberOfTrades=socketKline['k']['n'], TakerBuyBaseAssetVolume=socketKline['k']['V'], TakerBuyQuoteAssetVolume=socketKline['k']['Q'], Ignore=socketKline['k']['B'])
    return kline