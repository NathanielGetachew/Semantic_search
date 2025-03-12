from neo4j import GraphDatabase

# Neo4j connection setup
uri = "bolt://localhost:7687"  # Change to your Neo4j instance URI
username = "neo4j"
password = "natty123"  # Replace with your Neo4j password
driver = GraphDatabase.driver(uri, auth=(username, password))

def add_product_to_neo4j(product, index):
    """
    Adds a product to Neo4j.
    If no 'id' field is present, we generate a unique ID based on the index.
    """
    try:
        product_id = str(index)

        query = """
        MERGE (p:Product {id: $id})
        ON CREATE SET p.title = $title, 
                      p.description = $description, 
                      p.features = $features, 
                      p.categories = $categories,
                      p.created = timestamp()
        """
        with driver.session() as session:
            session.run(query, 
                        id=product_id, 
                        title=product['title'], 
                        description=product['description'],
                        features=product.get('features', []),  # Avoid KeyError
                        categories=product.get('categories', []))  # Avoid KeyError
    except Exception as e:
        print(f"Error adding product to Neo4j: {e}")

def add_all_products_to_neo4j(products):
    """
    Adds all products to Neo4j.
    """
    for index, product in enumerate(products):
        add_product_to_neo4j(product, index)

def get_product_recommendations(category, top_n=5):
    """
    Fetches product recommendations from Neo4j based on the category.
    """
    try:
        query = """
        MATCH (p:Product)
        WHERE $category IN p.categories
        RETURN p.title AS title, p.description AS description, p.features AS features
        LIMIT $top_n
        """
        with driver.session() as session:
            result = session.run(query, category=category, top_n=top_n)
            recommendations = []
            for record in result:
                recommendations.append({
                    'title': record['title'],
                    'description': record['description'],
                    'features': record['features']
                })
            return recommendations
    except Exception as e:
        print(f"Error fetching product recommendations from Neo4j: {e}")
        return []

def close_neo4j_driver():
    """
    Closes the Neo4j driver to free up resources.
    """
    driver.close()
