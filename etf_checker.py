from cat.mad_hatter.decorators import tool, hook
from typing import Dict
from .etf_data import ETFData

@hook(priority=1)
def before_cat_bootstrap(cat):
    ETFData.retrive_complete_etf_data()

@tool
def search_etf_by_isin(query, cat):
    """
    Search for an ETF, ETN or ETC. The input is a query

    For example, give me some informations about this ETF: IE00BYZK4883
    Query -> IE00BYZK4883
    """
    if ETFData.isin_map is not None:
        return ETFData.get_etf_info(ETFData.isin_map, query)
    else:
        return "There was an error while checking for the list of ETFs"

@tool
def search_etf_by_ticker(query, cat):
    """
    Search for an ETF, ETN or ETC. The input is a 3 to 5 letters query

    For example, give me some informations about this ETF: SWRD
    Query -> SWRD
    """
    if ETFData.ticker_map is not None:
        return ETFData.get_etf_info(ETFData.ticker_map, query)
    else:
        return "There was an error while checking for the list of ETFs"
    
@tool(return_direct=True)
def suggest_similar_etf(query, cat):
    """
    Suggest 5 ETF similar to given ETF ISIN. The input is a query

    For example, suggest some alternatives to this ETF: IE00BYZK4883
    Query -> IE00BYZK4883
    """
    if ETFData.ticker_map is not None:
        etf = ETFData.isin_map.get(query)
        return ETFData.find_similar_etfs(etf)
    else:
        return "There was an error while checking for the list of ETFs"