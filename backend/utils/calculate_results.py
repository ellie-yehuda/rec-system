from pymongo import MongoClient
import numpy as np

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['restaurant_db']
collection = db['user_ratings']

# Retrieve all user ratings
data = collection.find()

# Initialize lists for rankings
median_ours_list = []
average_random_list = []
average_highly_rated_list = []

# Counter for the number of users
num_users = 0

# Process each user's ratings
for entry in data:
    rated_restaurants = entry['rated_restaurants']

    # Extract ranks based on categories
    ours_ranks = [r['rank'] for r in rated_restaurants if r['category'] == 'ours']
    random_rank = next(r['rank'] for r in rated_restaurants if r['category'] == 'random')
    highly_rated_rank = next(r['rank'] for r in rated_restaurants if r['category'] == 'highly rated')

    # Calculate median of 'ours' rankings
    median_ours = np.median(ours_ranks)
    median_ours_list.append(median_ours)

    # Add random and highly rated ranks to respective lists
    average_random_list.append(random_rank)
    average_highly_rated_list.append(highly_rated_rank)

    # Increment user counter
    num_users += 1

# Calculate results
average_of_median_ours = np.mean(median_ours_list)
average_random = np.mean(average_random_list)
average_highly_rated = np.mean(average_highly_rated_list)

# Display the results
print("Results:")
print(f"Number of Users: {num_users}")
print(f"Average of Median Rankings (Ours): {average_of_median_ours:.2f}")
print(f"Average Rankings (Random): {average_random:.2f}")
print(f"Average Rankings (Highly Rated): {average_highly_rated:.2f}")

# Determine success levels
partial_success = average_of_median_ours < average_random
complete_success = average_of_median_ours < average_random and average_of_median_ours < average_highly_rated

print("\nEvaluation:")
print(f"Partial Success: {'Yes' if partial_success else 'No'}")
print(f"Complete Success: {'Yes' if complete_success else 'No'}")