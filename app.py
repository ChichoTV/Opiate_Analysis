# flask imports
from flask import Flask, jsonify,render_template
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy import *

# connection string for Taylor's DB
conn_string='tester:taylor@localhost:5432/Opiate_Analysis'
engine= create_engine(f'postgresql://{conn_string}')
Base=automap_base()
Base.prepare(engine,reflect=True)
inspector=inspect(engine)
def column_grab(inp):
    return inp['name']
cols_wide=list(map(column_grab,inspector.get_columns('Wide_data')))
cols_pre=list(map(column_grab,inspector.get_columns('Prescriber_info')))
    
app = Flask(__name__)

@app.route("/")
def home():
    return (
        'Available columns:<br>'
        'State<br>'
        'Population<br>'
        'Deaths<br>'
        'Abbrev<br>'
        'SEPARATE EACH COLUMN IN YOUR QUERY WITH &'
    )


@app.route("/api_v1/Overdoses/<columns>")
def query(columns):
    data={}
    to_return={}
    col_list=columns.split('&')
    res_dict={}
    abbrev_list=[]
    abbrev=engine.connect().execute(f'select "Abbrev" from "Overdoses" ')
    for ab in abbrev:
        abbrev_list.append(ab[0])
    for column in col_list:
        result=engine.connect().execute(f'select "{column}" from "Overdoses" ')
        res_dict[column]=result
        for row in res_dict[column]:
            try:
                data[column].append(row[0])
            except:
                data[column]=[row[0]]
    i=0
    for ab in abbrev_list:
        temp={}
        for column in col_list:
            temp[column]=data[column][i]
        i=i+1
        to_return[ab]=temp
    return to_return

@app.route('/api_v1/Wide')
def wide():
    ret={}
    lists=engine.connect().execute('SELECT * FROM "Wide_data"')
    for key_name in cols_wide:
        i=0
        for item in lists:
            temp={}
            for num in range(11):
                temp[cols_wide[num]]=item[num]
            i=i+1
            ret[str(i)]=temp
    return ret


@app.route('/home')
def homepage():
    return render_template('matt_index.html')

@app.route('/api_v1/Prescriber')
def prescriber():
    ret={}
    lists=engine.connect().execute('SELECT * FROM "Prescriber_info"')
    for key_name in cols_pre:
        i=0
        for item in lists:
            temp={}
            for num in range(45):
                temp[cols_pre[num]]=item[num]
            i=i+1
            ret[str(i)]=temp
    return ret