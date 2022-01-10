import machine
import utime
import random

for i in range(15):
    machine.Pin(i,machine.Pin.OUT)

for i in range(15):
    machine.Pin(i).value(0)

def lightup(id):
    for i in range(id):           
        machine.Pin(i).value(1)
        utime.sleep(0.01)
        
    for i in reversed(range(id)):           
        machine.Pin(i).value(0)
        utime.sleep(0.01)
        
while True:
    randnum = random.randint(0,15)
    lightup(randnum)
    utime.sleep(0.25)  
