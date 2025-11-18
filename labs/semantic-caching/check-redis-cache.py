#!/usr/bin/env python3
"""
Redis Semantic Cache Inspector
Inspects the Redis cache used by Azure API Management semantic caching policy
"""

import sys
import json
import redis

# Configuration
REDIS_HOST = "your-redis-cache.region.redis.azure.net"
REDIS_PORT = 10000
REDIS_PASSWORD = "your-redis-password-here"

def main():
    try:
        # Connect to Redis
        r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            ssl=True,
            decode_responses=False  # Keep as bytes for binary data handling
        )
        
        # Test connection
        r.ping()
        
        # Get all keys
        keys = r.keys('*')
        
        if not keys:
            print("Cache is empty - no entries found")
            print("Run some API requests first to populate the cache")
        else:
            print("-" * 60)
            print("Cached Entries:")
            print("-" * 60)
            
            for idx, key in enumerate(keys, 1):
                key_str = key.decode('utf-8') if isinstance(key, bytes) else key
                print(f"Entry {idx}/{len(keys)}")
                
                # Get TTL
                ttl = r.ttl(key)
                if ttl > 0:
                    print(f"TTL: {ttl} seconds remaining")
                elif ttl == -1:
                    print(f"TTL: No expiration")
                else:
                    print(f"TTL: Expired")
                
                # Get key type
                key_type = r.type(key).decode('utf-8') if isinstance(r.type(key), bytes) else r.type(key)
                
                # If it's a hash, get all fields
                if key_type == 'hash':
                    hash_data = r.hgetall(key)
                    
                    # First pass: display vector immediately after TTL
                    for field_name_bytes, field_val in hash_data.items():
                        field_name = field_name_bytes.decode('utf-8') if isinstance(field_name_bytes, bytes) else field_name_bytes
                        if field_name == 'Vector':
                            import struct
                            try:
                                num_floats = min(5, len(field_val) // 4)
                                floats = struct.unpack(f'{num_floats}f', field_val[:num_floats * 4])
                                floats_str = ', '.join(f'{f:.6f}' for f in floats)
                                print(f"Vector: [{floats_str}, ...]")
                            except:
                                print(f"Vector: [binary vector data]")
                            break
                    
                    # Second pass: display cache entry
                    for field_name_bytes, field_val in hash_data.items():
                        field_name = field_name_bytes.decode('utf-8') if isinstance(field_name_bytes, bytes) else field_name_bytes
                        
                        # Handle CacheEntry field (protobuf-encoded HTTP response from APIM)
                        if field_name == 'CacheEntry':
                            print(f"CacheEntry:")
                            
                            # Try to extract JSON body from protobuf-encoded response
                            try:
                                # Look for JSON body in the binary data
                                body_start = field_val.find(b'{"')
                                if body_start > 0:
                                    json_data = field_val[body_start:]
                                    json_str = json_data.decode('utf-8', errors='ignore')
                                    
                                    # Try to find complete JSON object
                                    try:
                                        response_data = json.loads(json_str)
                                        
                                        # Extract OpenAI response content
                                        if 'choices' in response_data and len(response_data['choices']) > 0:
                                            choice = response_data['choices'][0]
                                            if 'message' in choice:
                                                message = choice['message']
                                                content = message.get('content', '')
                                                print(f"  {content}")
                                    except json.JSONDecodeError:
                                        # Try to extract just the content field with regex
                                        import re
                                        content_match = re.search(r'"content":\s*"([^"]+)"', json_str)
                                        if content_match:
                                            print(f"  {content_match.group(1)}")
                                else:
                                    print(f"  Could not find JSON body in protobuf data")
                            except Exception as e:
                                print(f"  Error parsing: {e}")
                
                print()
        
        # Print vector format info
        print()
        print("Vector Format Information:")
        print("  Dimensions: 1536 (text-embedding-3-small)")
        print("  Precision: FP32 (32-bit floating point)")
        print("  Storage: 4 bytes per dimension (32 bits)")
        print("  Total size: 6,144 bytes per vector")
        print("  Display: Decimal representation (e.g., -0.042272)")
        print()
        
        print("=" * 60)
        
    except redis.ConnectionError as e:
        print(f"Failed to connect to Redis: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
