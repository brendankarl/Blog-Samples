# Python script that calls an ML model created using AutoML.
# Model trained using an employee attrition dataset - https://www.kaggle.com/datasets/patelprashant/employee-attrition

import requests

restauth = "x.oraclecloudapps.com/omlusers/"
rest = "x.oraclecloudapps.com/omlmod/"

model = "EmpAttrition"

# Get token
tokenurl = restauth + "api/oauth2/v1/token"
data = {"grant_type":"password", "username":"OMLUSER", "password":"PASSWORD"}
headers = {"Content-Type": "application/json"}
gt = requests.post(tokenurl,json=data,headers=headers)
token = gt.json()["accessToken"]
print(token)

# Option 1 - No Overtime / 10 years at company / travels rarely
probabilityurl = rest + "v1/deployment/" + model + "/score"
headers = {"Content-Type": "application/json","Authorization": "Bearer " + token}
input = {"inputRecords":[{"OVERTIME":"No","YEARSATCOMPANY":10,"BUSINESSTRAVEL":"Travel_Rarely"}]}
usemodel = requests.post(probabilityurl,json=input,headers=headers)
print(usemodel.json()["scoringResults"])

for label in usemodel.json()["scoringResults"][0]["classifications"]:
    print(label)

# Option 2 - Overtime / 5 years at company / travels frequently
probabilityurl = rest + "v1/deployment/" + model + "/score"
headers = {"Content-Type": "application/json","Authorization": "Bearer " + token}
input = {"inputRecords":[{"OVERTIME":"Yes","YEARSATCOMPANY":5,"BUSINESSTRAVEL":"Travel_Frequently"}]}
usemodel = requests.post(probabilityurl,json=input,headers=headers)
print(usemodel.json()["scoringResults"])

for label in usemodel.json()["scoringResults"][0]["classifications"]:
    print(label)
