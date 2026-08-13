// M7: downstream causal impact traversal.
MATCH (source:Event {id: $event_id})
OPTIONAL MATCH path=(source)-[:CAUSES*0..5]->(downstream:Event)
WITH source, downstream, path
OPTIONAL MATCH (downstream)-[:AFFECTS]->(affected)
OPTIONAL MATCH (affected)<-[:HAS_SUPPLY_GAP]-(pl:ProductLocation)
OPTIONAL MATCH (pl)-[:HAS_SUPPLY_GAP]->(gap:SupplyGap)
OPTIONAL MATCH (risk:Risk)-[:EXPOSES]->(pl)
RETURN source.id AS sourceEvent,
       downstream.id AS downstreamEvent,
       [node IN nodes(path) | node.id] AS causalPath,
       labels(affected) AS affectedLabels,
       affected.id AS affectedObject,
       pl.id AS productLocation,
       gap.id AS supplyGap,
       gap.gapQuantity AS gapQuantity,
       risk.id AS risk,
       risk.severity AS riskSeverity
ORDER BY size(causalPath), downstreamEvent;
