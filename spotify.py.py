#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st

client_id = "23866dd5e1f14fd78f0bcd091e6bbd3a"
client_secret = "1eb3cb30af3f4bfd88f20b6f5c86f2fd"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Search for tracks matching the title provided by the user. Creates a list of music tracks limited to 10 tracks.
def search_tracks(sp, track_name):
    results = sp.search(q=track_name, type="track", limit=10)
    tracks = results["tracks"]["items"]
    return tracks

# Obtain details for the track selected by the user.
def get_track_details(sp, track_id):
    track = sp.track(track_id)
    track_name = track["name"]
    artist_name = track["artists"][0]["name"]

    audio_features = sp.audio_features([track_id])[0]
    if not audio_features:
        return None

    danceability = audio_features["danceability"]
    energy = audio_features["energy"]
    liveness = audio_features["liveness"]
    valence = audio_features["valence"]

    return {
        "track_name": track_name,
        "artist_name": artist_name,
        "danceability": danceability,
        "energy": energy,
        "liveness": liveness,
        "valence": valence
    }

# Display the top 10 tracks matching the user query.
def display_track_options(tracks):
    print("Here are the closest matches:")
    for i, track in enumerate(tracks):
        track_name = track["name"]
        artist_name = track["artists"][0]["name"]
        print(f"{i + 1}: {track_name} by {artist_name}")

# Display the details for the track selected by the user.
def display_track_details(track_details):
    if track_details:
        print(f"Track Name: {track_details['track_name']}")
        print(f"Artist: {track_details['artist_name']}")
        print(f"Danceability: {track_details['danceability']}")
        print(f"Energy: {track_details['energy']}")
        print(f"Liveness: {track_details['liveness']}")
        print(f"Valence: {track_details['valence']}")
    else:
        print("No track found or unable to retrieve audio features.")

def main():
    while True:
        # Ask the user to enter a track name.
        track_name = input("Enter the track name: ")

        # Check for tracks matching the user input.
        tracks = search_tracks(sp, track_name)

        # Filter tracks to ensure the track name contains the search term provided by the user.
        filtered_tracks = []
        for track in tracks:
            if track_name.lower() in track["name"].lower() or track_name.lower() in track["artists"][0]["name"].lower():
                filtered_tracks.append(track)

        # Check if any filtered tracks were found.
        if not filtered_tracks:
            print("No tracks found. Please try again.")
        else:
            # Display the top 10 tracks matching the title provided with corresponding artist.
            display_track_options(filtered_tracks)

            while True:
                try:
                    # Ask the user to select a track from the list. Then validate the number provided by the user.
                    choice = int(input("Select the track number: ")) - 1
                    if choice < 0 or choice >= len(filtered_tracks):
                        raise ValueError("Invalid choice.")
                    break  # Exit the loop if a valid number is provided.
                except ValueError:
                    print("Please enter a valid track number.")

            # Retrieve details and audio features for the selected track.
            selected_track_id = filtered_tracks[choice]["id"]
            track_details = get_track_details(sp, selected_track_id)

            #Display the track details.
            display_track_details(track_details)

            # Exit the loop after successfully processing a track
            break

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:





# In[ ]:




