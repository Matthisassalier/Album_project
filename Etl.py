import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from requests import get
import requests
import json

class Album:
    title:str
    author:str
    year:int
    
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        
    def __str__(self):
        return f"{self.author}:{self.title} ({self.year})"

class AlbumRepository:
    Album_list =[]
    
    def return_list(self):
        return self.Album_list 
  
    def add_album(self, album_data):
        self.Album_list.append(Album(**album_data))
        print ("The album is added")
    
    def delete_album(self, album_data):
        for album in self.Album_list:

            if album.title == album_data['title']:
                self.Album_list.remove(album)
        print ("The album is deleted")

    def modify_album(self,album_data,update):
        
        for album in self.Album_list:
            if album.title == album_data['title']:
                album.title = update['title']
                album.author = update['author']
                album.year = update['year']
            
        print ("The album is modified")



def scrap_album(artist):
    albums=[]
    url = requests.get(f"https://www.allformusic.fr/{artist}/discographie")
    soup = BeautifulSoup(url.content, "html5lib")
    id = soup.find(id="disco-album")
    alldiv = id.find_all("div")

    for disco in alldiv:
        albums.append(Album(disco.strong.get_text(), artist,int(disco.span.get_text()[-4:])))
    return albums

discography= []
albums = []
artist=["jamiroquai", "daft-punk", "justice"]

for i in artist:
    albums+= scrap_album(i)

for i in albums:
    jsonString = (i.__dict__)
    discography.append(jsonString)

with open('discography.json', 'w') as a:
    json.dump(discography, a, indent=8)
    print("JSON file created")