import sqlalchemy
apiKey = 'O2u58tbg01wTgCHcGgGCBnpdpmStaqP0WeVy3Iiif6MAwlbdEhMpvWaL74n8VdAs'
apiSecurity = 'wQb4Gyh9zxM2GZ03Xx8Ldok40tVjhO1KG1RBjYdoegbG67r3ogt2qeDocCDwGhIV'
DbHistorical = 'BTCBUSDHistorical'
DbRealTime = 'BTCBUSD'
engineHistorical = sqlalchemy.create_engine('sqlite:///BTCBUSDHistorical.db')
engineRealTime = sqlalchemy.create_engine('sqlite:///BTCBUSD.db')
currencySymbol = 'BTC'
moneySymbol = 'BUSD'
# Zsombi

# apiKey = 'k9PP6Q9Zop25GDns7iDwopDx9ERmqmgp7tokaNlVCmNT5nk9hQvzXU0Q7DzOOvca'
# apiSecurity = 'CaX9mtvJUpytOQeTL5WxkOsz7qyYyF6Q2sKAvAHBkRnehcVn9QOekfmvQH6bSqo5'
# Zsolt

# In this file, the costumer has to give his or her API key and its security key, to connect to his or her account.
# The rest can remain the same.
