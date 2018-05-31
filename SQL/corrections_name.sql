UPDATE DBALBUMS
SET Name = REPLACE(name,CONCAT(' (',year,')'),'')
WHERE year IS NOT NULL

UPDATE DBALBUMS
SET  Name = REPLACE(name,CONCAT('[',ISRC,'] '),'')
WHERE char_length(ISRC)>0