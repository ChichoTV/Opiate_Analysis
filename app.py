# flask imports
from flask import Flask, jsonify,render_template,Response
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy import *
import json 
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
cols_agg=['Deaths','State','Year']
    
app = Flask(__name__)

@app.route("/api_routes")
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


@app.route('/')
def homepage():
    return render_template('index.html')

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
@app.route('/overdoses')
def od():
    return render_template('overdoses.html')
@app.route('/prescriptions')
def pre():
    return render_template('prescriptions.html')

@app.route('/data')
def data():
    return render_template('data_routes.html')



@app.route('/api_v1/Wide_agg')
def agg():
    data=engine.connect().execute('SELECT CAST( SUM("Total") AS INT) AS "sum","State","Year" FROM "Wide_data" GROUP BY "State","Year" ORDER BY "State","Year"')
    ret=[]
    for key_name in cols_agg:
        i=0
        for item in data:
            temp={}
            for num in range(3):
                temp[cols_agg[num]]=item[num]
            i=i+1
            ret.append(temp)
    return jsonify(ret)

@app.route('/api_v1/percents')
def percent():
    data=engine.connect().execute('SELECT CAST(100000*"Deaths"/"Population" AS FLOAT) AS "Percent" ,"State" FROM "Overdoses"')
    ret={}
    for item in data:
        ret[item[1]]=item[0]
    return ret
