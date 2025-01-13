import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

def get_transactions(wallet_address, api_key):
    """
    Fetches transactions for a given wallet address using Etherscan API.
    """
    url = f"https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": wallet_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "1":
            return data["result"]
    return []

def monitor_wallet(wallet_address, api_key, callback_url, poll_interval=30):
    """
    Monitors a wallet address for new transactions and sends a webhook notification.
    
    :param wallet_address: Ethereum wallet address to monitor
    :param api_key: API key for Etherscan
    :param callback_url: URL to send webhook notifications
    :param poll_interval: Time interval in seconds to poll for updates
    """
    seen_transactions = set()

    while True:
        transactions = get_transactions(wallet_address, api_key)
        for tx in transactions:
            if tx["hash"] not in seen_transactions:
                seen_transactions.add(tx["hash"])
                notify_webhook(callback_url, tx)
        
        time.sleep(poll_interval)

def notify_webhook(callback_url, transaction):
    """
    Sends a webhook notification with transaction details.
    
    :param callback_url: Webhook URL to notify
    :param transaction: Transaction details
    """
    payload = {
        "transaction_hash": transaction["hash"],
        "from": transaction["from"],
        "to": transaction["to"],
        "value": transaction["value"],
        "timestamp": transaction["timeStamp"]
    }
    response = requests.post(callback_url, json=payload)
    if response.status_code == 200:
        print(f"Webhook sent successfully for transaction {transaction['hash']}")
    else:
        print(f"Failed to send webhook for transaction {transaction['hash']}: {response.status_code}")

# Example usage
if __name__ == "__main__":
    wallet = "0x73bceb1cd57c711feac4224d062b0f6ff338501e"
    api_key = os.getenv("ETHERSCAN_API_KEY")
    callback_url = os.getenv("WEBHOOK_CALLBACK_URL")
    monitor_wallet(wallet, api_key, callback_url)
