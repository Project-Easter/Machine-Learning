import pandas as pd 
import pickle as pkl 
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

class recommendation:
    
    def __init__(self):
        self.df = pd.read_csv('model_2_data_updated.csv')
        self.preprocessing()

    def preprocessing(self):
        self.df.dropna(inplace=True)
        mat = self.df.pivot(index=' isbn', columns='user_id', values=' no_of_exchanges').fillna(0)
        self.sparse_mat = csr_matrix(mat.values)
        book_map = self.df[[' isbn',' title']]
        self.hash_map = { book : i for i,book in enumerate(list(book_map.set_index(' isbn').loc[mat.index][' title']))}
        self.book_dict = dict(zip(book_map[' isbn'], book_map[' title']))

    def loading_model(self):
        self.model = NearestNeighbors(algorithm='brute',metric='cosine')
        self.model.fit(self.sparse_mat)
    
    def get_title(self,isbn):
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
        recoms = self.get_title(isbn)
        isbns = []
        for book_name in recoms:
            for isb,title in self.book_dict.items():
                if title == book_name:
                    isbns.append(isb)
        return isbns
       


