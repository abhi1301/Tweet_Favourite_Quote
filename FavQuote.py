'''
Posting my favourites quotes on my twitter page as images.
'''

from TwitterAPI import TwitterAPI
from PIL import Image, ImageDraw, ImageFont
import textwrap
import requests
import json

TWEET_TEXT = 'Quote of the day:'
# IMAGE_PATH = 'upload.jpg'

# Credentials -------------------
CONSUMER_KEY = 'M3ExtQJiDqipGXaRDRiPdn0fi'
CONSUMER_SECRET = 'pFhb4QoRjd7mWTALBnoSt0uWJeD9zMz6YQeFpBCvk4JoYu7r3d'
ACCESS_TOKEN_KEY = '4086270673-Ldr8KMe8HD9DOlEFJ6LjFgBLGqBSnsyUF2nDz8b'
ACCESS_TOKEN_SECRET = 'HeG3lyNQ6qptXgr2bP8Cekxkanl7A8HiUopKC4aOsvFKx'


api = TwitterAPI(CONSUMER_KEY,
                 CONSUMER_SECRET,
                 ACCESS_TOKEN_KEY,
                 ACCESS_TOKEN_SECRET)

# These code snippets use an open-source library.
response = requests.get("https://talaikis.com/api/quotes/random")
RandQuote = json.loads(response.text)
print(RandQuote['quote'])
print(RandQuote['author'])


Quote = RandQuote['quote']
para = textwrap.wrap(Quote, width=50)
lines = 0
for line in para:
    lines+=1

# print(para[1])
MAX_W, MAX_H = 400, 300
im = Image.new('RGB', (MAX_W, MAX_H), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)
current_h, pad = 30, 10
w, h = draw.textsize(para[0])
MAX_H = (h+pad)*lines + 80
im = Image.new('RGB', (MAX_W, MAX_H), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)
# font = ImageFont.truetype('Arial.ttf', 18)

for line in para:
    w, h = draw.textsize(line)#, font=font)
    print(w,'   ',h)
    draw.text(((MAX_W - w) / 2, current_h), line)#, font=font)
    current_h += h + pad

im.save('test.png')

# --------------------------------------------------------------------
# with Drawing() as draw:
#     with Image(width=600, height=300, background=Color('white')) as image:
#         # draw.font = 'wandtests/assets/League_Gothic.otf'
#         draw.font_family = 'monospace'
#         draw.font_size = 25
#         metrics = draw.get_font_metrics(image,"How BIG am I?", multiline=False)
#         print(metrics)
#
#         # draw.font_size = 40
#         # draw.text(int(image.width / 2), int(image.height / 2),TEXT_ALIGN_TYPES='center', 'Hello, world!')
#         # draw.text(text_alignment()
#         draw(image)
#         image.save(filename='200x100-transparent.png')
# ?_________________________________________________________________________________________________________-


# STEP 1 - upload image
file = open('test.png', 'rb')
data = file.read()

r = api.request('media/upload', None, {'media': data})
print(r.status_code)

print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE')

# STEP 2 - post tweet with a reference to uploaded image
if r.status_code == 200:
    media_id = r.json()['media_id']
    r = api.request(
        'statuses/update', {'status': TWEET_TEXT, 'media_ids': media_id})
    print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE')
