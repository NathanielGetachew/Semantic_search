import json
import re

def clean_text(text):
    """
    Clean text by lowercasing, removing special characters, and fixing Unicode issues.
    Handles both strings and lists.
    """
    if isinstance(text, list):  # If the input is a list, clean each item
        return [clean_text(item) for item in text]
    elif isinstance(text, str):  # If the input is a string, clean it
        text = text.lower()
        text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
        text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
        return text
    else:  # If the input is neither a list nor a string, return an empty string
        return ""

def get_combined_text(product):
    """
    Combine title, description, features, and product details into a single string.
    """
    title = clean_text(product.get('title', ''))
    description = clean_text(product.get('description', ''))
    features = clean_text(product.get('features', []))
    product_details = clean_text([f"{detail['type']}: {detail['value']}" for detail in product.get('product_details', [])])
    
    combined_text = f"{title} {description} {' '.join(features)} {' '.join(product_details)}"
    return combined_text

def preprocess_data(input_file, output_file):
    """
    Preprocess the dataset by cleaning and combining fields.
    """
    try:
        # Load the original JSON file
        with open(input_file, 'r', encoding='utf-8') as file:
            products = json.load(file)

        # Preprocess each product
        preprocessed_data = []
        for product in products:
            preprocessed_product = {
                'title': clean_text(product.get('title', '')),
                'description': clean_text(product.get('description', '')),
                'categories': clean_text(product.get('categories', [])),
                'features': clean_text(product.get('features', [])),
                'product_details': clean_text([f"{detail['type']}: {detail['value']}" for detail in product.get('product_details', [])]),
                'combined_text': get_combined_text(product)  # Combined text for embeddings
            }
            preprocessed_data.append(preprocessed_product)

        # Save the preprocessed data to a new JSON file
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(preprocessed_data, file, indent=4)

        print(f"Preprocessing complete. Saved data to {output_file}")

    except Exception as e:
        print(f"Error during preprocessing: {e}")

# Define the input and output file paths
input_file = './data/products.json'  # Path to the original dataset
output_file = './data/preprocessed.json'  # Path to save the preprocessed data

# Run preprocessing
preprocess_data(input_file, output_file)