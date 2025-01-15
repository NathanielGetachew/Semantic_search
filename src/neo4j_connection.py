from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        self.session = None

    def connect(self):
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            self.session = self.driver.session()
            print(f"Successfully connected to Neo4j at {self.uri}")
        except Exception as e:
            print(f"Failed to connect to Neo4j: {str(e)}")
            raise

    def close(self):
        if self.session:
            self.session.close()
        if self.driver:
            self.driver.close()

    def run_query(self, query):
        try:
            return self.session.run(query)
        except Exception as e:
            print(f"Error running query: {str(e)}")
            raise
