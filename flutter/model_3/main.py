from flask import Flask, jsonify
from script import recommendation
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/recommend_isbn/<int:isbn>')
def recommend_with_isbn(isbn):
    re = recommendation()
    recommend_list = re.get_recommedations(isbn)
    return jsonify(recommend_list)

@app.route('/book_title/<string:title>')
def get_title(title):
    re = recommendation()
    matches = re.matching(title)
    match_list = {}
    i = int(0)
    for match in matches:
        book_number = "Book_" + str(i+1)
        title = match[0]
        isbn = match[1]
        match_list[book_number] = {'Title' : title, 'ISBN' : isbn}
        i += 1 
    
    return jsonify(match_list)
    
if __name__ == "__main__":
    app.run(debug = True)