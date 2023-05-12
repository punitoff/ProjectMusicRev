import random
import datetime

class CDNNode:
    def __init__(self, name, location, network, cdn_location):
        self.name = name
        self.location = location
        self.network = network
        self.cdn_location = cdn_location
        self.content = {}
        self.frontloaded_content = {}
        self.user_behavior = {}

    # Define the network latencies between stations
    network_latencies = {
        "New York Bay Ridge - 86th Street": {
            "77th Street": 2,
            "Bay Ridge Avenue": 3,
            "59th Street": 4,
            "53rd Street": 2,
            "45th Street": 3,
            "36th Street": 2,
            "25th Street": 4,
            "Prospect Avenue": 3,
            "9th Street": 4,
            "Union Street": 3,
            "4th Avenue - 9th Street": 2,
            "DeKalb Avenue": 4,
            "Jay Street-MetroTech": 5
        },

    }

    def add_content(self, song, availability_time):
        self.content[song] = availability_time

    def frontload_content(self, song, availability_time):
        self.frontloaded_content[song] = availability_time

    def deliver_content(self, song, user_location, current_time):
        network_latency = self.calculate_network_latency(user_location)
        cdn_latency = self.calculate_cdn_latency(user_location)
        total_latency = network_latency + cdn_latency

        availability_time = self.content.get(song)
        if availability_time and availability_time <= current_time + datetime.timedelta(minutes=total_latency):
            return song
        else:
            return None

    def calculate_network_latency(self, user_location):
        if user_location == self.location:
            return 0
        elif user_location in self.network_latencies[self.location]:
            return self.network_latencies[self.location][user_location]
        else:
            return float('inf')

    def calculate_cdn_latency(self, user_location):
        if user_location == self.location:
            return 0
        elif user_location == self.cdn_location:
            return random.randint(1, 5)  # Adjust latency based on specific CDN location
        else:
            return float('inf')

    def learn_user_behavior(self, song, listened_time):
        if song not in self.user_behavior:
            self.user_behavior[song] = []
        self.user_behavior[song].append(listened_time)

