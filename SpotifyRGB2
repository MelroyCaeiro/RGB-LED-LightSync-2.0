import os
import spotipy
import spotipy.util as util
import requests
import PIL as pil
from PIL import Image, ImageFilter
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
currentTrack = 1000
x = 1

token = util.prompt_for_user_token(username, scope, os.environ["SPOTIPY_CLIENT_ID"],
                                   os.environ["SPOTIPY_CLIENT_SECRET"], uri)
sp = spotipy.Spotify(auth=token)

while (x == 1):
    playback = sp.current_playback()
    nowPlaying = sp.current_user_playing_track()

    try:
        trackNow = nowPlaying["item"]["id"]
    except TypeError:
        trackNow = 101010

    if (trackNow != currentTrack):

        try:
            currentTrack = trackNow
            trackname = nowPlaying["item"]["name"]
            artistname = nowPlaying["item"]["artists"][0]["name"]
            print("NOW PLAYING: " + trackname + " - " + artistname.upper())

            device = playback["device"]["name"]
            print("PLAYING ON: " + device)

            url = nowPlaying['item']['album']['images'][0]['url']
            r = requests.get(url, allow_redirects=True)
            open('SPOTIFY-Image.jpg', 'wb').write(r.content)

            album_art = pil.Image.open("SPOTIFY-Image.jpg")

            # histogram = album_art.histogram() # not working
            # print(rgb_data)

            rgb_tuples = np.asarray(album_art)
            # print(rgb_tuples) # Debugging

            for i in range(0, len(rgb_tuples)):
                if i == 0:
                    np_stack = rgb_tuples[i]
                if i > 0:
                    np_stack = np.vstack((np_stack, rgb_tuples[i]))  # Creates a stack

            # print(np.shape(np_stack)) # Debugging, prints array of RGB colour codes
            # no clue why print(np.stack) isn't used instead

            pd_rgb_stack = pd.DataFrame(np_stack, columns=["r", "g", "b"])
            pd_rgb_stack["rgb"] = (pd_rgb_stack["r"].astype(str)) + "-" + (pd_rgb_stack["g"].astype(str)) + "-" + (
                pd_rgb_stack["b"].astype(str))
            pd_rgb_stack["check_sum"] = pd_rgb_stack[["r", "g", "b"]].sum(axis=1)
            # print(pd_rgb_stack["check_sum"].head(20)) # Debugging, lists first 20 RGB sum values
            check_sum_mean = pd_rgb_stack["check_sum"].mean()
            # print(check_sum_mean) # Debugging, isn't this obvious?

            pd_rgb_sorted = pd_rgb_stack["rgb"].value_counts().to_frame()
            pd_rgb_sorted.astype(int)
            # print(pd_rgb_sorted["int"]) # Debugging, quite unnecessary at this point

            rgb_temp_std = 0  # Initialize variable to zero, for while loop
            rgb_temp_sum = 0  # Initialize variable to zero, for while loop
            i = -1

            while (rgb_temp_std < 15):
                i += 1  # Simple increment function, what else could it be?
                temp = pd_rgb_sorted.index[i]
                parse_1 = temp.find("-")
                parse_2 = temp.find("-", parse_1 + 1)
                rgb_temp = pd.DataFrame(
                    {"r": [temp[0:parse_1]], "g": [temp[parse_1 + 1:parse_2]], "b": [temp[parse_2 + 1:]]}).astype(int)
                rgb_temp_std = np.std(rgb_temp, 1)[0]
                rgb_temp_sum = rgb_temp["r"] + rgb_temp["g"] + rgb_temp["b"]
                rgb_temp_sum = rgb_temp_sum.astype(int)
                rgb1_colourR = temp[0:parse_1]
                rgb1_colourG = temp[parse_1 + 1:parse_2]
                rgb1_colourB = temp[parse_2 + 1:]

            rgb_select1 = rgb_temp
            print("The first selected colour is: ")
            print(
                rgb_select1)  # Printed on a separate line bcs the above is one line, while this is an array [they don't go together well, lol]

            pd_rgb_stack["r_select"] = rgb_select1["r"][0]
            pd_rgb_stack["g_select"] = rgb_select1["g"][0]
            pd_rgb_stack["b_select"] = rgb_select1["b"][0]

            pd_rgb_stack["dist_score"] = np.sqrt(np.square(pd_rgb_stack["r"] - pd_rgb_stack["r_select"]) + np.square(
                pd_rgb_stack["g"] - pd_rgb_stack["g_select"]) + np.square(pd_rgb_stack["b"] - pd_rgb_stack["b_select"]))
            # print(pd_rgb_stack["dist_score"].head(20)) # Debugging, once more

            dist_score_sorted = pd_rgb_stack["dist_score"].value_counts().to_frame()
            dist_score_std = np.std(pd_rgb_stack["dist_score"])
            # print(dist_score_sorted)
            # print(dist_score_std)

            ## pd_rgb_sorted = pd_rgb_stack['rgb'].value_counts().to_frame()
            ## pd_rgb_sorted.astype(int)

            pd_rgb_merged = pd_rgb_stack.join(pd_rgb_sorted, on="rgb", how="left", rsuffix="_count")

            pd_rgb_merged = pd_rgb_merged.sort_values(by=["rgb_count", "dist_score"], ascending=False)
            pd_rgb_merged["std"] = np.std(pd_rgb_merged[["r", "g", "b"]], axis=1)
            pd_rgb_merged = pd_rgb_merged.drop_duplicates()

            rgb_temp_std = 0
            rgb_temp_sum = 0
            temp_dist_score = 0
            j = -1

            while (rgb_temp_std < 15 or temp_dist_score < 2 * dist_score_std or rgb_temp_sum < 120):
                j += 1
                temp = pd_rgb_merged.iloc[j]["rgb"]
                temp_r = pd_rgb_merged.iloc[j]["r"]
                temp_g = pd_rgb_merged.iloc[j]["g"]
                temp_b = pd_rgb_merged.iloc[j]["b"]
                temp_dist_score = pd_rgb_merged.iloc[j]["dist_score"]
                rgb_temp_sum = pd_rgb_merged.iloc[j]["check_sum"]
                rgb_temp_std = pd_rgb_merged.iloc[j]["std"]

            rgb_select2 = pd.DataFrame({"r": [temp_r], "g": [temp_g], "b": [temp_b]}).astype(int)
            print("The second selected colour is: ")
            print(rgb_select2)
            print(" ")
            rgb2_colourR = temp_r.astype(str)
            rgb2_colourG = temp_g.astype(str)
            rgb2_colourB = temp_b.astype(str)

            colourcode = "http://192.168.1.9/?r" + rgb1_colourR + "g" + rgb1_colourG + "b" + rgb1_colourB + "x" + rgb2_colourR + "y" + rgb2_colourG + "z" + rgb2_colourB + "&"

            print("Colour code is: " + colourcode)  # Debugging

            call = requests.get(colourcode)

            #webbrowser.open(colourcode)
            #sleep(7)
            #os.system("taskkill /im iexplore.exe /f")

            # browser = webdriver.chrome(executable_path='/home/aman/Downloads/geckodriver')
            # browser.get(colourcode2)
            # browser.close()

            # print subprocess.check_output(['open',colourcode1,'--hide'])

            # webUrl = urllib.request.urlopen(colourcode2)

            # print("Result code: " + str(webUrl.getcode())) # Debugging

            # histogram_test = album_art.histogram()
            # print(histogram_test)

            # histogram stuff that didnt work

            # print(nowPlaying['item']['album']['images'][0]['url']) # Debugging
            # print(r.headers.get("content-type")) # Debugging, if you wanna see the request library in action
            # print(playback["is_playing"]) # Debugging, playback state (Boolean)

        except:
            print("Oh, no! An error has occurred.")
            print("Is Spotify playing music? Make sure it's up and running before you run this program.")
            print("If this problem persists, hit pause and play on Spotify.")

            # os.remove(f".cache-melroy_caeiro") # Debugging, for cache error (haven't tested)

