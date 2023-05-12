import os
import pickle
import pandas as pd
from surprise import Dataset, Reader
from surprise import KNNWithMeans, SVD
from surprise.model_selection import cross_validate

# Load user_agent_data.pkl
def load_data(file_path):
    with open(file_path, "rb") as file:
        data = pickle.load(file)
    return data

data_directory = "data"
user_agent_data_file = os.path.join(data_directory, "user_agent_data.pkl")
user_agent_data = load_data(user_agent_data_file)

# Prepare the data for recommendation engine
def prepare_data(user_agent_data):
    data = []
    for user_id, user_data in enumerate(user_agent_data["history"]):
        for song, song_stats in user_data["song_statistics"].items():
            data.append({sanal-
                "user_id": user_id,
                "song_id": song,
                "genre": song_stats["genre"],
                "listening_count": len(song_stats["listened_time"]),
                "skipped_count": song_stats["skipped"],
                "not_loaded_count": song_stats["not_loaded"],
            })

    return pd.DataFrame(data)

df = prepare_data(user_agent_data)

# Load the data into the surprise library
reader = Reader(rating_scale=(0, df["listening_count"].max()))
data = Dataset.load_from_df(df[["user_id", "song_id", "genre", "listening_count"]], reader)

# Train and evaluate the model
algo = SVD()
cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

# Make a prediction for a user and song
user_id = 0
song_id = "song_0"
rating = algo.predict(user_id, song_id)
print(f"Estimated rating for user {user_id} and song {song_id}: {rating.est}")

def update_cdn_node_with_recommendations(user_agent_data, cdn_node_data, algo, n_recommendations=10):
    for user_id, user_data in enumerate(user_agent_data["history"]):
        user_recommendations = get_recommendations(algo, user_id, n_recommendations)
        cdn_node_data["content"][user_id] = user_recommendations
    return cdn_node_data

def get_recommendations(algo, user_id, n=10):
    all_items = set(song for user_data in user_agent_data["history"] for song in user_data["song_statistics"].keys())
    user_listened_items = set(user_agent_data["history"][user_id]["song_statistics"].keys())
    unlistened_items = all_items - user_listened_items
    predicted_ratings = []

    for item_id in unlistened_items:
        predicted_rating = algo.predict(user_id, item_id)
        predicted_ratings.append((item_id, predicted_rating.est))

    # Sort the items by their predicted ratings and return the top n items
    sorted_items = sorted(predicted_ratings, key=lambda x: x[1], reverse=True)
    return [item_id for item_id, rating in sorted_items[:n]]

