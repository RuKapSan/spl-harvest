from beem import Hive
from beem.account import Account
from datetime import datetime
import requests
import sys
import yaml
from yaml.loader import SafeLoader


receiver = INPUT YOUR HIVE ACCOUNT


with open('config.yaml') as config_file:
  config = yaml.load(config_file, Loader=SafeLoader)
  hive_node = config['hive-node']
  for account in config['accounts']:
    # Wallet Setup
    hive_name = account['name']
    hive = Hive(keys=[account['active-key']], node=hive_node)
    hive_account = Account(hive_name, blockchain_instance=hive)

    # find decs and cards
    balances = []
    try:
      balances = requests.get(f'https://api.splinterlands.io/players/balances?username={hive_name}').json()
      details = requests.get(f"https://steemmonsters.com/cards/collection/{hive_name}").json()
    except:
      print(f"ERROR: Could not fetch Splinterlands balances for {hive_name}", file=sys.stderr)
      continue
    dec = 0 # Defaulting to 0 to claim only
    for balance in balances:
      if balance['token'] == 'DEC':
        dec = balance['balance']
        break
    cardlist = []
    for card in details['cards']:
      if card["player"] == hive_name:
        cardlist.append(card["uid"])
    if account['action'] is None or account['action'] == 'transfer':
      # Execute transaction
      hive.custom_json(id="sm_token_transfer", required_auths=[hive_name],
                       json_data=f"{{\"to\":\"{receiver}\",\"qty\":{dec},\"token\":\"DEC\",\"type\":\"withdraw\",\"memo\":\"{receiver}\",\"app\":\"steemmonsters/0.7.130\",\"n\":\"8UbDCbSJmB\"}}")
      print(f"Dec received from {hive_name} in count: {dec}")
      hive.custom_json('sm_gift_cards', {'to': receiver, 'cards': cardlist}, required_auths=[hive_name])
      print(f"Cards received from {hive_name} in count: {len(cardlist)}")
