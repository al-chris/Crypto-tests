import os
from requests import get
from matplotlib import pyplot as plt
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ETHERSCAN_API_KEY")
BASE_URL = os.getenv("ETHERSCAN_BASE_URL")
address = "0x73bceb1cd57c711feac4224d062b0f6ff338501e"
ETH_VALUE = 10 ** 18


def make_api_url(module, action, address, **kwargs):
    url = f"{BASE_URL}?module={module}&action={action}&address={address}&apikey={API_KEY}"

    for key, value in kwargs.items():
        url += f"&{key}={value}"

    return url


def get_account_balance(address):
    balance_url = make_api_url("account", "balance", address, tag="latest")

    response = get(balance_url)
    data = response.json()
    value = int(data["result"]) / ETH_VALUE
    return value

"""
https://api.etherscan.io/api
   &module=account
   &action=txlist
   &address=0xc5102fE9359FD9a28f877a67E36B0F050d81a3CC
   &startblock=0
   &endblock=99999999
   &page=1
   &offset=10
   &sort=asc
   &apikey=YourApiKeyToken
"""

def get_transactions(address):
    transactions_url = make_api_url(
        "account", 
        "txlist", 
        address, 
        startblock=0, 
        endblock=99999999, 
        page=1,
        offset=100,
        sort="asc"
    )

    response = get(transactions_url)
    data = response.json()["result"]

    internal_tx_url = make_api_url(
        "account", 
        "txlistinternal", 
        address, 
        startblock=0, 
        endblock=99999999, 
        page=1,
        offset=100,
        sort="asc"
    )
    response2 = get(internal_tx_url)
    data2 = response2.json()["result"]

    data.extend(data2)
    data.sort(key=lambda x: int(x['timeStamp']))

    current_balance = 0
    balances = []
    times = []
    
    for tx in data:
        to = tx["to"]
        from_addr = tx["from"]
        value = int(tx["value"]) / ETH_VALUE
        if "gasPrice" in tx:
            gas = int(tx["gasUsed"]) * int(tx["gasPrice"]) / ETH_VALUE
        else:
            gas = int(tx["gasUsed"]) / ETH_VALUE
        time = datetime.fromtimestamp(int(tx["timeStamp"]))
        money_in = to.lower() == address.lower()

        if money_in:
            current_balance += value
        else:
            current_balance -= value + gas

        balances.append(current_balance)
        times.append(time)

    plt.plot(times, balances)
    plt.show()

get_transactions(address)