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
Base.prepare(engine,reflect=True)
print(Base.classes.keys())
Overdoses=Base.classes.Overdoses
Wide=Base.classes.Wide_data
Prescriber=Base.classes.Prescriber_info
inspector=inspect(engine)
for item in inspector.get_columns('Wide_data'):
    print(item['name'])
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


@app.route("/api_v1/<columns>")
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
            # to_return[ab]=data[column][i]
            temp[column]=data[column][i]
        i=i+1
        to_return[ab]=temp
    return to_return

@app.route('/tester')
def tester():
    ret=[]
    session=Session(engine)
    lists=session.query(Overdoses.State).all()
    session.close()
    for death in lists:
        temp={}
        temp["death"]=death
        ret.append(temp)
        print(death)
    return 'yay'
