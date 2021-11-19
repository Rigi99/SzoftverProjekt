import datetime

import binanceData
import config
import time
import pandas

if __name__ == '__main__':
    # coinbaseData.getCoinBaseData()
    # coinbaseData.movingAverageMethodCoinBase()
    # aux = pandas.read_sql(config.DbHistorical, config.engineHistorical)
    # print(aux)
    binanceData.run()
    # binanceData.deleteDataBase(config.DbRealTime+'.db')
    # binanceData.run()
