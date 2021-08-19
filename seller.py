from beem import Hive
from beem.account import Account
from datetime import datetime
import requests
import sys
from hiveengine.market import Market
from hiveengine.wallet import Wallet
import pandas as pd
import time



hive_node = 'https://api.hive.blog'
df = pd.read_csv('accounts.csv')


hive_name = 'rkps'
id = list(df['names']).index(hive_name)
hive = Hive(keys=[df['Active Key'][id]], node=hive_node)
hive_account = Account(hive_name, blockchain_instance=hive)
balances = []

def main():
    try:
        balances = requests.get(f'https://api.splinterlands.io/players/balances?username={hive_name}').json()
    except:
        print(f"ERROR: Could not fetch Splinterlands balances for {hive_name}", file=sys.stderr)

    for balance in balances:
        if balance['token'] == 'DEC':
            dec = balance['balance']
            break
    hive.custom_json('sm_token_transfer', {"to": 'sl-hive',
                                               "qty": dec,
                                               "token": "DEC",
                                               "type": "withdraw",
                                               "memo": hive_name}, required_auths=[hive_name])

    time.sleep(5*60)
    market = Market(blockchain_instance=hive)
    wallet = Wallet(hive_name,blockchain_instance=hive)
    market.sell(hive_name,dec,'DEC', 0.0001)
    time.sleep(2*60)
    wallet_balances = wallet.get_balances()
    SWAP_HIVE = 0
    for balance in wallet_balances:
        if balance['symbol'] == 'SWAP.HIVE':
            SWAP_HIVE = balance['balance']
            break
    time.sleep(5*60)
    market.withdraw(hive_name, int(float(SWAP_HIVE)))
    market.withdraw(hive_name, int(float(SWAP_HIVE)))
    market.withdraw(hive_name, int(float(SWAP_HIVE)))
    market.withdraw(hive_name, int(float(SWAP_HIVE)))
    market.withdraw(hive_name, int(float(SWAP_HIVE)))



if __name__ == "__main__":
    main()