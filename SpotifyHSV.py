import os
import spotipy
import spotipy.util as util
import requests
import PIL as pil
from PIL import Image, ImageFilter
import colorsys
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as pypl
import urllib.request
import webbrowser
import subprocess
from time import sleep

# TO:DO[next version]: detect changes in playback state, so that it runs automatically
# here's an idea for the above; detect when playback progress = 0, so that the program runs again, ez

# TO:DO[next version]: place all these info in another .py file
os.environ["SPOTIPY_CLIENT_ID"] = "CLIENT-ID-HERE"
os.environ["SPOTIPY_CLIENT_SECRET"] = "CLIENT-SECRET-HERE"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8080"
username = "melroy_caeiro"
scope = "user-read-playback-state user-read-currently-playing"
uri = "http://localhost:8080"
currentTrack = 10000
x = 1

token = util.prompt_for_user_token(username, scope, os.environ["SPOTIPY_CLIENT_ID"], os.environ["SPOTIPY_CLIENT_SECRET"], uri)
sp = spotipy.Spotify(auth=token)

while(x == 1):
    playback = sp.current_playback()
    nowPlaying = sp.current_user_playing_track()
    trackNow = nowPlaying["item"]["id"]

    if (trackNow != currentTrack):

        try:

            trackname = nowPlaying["item"]["name"]
            artistname = nowPlaying["item"]["artists"][0]["name"]
            print("NOW PLAYING: " + trackname + " - " + artistname.upper())

            device = playback["device"]["name"]
            print("PLAYING ON: " + device)

            url = nowPlaying['item']['album']['images'][0]['url']
            r = requests.get(url, allow_redirects=True)
            open('SPOTIFY-Image.jpg', 'wb').write(r.content)

            album_art = pil.Image.open("SPOTIFY-Image.jpg")
            imageRGBvalues = np.asarray(album_art)
            pixelNum = len(imageRGBvalues)
            tupleNum = pixelNum*pixelNum
            rgbvalues1D = np.reshape(imageRGBvalues, (tupleNum,3))
            rgbvalues1D2 = rgbvalues1D/255
            #print(rgbvalues1D) # Debugging, displays a one-line array of tuples
            tempvalues = matplotlib.colors.rgb_to_hsv(rgbvalues1D2)
            #print(tempvalues) # Debugging, displays HSV values, converted from RGB values

            hsvValue = pd.DataFrame(tempvalues, columns = ["h", "s", "v"])
            hsvValue["h"] = 360 * hsvValue["h"]
            hsvValue["s"] = 100 * hsvValue["s"]
            hsvValue["v"] = 100 * hsvValue["v"]
            # print(hsvValue)

            hsvValueInt = hsvValue.astype(int)
            # print(hsvValueInt)

            satMax = 40  # Define saturation tolerances, as in minimum before colour = white
            valMax = 50  # Define value tolerances, as in minimum before colour = black

            x = 0
            while (x <= satMax):
                hsvValueInt = hsvValueInt[(hsvValueInt.s != x)]  # Filters whites through saturation limiting
                x += 1

            y = 0
            while (y <= valMax):
                hsvValueInt = hsvValueInt[hsvValueInt.v != y]  # Filters blacks through value/brightness limiting
                y += 1
            # print(hsvValueInt) # Debugging, displays filtered colour codes

            hsvValueMode1 = pd.DataFrame.mode(hsvValueInt, axis = 0).astype(int)
            print(hsvValueMode1)
            huedeletevalue = hsvValueMode1["h"][0]

            j = huedeletevalue - 10
            while(j <= huedeletevalue):

                hsvValueInt = hsvValueInt[hsvValueInt.h != j]
                j +=1

            hsvValueMode2 = pd.DataFrame.mode(hsvValueInt, axis=0).astype(int)
            print(hsvValueMode2)

            mode1RGBarr = np.array([hsvValueMode1["h"][0]/360, hsvValueMode1["s"][0]/100, hsvValueMode1["v"][0]/100])
            mode1RGB = matplotlib.colors.hsv_to_rgb(mode1RGBarr)
            mode1RGB = mode1RGB*255
            print(mode1RGB)
            rgb1_colourR = mode1RGB[0].astype(str)
            rgb1_colourG = mode1RGB[1].astype(str)
            rgb1_colourB = mode1RGB[2].astype(str)
            print()

            mode2RGBarr = np.array([hsvValueMode2["h"][0] / 360, hsvValueMode2["s"][0] / 100, hsvValueMode2["v"][0] / 100])
            mode2RGB = matplotlib.colors.hsv_to_rgb(mode2RGBarr)
            mode2RGB = mode2RGB * 255
            print(mode2RGB)
            rgb2_colourR = mode2RGB[0].astype(str)
            rgb2_colourG = mode2RGB[1].astype(str)
            rgb2_colourB = mode2RGB[2].astype(str)
            print()

            colourcode = "192.168.1.9/?r" + rgb1_colourR + "g" + rgb1_colourG + "b" + rgb1_colourB + "x" + rgb2_colourR + "y" + rgb2_colourG + "z" + rgb2_colourB + "&"

            webbrowser.open(colourcode)
            sleep(5)
            os.system("taskkill /im iexplore.exe /f")

            #rgbValue = pd.DataFrame(rgbvalues1d, columns=["r", "g", "b"])
            #rgbValueSorted = rgbValue.sort_values(by=["r", "g", "b"], ascending=True)
            #rgbValueSorted.reset_index(drop=True, inplace=True)

            #rgbValueMode1 = pd.DataFrame.mode(rgbValue, axis = 0)
            #r1 = rgbValueMode1["r"][0]
            #print(rgbValueMode1)
            #print(r1)

            # rgbValueMode = pd.DataFrame.mode(rgbValue, axis = 0)
            #something = rgbValue.iloc[]["r"]
            #print(something)

        except:
            print("Oh, no! An error has occurred.")
            print("Is Spotify playing music? Make sure it's up and running before you run this program.")
            print("If this problem persists, hit pause and play on Spotify.")

            # os.remove(f".cache-melroy_caeiro") # Debugging, for cache error (haven't tested)


        currentTrack = trackNow
