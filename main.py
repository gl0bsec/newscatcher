#%% 
#Import packages

# import load_data
import processing 
import pandas as pd
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from bertopic import BERTopic

filename = 'migrants_2023_08_15_page_size_20.json'
db_name = 'articles.sqlite'
table_name = 'articles_table'

#%%
# Testing

## SQL Skeleton "SELECT cols FROM table WHERE conditions"
con = sqlite3.connect(db_name)
cur = con.cursor()
cur.execute("SELECT _id, title,topic,summary,excerpt,published_date,clean_url,topic from articles_table")
data2 = cur.fetchall()
df2 = pd.read_sql_query("SELECT _id, title,topic,summary,excerpt,published_date,clean_url,topic from articles_table", con)
test_result = processing.process_text(data2, 3)
df3 = pd.DataFrame(test_result,columns=['uuid','neg','neu','pos','compound','spacy_entities'])
df3.head()

