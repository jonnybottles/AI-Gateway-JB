import redis

# Redis connection details
host = "your-redis-cache.region.redis.azure.net"
port = 10000
password = "your-redis-password-here"

# Connect to Redis
r = redis.Redis(host=host, port=port, password=password, ssl=True)

# Get all keys before clearing
keys_before = r.keys('*')
print(f'Keys in cache before clearing: {len(keys_before)}')

# Clear all keys
if keys_before:
    for key in keys_before:
        r.delete(key)
    print(f'Deleted {len(keys_before)} keys from cache')
else:
    print('Cache was already empty')

# Verify cache is empty
keys_after = r.keys('*')
print(f'Keys in cache after clearing: {len(keys_after)}')

if len(keys_after) == 0:
    print('✓ Cache successfully cleared!')
else:
    print(f'⚠ Warning: {len(keys_after)} keys still remain')
