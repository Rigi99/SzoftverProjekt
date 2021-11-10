import binanceData
# import coinbaseData
import config

if __name__ == '__main__':
    # binanceData.getBinanceData()
    # coinbaseData.getCoinBaseData()
    # coinbaseData.movingAverageMethodCoinBase()
    # binanceData.getHistoricalData(config.DbHistorical)
    # binanceData.movingAverageMethodBinance(config.DbHistorical)
    binanceData.deleteDataBase(config.DbRealTime+'.db')
    # binanceData.deleteDataBase(config.DbHistorical + '.db')
