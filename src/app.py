from datetime import datetime
from src.models.upcomingmovies import Upmovies

__author__ = 'Akshay_Rahar'

import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

from src.common.database import Database
from src.models.upcomingmovies import Upmovies

app = Flask(__name__)
app.secret_key= "Akshay Rahar"
Database.initialize()

fandango_link = 'http://www.fandango.com/moviescomingsoon?pn='
fandango_link1 = '&GenreFilter='

def show_title(genre, page_no):
    title=[]
    request = requests.get(fandango_link+str(page_no)+fandango_link1+str(genre))
    content = request.content

    soup = BeautifulSoup(content, "html.parser")
    soup2 = soup.find('div', {'class':'movie-ls-group'})
    elements = soup2.find_all('a', {'class': 'visual-title dark'})

    for element in elements:
        title.append(element.text)

    print(len(title))
    return title


def release_date(genre, page_no):
    release_date = []
    request = requests.get(fandango_link+str(page_no)+fandango_link1+str(genre))
    content = request.content

    soup = BeautifulSoup(content, "html.parser")
    soup2 = soup.find('div', {'class':'movie-ls-group'})
    elements = soup2.find_all('span', {'class': 'visual-sub-title'})

    for element in elements:
        release_date.append(element.text)

    return release_date


def poster(genre, page_no):
    poster_link = []
    request = requests.get(fandango_link+str(page_no)+fandango_link1+str(genre))
    content = request.content

    soup = BeautifulSoup(content, "html.parser")
    soup2 = soup.find('div', {'class':'movie-ls-group'})
    elements = soup2.find_all('img')

    for element in elements:
        poster_link.append(element.get('src'))

    return poster_link


def update_database(genre):
    show = Upmovies(None, None, None)
    page_no = 1
    print("rahar1")
    titles = show_title(genre, page_no)
    print("rahar2")
    release_dates = release_date(genre, page_no)
    poster_links = poster(genre, page_no)

    print(len(poster_links))

    Database.remove_all(genre)

    i=0
    while i<len(titles):
        show.title = titles[i]
        show.release_date = release_dates[i]
        show.poster = poster_links[i]
        show.save_to_mongo(genre)
        i=i+1

    print("Database Updated")


genres= ['Action/Adventure', 'Drama', 'Comedy', 'Kids', 'Horror',
        'Romance', 'Sci-Fi/Fantasy', 'Animated', 'Documentaries',
        '3D', 'Suspense', 'Indie', 'Foreign',
        'Concert/Special Events', 'Western', 'War', 'Music/Performing Arts',
        ]


@app.route('/<string:genre>')
@app.route('/')

def home(genre = 'Drama'):

    new_title = []
    new_release_date = []
    new_poster_links = []

    #update database
    print("akshay_rahar")
    update_database(genre)
    print("akshay_rahar1")

    title= Database.find_coloumn(genre,"title")
    for t in title:
        new_title.append(t['title'])

    #The lstrip() method will remove leading whitespaces, newline and tab characters on a string beginning:
    i=0
    while i< len(new_title):
          new_title[i]=new_title[i].lstrip()
          print(new_title[i])
          i=i+1


    poster_links = Database.find_coloumn(genre, "poster")
    for poster_link in poster_links:
        new_poster_links.append(poster_link['poster'])

    release_dates = Database.find_coloumn(genre, "release_date")
    for date in release_dates:
        new_release_date.append(date['release_date'])


    return render_template('movieslist.html',
                           google_link='https://www.google.com/search?q=',
                           youtube_link='https://www.youtube.com/results?search_query=',
                           elements=new_title,
                           release_dates=new_release_date,
                           poster_links=new_poster_links,
                           genres=genres,
                           current_genre=genre,
                           length=len(new_title))



if __name__ == '__main__':
        # enable debug mode so Flask will actually tell us what the error is.
    app.debug = True
    app.run(port=4996)

