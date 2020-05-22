from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.conf import settings
import pandas as pd
import os
import pprint
import numpy as np
from django.shortcuts import render
from pickle import load
scaler_x = load(open(os.path.join('notebook_files','scaler_x.pkl'), 'rb'))
scaler_y = load(open(os.path.join('notebook_files','scaler_y.pkl'),'rb'))
regressor = load(open(os.path.join('notebook_files','model.pkl'),'rb'))
pp = pprint.PrettyPrinter(indent=4)

def predict(cpu_used, memory_used, temp):
    inp = np.array([cpu_used,memory_used,temp]).reshape(1,-1)
    inp = scaler_x.transform(inp)
    y = regressor.predict(inp)
    y = scaler_y.inverse_transform(y)
    return y[0][0]

def predict_multiple(x):
    inp = np.array(x)
    inp = scaler_x.transform(inp)
    y = regressor.predict(inp)
    y = scaler_y.inverse_transform(y)
    return y[:,0]

@api_view(['POST'])
def storeData(request):
    received_json_data = json.loads(request.body.decode("utf-8"))
    with open(os.path.join(settings.BASE_DIR, "static", "file.csv"),"a+") as f:
        f.write('\n'+received_json_data["data"])
    return Response(status=200)


@api_view(['POST'])
def query(request):
    received_json_data = json.loads(request.body.decode("utf-8"))
    y = predict(received_json_data['CPU_total'],received_json_data['memory_used'], received_json_data['temp'])
    return Response(y,status=200)

@api_view(['POST'])
def query_multiple(request):
    received_json_data = json.loads(request.body.decode("utf-8"))
    # print(received_json_data)
    x = []
    for i in received_json_data:
        x.append([i['CPU_total'],i['memory_used'],i['temp']])
    y = predict_multiple(np.array(x))
    pp.pprint(y)
    return Response(y,status=200)

def index(request):
    return render(request, "build/index.html")
