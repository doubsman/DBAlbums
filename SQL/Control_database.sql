-- 14087 ALBUMS
-- SELECT * FROM ALBUMS;

-- TYPE MEDIA
SELECT TYPEMEDIA, COUNT(*) FROM TRACKS GROUP BY TYPEMEDIA;
-- SELECT * FROM TRACKS WHERE TYPEMEDIA = 'audio/mp2'

-- 164 NO TAG ARTISTS
SELECT * FROM ALBUMS WHERE ARTIST IS NULL;

-- 1460 NO TAG NUMBER TRACK
SELECT DISTINCT ALBUMS.* FROM ALBUMS
INNER JOIN TRACKS
ON TRACKS.ID_CD = ALBUMS.ID_CD
WHERE TRACKORDER IS NULL AND AUDIOTRACKS>1;

-- 105 NO TAG YEAR
SELECT * FROM ALBUMS WHERE year IS NULL OR Year='' OR Year='????' OR Year =0;

-- 0 ALBUMS WITH BAD FILE TRACKS
SELECT * FROM ALBUMS
INNER JOIN (SELECT ID_CD, COUNT(*) AS NBTRK FROM TRACKS GROUP BY ID_CD) TR
ON TR.ID_CD = ALBUMS.ID_CD
WHERE NBTRK<>AUDIOTRACKS AND TAGMETHOD = 'TAG';

-- 0 COVER EXIST PROBLEM
SELECT * FROM ALBUMS
LEFT JOIN COVERS 
ON ALBUMS.ID_CD = COVERS.ID_CD
WHERE COVERS.ID_CD IS NULL AND ALBUMS.COVER<>'<No Picture>';

-- 2105 NO COVER
SELECT * FROM ALBUMS WHERE PIC = 0;

-- 869 MORE CHOICE COVER
SELECT * FROM ALBUMS
WHERE PIC > 0 AND ALBUMS.COVER='<No Picture>';

-- ALBUMS WITH NO TRACKS > DELETE ALBUMS FROM ALBUMS WHERE ALBUMS.ID_CD  NOT IN (SELECT DISTINCT TRACKS.ID_CD FROM TRACKS);
SELECT DISTINCT ALBUMS.* FROM ALBUMS
WHERE ALBUMS.ID_CD  NOT IN (SELECT DISTINCT TRACKS.ID_CD FROM TRACKS);

-- ORPHELIN TRACKS > DELETE FROM TRACKS WHERE TRACKS.ID_CD  NOT IN (SELECT DISTINCT ALBUMS.ID_CD FROM ALBUMS);
SELECT DISTINCT TRACKS.* FROM TRACKS
WHERE TRACKS.ID_CD  NOT IN (SELECT DISTINCT ALBUMS.ID_CD FROM ALBUMS);




-- ANALYSE ALBUMS
SELECT * FROM ALBUMS WHERE ID_CD = 4561;

SELECT * FROM TRACKS WHERE ID_CD = 214;

SELECT * FROM COVERS WHERE ID_CD = 214;
