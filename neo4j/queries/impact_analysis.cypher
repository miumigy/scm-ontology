MATCH path = (e:Event)-[:CAUSES*1..5]->(downstream:Event)
WHERE e.eventType = 'SUPPLIER_DELAY'
RETURN path;
