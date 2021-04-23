import pandas as pd 
import pickle as pkl 
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import fuzz 
from urllib.request import urlopen
import json
import shortuuid
import random

class gen_recommendation:
    """
    Class containing all necessary methods for making recommendations based on title as well as isbn of a certain book
    """
    def __init__(self, genre):
        """
        Constructor for initialising class with dataframe
        """
        self.df = pd.read_csv('model_data_updated.csv', encoding='latin-1', error_bad_lines=False)
        self.preprocessing(genre)
        self.loading_model()

    def preprocessing(self, genre):
        """
        Function for creating all necessary variables for making recommendations

        sparse_mat - sparse matrix between user_id and isbn made with coressponding no of exchanges
        book_dict - dictionary mapping isbn with book title
        hash_map - dictionary mapping book title with pivot matrix index
        """
        self.df.dropna(inplace=True)
        self.df = self.df[self.df[' genre']==genre]
        # making pivot matrix
        mat = self.df.pivot(index=' isbn', columns='user_id', values=' no_of_exchanges').fillna(0)
        self.sparse_mat = csr_matrix(mat.values)
        # making a crosstab of isbn and title from df
        self.book_map = self.df[[' isbn',' title']]
        self.hash_map = { book : i for i,book in enumerate(list(self.book_map.set_index(' isbn').loc[mat.index][' title']))}
        self.book_dict = dict(zip(self.book_map[' isbn'], self.book_map[' title']))

    def loading_model(self):
        """
        Function initialising model which will be used for recommendations
        """
        self.model = pkl.load(open('model_file.pkl','rb'))
        self.model.fit(self.sparse_mat)

    def get_title(self,isbn):
        """
        Function to return title of recommended books using isbn

        Parameters
        -----------
        model : base model globally trained to recommend books
        isbn : isbn of book from which recommendations are to be made

        Return
        -----------
        recoms : list of titles of recommended books
        """
        title = self.book_dict[isbn]
        r,d = self.model.kneighbors(self.sparse_mat[self.hash_map[title]],n_neighbors=11)
        recoms = [] 
        recommends = sorted(list(zip(d.squeeze().tolist(),r.squeeze().tolist())),key=lambda x:x[1])[:0:-1]
        for (i,j) in recommends:
            for title, num in self.hash_map.items():
                if num == i:
                    recoms.append(title)
        return recoms
    
    def get_recommedations(self,isbn):
        """
        Function to isbn of recommended books by using a globally declared model

        Parameters
        ----------
        model - globally trained model for recommendations
        isbn - isbn of book from which recommendations are to be made

        Return
        ----------
        isbns - list of recommended books' isbns
        """
        recoms = self.get_title(isbn)
        isbns = []
        for book_name in recoms:
            for isb,title in self.book_dict.items():
                if title == book_name:
                    isbns.append(isb)
        return isbns