from dotenv import load_dotenv
from db import Neo4jConnection
import os
from seeder import add_node, add_relationship
from fraudDetection import add_fraud_transaction, check_impossible_travel
load_dotenv()

URI = os.getenv("NEO4J_URI_LOCAL")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))


neo4j_db = Neo4jConnection(URI, auth=AUTH)

load_dummy_data = False

if __name__ == "__main__":
    if load_dummy_data:
        print("\nLoading dummy data...")
        neo4j_db.execute_write(add_node)
        neo4j_db.execute_write(add_relationship)
        print("Dummy data loaded successfully.")

    # a customer submit a transaction request 

    #neo4j_db.execute_write(add_fraud_transaction)
    results=neo4j_db.query(check_impossible_travel)

    print(results)
    neo4j_db.close()