#Import common  
#%%
import json
import pandas as pd
import sqlite3
import spacy 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Load data from newscatcher
#%%
import news_api as api
search_terms = ["United Nations", "United Nations universal periodic review", "united nations committee against torture", "refugees", "migrants"]
filenames = []
from_date="2023/08/15"
page_size=20
safe_from_date = from_date.replace('/', '_')

for term in search_terms:
    filenames.append(f"{q}_{safe_from_date}_page_size_{page_size}.json")
    api.fetch_and_save_to_excel(q=term, from_date="2023/08/15", page_size=20)


# Deserialize and dump
#%% 
def add_unique_id(df):
    """
    Add a unique ID column to the DataFrame.
    """
    df['unique_id'] = range(1, len(df) + 1)
    return df

def load_data(filename,db_name,table_name):
    with open(filename, 'r') as f:
        json_data = json.load(f)
    df = pd.DataFrame(json_data['articles'])
    
    # Step 2: Add Unique ID
    df = add_unique_id(df)
    
    # Step 3: Create SQLite DB
    conn = sqlite3.connect(db_name)
    
    # Step 4: Create Table and Insert Data
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"Successfully loaded data into {db_name}, table name: {table_name}")
    conn.close()
    return 

def mass_load(filenames,db_name,table_name):
    for name in filenames:
        load_data(name,db_name,table_name) 
    return

## Process data 
#%% 
## TODO Locations 
### TODO Add col names vader_neg, vader_neu, vader_pos, vader_pol
### TODO Database schema, multivar process 
from bertopic import BERTopic

analyzer = SentimentIntensityAnalyzer()
nlp = spacy.load("en_core_web_trf",exclude=['tagger', 'attribute_ruler', 'lemmatizer'])

def flatten_concatenation(matrix):
     flat_list = []
     for row in matrix:
         flat_list += row
     return flat_list

def process_text(data, var):
    text_data = [k[var] for k in data]
    uuid = [k[18] for k in data]
    result = []
    # Sentiment  
    for k in data:
        result.append(analyzer.polarity_scores(k[var]).values())
    
    # Basic NLP
    for k in data:
        doc = nlp(k[var])
        for ent in doc.ents:
            result.append(dict([('ent_text',ent.text),('ent_type',ent.label_)]))
            
    # BERTopic 
    topic_model = BERTopic(embedding_model=nlp)
    topics, probs = topic_model.fit_transform(text_data)
    fig = topic_model.visualize_topics()
    fig.show()
    
    return result

# Testing
## Load and create DB 
#%% 
filename = 'migrants_2023_08_15_page_size_20.json'
db_name = 'articles.sqlite'
table_name = 'articles_table'
load_data(filename,db_name,table_name)

## Get Data 
#%%
## SQL Skeleton "SELECT cols FROM table WHERE conditions"

con = sqlite3.connect(db_name)
cur = con.cursor()
cur.execute('SELECT * FROM articles_table')
data = cur.fetchall()
df = pd.read_sql_query("SELECT title,topic,summary,excerpt,published_date,clean_url,topic from articles_table", con)



