import requests
from typing import List, Dict

class ETFData:
    JUSTETF_BASE_URL = "https://www.justetf.com/servlet/etfs-table"

    BASE_PARAMS = {
        "draw": 1,
        "start": 0,
        "length": -1,
        "lang": "en",
        "country": "DE",
        "universeType": "private",
    }

    isin_map = None
    ticker_map = None

    @staticmethod
    def retrive_complete_etf_data() -> None:
        params = "groupField=index&productGroup=epg-longOnly"

        response = requests.post(
            ETFData.JUSTETF_BASE_URL,
            {
                **ETFData.BASE_PARAMS,
                "etfsParams": params,
            },
        )

        if response.status_code == requests.codes.ok:
            data = response.json()["data"]
            ETFData.isin_map = ETFData.create_hashmap_by_key(data, "isin")
            ETFData.ticker_map = ETFData.create_hashmap_by_key(data, "ticker")

    @staticmethod
    def create_hashmap_by_key(etf_data: List[Dict[str, str]], key: str) -> Dict[str, Dict[str, str]]:
        isin_hashmap = {element[key]: element for element in etf_data}
        return isin_hashmap
    
    def find_similar_etfs(etf: Dict[str, str]) -> str:
        url_encoded_index = etf["groupValue"]
        response = requests.post(
            ETFData.JUSTETF_BASE_URL,
            {
                **ETFData.BASE_PARAMS,
                "etfsParams": f"groupField=index&index={url_encoded_index}",
            },
        )
        assert response.status_code == requests.codes.ok
        etf_list = response.json()["data"]
        sorted_etf_list = sorted(etf_list, key=lambda x: x.get('fundSize', 0))
        sorted_etf_list = [item for item in sorted_etf_list if item.get('ticker') != etf["ticker"]]
        if len(sorted_etf_list) > 5:
            sorted_etf_list = sorted_etf_list[:5]
        elif len(sorted_etf_list) == 0:
            result = f"There aren't other ETFs with the index: {etf['groupValue']}"
            return result

        result = "Here are other ETFs with the same index: \n"
        for selected_etf in sorted_etf_list:
            result = result + f'''
            \nETF Information:
            
            - Name: {selected_etf["name"]}
            - ISIN: {selected_etf["isin"]}
            - Ticker: {selected_etf["ticker"]}
            - Distribution Policy: {selected_etf["distributionPolicy"]}
            - TER: {selected_etf["ter"]}
            - Found Currency: {selected_etf["fundCurrency"]}
            - Inception Date: {selected_etf["inceptionDate"]}
            - 1 Year Returns: {selected_etf["yearReturn1CUR"]}
            - Found Size: {selected_etf["fundSize"]} mln
            - Current Dividend Yield: {selected_etf["currentDividendYield"]}\n\n
            '''
        return result
    
    @staticmethod
    def get_etf_info(hashmap: Dict[str, Dict[str, str]], key: str):
        selected_etf = hashmap.get(key)
        if selected_etf:
            return f'''
                \nETF Information:
                
                - Name: {selected_etf["name"]}
                - ISIN: {selected_etf["isin"]}
                - Ticker: {selected_etf["ticker"]}
                - Distribution Policy: {selected_etf["distributionPolicy"]}
                - TER: {selected_etf["ter"]}
                - Found Currency: {selected_etf["fundCurrency"]}
                - Inception Date: {selected_etf["inceptionDate"]}
                - 1 Year Returns: {selected_etf["yearReturn1CUR"]}
                - Found Size: {selected_etf["fundSize"]} mln
                - Current Dividend Yield: {selected_etf["currentDividendYield"]}
                '''
        else:
            return "No ETF found with the key: {key}"