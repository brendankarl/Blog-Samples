import requests
import datetime

PAT = "Insert Personal Access Token"
url = "https://api.starlingbank.com/api/v2/"
headers = {"Authorization": "Bearer " + PAT}

def get_account():
    r = requests.get(url + "accounts", headers=headers)
    return r.json()["accounts"][0]["accountUid"]

def get_default_category():
    r = requests.get(url + "accounts", headers=headers)
    return r.json()["accounts"][0]["defaultCategory"]

def get_balance():
    balance = requests.get(url + "accounts/" + (get_account()) + "/balance", headers=headers)
    print(str("£") + str(balance.json()["effectiveBalance"]["minorUnits"] / 100))

def get_transactions(days):
    datefrom = (datetime.datetime.now()-datetime.timedelta(days=days)).strftime("%Y-%m-%d") + "T00:00:00Z"
    feeditems = requests.get(url + "feed/account/" + (get_account()) + "/category/" + (get_default_category()) + "?changesSince=" + datefrom, headers=headers)
    print(feeditems.json()["feedItems"][0]["source"] + "\n" + feeditems.json()["feedItems"][0]["direction"] + "\n" + feeditems.json()["feedItems"][0]["amount"]["currency"] \
    + ":" + str(feeditems.json()["feedItems"][0]["amount"]["minorUnits"] / 100))
