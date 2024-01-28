import pandas as pandas
import spacy #spacy with CUDA
from fuzzywuzzy import fuzz
import math
from unidecode import unidecode
import re


def tokenize_lemmatize(text):
    spacy.prefer_gpu()
    nlp = spacy.load("pl_core_news_lg")
    if not text:
        return None
    doc = nlp(text)
    lemmas = [unidecode(token.lemma_.lower()) for token in doc if not token.is_punct]
    return " ".join(lemmas)


def process_df_summary(dataframe: pandas.DataFrame) -> pandas.DataFrame:
    dataframe['tk_lemmatized'] = dataframe['summary'].apply(tokenize_lemmatize)
    return dataframe


def retrieve_filtered(dataframe, keyword):
    def is_keyword_present(summary):
        if summary:
            keyword_pattern = re.compile(r'\b' + re.escape(unidecode(keyword.lower())) + r'\b', flags=re.IGNORECASE | re.UNICODE)
            return bool(re.search(keyword_pattern, unidecode(summary.lower()))) or \
            fuzz.partial_ratio(unidecode(keyword.lower()), unidecode(summary.lower())) > 75
        else:
            return False
    
    dataframe['is_present'] = dataframe['summary'].apply(is_keyword_present)
    # dataframe[['id', 'title', 'summary', 'engine_size', 'bhp_count', 'mileage', 'fuel', 'gearbox', 'year', 'price']]
    dataframe = dataframe.loc[dataframe['is_present'] == True]
    return dataframe


def calculate_stats(dataframe):
    print(len(dataframe))
    if len(dataframe) == 0:
        return "No matching cars found!"
    return {
        "avg_price": dataframe['price'].mean(),
        "avg_year": math.ceil(dataframe['year'].mean()),
        "avg_mileage": dataframe['mileage'].mean(),
        "avg_bhp": dataframe['bhp_count'].mean(),
        "offer_count": dataframe['title'].count(),
        "min_price": dataframe['price'].min(),
        "max_price": dataframe['price'].max(),
    }




