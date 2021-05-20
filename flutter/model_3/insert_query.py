from urllib.request import urlopen
import json 
from uuid import uuid1
import datetime
import time 

columns = "id, isbn, title, description, author, genre, language, pages, image, rating, addedAt, latitude, longitude, ownerId"

insert_query = "INSERT INTO \"Book\"(" + columns + ")\nVALUES("

genres_list = ['ACTION', 'ADVENTURE', 'BIOGRAPHY', 'BUSINESS', 'CHILDRENS', 'COOKING', 'CRIME', 'DRAMA', 'DICTIONARY', 'ENCYCLOPEDIA', 'GUIDE', 'FAIRYTALE','FANTASY', 'HEALTH', 'HISTORICAL', 'HUMOR', 'HORROR', 'JOURNAL', 'MATH', 'OTHERS', 'ROMANCE', 'PHILOSOPHY', 'RELIGION', 'SCIENCE_FICTION', 'SELF_DEVELOPMENT', 'SPORTS' ,'TRAVEL' ,'WESTERN']

def update_query(isbn=None):
    
    base_api_link = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'

    with urlopen(base_api_link + str(isbn)) as f:
        text = f.read()

    decoded_text = text.decode('utf-8')
    obj = json.loads(decoded_text)

    with open('file.json', 'w') as json_file:
        json.dump(obj, json_file)

    volume_info = obj['items'][0]
    authors = obj['items'][0]['volumeInfo']['authors']
    langs = {
        'en': 'ENGLISH',
        'fr': 'FRENCH',
        'es': 'SPANISH',
        'de': 'GERMAM',
        'hi': 'HINDI'
    }

    user_id = str(uuid1())

    title = volume_info['volumeInfo']['title']
    author = authors[0]
    try:
        genres = volume_info['volumeInfo']['categories']
    except KeyError:
        genres = ''
    try:
        language = langs[volume_info['volumeInfo']['language']]
    except KeyError:
        language = 'OTHERS'
    try:
        ratings = volume_info['volumeInfo']['averageRating']
    except KeyError:
        ratings = 0

    pages = volume_info['volumeInfo']['pageCount']
    image = volume_info['volumeInfo']['imageLinks']['smallThumbnail']
    description = volume_info['volumeInfo']['description']
    description = description.replace("\'","")
    addedAt = datetime.datetime.fromtimestamp(time.time()).strftime("%d-%m-%Y %H:%M:S")
    ownerId = '41e5b097-e09d-427b-a770-45aef3eedfd6'
    genre = genre_selector(genres)

    query  = insert_query + '\'' + user_id + "\',\'" + str(isbn) + "\',\'" + title + "\',E\'" + description + "\',\'" + author + "\',\'" + genre + "\',\'" + language + "\',\'" + str(pages) + "\',\'" + image + "\'," + str(ratings) + ",\'" + addedAt + "\',44,-184,\'" + ownerId + "\');"

    return query


def genre_selector(genres=None):

    genres = [ x.upper() for x in genres]
    genres = [ x.replace(' ','_') for x in genres]

    cross_map = [[(i,j) for i in genres] for j in genres_list]

    final_genre = 'OTHERS'

    for cross in cross_map:
        for p in cross:
            if p[0] in p[1]:
                final_genre = p[1]

    return final_genre
    

    

