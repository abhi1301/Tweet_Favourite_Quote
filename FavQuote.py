'''
Posting my favourites quotes on my twitter page as images.
'''

from TwitterAPI import TwitterAPI


TWEET_TEXT = 'Quote of the day:'
IMAGE_PATH = 'upload.jpg'

# Credentials -------------------
CONSUMER_KEY = 'M3ExtQJiDqipGXaRDRiPdn0fi'
CONSUMER_SECRET = 'pFhb4QoRjd7mWTALBnoSt0uWJeD9zMz6YQeFpBCvk4JoYu7r3d'
ACCESS_TOKEN_KEY = '4086270673-Ldr8KMe8HD9DOlEFJ6LjFgBLGqBSnsyUF2nDz8b'
ACCESS_TOKEN_SECRET = 'HeG3lyNQ6qptXgr2bP8Cekxkanl7A8HiUopKC4aOsvFKx'


api = TwitterAPI(CONSUMER_KEY,
                 CONSUMER_SECRET,
                 ACCESS_TOKEN_KEY,
                 ACCESS_TOKEN_SECRET)



# STEP 1 - upload image
file = open(IMAGE_PATH, 'rb')
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
