import requests
from bs4 import BeautifulSoup
import csv
import os
from pygame import mixer

#THIS PROGRAM ONLY FILLS THE CSV FILE, THIS IS ONLY A PROOF OF API USAGE

abspath = os.path.abspath(__file__) #stupid python directory bullcrap, im angry. 
dname = os.path.dirname(abspath) # do ABSOLUTELY FIRST
os.chdir(dname)

mixer.init() #MUSIC
mixer.music.load(os.path.join("Music.mp3"))
mixer.music.play(loops=-1)


def fill_starship_CSV():
    with open("starship.csv", mode='w', newline='') as csvfile:
        fieldnames = ['url', 'movie']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(2, 75):  # first starship is in index 2, last is in 75
            response = requests.get(f'https://swapi.dev/api/starships/{i}/')
            data = response.json()
            if data != {'detail': 'Not found'}:
                name = data["name"].replace(" ", "_")  # Get the name of the ship from the JSON
                url = getShipURL(name)
                if url is not None:
                    moviejson = data['films'][0]  # Get the first film's URL
                    movietitle = getMovieID(moviejson)
                    writer.writerow({'url': url, 'movie': movietitle})
                    print(f'{name} {movietitle}')

def getMovieID(StringURL):
    response = requests.get(StringURL)
    data = response.json()
    return data.get("title", None)  # Get the movie title

def getShipURL(shipName):
    wikiRequest = requests.get(f"https://starwars.fandom.com/wiki/{shipName}")  # Get the wiki of the ship based on the ship's name.
    soup = BeautifulSoup(wikiRequest.text, 'html.parser')
    wikiImgURL = soup.find('a', {'class': "image image-thumbnail"})
    if wikiImgURL:
        imgTag = wikiImgURL.find('img')
        if imgTag and 'src' in imgTag.attrs:
            return imgTag['src']
    return None

# Execute the function to fill the CSV
fill_starship_CSV()
