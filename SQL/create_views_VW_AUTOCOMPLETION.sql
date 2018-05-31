SELECT COUNT(*) AS `Score`, Synthax FROM
(
	SELECT DISTINCT
		ID_CD, 
		CASE 	WHEN TAG_Albumartists IS NOT NULL AND TRIM(TAG_Albumartists)<>"" AND TAG_Albumartists<>"Various" AND TAG_Albumartists<>"Various Artists"AND TAG_Albumartists<>"VA"
				THEN TAG_Albumartists
				ELSE TAG_Artists END AS Synthax
	FROM DBTRACKS
UNION
	SELECT ID_CD, Label AS Synthax
	FROM DBALBUMS
	WHERE Label<>''
) KKK
GROUP BY Synthax
ORDER BY `Score` DESC
LIMIT 1500

DROP VIEW VW_AUTOCOMPLBUILD;
DROP VIEW VW_AUTOCOMPLETION;
CREATE VIEW VW_AUTOCOMPLETION AS
	SELECT DISTINCT
		ID_CD, 
		CASE 	WHEN TAG_Albumartists IS NOT NULL AND TRIM(TAG_Albumartists)<>"" AND TAG_Albumartists<>"Various" AND TAG_Albumartists<>"Various Artists"AND TAG_Albumartists<>"VA"
				THEN TAG_Albumartists
				ELSE TAG_Artists END AS Synthax
	FROM DBTRACKS
UNION
	SELECT ID_CD, Label AS Synthax
	FROM DBALBUMS
	WHERE Label<>'';

SELECT Synthax FROM VW_AUTOCOMPLETION GROUP BY Synthax ORDER BY COUNT(*) DESC LIMIT 1500;