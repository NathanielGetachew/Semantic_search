import json
from sentence_transformers import SentenceTransformer
import numpy as np

# Load data
input_file = '../data/products.json'
with open(input_file, 'r') as file:
    products = json.load(file)

# Initialize the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Compute embeddings for each product
product_embeddings = []
for product in products:
    # Get title, description, category, and features
    title = product.get('title', "")
    description = product.get('description', "")
    category = product.get('categories', "")
    features = " ".join(product.get('features', []))  # Join features into a single string

    # Combine all relevant fields into a single string for embedding computation
    combined_text = f"{title} {description} {category} {features}"

    # Compute embedding
    embedding = model.encode(combined_text)

    # Append the embedding and other data to the product dictionary
    product_embeddings.append({
        'title': title,
        'description': description,
        'categories': category,
        'features': product.get('features', []),  # Keep features as a list
        'embedding': embedding.tolist()  # Convert ndarray to list
    })

# Save the updated embeddings to a JSON file
output_file = '../data/product_embeddings.json'
with open(output_file, 'w') as file:
    json.dump(product_embeddings, file, indent=4)

print("Updated embeddings computed and saved successfully!")
