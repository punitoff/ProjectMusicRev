import random
import datetime
from cdn_node import CDNNode
import os
import pickle


#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
#import sklearn
#import requests
#from bs4 import BeautifulSoup

class MusicData:
    def __init__(self):
        self.listening_time = {}
        self.skip_count = {}
        self.not_loaded_count = {}
        self.location_based_data = {}

    def log_listening_time(self, song_id, time):
        self.listening_time[song_id] = self.listening_time.get(song_id, 0) + time

    def log_skip(self, song_id):
        self.skip_count[song_id] = self.skip_count.get(song_id, 0) + 1

    def log_not_loaded(self, song_id):
        self.not_loaded_count[song_id] = self.not_loaded_count.get(song_id, 0) + 1

    def log_location_data(self, location, song_id):
        if location not in self.location_based_data:
            self.location_based_data[location] = {}
        self.location_based_data[location][song_id] = self.location_based_data[location].get(song_id, 0) + 1


class UserAgent:
    def __init__(self, location, music_preferences, storage_capacity):
        self.location = location
        self.music_preferences = music_preferences
        self.storage_capacity = storage_capacity
        self.state = "searching"
        self.history = []
        self.location_history = []
        self.time_history = []
        self.music_data = MusicData[]
        self.movement_duration = 0  # Movement duration in minutes


    def move(self):
        # Define the list of subway stations with their coordinates
        stations = {
            "New York Bay Ridge - 86th Street": (40.6213, -74.0291),
            "77th Street": (40.6296, -74.0259),
            "Bay Ridge Avenue": (40.6347, -74.0239),
            "59th Street": (40.6412, -74.0172),
            "53rd Street": (40.6449, -74.0142),
            "45th Street": (40.6489, -74.0108),
            "36th Street": (40.6551, -74.0036),
            "25th Street": (40.6604, -73.9984),
            "Prospect Avenue": (40.6653, -73.9927),
            "9th Street": (40.6708, -73.9881),
            "Union Street": (40.6774, -73.9835),
            "4th Avenue - 9th Street": (40.6703, -73.9885),
            "DeKalb Avenue": (40.6905, -73.9816),
            "Jay Street-MetroTech": (40.6923, -73.9875)
        }

        # Get the coordinates of the current location
        current_coordinates = stations[self.location]

        # Determine the next location based on current location
        next_station = random.choice(list(stations.keys()))
        next_coordinates = stations[next_station]

        # Update the location to the next station
        self.location = next_station

        # Print the new location
        print(f"Moved to {self.location}")

        # Update music preferences based on location
        if self.location == "New York Bay Ridge - 86th Street":
            self.music_preferences = ["pop", "rock"]
        elif self.location == "Jay Street-MetroTech":
            self.music_preferences = ["hip-hop", "electronic"]

        # Update location history
        self.location_history.append(self.location)

        # Update time history
        current_time = datetime.datetime.now()
        self.time_history.append(current_time)

        # Calculate movement duration
        if current_time.hour >= 20:  # If it's late in the day
            self.movement_duration += 60  # Move for 60 minutes
        else:
            self.movement_duration += 30  # Move for 30 minutes

        # Check if the user is currently listening to music
        if self.state == "listening":
            print("User is listening to music. Cannot move.")
            return

    def perform_action(self, current_time, cdn_node):
        # Simulating user actions like searching for music and listening
        if self.state == "searching":
            selected_music = self.search_music()
            if selected_music:
                cdn_song = cdn_node.deliver_content(selected_music, self.location, current_time)
                if cdn_song:
                    self.play_music(cdn_song)
                    self.state = "listening"
                    print(f"Received content from CDN: {cdn_song}")
                else:
                    print("Content not available in CDN")
                    self.continue_searching()
                    self.music_data.log_not_loaded(selected_music)
        elif self.state == "listening":
            self.listen_to_music(current_time)
            self.state = "searching"
        elif self.state == "resting":
            print("User is resting...")
            return

        # Update time history
        self.time_history.append(current_time)


    def search_music(self):
        # Simulating music search based on user preferences
        available_music = self.query_music_database(self.music_preferences)
        if available_music:
            return random.choice(available_music)
        else:
            return None

    def continue_searching(self):
        # Continue searching for music if none is available
        selected_music = self.search_music()
        if selected_music:
            self.play_music(selected_music)
            self.state = "listening"

    def listen_to_music(self, current_time):
        # Simulating user listening to music for a random duration
        selected_music = self.history[-1]
        duration = self.get_song_duration(selected_music)
        self.music_data.log_listening_time(selected_music, duration)
        print(f"Listening to music: {selected_music} for {duration} minutes...")

        # Decrease the movement_duration by the song duration
        self.movement_duration -= duration

        # Simulating user behavior like skipping songs
        if self.should_skip_song():
            print("Skipping the song...")
            self.state = "searching"
            self.music_data.log_skip(selected_music)

        # Simulating time-based behavior
        if current_time.hour >= 20:
            print("It's late in the day. Time to rest...")
            self.state = "resting"

    def should_skip_song(self):
        # Simulating random user behavior to determine if the user skips a song
        skip_probability = 0.3  # Adjusting this value to change the probability of skipping
        return random.random() < skip_probability

    def get_song_duration(self, song):
        # Simulating retrieving the duration of a song from the music database
        song_durations = {
            "Pop Song 1": 4,
            "Pop Song 2": 3,
            "Pop Song 3": 5,
            "Pop Song 4": 4,
            "Rock Song 1": 3,
            "Rock Song 2": 4,
            "Rock Song 3": 5,
            "Rock Song 4": 3,
            "Hip-Hop Song 1": 5,
            "Hip-Hop Song 2": 4,
            "Hip-Hop Song 3": 3,
            "Hip-Hop Song 4": 4,
            "Electronic Song 1": 3,
            "Electronic Song 2": 5,
            "Electronic Song 3": 4,
            "Electronic Song 4": 3,
            "Jazz Song 1": 4,
            "Jazz Song 2": 3,
            "Jazz Song 3": 5,
            "Jazz Song 4": 4,
            "Classical Song 1": 3,
            "Classical Song 2": 4,
            "Classical Song 3": 5,
            "Classical Song 4": 3,
            "Dance Song 1": 4,
            "Dance Song 2": 3,
            "Dance Song 3": 5,
            "Country Song 1": 4,
            "Country Song 2": 3,
            "Country Song 3": 5,
            "Alternative Song 1": 4,
            "Alternative Song 2": 3,
            "Alternative Song 3": 5,
        }
        return song_durations.get(song, 0)  # Return 0 if the song duration is not found

    def play_music(self, music):
        # Simulating playing music and recording it in user history
        print(f"Playing music: {music}")
        self.history.append(music)

    def query_music_database(self, preferences):
        # Simulating querying the music database and returning available music based on user preferences
        available_music = []

        genre_songs = {
            "pop": ["Pop Song 1", "Pop Song 2", "Pop Song 3", "Pop Song 4"],
            "rock": ["Rock Song 1", "Rock Song 2", "Rock Song 3", "Rock Song 4"],
            "hip-hop": ["Hip-Hop Song 1", "Hip-Hop Song 2", "Hip-Hop Song 3", "Hip-Hop Song 4"],
            "electronic": ["Electronic Song 1", "Electronic Song 2", "Electronic Song 3", "Electronic Song 4"],
            "jazz": ["Jazz Song 1", "Jazz Song 2", "Jazz Song 3", "Jazz Song 4"],
            "classical": ["Classical Song 1", "Classical Song 2", "Classical Song 3", "Classical Song 4"],
        }

        for genre in preferences:
            if genre in genre_songs:
                available_music.extend(genre_songs[genre])

        if self.location == "New York Bay Ridge - 86th Street":
            available_music.extend(["NY Location Song 1", "NY Location Song 2", "NY Location Song 3"])
        elif self.location == "Jay Street-MetroTech":
            available_music.extend(["Brooklyn Location Song 1", "Brooklyn Location Song 2", "Brooklyn Location Song 3"])

        return available_music

    def save_data_to_file(data, filename):
        with open(filename, 'wb') as file:
            pickle.dump(data, file)


# Example usage:
cdn_node = CDNNode("CDN1", "New York Bay Ridge - 86th Street", {"77th Street": 2, "Bay Ridge Avenue": 3}, "CDN Location")

user_agent = UserAgent("New York Bay Ridge - 86th Street", ["pop", "rock", "hip-hop"], 100)

for _ in range(5):  # Simulate 5 iterations
    user_agent.move()
    current_time = datetime.datetime.now()
    user_agent.perform_action(current_time, cdn_node)