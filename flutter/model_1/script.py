# Importing necessary modules
import pandas as pd 
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity 
from sklearn.feature_extraction import CountVectorizer, TfidfVectorizer 

class recommendation:
    def __init__(self):
        """
        Constructor for recommendation class
        """

    def preprocessing(self):
        self.df = pd.read_csv('model1_data.csv')
        self.df = self.df.sample(frac=1)
        self.df.drop('Unnamed: 0', axis=1, inplace=True)
        self.df.dropna(inplace=True)
        self.book_data = self.df.loc[self.df['Genre'] == genre]
        self.book_data.reset_index(level = 0, inplace = True)
        self.indices = pd.Series(self.book_data.index, index = self.book_data['Title'])

        self.tf = TfidfVectorizer(analyzer = 'word', ngram_range = (2,2), min_df = 1, stop_words = 'english')
        self.tfidf_mat = self.tf.fit_transform(self.book_data['Title'])

    def recommend_with_genre(title,genre,self.tfidf_mat):
        sg = cosine_similarity(self.tfidf_mat, self.tfidf_mat)

        idx = self.indices[title]

        sig = list(enumerate(sg[idx]))

        sig = sorted(sig, key=lambda x : x[1], reverse = True)
        sig = sig[1:6]

        return sig

    def get_title_recommedations(title,genre,self.tfidf_mat):
        recoms  = self.recommend_with_genre(title,genre)

        book_indices = [i[0] for i in recoms]

        recommendations = []
        for i in book_indices:
            recommendations.append(self.book_data['Title'].loc[i])
        return recommendations
