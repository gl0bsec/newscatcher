#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import ast

# Load the CSV file into a DataFrame
df = pd.read_csv('news_analysis.csv')

# Function to safely extract "PERSON" entities
def safe_extract_person_entities(entity_list_str):
    try:
        entity_list = ast.literal_eval(entity_list_str)
        persons = [entity['ent_text'] for entity in entity_list if entity['ent_type'] == 'PERSON']
        return persons
    except (ValueError, SyntaxError):
        return []
df['person_entities'] = df['spacy_entities'].apply(safe_extract_person_entities)

# Function to extract all entity types
def extract_entity_types(entity_list):
    return [entity['ent_type'] for entity in entity_list]
df['entity_types'] = df['spacy_entities'].apply(ast.literal_eval).apply(extract_entity_types)

#%% 
# Count entity types
all_entity_types = [ent_type for sublist in df['entity_types'].tolist() for ent_type in sublist]
entity_type_counts = Counter(all_entity_types)
entity_type_df = pd.DataFrame.from_dict(entity_type_counts, orient='index', columns=['Count']).reset_index()
entity_type_df.rename(columns={'index': 'Entity Type'}, inplace=True)

# Plot for entity types
plt.figure(figsize=(12, 8))
sns.barplot(x='Count', y='Entity Type', data=entity_type_df.sort_values('Count', ascending=False), palette='viridis')
plt.title('Frequency of Each Entity Type')
plt.xlabel('Count')
plt.ylabel('Entity Type')
plt.show()

# Group data by clean_url for sentiment
grouped_sentiment_df = df.groupby('clean_url').agg({
    'compound': 'mean'
}).reset_index().sort_values('compound')

# Plot for average sentiment by clean_url
plt.figure(figsize=(14, 8))
sns.barplot(x='compound', y='clean_url', data=grouped_sentiment_df, palette='coolwarm_r')
plt.title('Average Sentiment by Clean URL (Reversed Color Coding)')
plt.xlabel('Average Compound Sentiment')
plt.ylabel('Clean URL')
plt.show()

# Count the number of entries for each 'clean_url'
url_count_df = df['clean_url'].value_counts().reset_index()
url_count_df.columns = ['clean_url', 'Count']
url_count_df = url_count_df.sort_values('Count', ascending=True)

# Plot for count of entries by clean_url
plt.figure(figsize=(14, 8))
sns.barplot(x='Count', y='clean_url', data=url_count_df, palette='mako')
plt.title('Count of Entries by Clean URL')
plt.xlabel('Count')
plt.ylabel('Clean URL')
plt.show()
# %%
