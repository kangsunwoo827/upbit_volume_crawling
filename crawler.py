import pandas as pd
import requests
import json
import time
class Crawler():
    def __init__(self):
        self.tickers=self.getTickers()
        self.BTCprice =self.getBTCprice()
        self.USDTprice =self.getUSDTprice()
        self.volumes=self.getVolumes()
        
    def getTickers(self):
        url = "https://api.upbit.com/v1/market/all?isDetails=false"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        data_tickerName = json.loads(response.text)
        df_tickerName = pd.DataFrame(data_tickerName)
        
                # Extracting the leading string from the 'market' column
        df_tickerName['leading_str'] = df_tickerName['market'].str.split('-').str[0]

        # Grouping the data by the leading string
        grouped_data = df_tickerName.groupby('leading_str')['market'].apply(list)

        return grouped_data
    
    def getBTCprice(self):
        url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        data = json.loads(response.text)
                
        self.BTCprice = data[0]['trade_price']
        return self.BTCprice
    
    def getUSDTprice(self):
        url = "https://api.upbit.com/v1/ticker?markets=USDT-BTC"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        data = json.loads(response.text)
                
        self.USDTprice = self.BTCprice/data[0]['trade_price']
        return self.USDTprice
        
    def getVolumes(self):
        tickers = self.getTickers().copy()
        tot_volume=0
        for currency in tickers.index:
            for ticker in tickers.loc[currency]:
                url = f"https://api.upbit.com/v1/ticker?markets={ticker}"

                headers = {"accept": "application/json"}

                response = requests.get(url, headers=headers)

                data = json.loads(response.text)
                
                volume = data[0]['acc_trade_price_24h']
                
                time.sleep(0.05)
                if currency =='BTC':
                    tot_volume+=volume*self.BTCprice
                elif currency =='USDT':
                    tot_volume+=volume*self.USDTprice
                else:
                    tot_volume+=volume
        
        return tot_volume
        

if __name__=="__main__":
    a=time.time()
    print(Crawler().getVolumes())
    print(time.time()-a)