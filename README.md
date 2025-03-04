# Spotify Favorite Tracks Playlist Creator

This script creates a Spotify playlist by fetching your favorite tracks and filtering them by specified artists. The playlist is then created and populated with the matching tracks.

---

## 🛠️ Requirements

- **Python 3.x**
- **`spotipy` library**

You can install the `spotipy` library using pip:

```bash
pip install spotipy
```

🚀 Setup
Clone this repository and navigate to the project directory.

Change in main.py the CLIENT_ID and CLIENT_SECRET to add your Spotify API credentials:

```bash
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
```
Replace the placeholders in the script with your actual Spotify API credentials.


🔑 Obtaining Spotify API Credentials
Visit the Spotify Developer Dashboard and log in with your Spotify account.

Click on Create an App and provide the necessary details.

Once the app is created, you will be provided with a Client ID and Client Secret. Note these values.

Set the Redirect URI to http://127.0.0.1:8888/callback in your Spotify Developer Dashboard settings.

🎯 Usage
Run the script:

```bash

python main.py
```
Enter the names of the artists you want to filter by (separated by commas) when prompted.

Enter a name for the new playlist when prompted.

Example:

Which artists would you like to filter by? (Separate multiple with commas) The Beatles, Queen
Enter a name for the playlist: My Favorite Tracks
Playlist 'My Favorite Tracks' has been created with X songs!

**📜 License**<br>
This project is licensed under the MIT License. See the LICENSE file for details.

**💡 How It Works**<br>
The script authenticates with Spotify using the spotipy library and your API credentials.

It fetches your saved tracks (favorite tracks) from your Spotify account.

It filters the tracks based on the specified artists.

It creates a new playlist and adds the filtered tracks to it.

