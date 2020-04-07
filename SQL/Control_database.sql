
-- 01 TYPE MEDIA
SELECT TYPEMEDIA, COUNT(*) AS NUMBERTRACKS 
FROM TRACKS 
GROUP BY TYPEMEDIA;

-- 02 BAD FILE TRACK
SELECT ALBUMS.ID_CD, ALBUMS.NAME FROM ALBUMS
INNER JOIN (SELECT ID_CD, COUNT(*) AS NBTRK FROM TRACKS GROUP BY ID_CD) TR
ON TR.ID_CD = ALBUMS.ID_CD
WHERE NBTRK<>AUDIOTRACKS AND TAGMETHOD = 'TAG';

-- 03 BAD FILE COVER
SELECT ALBUMS.ID_CD, ALBUMS.COVER FROM ALBUMS
LEFT JOIN COVERS
ON ALBUMS.ID_CD = COVERS.ID_CD
WHERE COVERS.ID_CD IS NULL AND ALBUMS.COVER<>'<No Picture>';

-- 04 NO FILE COVER
SELECT ALBUMS.ID_CD, ALBUMS.NAME
FROM ALBUMS 
WHERE PIC = 0;

-- 05 MORE CHOICE FILES FOR COVER
SELECT ALBUMS.ID_CD, ALBUMS.NAME 
FROM ALBUMS
WHERE PIC > 0 AND ALBUMS.COVER='<No Picture>';

-- 06 INTEGRITY ORPHAN ALBUMS (NO TRACKS)
SELECT DISTINCT ALBUMS.ID_CD, ALBUMS.NAME 
FROM ALBUMS
WHERE ALBUMS.ID_CD  NOT IN (SELECT DISTINCT TRACKS.ID_CD FROM TRACKS);

-- 07 INTEGRITY ORPHAN TRACKS
SELECT DISTINCT TRACKS.ID_CD, TRACKS.FILENAME 
FROM TRACKS
WHERE TRACKS.ID_CD  NOT IN (SELECT DISTINCT ALBUMS.ID_CD FROM ALBUMS);

-- 08 INTEGRITY ORPHAN COVERS
SELECT ID_CD, NAME 
FROM COVERS 
WHERE COVERS.ID_CD  NOT IN (SELECT DISTINCT ALBUMS.ID_CD FROM ALBUMS);

-- 09 SCORING ALIGMENT ALBUMS<-TRACKS
SELECT ALBUMS.ID_CD, ALBUMS.NAME FROM ALBUMS
INNER JOIN (
	SELECT ID_CD, MAX(SCORE) AS SCORE FROM TRACKS GROUP BY ID_CD
	HAVING SCORE <>0) KKK
ON KKK.ID_CD=ALBUMS.ID_CD AND KKK.SCORE>ALBUMS.SCORE;

-- 10 NO TAG <ARTISTS>
SELECT ALBUMS.ID_CD, ALBUMS.NAME
FROM ALBUMS 
WHERE ARTIST IS NULL;

-- 11 NO TAG <NUMBERTRACK>
SELECT DISTINCT ALBUMS.ID_CD, ALBUMS.NAME 
FROM ALBUMS
INNER JOIN TRACKS
ON TRACKS.ID_CD = ALBUMS.ID_CD
WHERE TRACKORDER IS NULL AND AUDIOTRACKS>1;

-- 12 NO TAG <YEAR>
SELECT ALBUMS.ID_CD, ALBUMS.NAME
FROM ALBUMS 
WHERE year IS NULL OR Year='' OR Year='????' OR Year =0;

