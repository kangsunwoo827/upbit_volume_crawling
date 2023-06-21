import pandas as pd
import aiohttp
import json
import asyncio
import time

class Crawler():
    def __init__(self):
        self.tickers = None
        self.BTCprice = None
        self.USDTprice = None
        self.volumes = None

    async def fetch_data(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    async def getTickers(self):
        url = "https://api.upbit.com/v1/market/all?isDetails=false"
        headers = {"accept": "application/json"}

        data = await self.fetch_data(url)
        data_tickerName = json.loads(data)
        df_tickerName = pd.DataFrame(data_tickerName)

        df_tickerName['leading_str'] = df_tickerName['market'].str.split('-').str[0]
        grouped_data = df_tickerName.groupby('leading_str')['market'].apply(list)

        self.tickers = grouped_data

    async def getBTCprice(self):
        url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
        headers = {"accept": "application/json"}

        data = await self.fetch_data(url)
        data = json.loads(data)
        self.BTCprice = data[0]['trade_price']

    async def getUSDTprice(self):
        url = "https://api.upbit.com/v1/ticker?markets=USDT-BTC"
        headers = {"accept": "application/json"}

        data = await self.fetch_data(url)
        data = json.loads(data)
        self.USDTprice = self.BTCprice / data[0]['trade_price']

    async def getVolumes(self):
        tickers = self.tickers
        tot_volume = 0

        async with aiohttp.ClientSession() as session:
            for currency in tickers.index:
                for ticker in tickers.loc[currency]:
                    url = f"https://api.upbit.com/v1/ticker?markets={ticker}"
                    headers = {"accept": "application/json"}

                    data = await self.fetch_data(url)
                    data = json.loads(data)
                    volume = data[0]['acc_trade_price_24h']

                    await asyncio.sleep(0.04)
                    if currency == 'BTC':
                        tot_volume += volume * self.BTCprice
                    elif currency == 'USDT':
                        tot_volume += volume * self.USDTprice
                    else:
                        tot_volume += volume

        self.volumes = tot_volume


async def main():
    crawler = Crawler()
    await asyncio.gather(
        crawler.getTickers(),
        crawler.getBTCprice(),
        crawler.getUSDTprice()
    )
    await crawler.getVolumes()
    volumes = crawler.volumes
    print(volumes)


if __name__ == "__main__":
    asyncio.run(main())