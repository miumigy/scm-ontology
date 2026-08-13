MATCH (d:Demand)-[:FOR_PRODUCT]->(p:Product)
MATCH (site:Site)-[:STOCKS]->(p)
OPTIONAL MATCH (i:InventoryPosition)-[:FOR_PRODUCT]->(p)
RETURN p.id AS product,
       sum(d.quantity) AS demand,
       coalesce(i.available, 0) AS available,
       sum(d.quantity) - coalesce(i.available, 0) AS gap;
