// Trace supply risk from a supplier delay to exposed material/product-location context.
// The causal chain is Event(CAUSES) Event, while Risk(EXPOSES) identifies downstream exposure.

MATCH (delay:Event {eventType: 'SUPPLIER_DELAY'})-[:AFFECTS]->(supplier:Party)
MATCH (delay)-[:CAUSES]->(shortage:Event {eventType: 'MATERIAL_SHORTAGE_RISK'})
MATCH (risk:Risk {riskType: 'SUPPLY_SHORTAGE'})-[:EXPOSES]->(material:Material)
MATCH (risk)-[:EXPOSES]->(pl:ProductLocation)
RETURN supplier.id AS supplier,
       delay.id AS delayEvent,
       shortage.id AS shortageEvent,
       risk.id AS risk,
       risk.severity AS severity,
       risk.probability AS probability,
       material.id AS material,
       pl.id AS productLocation
ORDER BY probability DESC;
