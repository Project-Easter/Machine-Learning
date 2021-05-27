from flask import Flask, jsonify, request
from script import recommendation
from gen_script import gen_recommendation
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

dist = None
lat = None
lon = None 

@app.route('/set_distance', methods = ['GET'])
def set_distance():
    distance = int(request.args.get("distance",None))
    latitude = int(request.args.get("latitude",None))
    longitude = int(request.args.get("longitude",None))
    global dist 
    dist = distance
    global lat 
    lat = latitude
    global lon 
    lon = longitude

re = recommendation(dist, lat, lon)

@app.route('/recommend_isbn/', methods = ['GET'])
def recommend_with_isbn():
    isbn = request.args.get("isbn",None) # initialising class object
    try:
        recommend_list = re.get_recommedations(isbn) # getting list of isbns of recommended books
        return jsonify(recommend_list)
    except KeyError:
        re.append_missing(isbn)
        return 'Book was missing! added to database!'

@app.route('/book_title/', methods = ['GET'])
def get_title():
    title = request.args.get("title", None) # initialising class object
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
    isbn = request.args.get('isbn', None)
    genre = request.args.get('genre', None)
    try:
        re = gen_recommendation(genre=genre) # initialising class object
        recommend_list = re.get_recommedations(isbn) # getting list of isbns of recommended books
        return jsonify(recommend_list)
    except Exception as e:
        return str(e)

@app.route('/matching_book/', methods = ['GET'])
def get_book_details():
    isbn = request.args.get('isbn', None)
    title = request.args.get('title', None)
    try:
        result = re.matching_book(isbn, title)
        return jsonify(result)
    except Exception as e:
        re.append_missing(isbn)
        return "Book was missing from the database, now added!"

@app.route('/random_books/', methods = ['GET'])
def get_random_books():
    genre = request.args.get('genre', None)
    try:
        result = re.random_books(genre=genre)
        return jsonify(result)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)