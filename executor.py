import os
import pandas as pd
from multiprocessing import Pool
from random import randint
from time import sleep



def load_data(number):
    df = pd.read_csv('accounts.csv')
    name = df['names'][number]
    posting_key = df['Posting Key'][number]
    return name, posting_key

def run(number):
    sleep(randint(1,10))
    # Wallet Setup
    name, posting_key = load_data(number)
    # os.system(f'echo ACCOUNT={name} > .env')
    os.environ['ACCOUNT'] = name
    # os.system(f'echo PASSWORD={posting_key} >> .env')
    os.environ['PASSWORD'] = posting_key
    print(fr'Node exec in account {number}.')
    os.system(r'node C:\Users\stamvivalio\splinterlands-bots\splinterlands-bot\index.js')


def main(start, end):
    accs_list = []
    for i in range(start, end):
        accs_list.append(i)
    p = Pool(processes=len(accs_list))
    p.map(run, accs_list)


if __name__ == "__main__":
    start = int(input("input first account: "))
    end = int(input("input last account: "))+1
    main(start, end)
