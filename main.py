import json
import os
import creds
import spotipy
import spotipy.util as util
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

cid = creds.CID
secret = creds.SECRET


def get_user_two(username):
    url = "https://api.spotify.com/v1/users/" + username + "/playlists/PLAYLIST_ID"
    print(url)
    # Set the appropriate headers
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "Content-Type": "application/json",
    }

    # Make the request
    response = requests.get(url, headers=headers)

    # Check for a successful response
    if response.status_code == 200:
        # Get the playlist object from the response
        playlist = response.json()
        # Get the playlist's external_urls field, which contains the URL for the playlist
        playlist_url = playlist["external_urls"]["spotify"]
        print(playlist_url)
    else:
        print(f"Request failed with status code {response.status_code}")


def get_user_three(display_name):
    auth_header = {'Authorization': 'Basic ' + (cid + ':' + secret).encode('utf-8').hex()}
    auth_payload = {'grant_type': 'client_credentials'}
    auth_response = requests.post('https://accounts.spotify.com/api/token', headers=auth_header, data=auth_payload)
    access_token = auth_response.json()['access_token']
    auth_header = {'Authorization': 'Bearer ' + access_token}
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager.get_access_token())
    response = requests.get(f"https://api.spotify.com/v1/search?q={display_name}&type=user&limit=1",
                            headers={
                                "Content-Type": "application/json",
                                "Authorization": f"Bearer {access_token}"
                            })

    # Get the user's Spotify ID from the search results
    user_id = response.json()["users"]["items"][0]["id"]

    # Use the Spotify Web API to get a list of the user's public playlists
    response = requests.get(f"https://api.spotify.com/v1/users/{user_id}/playlists",
                            headers={
                                "Content-Type": "application/json",
                                "Authorization": f"Bearer {access_token}"
                            })

    playlist_url = response.json()["items"][0]["external_urls"]["spotify"]
    print(playlist_url)


def get_user(display_name):
    # Replace these values with your own
    auth_header = {'Authorization': 'Basic ' + (cid + ':' + secret).encode('utf-8').hex()}
    auth_payload = {'grant_type': 'client_credentials'}
    auth_response = requests.post('https://accounts.spotify.com/api/token', headers=auth_header, data=auth_payload)
    access_token = auth_response.json()['access_token']
    auth_header = {'Authorization': 'Bearer ' + access_token}

    search_url = 'https://api.spotify.com/v1/search'
    search_params = {'q': display_name, 'type': 'user'}
    search_response = requests.get(search_url, headers=auth_header, params=search_params)
    users = search_response.json()['items']

    # Find the user with the specified display name
    for user in users:
        if user['display_name'] == display_name:
            user_id = user['id']
            print(user_id, 'found')
            break
    else:
        print(f'User with display name "{display_name}" not found.')

    # Set the URL for the API request to get the user's authorization URL
    auth_url = f'https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&scope=user-library-read&redirect_uri=http://localhost/&state=123'

def get_playlist_info(display_name, player_one):
    # Authentication - without user
    scope = "playlist-view-public"
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager.get_access_token())

    results = sp.search(q=display_name, type="playlist", market="from_token")
    playlists_list = results["playlists"]["items"]
    playlists = [playlist["uri"] for playlist in playlists_list]

    track_name_list = []
    genre_list = []
    artist_list = []

    for thing in playlists:
        cur_playlist_URI = thing.split("/")[-1].split("?")[0]

        for track in sp.playlist_items(cur_playlist_URI):
            try:
                # Track name
                track_name = track["track"]["name"]
                track_name_list.append(track_name)

                # Main Artist
                artist_uri = track["track"]["artists"][0]["uri"]
                name = artist_uri["artists"]["name"]
                artist_info = sp.artist(artist_uri)

                # genre
                artist_genre = artist_info["genres"]
                genre_list.append(artist_genre)

            except:
                print("Failure Occured")

    dict = {'name': track_name_list, 'genre': genre_list, 'artist': artist_list}
    df = pd.DataFrame(dict)

    # normalize the data
    df = df.drop_duplicates()
    df = df[df['genre'] != 'N/A']
    df = df[df['time_signature'] != 0]

    df.to_csv('df.csv', index=False) if player_one else df.to_csv('df2.csv', index=False)


# K-means
# cluster data based off of acoustic values
# use gini scores (decision trees) to
def main():
    print("end")


main()
print("stuff")
