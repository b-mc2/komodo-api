import requests
from typing import List



class KomodoAPI:
    def __init__(self):
        self.overview_url = "https://www.atomicexplorer.com/api/explorer/overview"
        self.dexstats_explorers_url = "https://dexstats.info/api/explorerstatus.php"
        self.summary_url = "https://www.atomicexplorer.com/api/explorer/summary"
        self.all_addresses_url = "https://dexstats.info/api/assetviewer.php?address={}"
        self.all_addresses_url_backup = "https://www.atomicexplorer.com/api/explorer/search?term={}"
        self.address_info_url = "https://{0}.explorer.dexstats.info/insight-api-komodo/addr/{1}"
        self.rewards_info_url = "https://dexstats.info/api/rewards.php?address={}"
        self.rewards_info_url_backup = "https://www.atomicexplorer.com/api/kmd/rewards?address={}"
        self.supply_url = "https://www.atomicexplorer.com/api/explorer/supply"
        self.ticker_24hr_url = "https://dexapi.cipig.net/public/ticker_24h.php"
        self.trades_24hr_url = "https://dexapi.cipig.net/public/trades_24h.php?market={}"
        self.total_supply_url = "https://api1.barterdexapi.net/supply.php?coin={}"
        self.prices_url = "https://www.atomicexplorer.com/api/mm/prices/v2?coins={0}&currency={1}&pricechange={2}"
        self.publish_tx_url = "https://komodod.com/tools/publishtx"

    def AllURLs(self):
        all_values = [value for name, value in vars(self).items()]
        return all_values

    def UpdateURLs(self, repo: str=None):
        url_repo = repo or "https://raw.githubusercontent.com/b-mc2/komodo-api/main/urls.json"
        try:
            response = requests.get(url_repo)
            if response.status_code == 200:
                updated_urls = response.json()[0]
                self.overview_url = updated_urls["overview_url"]
                self.dexstats_explorers_url = updated_urls["dexstats_explorers_url"]
                self.summary_url = updated_urls["summary_url"]
                self.all_addresses_url = updated_urls["all_addresses_url"]
                self.all_addresses_url_backup = updated_urls["all_addresses_url_backup"]
                self.address_info_url = updated_urls["address_info_url"]
                self.rewards_info_url = updated_urls["rewards_info_url"]
                self.rewards_info_url_backup = updated_urls["rewards_info_url_backup"]
                self.supply_url = updated_urls["supply_url"]
                self.ticker_24hr_url = updated_urls["ticker_24hr_url"]
                self.trades_24hr_url = updated_urls["trades_24hr_url"]
                self.total_supply_url = updated_urls["total_supply_url"]
                self.prices_url = updated_urls["prices_url"]
                self.publish_tx_url = updated_urls["publish_tx_url"]
                print(f'Updated URLs from {url_repo}')
            else:
                print(f'error, {url_repo} returned status code {response.status_code}')
        except:
            print(f'error, {url_repo} gave an unknown error')

    def RequestData(self, URL):
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {'msg': 'error', 'error_msg': f"error, status code {response.status_code}"}

    def Summary(self):
        data = self.RequestData(self.summary_url)
        return data

    def Overview(self):
        data = self.RequestData(self.overview_url)
        return data

    def DexstatsExplorers(self):
        data = self.RequestData(self.dexstats_explorers_url)
        return data

    def AddressInfo(self, address:str, coin: str='KMD'):
        built_address_info_url = self.address_info_url.format(coin, address)
        data = self.RequestData(built_address_info_url)
        return data

    def CoinSupply(self, coin: str):
        built_supply_url = self.total_supply_url.format(coin)
        data = self.RequestData(built_supply_url)
        return data

    def TickerInfo(self, coin_pair: str=None):
        if coin_pair:
            built_ticker_url = self.ticker_24hr_url + f"?market={coin_pair}"
            data = self.RequestData(built_ticker_url)
            return data
        else:
            data = self.RequestData(self.ticker_24hr_url)
            return data

    def TradeInfo(self, coin_pair: str):
        built_trade_url = self.trades_24hr_url.format(coin_pair)
        data = self.RequestData(built_trade_url)
        return data

    def AllAddresses(self, address: str, backup:bool=False):
        if backup:
            built_address_url = self.all_addresses_url_backup.format(address)
        else:
            built_address_url = self.all_addresses_url.format(address)
        data = self.RequestData(built_address_url)
        return data

    def RewardsInfo(self, address: str, backup:bool=False):
        if backup:
            built_rewards_url = self.rewards_info_url_backup.format(address)
        else:
            built_rewards_url = self.rewards_info_url.format(address)
        data = self.RequestData(built_rewards_url)
        return data

    def PriceInfo(self, coin: List[str], currency: str='all', price_change: bool=True):
        coin_list = ",".join(coin)
        price_change_selection = price_change or ""
        built_prices_url = self.prices_url.format(coin_list, currency, price_change_selection)
        data = self.RequestData(built_prices_url)
        return data

    def PublishTX(self, hex: str):
        package = f'{{"hexrw": "{hex}"}}'
        response = requests.post(self.publish_tx_url, data=package)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {'msg': 'error', 'error_msg': f"error, status code {response.status_code}"}

