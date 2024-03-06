import io
import random
import json
from fdk import response
 
def handler(ctx,data):
    max = ctx.RequestURL() # Get the requested URL
    max = max.split("=")[1] # Extract the value passed to the query string, this makes the presumption that there is a single query string (I know you should never presume!) and uses this for the max variable that the for loop uses
    exerciselist = ['50 Star Jumps','20 Crunches','30 Squats','50 Press Ups','1 Min Wall Sit','10 Burpees','20 Arm Circles',\
        '20 Squats','30 Star Jumps','15 Crunches','10 Press Ups','2 Min Wall Sit','20 Burpees','40 Star Jumps','25 Burpees',\
        '15 Arm Circles','30 Crunches','15 Press Ups','30 Burpees','15 Squats','30 Sec Arm Circles','2 Min Wall Sit','20 Burpees',\
        '60 Star Jumps','10 Crunches','25 Press Ups'
        ]
    workout = []
    for i in range(0,int(max)):
        randomnumber = random.randint(0,(len(exerciselist)-1))
        workout.append(exerciselist[randomnumber])
 
    return response.Response(ctx, response_data=workout)
