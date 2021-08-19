from beem import Hive
from beem.account import Account
from datetime import datetime
import requests
import sys
import pandas as pd


hive_node = 'https://api.hive.blog'
receiver = INPUT YOUR HIVE ACCOUNT
df = pd.read_csv('accounts.csv')
#List for accounts from which you do not want to collect anything.
NOPE_CARDS = ['lobanov00213']
NOPE_DECS = []
NOPE_SPS = []

for id, account in enumerate(df['names']):
    # Wallet Setup
    hive_name = account
    hive = Hive(keys=[df['Active Key'][id]], node=hive_node)
    hive_account = Account(hive_name, blockchain_instance=hive)
    print(f'Log in account {account}.')
    # find decs and cards
    balances = []
    try:
        balances = requests.get(f'https://api.splinterlands.io/players/balances?username={hive_name}').json()
        details = requests.get(f"https://steemmonsters.com/cards/collection/{hive_name}").json()
    except:
        print(f"ERROR: Could not fetch Splinterlands balances for {hive_name}", file=sys.stderr)
        continue
    print('Checked balances and cards.')
    sps = 0
    dec = 0  # Defaulting to 0 to claim only
    for balance in balances:
        if balance['token'] == 'DEC' and hive_name not in NOPE_DECS:
            dec = balance['balance']
            break
    for balance in balances:
        if balance['token'] == 'SPS' and hive_name not in NOPE_SPS:
            sps = balance['balance']
            break
    cardlist = []
    for card in details['cards']:
        if card["player"] == hive_name and card['market_id'] == None and hive_name not in NOPE_CARDS:
            cardlist.append(card["uid"])
    # Execute transactions
    hive.custom_json('sm_token_transfer', {"to": receiver,
                                           "qty": dec,
                                           "token": "DEC",
                                           "type": "withdraw",
                                           "memo": receiver}, required_auths=[hive_name])
    print(f"Dec received from {hive_name} in count: {dec}")
    hive.custom_json('sm_token_transfer', {"to": receiver,
                                           "qty": sps,
                                           "token": "SPS",
                                           "type": "withdraw",
                                           "memo": receiver}, required_auths=[hive_name])
    hive.custom_json('sm_gift_cards', {'to': receiver, 'cards': cardlist}, required_auths=[hive_name])
    print(f"Cards received from {hive_name} in count: {len(cardlist)}")
