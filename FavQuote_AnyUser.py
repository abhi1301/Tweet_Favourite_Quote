'''
Posting famous quotes on any user's twitter page as images.
'''

from TwitterAPI import TwitterAPI
from PIL import Image, ImageDraw, ImageFont
import textwrap
import requests
from appJar import gui
from urllib.parse import urlparse
import urllib.parse
import oauth2 as oauth
import json

# ----------%%%%%%% Initializations %%%%%%%----------------------
CONSUMER_KEY = 'M3ExtQJiDqipGXaRDRiPdn0fi'
CONSUMER_SECRET = 'pFhb4QoRjd7mWTALBnoSt0uWJeD9zMz6YQeFpBCvk4JoYu7r3d'
ACCESS_TOKEN_KEY = ''
ACCESS_TOKEN_SECRET = ''

request_token_url = 'https://api.twitter.com/oauth/request_token?x_auth_access_type=read-write'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'

consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
client = oauth.Client(consumer)
# --------------------------------------------------------------------


# ------------%%%%%%%%%%% OAuth Authorization by end user %%%%%-------------------
# Asking the user to authorize my app to post on his timeline .....

# Step 1: Get a request token from twitter

resp, content = client.request(request_token_url, "GET")
if resp['status'] != '200':
    raise Exception("Invalid response %s." % resp['status'])
# Parsing the byte object to string....
request_token = dict(urllib.parse.parse_qsl(content.decode('utf-8')))
# print ("Request Token:")
# print ("    - oauth_token        = " + request_token['oauth_token'])
# print( "    - oauth_token_secret = " + request_token['oauth_token_secret'])
# print()

# Step 2: Redirect to the provider, i.e to twitter to allow the user to authorize our app permissions.
# Since this is a  script not a web-app, user need to manually go to the following URL to authorize this app.

print( "Go to the following link in your browser to authorize this app:")
print( "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token']))
print()

# Waiting untill the user has granted the permissions
accepted = 'n'
while accepted.lower() == 'n':
    accepted = input('Have you authorized me? (y/n) ')
# Twitter provides a PIN after authorizing the app to complete this process, user need to provide that to the app.
oauth_verifier = input('What is the PIN? ')

# Step 3: Request the access token the user has approved. You use the
# request token to sign this request.
token = oauth.Token(request_token['oauth_token'],
    request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth.Client(consumer, token)

# Request twitter for the token and the token secret of that user..
resp, content = client.request(access_token_url, "POST")
access_token = dict(urllib.parse.parse_qsl(content.decode('utf-8')))

ACCESS_TOKEN_KEY = access_token['oauth_token']
ACCESS_TOKEN_SECRET = access_token['oauth_token_secret']

print ("User's access Token:")
print ("    - oauth_token        = " + access_token['oauth_token'])
print( "    - oauth_token_secret = " + access_token['oauth_token_secret'])
print()
print()
# Token and Token secret of the user has been obtained, now use it to post on his wall....
# ------------------------------------------------------------------------------------------------

# --------------------------%%%%%%%%%% Posting on the user's wall %%%%%%%%%%%------------------



#########################################################################################################
# From here everything is same as FavQuote.py....
########################################################################################################

# -----------%%%%%%%% Quote image formatting attributes  %%%%%%%%%%%-------------------
# For better visibilty and quality of picture use appropriate values....
FONT_NAME = 'Fonts/arial.ttf'
FONT_COLOR = 'red'
BACKGROUND_COLOR = 'white'
FONT_SIZE = 38
NMBR_OF_CHAR_PER_LINE  = 40

# -----------------%%%%%%%%% Form GUI starts %%%%%%%%%%%%%%-----------------------------
# GUI form to cutomize the font attributes and image background color. ................

# function for color picker.......
def pick(button):
    global BACKGROUND_COLOR, FONT_COLOR
    val = app.colourBox(colour="#FF0000")               # color picker
    # print(val)
    if val != None:
        if button == 'Pick FONT COLOR':
            # print('font color = '+val)
            FONT_COLOR = val;
        elif button == 'Pick BACKGROUND COLOR':
            # print('bgcolor = '+val)
            BACKGROUND_COLOR = val

# function for setting font type and size....
def press(button):
    global FONT_NAME, FONT_SIZE
    if button == "Cancel":
        app.stop()                  # exits the GUI form
    else:
        FONT_NAME = 'Fonts/'+app.getOptionBox("Fonts")+'.ttf'
        if int(app.getEntry('Font Size')):
            FONT_SIZE = int(app.getEntry('Font Size'))
        app.stop()

# create a GUI variable called app
app = gui("Formatting Window", "420x300")
app.setBg("orange")
app.setFont(12)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Welcome to FavQuotes")
app.setLabelBg("title", "blue")
app.setLabelFg("title", "orange")

# Font type ---------------
app.addLabelOptionBox("Fonts", ["arial", "Anton-Regular", "JosefinSans-Bold",
                        "Lobster-Regular", "OpenSans-Bold", "Roboto-BoldItalic",
                        "PlayfairDisplay-Black", "EBGaramond-Regular"])

# Font size ----------------
app.addNumericEntry('Font Size')
app.setEntryDefault("Font Size", 12)

# Image BACKGROUND_COLOR and FONT_COLOR selection --------------
app.addButtons(["Pick BACKGROUND COLOR", "Pick FONT COLOR"], pick)

# Footer note
app.addLabel("footer", "Click Cancel for default values")

# link the buttons to the function called press
app.addButtons(["Submit", "Cancel"], press)

# start the GUI
app.go()

# -----------------%%%%%%%%% Form GUI ends%%%%%%%%%%%%%%-----------------------------

# *****************************************************************************************************************************

# -----------------%%%%%%%%% Creating the post image from quote %%%%%%%%%%%%%%-----------------------------
#  Using an online API to fetch a random famous quote and conerting it to an image.....
response = requests.get("https://talaikis.com/api/quotes/random")
RandQuote = json.loads(response.text)           # converting the response to json format,,,
print('Quote tweeted : '+RandQuote['quote'])
print('Author : '+RandQuote['author'])
TWEET_TEXT = 'Quote of the day:\nBy- '+RandQuote['author']
Quote = RandQuote['quote']          # fetched quote

# processing the quote for the image boundaries.......
para = textwrap.wrap(Quote, width= NMBR_OF_CHAR_PER_LINE)
lines = 0
for line in para:
    lines+=1

MAX_W, MAX_H = 400, 300             # initial image dimensions

# creating a blank image for background..
# Using PIL library of Python
image = Image.new('RGB', (MAX_W, MAX_H), BACKGROUND_COLOR)
draw = ImageDraw.Draw(image)
font = ImageFont.truetype(FONT_NAME, FONT_SIZE)
current_h, pad = 30, 10
w, h = draw.textsize(para[0],font=font)

# Udating the image dimensions after processing the possible dimensions of the text on the image
MAX_H = (h+pad)*lines + 100
MAX_W = int(FONT_SIZE/2)* NMBR_OF_CHAR_PER_LINE + 50

# re-creating the background image with new dimensions
image = Image.new('RGB', (MAX_W, MAX_H), BACKGROUND_COLOR)
draw = ImageDraw.Draw(image)

# Writing the processed text onto the background image.......
for line in para:
    w, h = draw.textsize(line, font=font)
    draw.text(((MAX_W - w) / 2, current_h), line, font=font, fill = FONT_COLOR)
    current_h += h + pad

# Saving the final image after Writing..........
image.save('post.png')
# ---------------%%%%%%%%%%%%%% Image created %%%%%%%%%%%%%----------------------

# *****************************************************************************************************************************

# -----------------%%%%%%%%% Posting the image to my Twitter Wall : start %%%%%%%%%%%%%%-----------------------------
# reading the local image file..
file = open('post.png', 'rb')
data = file.read()
api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

# STEP 1 : Uploading the image to Twitter ..........
r = api.request('media/upload', None, {'media': data})
# print(r.status_code)
print()
print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE')

# STEP 2 - post tweet with a reference to uploaded image
if r.status_code == 200:
    media_id = r.json()['media_id']
    r = api.request(
        'statuses/update', {'status': TWEET_TEXT, 'media_ids': media_id})
    print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE')
# -----------------%%%%%%%%% Posting the image to Twitter Wall : end %%%%%%%%%%%%%%-----------------------------
