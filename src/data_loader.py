import logging
from neo4j_integration import Neo4jConnection
import json
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def load_products_to_neo4j(products):
    try:
        # Create a Neo4jConnection instance with the correct IP address
        neo4j_connection = Neo4jConnection(
            uri="bolt://172.28.32.1:7687",  # IP address of our Neo4j instance
            user="neo4j",  # Your Neo4j username
            password="your_password"  # Your Neo4j password
        )

        neo4j_connection.connect()

        for product in products:
            logging.debug(f"Processing product: {product}")
            add_product_to_neo4j(neo4j_connection, product)

        neo4j_connection.close()
        logging.debug("Finished loading products into Neo4j.")
    
    except Exception as e:
        logging.error(f"Error loading products into Neo4j: {str(e)}")

def add_product_to_neo4j(connection, product, product_id=None):
    try:
        # If no product_id is provided, generate a unique one based on the title or other fields
        if not product_id:
            product_id = f"{product['title'][:10]}_{product['categories'][0][:5]}"

        query = f"""
        CREATE (p:Product {{
            id: '{product_id}',
            title: '{product['title']}',
            description: '{product['description']}',
            category: '{', '.join(product['categories'])}',
            features: '{', '.join(product['features'])}'
        }})
        """
        connection.run_query(query)
        logging.debug(f"Successfully added product: {product['title']}")
    except Exception as e:
        logging.error(f"Error adding product to Neo4j: {str(e)}")

if __name__ == "__main__":
    # Define the path to your preprocessed JSON file
    data_file_path = os.path.join(os.path.dirname(__file__), "../data/preprocessed.json")
    
    try:
        # Load products from the preprocessed JSON file
        with open(data_file_path, "r") as file:
            products = json.load(file)

        load_products_to_neo4j(products)
    
    except Exception as e:
        logging.error(f"Error reading products file {data_file_path}: {str(e)}")
