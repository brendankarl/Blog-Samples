import requests
import datetime

PAT = "eyJhbGciOiJQUzI1NiIsInppcCI6IkdaSVAifQ.H4sIAAAAAAAA_31Sy5KcMAz8lS3O6y2eNnDLLT-QDxC2POMasCnbbLKVyr9Hg02W2SR7Q8jd6m7pZ2FCKMYCVvMSIvjZ2MsE9vYi3VI8F2GbqClV3YlaNKxpy4a1GgQbWl4y0Q6dbmpqI9Jj_LEWYyuGoSuHUvTPhYFYjBVvm77p2vsPkNJtNn51s0L_zSji5n0j9FSXrENN3LLq2dSVwHhVIdLUoVcTcUd3Q5sQqtdDz4eWYdkJ1laCs4G3ioFAzcUkdM0rQpCjL1JiCAklxcD5oCWbBjGxtqvpq6o148hBY9VXE8q7YelWpOeUhVWUBXOepI4eQT1FDzaAjMbZEZWJT2EFiam3whsiMwtc8o8ArwQP7OJgZjtSHzwL-BvGdSYwMzbixcPOmZtWQcRR4YwRnzxKNGscv3tD1T7laEnw6hHzriTpk85q45ednTnN9GZVOL86Ptm0zbdUQYwgrwvamGq5heiWQ_qpe1YkqUnF2fOhMq-cXfedMwtLHpsbn6WVaVO25_QTwRavzptw35KhZb0atdHc5Mk7beaHhfwv9eTjQfr-Pief8woYI_Ft62d6D8tKebq7fCNn4iMneUW1zagYWTtFTQtltLPo3ZzASfPd4OqRJqClg86K_84jJz2bcKS6TUF6MnF_k8VNMIOVD5l85E_YSErv2pgMr--HMjv574yT2fPAB1F5_fFtxY_8q9JZDUagO4bs_ahyaAeTUQQy2vw5yZz2XuACJmVX_PoNLEvnZNsEAAA.MMLM0mev29jA2ivyBx7KrDL-kwPiqUD2IZtchGND6ckkmILqyV2GcVupB1tM242RvRXAACI_zZ6KYNkQsYXisoNOTFl_5qJiUVEKQMWmLs3t_AwWKY83S7GUrb1By8pQzo5tbK3G8Gtk6hjYHZzsjboBHHK87ipqtdsk7X4cKC9aNvtr55VvfEwhOzUvC4CmLCpBkFEJtDrX8jGaNPwF3tqCDb2XAIpKqScUOfgiF_wsVuUtawLkvGApsssLAelf2Q9F109UpRMK5Om0K3CSIuJTVSZyVn1r2NRNKLb4epxdDGOIUnq_DSMFul9m0pjsfBe0yVfs_MWWTjHmeS_RGS_0YcvbnuVRwAneEsUdA-81sDO8vPcvxxdgpzgdasOgLoig4o47lJns61P0btBJnuwJNMnduNBhBlTeYpvtR01eRsyWEKXw4I_uP-nFAWmR_RtZlUj9_xyHEZLORtwSD5OWOTfVpprNtLsUnl8MQTfRoGRFsz8tIpDNqNO0ccwKW121xpDPCidxQZKuC5N7aEDdxu0yoPbyhG8ooXEBo13GiADi2Re7SYFOTLIJUXNk4z9Nh8PLGe6pZPfzjsQMfD-5nMhME65MoF0mOI9EeEOwrdcF3389JRuud14aLweLooij_Cb8E6FWNnOlkFR8QFYqpGDIYLLwHYEQ14m2GgA"
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