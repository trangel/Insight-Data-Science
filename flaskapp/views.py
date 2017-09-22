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
from get_questions import get_questions
from config import username,hostname,dbname,password

text='postgres://{}:{}@localhost/{}'.format(username,password,dbname)
db = create_engine(text)
con = None
con = psycopg2.connect(database = dbname, user = username, password=password, host=hostname)

#@app.route('/')
#@app.route('/index')
#def index():
#    return render_template("index.html",
#       title = 'Home', user = { 'nickname': 'Miguel' },
#       )

@app.route('/db_fancy')
def AutismExpert_page_fancy():
    sql_query = """
               SELECT * FROM \"articles-n-forums-posts\" WHERE title LIKE '%autism%';
                """
    query_results=pd.read_sql_query(sql_query,con)
    autism_docs = []
    for i in range(0,query_results.shape[0]):
        autism_docs.append(dict(title=query_results.iloc[i]['title'], href=query_results.iloc[i]['href'], text_short=query_results.iloc[i]['text_short']))
    return render_template('view_db.html',autism_docs=autism_docs)

@app.route('/')
@app.route('/index')
def index():
    question_list = get_questions()
    return render_template("input.html", question_list = question_list)

@app.route('/output')
def AutismExpert_output():
    #
    # Get query text from user:
    #
    text = request.args.get('autism_query')
    filter_opt = request.args.get('filter_opt')
    selection = request.args.get('selection')

    if text == "":
        text = selection

    if filter_opt == None:
        filter_posts_flag=False
    else:
        filter_posts_flag=True

#   Find similar articles from model
#   This returns a list of article ids
    result_forums, result_articles = query_model(text,filter_posts_flag)
#
    question_list = get_questions()
#   
#   Query db
#
#   Results from forums:
    forum_docs = []
    if len(result_forums) > 0 :
        query = "SELECT title, text_short, href FROM \"articles-n-forums-posts\" WHERE \"post id\" IN ({})".format(result_forums)
        query_results=pd.read_sql_query(query,con)
#       Convert result to list of dictionaries to handle in HTML page:
        for i in range(0,query_results.shape[0]):
            forum_docs.append(dict(title=query_results.iloc[i]['title'], href=query_results.iloc[i]['href'], text_short=query_results.iloc[i]['text_short']))
#
#   Results from articles:
    article_docs = []
    if len(result_articles) > 0 :
        query = "SELECT title, text_short, href FROM \"articles-n-forums-posts\" WHERE \"post id\" IN ({})".format(result_articles)
        query_results=pd.read_sql_query(query,con)

#       Convert result to list of dictionaries to handle in HTML page:
        for i in range(0,query_results.shape[0]):
            article_docs.append(dict(title=query_results.iloc[i]['title'], href=query_results.iloc[i]['href'], text_short=query_results.iloc[i]['text_short']))

    return render_template("output.html", autism_docs=forum_docs, forum_docs = forum_docs, article_docs = article_docs, question_list = question_list , this_query = text)

