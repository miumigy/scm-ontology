// Demand-Supply Gap at a ProductLocation.
// Canonical supply-side inputs come from InventoryPosition.
// Gap = Demand - Available - InTransit.

MATCH (pl:ProductLocation)-[:DEMANDS]->(d:Demand)
MATCH (pl)-[:HAS_INVENTORY_POSITION]->(ip:InventoryPosition)
WITH pl,
     sum(coalesce(d.quantity, 0)) AS demand,
     sum(coalesce(ip.available, 0)) AS available,
     sum(coalesce(ip.inTransit, 0)) AS inbound
RETURN pl.id AS productLocation,
       demand,
       available,
       inbound,
       CASE
         WHEN demand - available - inbound > 0
         THEN demand - available - inbound
         ELSE 0
       END AS gap
ORDER BY gap DESC;
