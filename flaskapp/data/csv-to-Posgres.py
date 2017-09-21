## Python packages - you may have to pip install sqlalchemy, sqlalchemy_utils, and psycopg2.
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd

#In Python: Define a database name (we're using a dataset on births, so I call it 
# birth_db), and your username for your computer (CHANGE IT BELOW). 
dbname = 'autism-docs'
username = 'rangel'

## 'engine' is a connection to a database
## Here, we're using postgres, but sqlalchemy can connect to other things too.
engine = create_engine('postgres://%s@localhost/%s'%(username,dbname))
print (engine.url)

## create a database (if it doesn't exist)
if not database_exists(engine.url):
    create_database(engine.url)
print(database_exists(engine.url))

# read a database from CSV and load it into a pandas dataframe
df = pd.DataFrame.from_csv('articles-n-forums-posts.csv')

## insert data into database from Python (proof of concept - this won't be useful for big data, of course)
df.to_sql('articles-n-forums-posts', engine, if_exists='replace')

