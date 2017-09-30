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

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/db_fancy')
def page_fancy():
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


@app.route('/output_text')
def output_text():
    question_list = get_questions()
    #
    # Get doc id to show
    #
    post_id = request.args.get('post_id')
    #
    if str(post_id) == 'None' :
        return render_template("input.html", question_list = question_list)
    #
    # Get text from db:
    #
    query = "SELECT \"post id\", title, text, href, href_short FROM \"articles-n-forums-posts\" WHERE \"post id\"  = {}".format(post_id)
    query_results=pd.read_sql_query(query,con)
    #
    doc = dict(
        post_id    = query_results.iloc[0]['post id'],
        title      = query_results.iloc[0]['title'], 
        text       = query_results.iloc[0]['text'],
        href       = query_results.iloc[0]['href'], 
        href_short = query_results.iloc[0]['href_short']
        )

    return render_template("output_text.html", doc = doc, question_list = question_list)

@app.route('/output')
def output():
    #
    # Get query text from user:
    #
    text = request.args.get('autism_query')
    filter_opt = request.args.get('filter_opt')
    selection = request.args.get('selection')

    question_list = get_questions()

    # Check inputs:
    if text == "":
        text = str(selection)

    if text == 'None' :
        return render_template("input.html", question_list = question_list)

    if filter_opt == None:
        filter_posts_flag=False
    else:
        filter_posts_flag=True

#   Find similar articles from model
#   This returns a list of article ids
    result_forums, result_articles = query_model(text,filter_posts_flag)
#
#   
#   Query db
#
#   Results from forums:
    forum_docs = []
    if len(result_forums) > 0 :
        query = "SELECT \"post id\", title, text_short, href, href_short FROM \"articles-n-forums-posts\" WHERE \"post id\" IN ({})".format(result_forums)
        query_results=pd.read_sql_query(query,con)
#       Convert result to list of dictionaries to handle in HTML page:
        for i in range(0,query_results.shape[0]):
            forum_docs.append(dict(
                post_id    = query_results.iloc[i]['post id'],
                title      = query_results.iloc[i]['title'], 
                text_short = query_results.iloc[i]['text_short'],
                href       = query_results.iloc[i]['href'], 
                href_short = query_results.iloc[i]['href_short']
                ))
#
#   Results from articles:
    article_docs = []
    if len(result_articles) > 0 :
        query = "SELECT \"post id\", title, text_short, href, href_short FROM \"articles-n-forums-posts\" WHERE \"post id\" IN ({})".format(result_articles)
        query_results=pd.read_sql_query(query,con)

#       Convert result to list of dictionaries to handle in HTML page:
        for i in range(0,query_results.shape[0]):
            article_docs.append(dict(
                post_id    = query_results.iloc[i]['post id'],
                title      = query_results.iloc[i]['title'], 
                text_short = query_results.iloc[i]['text_short'],
                href       = query_results.iloc[i]['href'], 
                href_short = query_results.iloc[i]['href_short']))

    no_results=False
    if len(forum_docs) + len(article_docs) == 0 :
        no_results=True
    

    return render_template("output.html", forum_docs = forum_docs, article_docs = article_docs, question_list = question_list , this_query = text, filter_posts_flag = filter_posts_flag, no_results = no_results )

