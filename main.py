import binanceData
import coinbaseData

if __name__ == '__main__':
    Db = 'BTCUSDTHistorical'
    # binanceData.getBinanceData()

    # coinbaseData.getCoinBaseData()
    # coinbaseData.movingAverageMethodCoinBase()
    binanceData.getHistoricalData(Db)
    binanceData.movingAverageMethodBinance(Db)
