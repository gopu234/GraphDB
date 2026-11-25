from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
from db_query import add_node, add_relationship
import csv


load_dotenv()

road_network_file="road_network.csv"
road_places_file="road_places.csv"
road_network_relationship_file="road_network_relation.csv"


URI=os.getenv("NEO4J_URI_LOCAL")
AUTH=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))


class Neo4jDriver:
    def __init__(self):
       try:
        self.driver = GraphDatabase.driver(URI, auth=AUTH)
        self.driver.verify_connectivity()
        print("Connected to Neo4j")
       except Exception as e:
        print(f"There is a connection exception: {e}")

    def close(self):
        if self.driver:
            self.driver.close()
            print("Connection closed")

    def createNode(self, filename:str):
        with self.driver.session() as session:
            with open (filename,newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                        session.execute_write(add_node, node=row['type'], **row)

    def createNodeRelationship(self, filename:str):
        with self.driver.session() as session:
            with open(filename, newline='' ) as file:
                reader= csv.DictReader(file)
                for row in reader:
                    filtered_item = {key: value for key, value in row.items() if key not in ['start_point','end_point'] }
                    session.execute_write(
                        add_relationship, 
                        nodeA = "Interceptor",
                        nodeB = "Interceptor",
                        nodeAMatch = row['start_point'],
                        nodeBMatch = row['end_point'],
                        rel_type= "CONNECTED_TO",
                        **filtered_item
                        )
                   
    def calShortestPathDijkstaApoc(self, start_node:str, end_node:str):
        with self.driver.session() as session:
            session.run(
                """
                MATCH ()- [r:CONNECTED_TO] ->()
                SET r.cost = toFloat(r.distance_km) * 0.4 + toFloat(r.time) * 0.3 + toFloat(r.traffic_factor) * 2.0
                """
            ).consume()

            result = session.run(
                """
                 MATCH (start:Interceptor {name:$start}), (end:Interceptor {name:$end})
                 CALL apoc.algo.dijkstra(start, end, 'CONNECTED_TO>', 'cost') YIELD path, weight
                 RETURN [n IN nodes(path) | n.name] AS pathNodes, weight
                """,
                start=start_node,
                end=end_node
            )

            record = result.single()
            if record is None:
                return [], None
            return record["pathNodes"], record["weight"]


    def getShortestPathDijkstraGDS(self, start_node:str, end_node:str):
        with self.driver.session() as session:
            result = session.run(
                """
                 MATCH ()-[r:CONNECTED_TO] ->()
                 set r.cost = toFloat(r.distance_km) * 0.4 + toFloat(r.time) * 0.3 + toFloat(r.traffic_factor) * 2.0
                """
            ).consume()

            """
                Remove any existing graph projection named "roads"
                GDS algorithm dont run direcly on your stored neo4j graph; they run on a projected in-memory graph
                if you try to project a graph with the same name twiceit will throw an error
            """

            session.run("CALL gds.graph.drop('roads', false) YIELD graphName").consume()

            """
                Create an in-memory graph called "roads" using the existing nodes and relationships.
                
            """

            session.run(
                """
                CALL gds.graph.project(
                    'roads',
                    'Interceptor',
                    {
                        CONNECTED_TO: {
                            orientation: 'NATURAL',
                            properties: 'cost'
                        }
                    }
                )
                """
            ).consume()

            result = session.run(
                """
                MATCH (start:Interceptor {name: $start}), (end:Interceptor {name: $end})
                CALL gds.shortestPath.dijkstra.stream(
                    'roads',
                    {
                        sourceNode: id(start),
                        targetNode: id(end),
                        relationshipWeightProperty: 'cost'
                    }
                ) YIELD totalCost,nodeIds 
                 RETURN [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS pathNodes, 
                 totalCost
                """,
                start=start_node,
                end=end_node
            )

            record = result.single()
            if record is None:
                return [], None
            return record["pathNodes"], record["totalCost"]
                    

if __name__ == "__main__":
    neo4j_driver = Neo4jDriver()
    #neo4j_driver.createNode(road_network_file)
    #neo4j_driver.createNode(road_places_file)
    #neo4j_driver.createNodeRelationship(road_network_relationship_file)
    #result = neo4j_driver.calShortestPathDijkstaApoc("Elizabeth Mountains", "Mitchell Stravenue")
    path, totalcost=neo4j_driver.getShortestPathDijkstraGDS("Elizabeth Mountains", "Mitchell Stravenue")
    print(f"Path is {path} and totalcost is {totalcost}")
    neo4j_driver.close()
    