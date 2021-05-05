import pandas as pd 
import pickle as pkl 
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import fuzz 
from urllib.request import urlopen
import json
import shortuuid
import random

class recommendation:
    """
    Class containing all necessary methods for making recommendations based on title as well as isbn of a certain book
    """
    def __init__(self):
        """
        Constructor for initialising class with dataframe
        """
        self.df = pd.read_csv('model_data_updated.csv', encoding='latin-1', error_bad_lines=False)
        self.preprocessing()
        self.loading_model()

    def preprocessing(self):
        """
        Function for creating all necessary variables for making recommendations

        sparse_mat - sparse matrix between user_id and isbn made with coressponding no of exchanges
        book_dict - dictionary mapping isbn with book title
        hash_map - dictionary mapping book title with pivot matrix index
        """
        self.df.dropna(inplace=True)
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
       
    def matching(self,fav_book):
        """
        This function matches search query with the books available in our database and returns the titles and isbns

        Parameters
        -----------
        fav_book : Keyword used for searching book

        Return
        -----------
        match : List of matching books with title and isbn
        
        """
        match = [] # list storing the names of matched books 
        # getting the matches 
        for isbn, title in self.book_dict.items():
            ratio = fuzz.ratio(title.lower(), fav_book.lower())
            if ratio >= 50:
                match.append((title, isbn, ratio))
        # sorting the titles in descending order
        match = sorted(match, key = lambda x : x[2])[::-1]
        if not match:
            print("No match found")
            return None 
        else:
            print("Found possible matches in our database: {}".format([x[0] for x in match]))
            return match 

    def append_missing(self, isbn):
        """
        This function automatically appends the records for missing book's isbn.

        Parameters
        -----------
        isbn: ISBN of missing book

        Return
        -----------
        None, appends the new record to model_2_data_updated.csv
        """
        self.base_api_link = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'
        with urlopen(self.base_api_link + str(isbn)) as f:
            text = f.read()

        decoded_text = text.decode('utf-8')
        obj = json.loads(decoded_text)

        volume_info = obj['items'][0]
        authors = obj['items'][0]['volumeInfo']['authors']
        langs = {
            'en': 'English',
            'fr': 'French',
            'es': 'Spanish',
            'de': 'German',
            'ru': 'Russian',
            'hi': 'Hindi'
        }

        f = open('model_data_updated.csv', 'a')

        user_id = shortuuid.uuid()
        no_of_exchanges = random.randrange(0,10)

        title = volume_info['volumeInfo']['title']
        author = authors[0]
        publisher = volume_info['volumeInfo']['publisher']
        try:
            language = langs[volume_info['volumeInfo']['language']]
        except KeyError:
            language = ''
        try:
            ratings = volume_info['volumeInfo']['averageRating']
        except KeyError:
            ratings = 0

        try:
            f.write(user_id + ',' + title.replace(',','|') + ',' + author.replace(',','|') + ',' + publisher.replace(',','|') + ',' + str(isbn) + ',' + language + ',' + str(no_of_exchanges) + ',' + str(ratings) + '\n')
            print('Record Added')
        except UnicodeDecodeError:
            pass
        f.close()

    def matching_book(self, book_isbn, book_name=None):
        """
        This function returns the details of the book whose name or isbn is provided.

        Parameters
        ------------
        book_isbn : isbn of the book 
        book_name : title of the book

        Return 
        ------------
        self.book_details(book_isbn) : dictionary having title, isbn, author and genre of the book
        """
        if book_name is None:
            return self.book_details(book_isbn)
            
        books = self.matching(book_name)
        for book in books:
            if book == book_name:
                isbn = self.df[' isbn'][self.df[' title']==book]
                return self.book_details(isbn)
        
        return self.book_details(book_isbn)
        
        
    def book_details(self, isbn):
        """
        This function return the details of a book whose isbn in passed

        Parameters
        -----------
        isbn : isbn of the book

        Return 
        ----------
        details : dictionary of the book with its title, author, isbn and genre
        """
        details = {}
        book_info = self.df[self.df[' isbn'] == isbn]
        details['Name'] = book_info.iloc[0][' title']
        details['ISBN'] = isbn
        details['Author'] = book_info.iloc[0][' author']
        details['Genre'] = book_info.iloc[0][' genre']
        return details
    
    def random_books(self, genre):
        """
        This function returns 5 random books based on the genre passed

        Parameters
        -----------
        genre : genre whose books are required

        Return 
        ----------
        books : dictionary of 5 random books with their details
        """
        genre = genre + ' '
        books_genre = self.df[self.df[' genre']==genre].sample(5)
        print(len(books_genre))
        books = {}
        for i in range(5):
            books[i+1] = self.book_details(books_genre.iloc[i][' isbn'])
        
        return books


