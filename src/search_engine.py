import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet
import redis
import json

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)



# Initialize the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load product embeddings from the file
with open('../data/product_embeddings.json', 'r') as file:
    product_embeddings = json.load(file)


def expand_query(query):
    """
    Expand the user's search query by finding synonyms of the main keywords.
    
    Args:
    query (str): The user's search query.
    
    Returns:
    list: A list of expanded terms including the original query terms and their synonyms.
    """
    expanded_terms = set(query.split())  # Include the original query terms
    for word in query.split():
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                expanded_terms.add(lemma.name().replace('_', ' '))  # Include synonyms

    return list(expanded_terms)


def search_products(query, top_n=5):
    """
    Perform a semantic search and return the top N products based on cosine similarity with the query.
    Utilizes Redis caching to store and retrieve results for repeated queries.

    Args:
    query (str): The search query from the user.
    top_n (int): The number of top results to return.

    Returns:
    list: A list of the top N most similar products and their similarity scores.
    """
    # Check if the query result exists in Redis
    cached_results = redis_client.get(query)
    if cached_results:
        print("Cache hit for query:", query)
        return json.loads(cached_results)

    print("Cache miss for query:", query)

    # Expand the query to include synonyms
    query_terms = expand_query(query)

    # Compute the embeddings for each expanded query term
    query_embeddings = [model.encode(term) for term in query_terms]

    similarities = []
    for product in product_embeddings:
        product_embedding = np.array(product['embedding'])

        # Compute the maximum similarity between the query and the product embedding
        max_similarity = max(
            cosine_similarity([query_embedding], [product_embedding])[0][0]
            for query_embedding in query_embeddings
        )

        similarities.append((product, max_similarity))  # Store product and its max similarity

    # Sort products by similarity (descending order)
    sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

    # Return the top N results
    top_results = sorted_similarities[:top_n]
    formatted_results = [
        {
            'title': product['title'],
            'description': product['description'],
            'categories': product.get('categories', []),
            'features': product.get('features', []),
            'similarity': similarity
        }
        for product, similarity in top_results
    ]

    # Store the results in Redis (set with an expiration time of 1 hour)
    redis_client.set(query, json.dumps(formatted_results), ex=3600)

    return formatted_results




def filter_products(results, category_filter=None, feature_filters=None):
    """
    Filters the search results based on category and features.

    Args:
        results (list): List of products to filter.
        category_filter (list): List of selected categories to include.
        feature_filters (list): List of selected features to include.

    Returns:
        list: Filtered list of products.
    """
    filtered_results = results

    # Filter by categories
    if category_filter:
        category_filter = [cat.lower() for cat in category_filter]  # Convert to lowercase for case-insensitive comparison
        filtered_results = [
            product for product in filtered_results
            if any(cat.lower() in category_filter for cat in product.get('categories', []))
        ]

    # Filter by features
    if feature_filters:
        feature_filters = [feature.lower() for feature in feature_filters]  # Convert to lowercase
        filtered_results = [
            product for product in filtered_results
            if all(feature.lower() in [f.lower() for f in product.get('features', [])] for feature in feature_filters)
        ]

    return filtered_results
