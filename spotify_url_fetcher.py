import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm

df = pd.read_csv("Spotify_Data.csv", encoding="latin1")

client_id = 'CLIEMT_ID'    
client_secret = 'CLIENT_SECRET'

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_album_cover(track, artist):
    query = f"track:{track} artist:{artist}"
    try:
        results = sp.search(q=query, type='track', limit=1)
        items = results['tracks']['items']
        if items:
            return items[0]['album']['images'][0]['url']
    except Exception as e:
        print(f"Error for {track} by {artist}: {e}")
    return None

tqdm.pandas()
df['album_cover_url'] = df.progress_apply(lambda row: get_album_cover(row['track_name'], row['artist(s)_name']), axis=1)

df.to_csv("spotify_with_album_covers.csv", index=False)
print("Saved to 'spotify_with_album_covers.csv'")
