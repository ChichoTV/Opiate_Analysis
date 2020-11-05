# flask imports
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# connection string for Taylor's DB
conn_string='tester:taylor@localhost:5432/Opiate_Analysis'
engine= create_engine(f'postgresql://{conn_string}')

app = Flask(__name__)

res=engine.connect().execute('select * from "Prescriber_info" limit 100')
for row in res:
    print(row[0])

@app.route("/")
def home():
    res=engine.connect().execute('select * from "Prescriber_info"')
    mydict={}
    for row in res:
        mydict[str(row[0])]=row[3]
    return jsonify(mydict)