from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)
        print("Neo4j connection obtained")


    def close(self):
        if self.driver:
            self.driver.close()
            print("Neo4j connection closed")

    def execute_write(self, method):
        with self.driver.session() as session:
            return session.execute_write(method)

    def query(self, method):
        with self.driver.session() as session:
             return session.execute_read(method)

        