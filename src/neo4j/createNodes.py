from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import csv

load_dotenv()
NEO4J_URI = os.getenv("NEO4J_URI_LOCAL")
NEO4J_USER = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

class Neo4jProvider:
    def __init__(self):
        try:
            self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
            self.driver.verify_connectivity()
            print("Connected to Neo4j")
        except Exception as e:
            print("Error connecting to Neo4j")
            print(e)

    def close(self):
        self.driver.close()
        print("Closed connection to Neo4j")

    def create_person(self, data):
        with self.driver.session() as session:
            session.run("CREATE (p:Person {name: $name, age: $age, location: $location, email: $email})", data)
            print("Person created successfully")

    def create_relationship(self,name1,name2):
        with self.driver.session() as session:
            session.run("MATCH (a:Person {name: $name1}) MATCH (b:Person {name: $name2}) CREATE (a)-[:FRIENDS_WITH]->(b)", {"name1": name1, "name2": name2})
            print("Relationship created successfully")

    def load_people_from_csv(self, csv_path):
        count = 0
        with open(csv_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                self.create_person({
                    "name": row["Name"],
                    "age": int(row["Age"]),
                    "location": row["City"],
                    "email": row["Email"],
                })
                count += 1
        print(f"Created {count} Person nodes")
        return count


if __name__ == "__main__":
    neo4j_provider = Neo4jProvider()
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "people.csv")
    #neo4j_provider.load_people_from_csv(csv_path)
    #neo4j_provider.create_relationship("Jeremy Ware", "Whitney Cantrell")
    neo4j_provider.create_relationship( "Jeremy Ware","Whitney Cantrell")
    neo4j_provider.close()