from bs4 import BeautifulSoup as bs
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# ------------GETTING TOP 100 SONGS IN A LIST------------------------

date = input('Which year do you wanna travel to? Type the date in this format YYYY-MM-DD')
# date = '2005-05-05'
url = 'https://www.billboard.com/charts/hot-100/'+date
r = requests.get(url)
soup = bs(r.text,'html.parser')
i=0
song_list = []

# selecting a tag that contains both the song name and the artist name
for tag in soup.select('.lrv-u-width-100p ul li'):

    try:
        song_name = tag.h3.get_text().strip()
        artist = tag.span.get_text().strip()

        i+=1
        song_list.append(f"{song_name} by {artist}")
    except:
        continue

    if(i==100):
        break

print(song_list)

#-----------------CREATING A PLAYLIST IN SPOTIFY--------------------

# Set up your Spotify API credentials
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = 'http://example.com'

# Initialize Spotipy with the required scopes and redirect URI
scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, open_browser=True))

# Fetch the access token using the cached token
token_info = sp.auth_manager.get_cached_token()
access_token = token_info['access_token']
print('Spotify Authentication complete')

# Fetch the current user's profile information
user_info = sp.me()

# get the user's display name
user = user_info['id']

# ----------------Creating a new playlist---------------
# Set up the API endpoint URL
url = f'https://api.spotify.com/v1/users/{user}/playlists'

# Set up the request headers
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Set up the request body
data = {
    "name": f"{date} Billboard 100",
    "description": "Musical Time Machine",
    "public": False
}

# Send the POST request
response = requests.post(url, headers=headers, json=data)

# Check the response status code

print("Playlist created successfully!")
playlist_id = response.json()['id']


#--------Getting URIs of all songs in the list into a list------

track_uris = []
# Set up the API endpoint URL for searching tracks
url = 'https://api.spotify.com/v1/search'

for item in song_list:
    # Set up the query parameters
    params = {
        'q': item,
        'type': 'track'
    }

    # Send the get request
    response = requests.get(url, headers=headers, params=params)
    track_uri = response.json()['tracks']['items'][0]['uri']
    track_uris.append(track_uri)
print("URI's fetched")

# ---- Adding the songs to the playlist------
url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

# Set up the request body
data = {
    "uris": track_uris,
    "position": 0
}

# Send the POST request
response = requests.post(url, headers=headers, json=data)


print("Tracks added to the playlist successfully!")
