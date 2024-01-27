import pandas as pandas
import spacy #spacy with CUDA
from fuzzywuzzy import fuzz
import math


def process_df_summary(dataframe: pandas.DataFrame) -> pandas.DataFrame:
    spacy.prefer_gpu()
    nlp = spacy.load("pl_core_news_lg")

    def tokenize_lemmatize(text):
        if not text:
            return None
        doc = nlp(text)
        lemmas = [token.lemma_.lower() for token in doc if not token.is_punct]
        print("lemmas ", " ".join(lemmas))
        print("\n", "ori: ", doc)
        return " ".join(lemmas)
    
    dataframe['tk_lemmatized'] = dataframe['summary'].apply(tokenize_lemmatize)
    return dataframe


def retrieve_filtered(dataframe, keyword):
    def is_keyword_present(summary):
        lemmas = summary
        return fuzz.partial_ratio(keyword.lower(), lemmas) > 75
    
    dataframe['is_present'] = dataframe['summary'].apply(is_keyword_present)
    dataframe[['id', 'title', 'summary', 'engine_size', 'bhp_count', 'mileage', 'fuel', 'gearbox', 'year', 'price']]
    dataframe = dataframe.loc[dataframe['is_present'] == True]
    return dataframe


def calculate_stats(dataframe):
    print(len(dataframe))
    if len(dataframe) == 0:
        return "No matching cars found!"
    # avg car
    return {
    "avg_price": dataframe['price'].mean(),
    "avg_year": math.ceil(dataframe['year'].mean()),
    "avg_mileage": dataframe['mileage'].mean(),
    "avg_bhp": dataframe['bhp_count'].mean(),
    "offer_count": dataframe['title'].count(),

    # extremes
    "min_price": dataframe['price'].min(),
    "max_price": dataframe['price'].max(),
    }




