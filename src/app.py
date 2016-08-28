
__author__ = 'Akshay_Rahar'

import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

from src.common.database import Database
from src.models.upcomingmovies import Upmovies

app = Flask(__name__)
app.secret_key= "Akshay Rahar"

#initialize the database
Database.initialize()

fandango_link = 'http://www.fandango.com/moviescomingsoon?pn='
fandango_link1 = '&GenreFilter='

#To get titles of the given genre
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


##To get release_dates of the given genre
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


##To get posters of the given genre
def poster(genre, page_no):
    poster_link = []
    request = requests.get(fandango_link+str(page_no)+fandango_link1+str(genre))
    content = request.content

    soup = BeautifulSoup(content, "html.parser")
    imgs = soup.find_all('img', {'class': 'visual-thumb'})
    for img in imgs:
        poster_link.append(img.get('data-src'))
    return poster_link


#update the database
def update_database(genre):
    show = Upmovies(None, None, None)
    page_no = 1
    print("rahar1")
    titles = show_title(genre, page_no)
    print("rahar2")
    release_dates = release_date(genre, page_no)
    poster_links = poster(genre, page_no)

    print(len(poster_links))

    #first remove the database
    Database.remove_all(genre)

    #now update the database
    i=0
    while i<len(titles):
        show.title = titles[i]
        show.release_date = release_dates[i]
        show.poster = poster_links[i]
        show.save_to_mongo(genre)
        i=i+1

    print("Database Updated")


#name of all genres
genres= ['Action/Adventure', 'Drama', 'Comedy', 'Kids', 'Horror',
        'Romance', 'Sci-Fi/Fantasy', 'Animated', 'Documentary',
        '3D', 'Suspense/Thriller', 'Indie', 'Art House/Foreign',
        'Concert/Special Events', 'Western', 'Historical Film',
        'War', 'Music/Performing Arts'
        ]


@app.route('/<string:genre>')
@app.route('/')

#Home page= Drama
def home(genre='Drama'):

    new_title = []
    new_release_date = []
    new_poster_links = []

    #update database
    print("akshay_rahar")

    if (genre=="Kids"):
        genre="Family"

    update_database(genre)
    print("akshay_rahar1")

    #find the all titles of the given genre from database
    title= Database.find_coloumn(genre,"title")
    for t in title:
        new_title.append(t['title'])


    #The lstrip() method will remove leading whitespaces, newline and tab characters on a string beginning
    i=0
    while i< len(new_title):
          new_title[i]=new_title[i].lstrip()
          print(new_title[i])
          i=i+1


    #find the all posters of the given genre from database
    poster_links = Database.find_coloumn(genre, "poster")
    for poster_link in poster_links:
        new_poster_links.append(poster_link['poster'])

    i=0
    while i< len(new_poster_links):
          print(new_poster_links[i])
          i=i+1



    #find the all release_dates of the given genre from database
    release_dates = Database.find_coloumn(genre, "release_date")
    for date in release_dates:
        new_release_date.append(date['release_date'])

    #rename the genre
    if (genre=="Family"):
        genre="Kids"

    #Provide all the data to movielist.html file
    return render_template('movieslist.html',
                           google_link='https://www.google.com/search?q=',
                           youtube_link='https://www.youtube.com/results?search_query=',
                           elements=new_title,
                           release_dates=new_release_date,
                           poster_links=new_poster_links,
                           genres=genres,
                           current_genre=genre,
                           length=len(new_title))

