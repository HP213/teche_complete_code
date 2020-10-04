import requests
import psutil
id = 45

temp = psutil.sensors_temperatures()['coretemp'][0][1]
count = psutil.cpu_count()

url = 'http://localhost:8000/storedata'


import time
t=time.time()

while True:
    if time.time()-t>5:
        temp = psutil.sensors_temperatures()['coretemp'][0][1]
        myobj = {'data': str(id)+','+str(count)+','+str(temp)}
        x = requests.post(url, json = myobj)
        print(myobj['data'])
        t=time.time()