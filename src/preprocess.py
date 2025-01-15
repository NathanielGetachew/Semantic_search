import json

# Define the input and output file paths
input_file = '../data/products.json'  # Adjust the path if necessary
output_file = '../data/preprocessed.json'  # Save in the data directory

# Load the large JSON file
with open(input_file, 'r') as file:
    data = json.load(file)

# Isolate the necessary fields: title, description, categories, and features
processed_data = []
for item in data:
    processed_item = {
        'title': item.get('title', ''),
        'description': item.get('description', ''),
        'categories': item.get('categories', []),  # Assuming categories is a list
        'features': item.get('features', [])  # Assuming features is a list
    }
    processed_data.append(processed_item)

# Save the preprocessed data to a new JSON file
with open(output_file, 'w') as file:
    json.dump(processed_data, file, indent=4)

print(f"Preprocessing complete. Saved data to {output_file}")
