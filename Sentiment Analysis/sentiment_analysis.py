import pandas as pd
import re
import nltk
import os
from zipfile import ZipFile
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def download_nltk_packages():
    # DOWNLOADING NECCESSARY FILES FOR THE NLTK TO WORK.
    if not os.path.exists(os.path.join(nltk.data.find('corpora'), 'stopwords')):
        nltk.download('stopwords')
    if not os.path.exists(os.path.join(nltk.data.find('tokenizers'), 'punkt', 'english.pickle')):
        nltk.download('punkt')
    # wordnet "package" seems bugged, doesn't self-extract. Gotta extract manually in the destination directory
    wordnet_path = os.path.join(nltk.data.find('corpora'), 'wordnet')    
    if not os.path.exists(wordnet_path):
        nltk.download('wordnet')
        with ZipFile(os.path.join(nltk.data.find('corpora'), 'wordnet.zip'), 'r') as zip_ref:
            zip_ref.extractall(wordnet_path)

def clean_data(data):
    """Preprocessing the data to clean the punctuations, stopwords etc."""
    # Removing dots, commas, apostrophes... There might be a way with string.punctuation but it might remove things I want to keep like / to see reviews like 9/10, 6/10 etc.
    # Not sure if / are a necessity though
    data = re.sub('[!?,.;:()*"]', '', data)
    # Converting the data to all lower case letters
    data = data.lower()
    # Adding stopwords
    custom_stopwords = ["'ve", "'s", "'m" ]
    nltk_stop_words = set(stopwords.words('english'))
    my_stop_words = nltk_stop_words.union(custom_stopwords)
    # Tokenizing the words
    tokens = word_tokenize(data)
    data = [word for word in tokens if not word in my_stop_words]
    data = ' '.join(data)   
    return data

def prepare_data(conn):
    df = pd.read_sql_query("SELECT feedback, reviewText FROM reviews", conn)
    df['cleanText'] = df['reviewText'].apply(clean_data)
    X = df['cleanText'] # Independent variable
    y = df['feedback'] # Dependent variable 
    # Splitting data into 80% train and 20% test sets, seed set to 100
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=100)
    return X_train, X_test, y_train, y_test
       
        
        