"""examples for from pprint import pprint"""
from pprint import pprint
from client import Client


client = Client()
try:
    coin = client.get_coin("btc")
    pprint(coin)
except Exception:
    print("something went worng")

