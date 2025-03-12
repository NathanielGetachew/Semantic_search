import redis
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to Redis
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

class ContextManager:
    def __init__(self, session_id):
        """Initialize context storage for a specific session."""
        self.session_id = session_id  # Unique ID for each user/session

    def store_context(self, user_query, bot_response):
        """Store user query and bot response in Redis."""
        conversation = {"query": user_query, "response": bot_response}
        redis_client.rpush(f"context:{self.session_id}", json.dumps(conversation))

    def get_context(self, last_n=5):
        """Retrieve the last 'n' conversations from Redis."""
        conversations = redis_client.lrange(f"context:{self.session_id}", -last_n, -1)
        return [json.loads(conv) for conv in conversations]

    def clear_context(self):
        """Clear stored context for this session."""
        redis_client.delete(f"context:{self.session_id}")

# Example usage
if __name__ == "__main__":
    session = ContextManager("user_123")  # Unique user session
    session.store_context("Who is Elon Musk?", "Elon Musk is the CEO of Tesla.")
    session.store_context("Where was he born?", "He was born in South Africa.")
    
    print("Stored Context:", session.get_context())  # Retrieve stored conversations
