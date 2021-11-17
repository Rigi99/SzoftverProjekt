import time

import binanceData
import coinbaseData
import config

if __name__ == '__main__':
    # binanceData.getBinanceData()
    # coinbaseData.getCoinBaseData()
    # coinbaseData.movingAverageMethodCoinBase()
    while True:
        binanceData.movingAverageMethodBinance1Day(config.DbHistorical)
        binanceData.movingAverageMethodBinance5Day(config.DbHistorical)
        binanceData.movingAverageMethodBinance25Days(config.DbHistorical)
        time.sleep(1800)
    # binanceData.deleteDataBase(config.DbRealTime+'.db')
    # binanceData.deleteDataBase(config.DbHistorical + '.db')
