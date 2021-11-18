import binanceData
import config
import time
import pandas

if __name__ == '__main__':
    # coinbaseData.getCoinBaseData()
    # coinbaseData.movingAverageMethodCoinBase()
    # aux = pandas.read_sql(config.DbHistorical, config.engineHistorical)
    # print(aux)
    i = 1
    binanceData.getHistoricalData1Day(config.DbHistorical, config.engineHistorical)
    aux = pandas.read_sql(config.DbHistorical, config.engineHistorical)
    print(aux)
    while i % 3 != 0:
        ma1Day, currentPrice1 = binanceData.movingAverageMethodBinance1Day(config.DbHistorical, config.engineHistorical)
        ma7Days, currentPrice7 = binanceData.movingAverageMethodBinance7Days(config.DbHistorical, config.engineHistorical)
        ma30Days, currentPrice30 = binanceData.movingAverageMethodBinance30Days(config.DbHistorical, config.engineHistorical)
        print(str(ma1Day) + '\t\t' + str(currentPrice1))
        print(str(ma7Days) + '\t\t' + str(currentPrice7))
        print(str(ma30Days) + '\t\t' + str(currentPrice30))
        binanceData.deleteDataBase(config.DbHistorical + '.db')
        time.sleep(65)
        i = i + 1
        binanceData.getHistoricalData1Day(config.DbHistorical, config.engineHistorical)
        aux = pandas.read_sql(config.DbHistorical, config.engineHistorical)
        print(aux)
    binanceData.deleteDataBase(config.DbHistorical + '.db')
    # binanceData.deleteDataBase(config.DbRealTime+'.db')
    # binanceData.run()
