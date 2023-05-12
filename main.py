import os
import pickle
import datetime
from user_agent import UserAgent
from cdn_nodes import CDNNode
from recommendation_engine import update_cdn_node_with_recommendations
from simulation import cdn_simulation, frontloaded_simulation
import multiprocessing

def save_data_to_file(data, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(data, f)

def load_data_from_file(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(f)

class CDNNode:
    def __init__(self, node_id, content):
        self.node_id = node_id
        self.content = content
        self.frontloaded_content = {}
        self.user_behavior = defaultdict(lambda: defaultdict(dict))
        self.color = (0, 255, 0)  # Green color for active nodes

    def set_inactive(self):
        self.color = (255, 0, 0)  # Red color for inactive nodes

    def set_active(self):
        self.color = (0, 255, 0)  # Green color for active nodes


class Station:
    def __init__(self, station_id):
        self.station_id = station_id
        self.color = (0, 0, 255)  # Blue color for active stations

    def set_inactive(self):
        self.color = (128, 128, 128)  # Gray color for inactive stations

    def set_active(self):
        self.color = (0, 0, 255)  # Blue color for active stations


# Example usage:
cdn_node = CDNNode("CDN1", "New York Bay Ridge - 86th Street", {"77th Street": 2, "Bay Ridge Avenue": 3}, "CDN Location")

user_agent = UserAgent("New York Bay Ridge - 86th Street", ["pop", "rock", "hip-hop"], 100)

for _ in range(5):  # Simulate user actions for 5 iterations
    user_agent.move()
    current_time = datetime.datetime.now()
    user_agent.perform_action(current_time, cdn_node)

# Create the data directory if it doesn't exist
data_directory = "data"
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# Save the user agent's data
user_agent_data = {
    "history": user_agent.history,
    "location_history": user_agent.location_history,
    "time_history": user_agent.time_history,
}
save_data_to_file(user_agent_data, os.path.join(data_directory, "user_agent_data.pkl"))

# Save the music data
music_data = {
    "listening_time": user_agent.music_data.listening_time,
    "skip_count": user_agent.music_data.skip_count,
    "not_loaded_count": user_agent.music_data.not_loaded_count,
    "location_based_data": user_agent.music_data.location_based_data,
}
save_data_to_file(music_data, os.path.join(data_directory, "music_data.pkl"))

from simulation import cdn_simulation, frontloaded_simulation

def main():
    p1 = multiprocessing.Process(target=cdn_simulation)
    p2 = multiprocessing.Process(target=frontloaded_simulation)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    # Constants for cost calculation
    data_transfer_cost = 0.01  # cost per unit of data transfer
    storage_cost = 0.005  # cost per unit of storage
    recommendation_request_cost = 0.1  # cost per recommendation request

    # Calculate the costs
    cdn_total_cost = cdn_simulation_data_transfer * data_transfer_cost + cdn_simulation_storage * storage_cost
    frontloaded_total_cost = frontloaded_simulation_data_transfer * data_transfer_cost + frontloaded_simulation_storage * storage_cost + frontloaded_simulation_recommendation_requests * recommendation_request_cost

    # Compare the costs
    if cdn_total_cost < frontloaded_total_cost:
        print("CDN simulation is more cost-effective.")
        print(f"CDN total cost: {cdn_total_cost}")
        print(f"Frontloaded total cost: {frontloaded_total_cost}")
    elif cdn_total_cost > frontloaded_total_cost:
        print("Frontloaded simulation is more cost-effective.")
        print(f"CDN total cost: {cdn_total_cost}")
        print(f"Frontloaded total cost: {frontloaded_total_cost}")
    else:
        print("Both simulations have the same cost.")
        print(f"CDN total cost: {cdn_total_cost}")
        print(f"Frontloaded total cost: {frontloaded_total_cost}")


# Save the CDN node's data
cdn_node_data = {
    "content": cdn_node.content,
    "frontloaded_content": cdn_node.frontloaded_content,
    "user_behavior": cdn_node.user_behavior,
}
save_data_to_file(cdn_node_data, os.path.join(data_directory, "cdn_node_data.pkl"))


# Saved data for further analysis
loaded_user_agent_data = load_data_from_file(os.path.join(data_directory, "user_agent_data.pkl"))
loaded_cdn_node_data = load_data_from_file(os.path.join(data_directory, "cdn_node_data.pkl"))
loaded_music_data = load_data_from_file(os.path.join(data_directory, "music_data.pkl"))

# loaded data for recommendation engine training
updated_cdn_node_data = update_cdn_node_with_recommendations(user_agent_data, cdn_node_data, algo)
save_data_to_file(updated_cdn_node_data, os.path.join(data_directory, "cdn_node_data.pkl"))


if __name__ == "__main__":
    with multiprocessing.Pool(processes=2) as pool:
        results = pool.map_async(func, [cdn_simulation, frontloaded_simulation])
        cdn_cost, frontloading_cost = results.get()
    main()

