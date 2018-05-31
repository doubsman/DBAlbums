-- MD5 en double
SELECT * FROM DBALBUMS WHERE MD5 IN (
SELECT MD5 
FROM DBALBUMS 
GROUP BY MD5
HAVING COUNT(*) > 1)

-- list MD5 suppression
SELECT MAX(ID_CD) 
FROM DBALBUMS 
WHERE MD5 IN (
	SELECT MD5 
	FROM DBALBUMS 
	GROUP BY MD5
	HAVING COUNT(*) > 1
GROUP BY MD5)

--
DELETE TRK FROM DBTRACKS AS TRK LEFT JOIN DBALBUMS AS ALB ON ALB.ID_CD=TRK.ID_CD WHERE ISNULL(ALB.ID_CD);