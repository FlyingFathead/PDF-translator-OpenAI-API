# rag_redis_delete_all_indexes.py

import redis

# Connect to your Redis server
redis_url = "redis://localhost:6379"  # Update with your Redis server details
r = redis.StrictRedis.from_url(redis_url)

# Get a list of all keys (indexes)
keys = r.keys('*')

# Ask for confirmation
confirmation = input("Are you sure you want to delete all indexes in Redis? (Y/n): ")

if confirmation.lower() == 'y':
    # Delete all indexes
    for key in keys:
        r.delete(key)
    print("All indexes have been deleted.")
else:
    print("Deletion aborted.")