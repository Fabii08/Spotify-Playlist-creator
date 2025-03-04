import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth

# Spotify API Credentials (replace with your own)
CLIENT_ID = "Your_client_id"
CLIENT_SECRET = "ur_client_secret"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
# Required Scopes
SCOPE = "user-library-read playlist-modify-private"

# Connect to Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

def get_favorite_tracks_by_artists(artist_names):
    """Fetches all favorite songs and filters them by multiple artists."""
    results = sp.current_user_saved_tracks(limit=50)
    matching_tracks = []
    artist_names = [name.lower() for name in artist_names]
    
    while results:
        for item in results['items']:
            track = item['track']
            artists = [artist['name'].lower() for artist in track['artists']]
            if any(artist in artists for artist in artist_names):
                matching_tracks.append(track['id'])
        
        # Load more pages if available
        if results['next']:
            results = sp.next(results)
        else:
            break
    
    return matching_tracks

def create_playlist(name, track_ids):
    """Creates a new playlist and adds tracks in batches of 50 with a 1-second delay."""
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user=user_id, name=name, public=False)
    
    # Add tracks in batches of 50 with a 1-second pause
    for i in range(0, len(track_ids), 50):
        sp.playlist_add_items(playlist_id=playlist['id'], items=track_ids[i:i+50])
        time.sleep(1)  # 1-second pause
    
    print(f"Playlist '{name}' has been created with {len(track_ids)} songs!")

if __name__ == "__main__":
    artists = input("Which artists would you like to filter by? (Separate multiple with commas) ")
    artist_list = [artist.strip() for artist in artists.split(",")]
    playlist_name = input("Enter a name for the playlist: ")
    tracks = get_favorite_tracks_by_artists(artist_list)
    
    if tracks:
        create_playlist(playlist_name, tracks)
    else:
        print("No matching songs found.")
