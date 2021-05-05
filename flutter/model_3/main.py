from flask import Flask, jsonify, request
from script import recommendation
from gen_script import gen_recommendation
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/recommend_isbn/', methods = ['GET'])
def recommend_with_isbn():
    isbn = int(request.args.get("isbn",None))
    try:
        re = recommendation() # initialising class object
        recommend_list = re.get_recommedations(isbn) # getting list of isbns of recommended books
        return jsonify(recommend_list)
    except KeyError:
        re.append_missing(isbn)
        return 'Book was missing! added to database!'

@app.route('/book_title/', methods = ['GET'])
def get_title():
    title = request.args.get("title", None)
    re = recommendation() # initialising class object
    matches = re.matching(title) # getting list of matching books
    match_list = {}
    i = int(0)
    for match in matches:
        book_number = "Book_" + str(i+1) # initialising book_number
        title = match[0] # getting title of matching book 
        isbn = match[1] # getting isbn of matching isbn
        match_list[book_number] = {'Title' : title, 'ISBN' : isbn} # making nested dictionary
        i += 1 
    
    return jsonify(match_list)

@app.route('/recommend_with_genre/', methods = ['GET'])
def recommend_with_genre():
    isbn = int(request.args.get('isbn', None))
    genre = request.args.get('genre', None)
    genre = genre + ' '
    try:
        re = gen_recommendation(genre=genre) # initialising class object
        recommend_list = re.get_recommedations(isbn) # getting list of isbns of recommended books
        return jsonify(recommend_list)
    except Exception as e:
        return str(e)

@app.route('/matching_book/', methods = ['GET'])
def get_book_details():
    isbn = int(request.args.get('isbn', None))
    title = request.args.get('title', None)
    try:
        re = recommendation()
        result = re.matching_book(title, isbn)
        return jsonify(result)
    except Exception as e:
        return str(e)

@app.route('/random_books/', methods = ['GET'])
def get_random_books():
    genre = request.args.get('genre', None)
    try:
        re = recommendation()
        result = re.random_books(genre=genre)
        return jsonify(result)
    except Exception as e:
        return str(e)

# if __name__ == "__main__":
#     app.run(debug=True)