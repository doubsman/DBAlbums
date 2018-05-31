-- convert mysql script 
-- http://www.sqlines.com/online


-- --------------------------------------------------------
-- Hôte :                        HOMERSTATION
-- Version du serveur:           5.5.54-MariaDB - Source distribution
-- SE du serveur:                Linux
-- HeidiSQL Version:             9.4.0.5174
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;



-- Export de la structure de la table DBAlbums. DBALBUMS
CREATE TABLE DBALBUMS (
  [ID_CD] int NOT NULL IDENTITY,
  [MD5] varchar(32) DEFAULT NULL,
  [Family] varchar(14) DEFAULT NULL,
  [Category] varchar(14) DEFAULT NULL,
  [Position1] varchar(75) DEFAULT NULL,
  [Position2] varchar(75) DEFAULT NULL,
  [Name] varchar(140) DEFAULT NULL,
  [Label] varchar(75) DEFAULT NULL,
  [ISRC] varchar(32) DEFAULT NULL,
  [Year] varchar(4) DEFAULT NULL,
  [Qty_CD] int DEFAULT NULL,
  [Qty_Cue] int DEFAULT NULL,
  [Qty_CueERR] int DEFAULT NULL,
  [Qty_repMusic] int DEFAULT NULL,
  [Qty_Tracks] int DEFAULT NULL,
  [Qty_audio] int DEFAULT NULL,
  [Typ_Audio] varchar(4) DEFAULT NULL,
  [Qty_repCover] int DEFAULT NULL,
  [Qty_covers] int DEFAULT NULL,
  [Cover] varchar(179) DEFAULT NULL,
  [Path] varchar(162) DEFAULT NULL,
  [Size] int DEFAULT NULL,
  [Duration] varchar(9) DEFAULT NULL,
  [Length] varchar(8) DEFAULT NULL,
  [Typ_Tag] varchar(3) DEFAULT NULL,
  [Date_Insert] datetime2(0) DEFAULT NULL,
  [Date_Modifs] datetime2(0) DEFAULT NULL,
  [RHDD_Modifs] datetime2(0) DEFAULT NULL,
  [Score] int NOT NULL DEFAULT '0',
  [Statut] varchar(7) DEFAULT NULL,
  PRIMARY KEY ([ID_CD])
)  ;

CREATE INDEX [ID_CD] ON DBALBUMS ([ID_CD]);
CREATE INDEX [Family] ON DBALBUMS ([Family]);
CREATE INDEX [Category] ON DBALBUMS ([Category]);
CREATE INDEX [MD5] ON DBALBUMS ([MD5]);
CREATE INDEX [Date_Insert] ON DBALBUMS ([Date_Insert]);

-- Les données exportées n'étaient pas sélectionnées.
-- Export de la structure de la table DBAlbums. DBCOVERS
CREATE TABLE DBCOVERS (
  [MD5] varchar(32) NOT NULL,
  [Cover64] varbinary(max) NOT NULL,
  [MiniCover64] varbinary(max),
  PRIMARY KEY ([MD5])
) ;

CREATE INDEX [MD5] ON DBCOVERS ([MD5]);

-- Les données exportées n'étaient pas sélectionnées.
-- Export de la structure de la table DBAlbums. DBERRORS
CREATE TABLE DBERRORS (
  [ID_CD] int NOT NULL DEFAULT '0',
  [Path] varchar(162) DEFAULT NULL,
  [MESS] varchar(255) DEFAULT NULL,
  [COD] varchar(3) DEFAULT NULL,
  [MODE] varchar(6) DEFAULT NULL,
  [Date_Insert] datetime2(0) NULL DEFAULT GETDATE()
) ;

CREATE INDEX [ID_CD] ON DBERRORS ([ID_CD]);

-- Les données exportées n'étaient pas sélectionnées.
-- Export de la structure de la table DBAlbums. DBFOOBAR
CREATE TABLE DBFOOBAR (
  [ID_FOO] int NOT NULL IDENTITY,
  [MD5] varchar(32) NOT NULL,
  [Name] varchar(140) NOT NULL,
  [Path] varchar(160) NOT NULL,
  [FIL_Track] varchar(140) NOT NULL,
  [Playlist] varchar(140) NOT NULL,
  [TAG_Album] varchar(70) NOT NULL,
  [TAG_Artists] varchar(70) NOT NULL,
  [TAG_Title] varchar(70) NOT NULL,
  [Date_Insert] datetime2(0) NOT NULL DEFAULT GETDATE(),
  PRIMARY KEY ([ID_FOO]),
  CONSTRAINT [ID_FOO] UNIQUE  ([ID_FOO])
)  ;

CREATE INDEX [MD5] ON DBFOOBAR ([MD5]);
CREATE INDEX [FIL_Track] ON DBFOOBAR ([FIL_Track]);
CREATE INDEX [TAG_Album] ON DBFOOBAR ([TAG_Album],[TAG_Artists],[TAG_Title]);

-- Les données exportées n'étaient pas sélectionnées.
-- Export de la structure de la table DBAlbums. DBFOOBOR
CREATE TABLE DBFOOBOR (
  [FIL_TRACK] varchar(160) DEFAULT NULL,
  [FIL_TRACKM] varchar(160) DEFAULT NULL
) ;

-- Les données exportées n'étaient pas sélectionnées.
-- Export de la structure de la table DBAlbums. DBTRACKS
CREATE TABLE DBTRACKS (
  [ID_CD] int NOT NULL DEFAULT '0',
  [ID_TRACK] int NOT NULL IDENTITY,
  [Family] varchar(14) DEFAULT NULL,
  [Category] varchar(14) DEFAULT NULL,
  [Position1] varchar(9) DEFAULT NULL,
  [Position2] varchar(30) DEFAULT NULL,
  [REP_Album] varchar(140) DEFAULT NULL,
  [REP_Track] varchar(140) DEFAULT NULL,
  [FIL_Track] varchar(140) DEFAULT NULL,
  [TAG_Exten] varchar(33) DEFAULT NULL,
  [TAG_Album] varchar(63) DEFAULT NULL,
  [TAG_Albumartists] varchar(30) DEFAULT NULL,
  [TAG_Year] varchar(4) DEFAULT NULL,
  [TAG_Disc] int DEFAULT NULL,
  [TAG_Track] int DEFAULT NULL,
  [ODR_Track] varchar(6) DEFAULT NULL,
  [TAG_Artists] varchar(40) DEFAULT NULL,
  [TAG_Title] varchar(70) DEFAULT NULL,
  [TAG_Genres] varchar(50) DEFAULT NULL,
  [TAG_Duration] varchar(8) DEFAULT NULL,
  [TAG_length] varchar(11) DEFAULT NULL,
  [Score] int NOT NULL DEFAULT '0',
  [Date_Insert] datetime2(0) DEFAULT NULL,
  [Statut] varchar(7) DEFAULT NULL,
  PRIMARY KEY ([ID_TRACK]),
  CONSTRAINT [ID_TRACK] UNIQUE  ([ID_TRACK])
)  ;

CREATE INDEX [ID_CD] ON DBTRACKS ([ID_CD]);
CREATE INDEX [Family] ON DBTRACKS ([Family]);
CREATE INDEX [Category] ON DBTRACKS ([Category]);
CREATE INDEX [FIL_Track] ON DBTRACKS ([FIL_Track]);
CREATE INDEX [TAG_Title] ON DBTRACKS ([TAG_Title]);
CREATE INDEX [TAG_Artists] ON DBTRACKS ([TAG_Artists]);
GO
CREATE VIEW VW_AUTOCOMPLETION AS
	SELECT DISTINCT
		ID_CD, 
		CASE 	WHEN TAG_Albumartists IS NOT NULL AND TAG_Albumartists<>'' AND TAG_Albumartists<>'Various' AND TAG_Albumartists<>'Various Artists' AND TAG_Albumartists<>'VA'
				THEN TAG_Albumartists
				ELSE TAG_Artists END AS Synthax
	FROM DBTRACKS
UNION
	SELECT ID_CD, Label AS Synthax
	FROM DBALBUMS
	WHERE Label<>'';
