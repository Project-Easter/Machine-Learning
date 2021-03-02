# Importing necessary modules
import pandas as pd 
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity 
from sklearn.feature_extraction.text import TfidfVectorizer 

class recommendation:
    """
    This class makes recommendations based on the choices of user, like favourite author and genre.
    This class has methods which help in doing these tasks.
    """
    def __init__(self):
        """
        Constructor for recommendation class
        """
        self.preprocessing()

    def preprocessing(self):
        """
        Function for cleaning data which is to be used for recommendations
        """
        self.df = pd.read_csv('flutter\model_1\model1_data.csv') # loading csv file
        self.df = self.df.sample(frac=1) # shuffling data
        self.df.drop('Unnamed: 0', axis=1, inplace=True) # dropping 'Unnamed: 0' column
        self.df.dropna(inplace=True) # dropping null values

    def recommend_with_genre(self,title,genre):
        """
        Function for making recommendations of books based on genre of a particular book

        Parameters
        ----------
        title : title of a book
        genre : genre of that book

        Return
        ---------
        sig : list of recommended books
        """
        book_data = self.df.loc[self.df['Genre'] == genre]
        book_data.reset_index(level = 0, inplace = True) # making a dataframe of books with selected genre
        indices = pd.Series(book_data.index, index = book_data['Title'])

        tf = TfidfVectorizer(analyzer = 'word', ngram_range = (2,2), min_df = 1, stop_words = 'english')
        tfidf_mat = tf.fit_transform(book_data['Title']) # initializing and using TfidfVectorizer()
        sg = cosine_similarity(tfidf_mat, tfidf_mat) # Finding cosine similarity

        idx = indices[title]

        sig = list(enumerate(sg[idx]))

        sig = sorted(sig, key=lambda x : x[1], reverse = True)
        sig = sig[1:6]

        return sig

    def get_title_recommendations(self,title,genre):
        """
        Function for getting names of recommended books based on a particular book

        Parameters
        -----------
        title : name of a book
        genre : genre of that book

        Return
        -----------
        recommendations : list of title of recommended books
        """
        book_data = self.df.loc[self.df['Genre'] == genre]
        book_data.reset_index(level = 0, inplace = True)

        recoms  = self.recommend_with_genre(title,genre)

        book_indices = [i[0] for i in recoms]

        recommendations = []
        for i in book_indices:
            recommendations.append(book_data['Title'].loc[i])
        return recommendations
