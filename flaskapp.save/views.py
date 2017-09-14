from flask import render_template,request
from flaskapp import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2

# Import "flaskapp/query_model.py"
import os
import sys
path2flaskapp=os.path.join(os.getcwd(),"flaskapp")
sys.path.insert(0, path2flaskapp)
from query_model import query_model

user = 'rangel' #add your username here (same as previous postgreSQL)            
host = 'localhost'
dbname = 'autism-docs'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, user = user)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Home', user = { 'nickname': 'Miguel' },
       )

@app.route('/db_fancy')
def AutismExpert_page_fancy():
    sql_query = """
               SELECT title,href,text FROM \"articles-n-forums-posts\" WHERE title LIKE '%autism%';
                """
    query_results=pd.read_sql_query(sql_query,con)
    autism_docs = []
    for i in range(0,query_results.shape[0]):
        autism_docs.append(dict(title=query_results.iloc[i]['title'], href=query_results.iloc[i]['href'], text=query_results.iloc[i]['text']))
    return render_template('view_db.html',autism_docs=autism_docs)

@app.route('/input')
def AutismExpert_input():
    return render_template("input.html")

@app.route('/output')
def AutismExpert_output():
  #pull 'birth_month' from input field and store it
  text = request.args.get('autism_query')

# Find similar articles from model
  result_forums, result_articles = query_model(text)


#    #just select the Cesareans  from the birth dtabase for the month that the user inputs
#  query = "SELECT index, attendant, birth_month FROM birth_data_table WHERE delivery_method='Cesarean' AND birth_month='%s'" % patient
#  print ( query )
#  query_results=pd.read_sql_query(query,con)
#  print ( query_results )
  births = []
#  for i in range(0,query_results.shape[0]):
#      births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['attendant'], birth_month=query_results.iloc[i]['birth_month']))
#      the_result = ModelIt(patient,births)
  return render_template("output.html", births = births, result_forums = result_forums, result_articles = result_articles)

