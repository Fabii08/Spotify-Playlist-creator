#Copyright © 2025 https://github.com/Fabii08?tab=repositories  
#All rights reserved.  

import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth

# Spotify API Credentials (replace with your own)
CLIENT_ID = "Your_client_id"
CLIENT_SECRET = "ur_client_secret"
REDIRECT_URI = "http://127.0.0.1:8888/callback"

# Required Scopes
SCOPE = "user-library-read playlist-modify-private playlist-modify-public playlist-read-private"

# Connect to Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

def get_favorite_tracks_by_artists(artist_names):
    """Fetches all favorite songs and filters them by multiple artists."""
    results = sp.current_user_saved_tracks(limit=50)
    matching_tracks = []
    
    if "!all" in artist_names:
        while results:
            matching_tracks.extend([item['track']['id'] for item in results['items']])
            if results['next']:
                results = sp.next(results)
            else:
                break
        return matching_tracks
    
    artist_names = [name.lower() for name in artist_names]
    while results:
        for item in results['items']:
            track = item['track']
            artists = [artist['name'].lower() for artist in track['artists']]
            if any(artist in artists for artist in artist_names):
                matching_tracks.append(track['id'])
        
        if results['next']:
            results = sp.next(results)
        else:
            break
    
    return matching_tracks

def list_own_playlists():
    """Retrieves and lists only playlists owned by the user."""
    user_id = sp.current_user()['id']
    playlists = sp.current_user_playlists()
    return {i+1: (playlist['name'], playlist['id']) for i, playlist in enumerate(playlists['items']) if playlist['owner']['id'] == user_id}

def get_playlist_tracks(playlist_id):
    """Retrieves track IDs from an existing playlist."""
    existing_tracks = set()
    results = sp.playlist_tracks(playlist_id)
    while results:
        existing_tracks.update(track['track']['id'] for track in results['items'] if track['track'])
        if results['next']:
            results = sp.next(results)
        else:
            break
    return existing_tracks

def create_playlist(name, track_ids):
    """Creates a new playlist and adds tracks in batches of 50 with a 1-second delay."""
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user=user_id, name=name, public=False)
    add_tracks_to_playlist(playlist['id'], track_ids)
    print(f"Playlist '{name}' has been created with {len(track_ids)} songs!")

def add_tracks_to_playlist(playlist_id, track_ids):
    """Adds tracks to an existing playlist in batches of 50, skipping duplicates."""
    existing_tracks = get_playlist_tracks(playlist_id)
    new_tracks = [track for track in track_ids if track not in existing_tracks]
    
    if not new_tracks:
        print("All tracks are already in the playlist. No new tracks were added.")
        return
    
    for i in range(0, len(new_tracks), 50):
        sp.playlist_add_items(playlist_id=playlist_id, items=new_tracks[i:i+50])
        time.sleep(1)  # 1-second pause
    
    print(f"Added {len(new_tracks)} new songs to the playlist.")

def main():
    while True:
        artists = input("Which artists would you like to filter by? (Separate multiple with commas, or type '!all' for all songs) ")
        artist_list = [artist.strip().lower() for artist in artists.split(",")]
        tracks = get_favorite_tracks_by_artists(artist_list)
        
        if tracks:
            break
        else:
            print("No matching songs found. Please try again.")
    
    choice = input("Do you want to create a new playlist or add to an existing one? (new/existing) ").strip().lower()
    
    if choice == "new":
        playlist_name = input("Enter a name for the new playlist: ")
        create_playlist(playlist_name, tracks)
    elif choice == "existing":
        playlists = list_own_playlists()
        if not playlists:
            print("No existing playlists found that you own.")
            return
        
        print("Available playlists you own:")
        for num, (name, _) in playlists.items():
            print(f"{num}. {name}")
        
        while True:
            try:
                selected_num = int(input("Enter the number of the playlist to add to: "))
                if selected_num in playlists:
                    playlist_name, playlist_id = playlists[selected_num]
                    break
                else:
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        add_tracks_to_playlist(playlist_id, tracks)
    else:
        print("Invalid choice. Please enter 'new' or 'existing'.")

if __name__ == "__main__":
    main()
