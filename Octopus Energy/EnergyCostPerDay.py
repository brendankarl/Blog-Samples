import requests
from requests.auth import HTTPBasicAuth
import datetime

# Set the peak and off-peak rates for Octopus Go
offpeakrate = 9.50
peakrate = 38.58

# The number of previous days to report on
numberofdays = 7

# Set the API key, meter MPAN and serial
key = ""
MPAN = ""
serial = ""

# Get today's date
today = datetime.date.today()

# Loop through the previous x number of days to report on (set by the "numberofdays" variable)
while numberofdays > 0:
    peakusage = 0
    offpeakusage = 0
    fromdate = (today - datetime.timedelta(days=numberofdays)).isoformat() # Get the from date
    todate = (today - datetime.timedelta(days=(numberofdays - 1))).isoformat() # Get the to date
    # Call the Octopus API for the date range
    baseurl = "https://api.octopus.energy/v1/"
    url = baseurl + "electricity-meter-points/" + MPAN + "/meters/" + serial + "/consumption" + "?period_from=" + fromdate + "&period_to=" + todate 
    request = requests.get(url,auth=HTTPBasicAuth(key,""))
    consumption = request.json()
    numberofdays -= 1 # Minus 1 from the number of days variable (the loop will stop when this hits 0)

    i = 0 # Used to index the results returned (48 results per day, one per 30 minutes)
    for result in consumption["results"]: # Loop through the results returned for the specified day, extract the peak and off-peak units consumed and calculate the cost
        if i in range(40,47): # These are the indexes of the off-peak hours (00:30-04:30)
            offpeakusage = offpeakusage + result["consumption"]
        else:
            peakusage = peakusage + result["consumption"]
        i += 1
    # Calculate the peak / off-peak and total cost for the day in £'s (rounded to 2 decimal places)
    peakcost = round((peakusage * peakrate / 100), 2)
    offpeakcost = round((offpeakusage * offpeakrate / 100), 2)
    totalcost = round((peakcost + offpeakcost), 2)
    
    # Print out the cost for the day
    print("Usage for " + fromdate)
    print("-Peak £" + (str(peakcost)))       
    print("-Offpeak £" + (str(offpeakcost)))  
    print("-Total cost for day £" + (str(totalcost)))
