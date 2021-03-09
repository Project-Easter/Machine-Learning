from flask import Flask, jsonify, request
from script import recommendation
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/recommend_isbn/', methods = ['GET'])
def recommend_with_isbn():
    isbn = int(request.args.get("isbn",None))
    re = recommendation() # initialising class object
    recommend_list = re.get_recommedations(isbn) # getting list of isbns of recommended books
    return jsonify(recommend_list)

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
