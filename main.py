#Import packages
import load_data as load
import processing as ps 
import pandas as pd
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

filename = " 'refugees' OR 'migrants' OR 'migrant' OR 'refugee' _2023_09_09_page_size_100.json"
db_name = 'articles.sqlite'
table_name = 'articles_table'
load.load_data(filename,db_name,table_name)


## SQL Skeleton "SELECT cols FROM table WHERE conditions"
con = sqlite3.connect(db_name)
cur = con.cursor()
cur.execute("SELECT _id, title,topic,summary,excerpt,published_date,clean_url,topic from articles_table")
data2 = cur.fetchall()
df2 = pd.read_sql_query("SELECT _id, title,topic,summary,excerpt,published_date,clean_url,topic from articles_table", con)
test_result = ps.process_text(data2, 3)
df3 = pd.DataFrame(test_result,columns=['uuid','neg','neu','pos','compound','spacy_entities'])
df3.to_json('processed.json')

load.load_data_df(df3,db_name,'analytics')

results = sqlite3.connect(db_name)
resluts_search = con.cursor()


# Read sqlite query results into a pandas DataFrame
query = """ SELECT articles_table.title,articles_table.clean_url,articles_table.summary,articles_table.published_date,analytics.*
FROM articles_table ,analytics
WHERE  analytics.uuid = articles_table._id;  """

con = sqlite3.connect("articles.sqlite")
analysis_df = pd.read_sql_query(query, con)
analysis_df.to_csv('news_analysis.csv')
analysis_df.to_json('news_analysis.json')
con.close()
# Verify that result of SQL query is stored in the 
analysis_df.head()
