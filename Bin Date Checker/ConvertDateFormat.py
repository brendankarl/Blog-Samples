from datetime import datetime

bluebindate = "Wednesday 16th Nov 2022" # Manually specifying the date string for testing using the format returned by the BinDateChecker.py Python script 

# Remove all instances of st, nd, rd and th as datetime.strptime cannot deal with these (I'm sure there's a more elegant approach!)
bluebindate = bluebindate.replace("st","")
bluebindate = bluebindate.replace("nd","")
bluebindate = bluebindate.replace("rd","")
bluebindate = bluebindate.replace("th","")

# Call datetime.strptime passing the format I'm using day name / date / month name / year, a full reference can be found here - https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
bluebindate = datetime.strptime(bluebindate, '%A %d %b %Y')
print(bluebindate)
