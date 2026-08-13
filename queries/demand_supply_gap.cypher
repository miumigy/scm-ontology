// M6: derive Demand-Supply Gap at a ProductLocation.
// Relevant supply = Available + InTransit.
// Gap = max(Demand - RelevantSupply, 0).
// The result is shaped as the canonical SupplyGap semantic object.

MATCH (pl:ProductLocation)-[:DEMANDS]->(d:Demand)
MATCH (pl)-[:HAS_INVENTORY_POSITION]->(ip:InventoryPosition)
WITH pl,
     sum(coalesce(d.quantity, 0)) AS demand,
     sum(coalesce(ip.available, 0)) AS available,
     sum(coalesce(ip.inTransit, 0)) AS inbound
WITH pl,
     demand,
     available,
     inbound,
     available + inbound AS relevantSupply
RETURN pl.id AS productLocation,
       demand AS demandQuantity,
       available AS availableQuantity,
       inbound AS inboundQuantity,
       relevantSupply AS relevantSupplyQuantity,
       CASE
         WHEN demand - relevantSupply > 0
         THEN demand - relevantSupply
         ELSE 0
       END AS gapQuantity
ORDER BY gapQuantity DESC;
