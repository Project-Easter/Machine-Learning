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

if __name__ == "__main__":
    app.run(debug = True)