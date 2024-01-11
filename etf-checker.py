from cat.mad_hatter.decorators import tool, hook
from typing import Dict, List, Literal, Optional
import requests

JUSTETF_BASE_URL = "https://www.justetf.com/servlet/etfs-table"

BASE_PARAMS = {
    "draw": 1,
    "start": 0,
    "length": -1,
    "lang": "en",
    "country": "DE",
    "universeType": "private",
}

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

@tool
def search_etf(query, cat):
    """
    Search for an ETF, ETN or ETC. The input is a query

    For example, give me some informations about this ETF: IE00BYZK4883
    Query -> IE00BYZK4883
    """

    params = "groupField=index&productGroup=epg-longOnly"

    response = requests.post(
        JUSTETF_BASE_URL,
        {
            **BASE_PARAMS,
            "etfsParams": params,
        },
    )

    def create_hashmap_by_key(etf_data: List[Dict[str, str]], key: str) -> Dict[str, Dict[str, str]]:
        isin_hashmap = {element[key]: element for element in etf_data}
        return isin_hashmap

    if response.status_code == requests.codes.ok:
        data = response.json()["data"]
        isin_map = create_hashmap_by_key(data, "isin")
        return get_etf_info(isin_map, query)
    else:
        return "There was an error while checking for the list of ETFs"
