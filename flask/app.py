# flask imports
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy import *

# connection string for Taylor's DB
conn_string='tester:taylor@localhost:5432/Opiate_Analysis'
engine= create_engine(f'postgresql://{conn_string}')
Base=automap_base()

app = Flask(__name__)

@app.route("/")
def home():
    return (
        'Available columns:<br>'
        'State<br>'
        'Population<br>'
        'Deaths<br>'
        'Abbrev'
    )

@app.route("/api_v1/<column1>&<column2>")
def query(column1,column2):
    data={}
    abbrev_list=[]
    try:
        results1=engine.connect().execute(f'select "{column1}" from "Overdoses" ')
        abbrev=engine.connect().execute(f'select "Abbrev" from "Overdoses" ')
        results2=engine.connect().execute(f'select "{column2}" from "Overdoses" ')
        res_list=[results1,results2]
    except:
        print('an error occurred')
    for ab in abbrev:
        abbrev_list.append(ab[0])
    # print(abbrev_list)
    for res in res_list:
        i=0
        for row in res:
            try:
                data[abbrev_list[i]].append(row[0])
                i=i+1
            except:
                data[abbrev_list[i]]=[row[0]]
                i=i+1
    
    return data