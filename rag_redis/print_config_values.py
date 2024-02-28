# print_config_values.py

try:
    from rag_redis.config import EMBED_MODEL, INDEX_NAME, INDEX_SCHEMA, REDIS_URL

    print("EMBED_MODEL:", EMBED_MODEL)
    print("INDEX_NAME:", INDEX_NAME)
    print("INDEX_SCHEMA:", INDEX_SCHEMA)
    print("REDIS_URL:", REDIS_URL)

except ImportError as e:
    print("Error importing from rag_redis.config:", e)