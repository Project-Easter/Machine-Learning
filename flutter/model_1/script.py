# Importing necessary modules
import pandas as pd 
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity 
from sklearn.feature_extraction.text import TfidfVectorizer 

class recommendation:

    def __init__(self):
        """
        Constructor for recommendation class
        """
        self.preprocessing()

    def preprocessing(self):
        self.df = pd.read_csv('flutter\model_1\model1_data.csv')
        self.df = self.df.sample(frac=1)
        self.df.drop('Unnamed: 0', axis=1, inplace=True)
        self.df.dropna(inplace=True)

    def recommend_with_genre(self,title,genre):
        book_data = self.df.loc[self.df['Genre'] == genre]
        book_data.reset_index(level = 0, inplace = True)
        indices = pd.Series(book_data.index, index = book_data['Title'])

        tf = TfidfVectorizer(analyzer = 'word', ngram_range = (2,2), min_df = 1, stop_words = 'english')
        tfidf_mat = tf.fit_transform(book_data['Title'])
        sg = cosine_similarity(tfidf_mat, tfidf_mat)

        idx = indices[title]

        sig = list(enumerate(sg[idx]))

        sig = sorted(sig, key=lambda x : x[1], reverse = True)
        sig = sig[1:6]

        return sig

    def get_title_recommendations(self,title,genre):
        book_data = self.df.loc[self.df['Genre'] == genre]
        book_data.reset_index(level = 0, inplace = True)

        recoms  = self.recommend_with_genre(title,genre)

        book_indices = [i[0] for i in recoms]

        recommendations = []
        for i in book_indices:
            recommendations.append(book_data['Title'].loc[i])
        return recommendations
