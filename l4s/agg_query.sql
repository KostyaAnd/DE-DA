WITH CTE AS (
SELECT SUM (item_price) AS revenue,
       count (DISTINCT sessionId) AS purchases,
       CASE WHEN purchases > 0 THEN ROUND(revenue / purchases, 1) ELSE 0 END AS aov 
FROM konstantin_andreev_lab04
WHERE detectedDuplicate = false AND detectedCorruption = false AND eventType = 'itemBuyEvent' 
AND timestamp >= 1545132000
AND timestamp <= 1545132600
)
SELECT purchases,aov
FROM CTE;









CASE WHEN purchases > 0 THEN ROUND(revenue / purchases, 1) ELSE 0 END AS aov 
