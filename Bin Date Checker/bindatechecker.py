import requests
import bs4
import os
dates = ""
r = requests.get("https://www.hull.gov.uk/bins-and-recycling/bin-collections/bin-collection-day-checker/checker/view/10093952819")
soup = bs4.BeautifulSoup(r.text, features="html.parser")

#Black bin
blackbin = soup.find(class_="region region-content")
div = blackbin.find_parent('div')
span = div.find_all('span')
spantext = str(span[1]).split(">")
date = spantext[1].split("<")
blackbindate = date[0]
dates += "Black Bin " + "- " + blackbindate + "," + "\n"

#Blue bin
blue = soup.find_all(style="color:blue;font-weight:800")
bluebin = str(blue[1]).split(">")
bluebincollection = bluebin[1].split("<")
bluebindate = bluebincollection[0]
dates += "Blue Bin " + "- " + bluebindate + "," + "\n"
        
#Brown bin
brown = soup.find_all(style="color:#654321;font-weight:800")
brownbin = str(brown[1]).split(">")
brownbincollection = brownbin[1].split("<")
brownbindate = brownbincollection[0]
dates += "Brown Bin " + "- " + brownbindate + "," + "\n"

print(dates)
