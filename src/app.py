from flask import Flask, request, render_template, jsonify
from search_engine import search_products, filter_products  # Import functions from models.py
import redis
import json

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

app = Flask(__name__)

@app.route('/')
def home():
    """
    Render the search page where users can enter their query.
    """
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """
    Perform semantic search and return results to be displayed on the results page.
    """
    data = request.json  # Get the JSON data
    query = data.get('query', '')

    # Step 1: Perform semantic search
    search_results = search_products(query)

    # Step 2: Extract unique categories dynamically
    categories = {cat for product in search_results for cat in product.get('categories', [])}

    # Return the results and categories
    return jsonify({'results': search_results, 'categories': list(categories)})

@app.route('/filter', methods=['POST'])
def filter_results():
    """
    Apply filtering to the search results based on selected categories and features.
    """
    data = request.json  # Get the JSON data
    results = data.get('results', [])  # Results to be filtered
    category_filter = data.get('categories', None)
    feature_filters = data.get('features', [])

    # Apply filters on the results
    filtered_results = filter_products(results, category_filter=category_filter, feature_filters=feature_filters)

    return jsonify(filtered_results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
