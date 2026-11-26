def add_fraud_transaction(tx):
    # - Impossible travel rule: Same account used in Delhi and London with in 10 minutes
    query = """
       MATCH (a:Account {id: "ACC001"}), (d:Device {id: "DEV001"})
       CREATE (t:Transaction {
            id : "TXN9992",
            amount: 4500.00,
            timestamp: "2026-11-26T11:30:00",
            location: "London"
       })
       CREATE (m:Merchant {
            id : "MER0052",
            name: "Premium Designer Store",
            category: "Fashion"
       })
       CREATE (a)-[:MAKES]->(t)
       CREATE (t)-[:USING]->(d)
       CREATE (t)-[:TO]->(m)
    """
    return tx.run(query)


def check_impossible_travel(tx):
    # Flag the transaction if same account has two transactions in different locations within 30 minutes
    query = """
    MATCH (a:Account {id: "ACC001"})-[:MAKES]->(t1:Transaction),
          (a)-[:MAKES]->(t2:Transaction)
    WHERE t1.location <> t2.location 
      AND t1.id < t2.id
    RETURN a.id AS AccountId, t1.id AS txn1, t2.id AS txn2
    """
    result = tx.run(query)
    return [record.data() for record in result]

