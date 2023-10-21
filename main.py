import sys
sys.path.append('Libs')
sys.path.append('Services')
import DataLibrary as dl
import Indicators as ind
import TestBot as tb
from datetime import datetime
import BinanceService as bs

startDate = f'{datetime.now().day} {datetime.now().strftime("%B")} {datetime.now().year - 1}'
endDate = f'{datetime.now().day} {datetime.now().strftime("%B")} {datetime.now().year}'

#bs.GetOldDatas('BTCUSDT', ['15m', '1h', '4h', '1d'], startDate, endDate)

#lastData = bs.GetLastData('BTCUSDT', '15m')

#check = bs.ControlDataSource('BTCUSDT', '15m')

bs.JoinKlineSocket('BTCUSDT', '15m')

print('İşlem tamamlandı.')