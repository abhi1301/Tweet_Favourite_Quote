'''
Posting my favourites quotes on my twitter page as images.
'''

from TwitterAPI import TwitterAPI
from PIL import Image, ImageDraw, ImageFont
import textwrap
import requests
import json
from appJar import gui

# -----------%%%%%%%% Quote image formatting attributes  %%%%%%%%%%%-------------------
# For better visibilty and quality of picture use appropriate values....
FONT_NAME = 'Fonts/arial.ttf'
FONT_COLOR = 'red'
BACKGROUND_COLOR = 'white'
FONT_SIZE = 38
NMBR_OF_CHAR_PER_LINE  = 40

# -----------%%%%%%%% TwitterAPI Credentials starts %%%%%%%%%%%-------------------
# Credentials required for accessing the TwitterAPI...........
CONSUMER_KEY = 'M3ExtQJiDqipGXaRDRiPdn0fi'
CONSUMER_SECRET = 'pFhb4QoRjd7mWTALBnoSt0uWJeD9zMz6YQeFpBCvk4JoYu7r3d'
ACCESS_TOKEN_KEY = '877229053526376452-9G5ky0mQnNOyjpFbM3cVyw1MbsRjITS'
ACCESS_TOKEN_SECRET = 'AD1yyvx1mDMESbdvyXtYxoiHzL1sd7nlgspfdSJRTPn4V'

# my credentials
# ACCESS_TOKEN_KEY = '4086270673-Ldr8KMe8HD9DOlEFJ6LjFgBLGqBSnsyUF2nDz8b'
# ACCESS_TOKEN_SECRET = 'HeG3lyNQ6qptXgr2bP8Cekxkanl7A8HiUopKC4aOsvFKx'
# -----------%%%%%%%% TwitterAPI Credentials ends %%%%%%%%%%%-------------------


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
print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE')

# STEP 2 - post tweet with a reference to uploaded image
if r.status_code == 200:
    media_id = r.json()['media_id']
    r = api.request(
        'statuses/update', {'status': TWEET_TEXT, 'media_ids': media_id})
    print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE')
# -----------------%%%%%%%%% Posting the image to Twitter Wall : end %%%%%%%%%%%%%%-----------------------------
