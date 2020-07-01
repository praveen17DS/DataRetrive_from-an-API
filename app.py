from flask import Flask
import zeep
import json
import sys
import pandas as pd
from flask_cors import CORS
# import ast
# import re
# import csv
# from pandas import DataFrame, read_csv;

app = Flask(__name__)
CORS(app)
wsdl = 'https://XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
client = zeep.Client(wsdl=wsdl)
n = len(sys.argv)

# mobNo = XXXXXXXXX

@app.route('/',methods=['GET'])
def home():
    return "hello world"


@app.route('/<mobNo>', methods=['GET'])
def mobile_no(mobNo):
    with client.settings(raw_response=True):
        res1 = client.service.GetPledges(mobNo)
        a1 = res1.content.decode("utf-8")
        d = json.loads(a1.split('<')[0])
        p = pd.DataFrame.from_dict(d)
        objs = [p, pd.DataFrame(p['pledgelst'].tolist()).iloc[:, :]]
        df2 = pd.concat(objs, axis=1).drop('pledgelst', axis=1)
        pledgeNos = df2["pledgeNo"]
        print(pledgeNos)
    return d

@app.route('/<mobNo>/<pledgeNo>', methods=['GET'])
def pledge_no(mobNo, pledgeNo):
    with client.settings(raw_response=True):
        res = client.service.GetPledgeDetails(pledgeNo)
        a = res.content.decode("utf-8")
        d1 = json.loads(a.split('<')[0])
        return d1

if '__main__' == __name__:
    app.run(debug=True)
