from dotenv import load_dotenv
from ariadne import load_schema_from_path, make_executable_schema, QueryType, MutationType, ObjectType
import os
import uuid
from db import Neo4jDB


load_dotenv()
URI = os.getenv("NEO4J_URI_LOCAL")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

query = QueryType()
mutation = MutationType()
order_type = ObjectType("Order")
user_type = ObjectType("User")

neo4j_db = Neo4jDB(URI, USERNAME, PASSWORD)


# ---------- Mutations ----------

@mutation.field("createUser")
def resolve_create_user(_, info, name, email):
    cypher = """
    CREATE (u:User {id: $id, name: $name, email: $email})
    RETURN u { .id, .name, .email } AS user
    """
    result = neo4j_db.query(cypher, {"id": str(uuid.uuid4()), "name": name, "email": email})
    return result[0]["user"]


@mutation.field("createProduct")
def resolve_create_product(_, info, name, price):
    cypher = """
    CREATE (p:Product {id: $id, name: $name, price: $price})
    RETURN p { .id, .name, .price } AS product
    """
    result = neo4j_db.query(cypher, {"id": str(uuid.uuid4()), "name": name, "price": price})
    return result[0]["product"]


@mutation.field("createOrder")
def resolve_create_order(_, info, userId, productIds, date):
    cypher = """
    MATCH (u:User {id: $userId})
    CREATE (u)-[:PLACED]->(o:Order {id: $id, date: $date, totalAmount: 0.0})
    WITH o
    UNWIND $productIds AS productId
    MATCH (p:Product {id: productId})
    MERGE (o)-[:CONTAINS]->(p)
    WITH o, collect(p) AS products
    SET o.totalAmount = reduce(total = 0.0, prod IN products | total + prod.price)
    RETURN o { .id, .date, .totalAmount } AS order
    """
    result = neo4j_db.query(
        cypher,
        {"id": str(uuid.uuid4()), "userId": userId, "productIds": productIds, "date": date},
    )
    if not result:
        raise Exception(f"Could not create order: user {userId} or its products were not found")
    return result[0]["order"]


# ---------- Queries ----------

@query.field("users")
def resolve_users(_, info):
    cypher = """
    MATCH (u:User)
    RETURN u { .id, .name, .email } AS user
    """
    return [r["user"] for r in neo4j_db.query(cypher)]


@query.field("products")
def resolve_products(_, info):
    cypher = """
    MATCH (p:Product)
    RETURN p { .id, .name, .price } AS product
    """
    return [r["product"] for r in neo4j_db.query(cypher)]


@query.field("orders")
def resolve_orders(_, info):
    cypher = """
    MATCH (o:Order)
    RETURN o { .id, date: toString(o.date), .totalAmount } AS order
    """
    return [r["order"] for r in neo4j_db.query(cypher)]


# ---------- Nested fields ----------
# The first argument is the parent object (the dict returned by the parent resolver).

@user_type.field("orders")
def resolve_user_orders(user, info):
    cypher = """
    MATCH (:User {id: $id})-[:PLACED]->(o:Order)
    RETURN o { .id, date: toString(o.date), .totalAmount } AS order
    """
    return [r["order"] for r in neo4j_db.query(cypher, {"id": user["id"]})]


@order_type.field("products")
def resolve_order_products(order, info):
    cypher = """
    MATCH (:Order {id: $id})-[:CONTAINS]->(p:Product)
    RETURN p { .id, .name, .price } AS product
    """
    return [r["product"] for r in neo4j_db.query(cypher, {"id": order["id"]})]


# ---------- Schema ----------

type_defs = load_schema_from_path(os.path.join(os.path.dirname(__file__), "schema.graphql"))
schema = make_executable_schema(type_defs, query, mutation, user_type, order_type)
