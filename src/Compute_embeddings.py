import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def compute_embeddings(input_file, output_json, output_npy, model_name='all-MiniLM-L6-v2', batch_size=32):
    """
    Compute embeddings for each product in the preprocessed dataset and save in JSON and NumPy format.
    """
    try:
        # Load the preprocessed data
        with open(input_file, 'r', encoding='utf-8') as file:
            preprocessed_data = json.load(file)

        # Initialize the SentenceTransformer model
        model = SentenceTransformer(model_name)

        # Prepare texts for embedding
        product_titles = []
        product_categories = []
        product_features = []
        metadata = []

        for product in preprocessed_data:
            title = product.get('title', '')
            description = product.get('description', '')
            categories = " ".join(product.get('categories', []))  # Ensure categories are a single string
            features = " ".join(product.get('features', []))  # Ensure features are a single string

            product_titles.append(title)
            product_categories.append(categories)
            product_features.append(features)

            # Save metadata (without embeddings) for reference
            metadata.append({
                'title': title,
                'description': description,
                'categories': product.get('categories', []),
                'features': product.get('features', [])
            })

        # Compute embeddings in batches for each field
        title_embeddings = model.encode(product_titles, batch_size=batch_size, convert_to_numpy=True)
        category_embeddings = model.encode(product_categories, batch_size=batch_size, convert_to_numpy=True)
        features_embeddings = model.encode(product_features, batch_size=batch_size, convert_to_numpy=True)

        # Save metadata and embeddings separately
        with open(output_json, 'w', encoding='utf-8') as file:
            json.dump(metadata, file, indent=4)

        np.save(output_npy, {
            'titles': title_embeddings,
            'categories': category_embeddings,
            'features': features_embeddings
        })  # Save embeddings as a NumPy binary file

        print(f"Embeddings computed and saved to {output_json} and {output_npy}")

    except Exception as e:
        print(f"Error during embedding computation: {e}")

def compute_cosine_similarity(query, product_embeddings, model_name='all-MiniLM-L6-v2'):
    """
    Compute cosine similarity between the query and product embeddings for title, category, and features.
    """
    try:
        # Initialize the SentenceTransformer model for encoding the query
        model = SentenceTransformer(model_name)

        # Compute the query embedding
        query_embedding = model.encode(query, convert_to_numpy=True).reshape(1, -1)  # Ensure it's 2D for cosine similarity

        # Calculate cosine similarities with each product field's embedding
        title_similarity = cosine_similarity(query_embedding, product_embeddings['titles'])
        category_similarity = cosine_similarity(query_embedding, product_embeddings['categories'])
        features_similarity = cosine_similarity(query_embedding, product_embeddings['features'])

        # Average the similarities for final similarity score
        final_similarity = np.mean([title_similarity, category_similarity, features_similarity], axis=0)

        return final_similarity

    except Exception as e:
        print(f"Error during cosine similarity computation: {e}")
        return None


# Example usage of the embedding and similarity functions

# Define input and output file paths
input_file = './data/preprocessed.json'  # Path to the preprocessed data
output_json = './data/product_metadata.json'  # Save metadata without embeddings
output_npy = './data/product_embeddings.npy'  # Save embeddings as NumPy binary file

# Run embedding computation
compute_embeddings(input_file, output_json, output_npy)

# Example query
query = "wireless mouse"

# Load product embeddings
product_embeddings = np.load(output_npy, allow_pickle=True).item()

# Compute cosine similarity between query and product embeddings
similarities = compute_cosine_similarity(query, product_embeddings)

# Print the similarity scores
if similarities is not None:
    print(similarities)
