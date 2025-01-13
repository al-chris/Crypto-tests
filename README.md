# Testing Etherscan and Remitano APIs

This project contains scripts for monitoring Ethereum transactions, interacting with the Remitano API, and tracking Ethereum wallet balances.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/crypto-tests.git
    cd crypto-tests
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project root directory and add your API keys and other environment variables:
    ```env
    ETHERSCAN_API_KEY=your_etherscan_api_key
    WEBHOOK_CALLBACK_URL=your_webhook_callback_url
    REMITANO_ACCESS_KEY=your_remitano_access_key
    REMITANO_SECRET_KEY=your_remitano_secret_key
    REMITANO_AUTHENTICATOR=your_remitano_authenticator
    REMITANO_BASE_URL=https://api.remitano.com
    ```

## Usage

### Monitoring Ethereum Transactions

The `trx_verification.py` script monitors an Ethereum wallet for new transactions and sends a webhook notification.

Example usage:
```sh
python trx_verification.py
```

### Interacting with Remitano API

The `test_remitano.py` script provides functions to interact with the Remitano API, such as fetching coin accounts and currency information.

Example usage:
```python
from test_remitano import get_coin_accounts, get_currencies

coin_accounts = get_coin_accounts('btc', '')
if coin_accounts:
    print(coin_accounts)

currencies = get_currencies()
if currencies:
    print(currencies)
```

### Tracking Ethereum Wallet Balance

The `eth_wallet_tracking.py` script fetches and plots the balance of an Ethereum wallet over time.

Example usage:
```sh
python eth_wallet_tracking.py
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.