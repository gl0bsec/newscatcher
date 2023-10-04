
#%%
## Import packages 
import spacy 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from bertopic import BERTopic

#%% 
## Process data 
## TODO Locations 
### TODO Add col names vader_neg, vader_neu, vader_pos, vader_pol
### TODO Database schema, multivar process 

analyzer = SentimentIntensityAnalyzer()
nlp = spacy.load("en_core_web_trf",exclude=['tagger', 'attribute_ruler', 'lemmatizer'])

def flatten_concatenation(matrix):
     flat_list = []
     for row in matrix:
         flat_list += row
     return flat_list

def process_text(data, var):
    text_data = [k[var] for k in data]
    uuid = [k[0] for k in data]
    sentiment = []
    entities = []
    # Sentiment  
    for k in data:
        sentiment.append(analyzer.polarity_scores(k[var]))
        # Basic NLP
        doc = nlp(k[var])
        ents = []
        for ent in doc.ents:
            ents.append(dict([('ent_text',ent.text),('ent_type',ent.label_)]))
        entities.append(ents)
    
    # BERTopic 
    # topic_model = BERTopic(embedding_model=nlp)
    # topics, probs = topic_model.fit_transform(text_data)
    # fig = topic_model.visualize_topics()
    # fig.show()
    
    return list(zip(uuid,[e['neg']for e in sentiment],[e['neu']for e in sentiment]
                    ,[e['pos']for e in sentiment],[e['compound']for e in sentiment],entities))

