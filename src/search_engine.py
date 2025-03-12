import json
import numpy as np
import logging
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import redis
from datetime import datetime
from thefuzz import process
import nltk
from nltk.corpus import wordnet
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Download necessary NLTK data
nltk.download("wordnet")

# Initialize Redis client
try:
    redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
except redis.ConnectionError:
    logging.error("Failed to connect to Redis. Make sure Redis is running.")
    redis_client = None

# Load product metadata
try:
    with open("./data/product_metadata.json", "r", encoding="utf-8") as file:
        product_metadata = json.load(file)
except FileNotFoundError:
    logging.error("Product metadata file not found.")
    product_metadata = []

# Load product embeddings
try:
    product_embeddings = np.load("./data/product_embeddings.npy", allow_pickle=True).item()
    
    # Ensure correct format
    if not isinstance(product_embeddings, dict) or "titles" not in product_embeddings:
        raise ValueError("Invalid embeddings file format")
    
    # Debugging: Log the shape and type of product embeddings
    logging.info("Loaded product embeddings successfully.")
    logging.info(f"Type of product_embeddings['titles']: {type(product_embeddings['titles'])}")
    
    if isinstance(product_embeddings["titles"], np.ndarray):
        logging.info(f"Shape of product_embeddings['titles']: {product_embeddings['titles'].shape}")
        logging.info(f"First 5 product embeddings: {product_embeddings['titles'][:5]}")
    
except (FileNotFoundError, ValueError) as e:
    logging.error(f"Error loading product embeddings: {str(e)}")
    product_embeddings = {"titles": np.array([])}

# Initialize the SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def simple_tokenize(text):
    """
    Tokenizes text by splitting on spaces and removing non-alphabetic characters.
    """
    return re.findall(r"\b\w+\b", text.lower())  # Extracts words and converts to lowercase

def expand_query(query):
    """
    Expands the search query using WordNet synonyms.
    """
    expanded_terms = set(simple_tokenize(query))  # Tokenize input query

    for word in expanded_terms.copy():  # Iterate over original words
        for syn in wordnet.synsets(word):  # Find WordNet synsets
            for lemma in syn.lemmas():
                expanded_terms.add(lemma.name().replace("_", " "))  # Add synonyms

    return list(expanded_terms)

def search_products(user_id, query, top_n=5):
    """Performs semantic search with caching and query expansion."""
    redis_key = f"search_results:{query}"
    cached_results = redis_client.get(redis_key) if redis_client else None

    if cached_results:
        logging.info("Cache hit for query: %s", query)
        return json.loads(cached_results)

    logging.info("Cache miss for query: %s", query)
    query_terms = expand_query(query)

    # Compute mean embedding for expanded query
    try:
        query_embedding = np.mean([model.encode(term) for term in query_terms], axis=0)
        logging.info(f"Query embedding shape: {query_embedding.shape}")
    except Exception as e:
        logging.error("Error computing query embedding: %s", str(e))
        return []

    # Ensure embeddings are loaded properly
    if "titles" not in product_embeddings or not isinstance(product_embeddings["titles"], np.ndarray):
        logging.error("Product embeddings are not properly loaded.")
        return []

    product_vectors = product_embeddings["titles"]  # This is a 2D NumPy array
    product_ids = list(range(len(product_vectors)))  # Generate numerical indices

    if len(product_vectors) == 0:
        logging.error("No valid product embeddings found.")
        return []

    # Compute cosine similarity
    similarities = cosine_similarity([query_embedding], product_vectors)[0]
    
    # Rank products based on similarity
    ranked_products = sorted(zip(product_ids, similarities), key=lambda x: x[1], reverse=True)[:top_n]

    # Format results
    formatted_results = [
        {
            "title": product_metadata[pid]["title"] if pid < len(product_metadata) else "Unknown",
            "description": product_metadata[pid].get("description", ""),
            "categories": product_metadata[pid].get("categories", []),
            "features": product_metadata[pid].get("features", []),
            "similarity": float(similarity),
        }
        for pid, similarity in ranked_products
    ]

    # Cache the results
    if redis_client:
        redis_client.set(redis_key, json.dumps(formatted_results), ex=3600)
        search_entry = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "result_count": len(formatted_results),
        }
        redis_client.lpush(f"user:{user_id}:search_history", json.dumps(search_entry))
        redis_client.ltrim(f"user:{user_id}:search_history", 0, 9)

    return formatted_results

def get_user_search_history(user_id):
    """Retrieves the last 10 searches by a user."""
    search_history = redis_client.lrange(f"user:{user_id}:search_history", 0, -1) if redis_client else []
    return [json.loads(entry) for entry in search_history]

def recommend_based_on_history(user_id, top_n=5):
    """Recommends products based on the last search."""
    search_history = get_user_search_history(user_id)
    if not search_history:
        return []
    return search_products(user_id, search_history[0]["query"], top_n)

def filter_products(results, category_filter=None, feature_filters=None):
    """Filters search results based on categories and features using fuzzy matching."""
    if category_filter:
        category_filter = [cat.lower() for cat in category_filter]
        results = [
            product
            for product in results
            if any(process.extractOne(cat, product.get("categories", []))[1] >= 80 for cat in category_filter)
        ]

    if feature_filters:
        feature_filters = [feature.lower() for feature in feature_filters]
        results = [
            product
            for product in results
            if all(process.extractOne(feature, product.get("features", []))[1] >= 80 for feature in feature_filters)
        ]

    return results
