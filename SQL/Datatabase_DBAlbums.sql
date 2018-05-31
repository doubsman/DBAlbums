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


-- Export de la structure de la base pour DBAlbums
CREATE DATABASE IF NOT EXISTS `DBAlbums` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `DBAlbums`;

-- Export de la structure de la table DBAlbums. DBALBUMS
CREATE TABLE IF NOT EXISTS `DBALBUMS` (
  `ID_CD` int(11) NOT NULL AUTO_INCREMENT,
  `MD5` varchar(32) DEFAULT NULL,
  `Family` varchar(14) DEFAULT NULL,
  `Category` varchar(14) DEFAULT NULL,
  `Position1` varchar(75) DEFAULT NULL,
  `Position2` varchar(75) DEFAULT NULL,
  `Name` varchar(140) DEFAULT NULL,
  `Label` varchar(75) DEFAULT NULL,
  `ISRC` varchar(32) DEFAULT NULL,
  `Year` varchar(4) DEFAULT NULL,
  `Qty_CD` int(1) DEFAULT NULL,
  `Qty_Cue` int(1) DEFAULT NULL,
  `Qty_CueERR` int(1) DEFAULT NULL,
  `Qty_repMusic` int(1) DEFAULT NULL,
  `Qty_Tracks` int(1) DEFAULT NULL,
  `Qty_audio` int(2) DEFAULT NULL,
  `Typ_Audio` varchar(4) DEFAULT NULL,
  `Qty_repCover` int(2) DEFAULT NULL,
  `Qty_covers` int(2) DEFAULT NULL,
  `Cover` varchar(179) DEFAULT NULL,
  `Path` varchar(162) DEFAULT NULL,
  `Size` int(4) DEFAULT NULL,
  `Duration` varchar(9) DEFAULT NULL,
  `Length` varchar(8) DEFAULT NULL,
  `Typ_Tag` varchar(3) DEFAULT NULL,
  `Date_Insert` datetime DEFAULT NULL,
  `Date_Modifs` datetime DEFAULT NULL,
  `RHDD_Modifs` datetime DEFAULT NULL,
  `Score` int(2) NOT NULL DEFAULT '0',
  `Statut` varchar(7) DEFAULT NULL,
  PRIMARY KEY (`ID_CD`),
  KEY `ID_CD` (`ID_CD`),
  KEY `Family` (`Family`),
  KEY `Category` (`Category`),
  KEY `MD5` (`MD5`),
  KEY `Date_Insert` (`Date_Insert`)
) ENGINE=InnoDB AUTO_INCREMENT=4278 DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.
-- Export de la structure de la table DBAlbums. DBCOVERS
CREATE TABLE IF NOT EXISTS `DBCOVERS` (
  `MD5` varchar(32) NOT NULL,
  `Cover64` mediumblob NOT NULL,
  `MiniCover64` mediumblob,
  PRIMARY KEY (`MD5`),
  KEY `MD5` (`MD5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.
-- Export de la structure de la table DBAlbums. DBERRORS
CREATE TABLE IF NOT EXISTS `DBERRORS` (
  `ID_CD` int(11) NOT NULL DEFAULT '0',
  `Path` varchar(162) DEFAULT NULL,
  `MESS` varchar(255) DEFAULT NULL,
  `COD` varchar(3) DEFAULT NULL,
  `MODE` varchar(6) DEFAULT NULL,
  `Date_Insert` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `ID_CD` (`ID_CD`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.
-- Export de la structure de la table DBAlbums. DBFOOBAR
CREATE TABLE IF NOT EXISTS `DBFOOBAR` (
  `ID_FOO` int(11) NOT NULL AUTO_INCREMENT,
  `MD5` varchar(32) NOT NULL,
  `Name` varchar(140) NOT NULL,
  `Path` varchar(160) NOT NULL,
  `FIL_Track` varchar(140) NOT NULL,
  `Playlist` varchar(140) NOT NULL,
  `TAG_Album` varchar(70) NOT NULL,
  `TAG_Artists` varchar(70) NOT NULL,
  `TAG_Title` varchar(70) NOT NULL,
  `Date_Insert` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID_FOO`),
  UNIQUE KEY `ID_FOO` (`ID_FOO`),
  KEY `MD5` (`MD5`),
  KEY `FIL_Track` (`FIL_Track`),
  KEY `TAG_Album` (`TAG_Album`,`TAG_Artists`,`TAG_Title`)
) ENGINE=InnoDB AUTO_INCREMENT=2748 DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.
-- Export de la structure de la table DBAlbums. DBFOOBOR
CREATE TABLE IF NOT EXISTS `DBFOOBOR` (
  `FIL_TRACK` varchar(160) DEFAULT NULL,
  `FIL_TRACKM` varchar(160) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.
-- Export de la structure de la table DBAlbums. DBTRACKS
CREATE TABLE IF NOT EXISTS `DBTRACKS` (
  `ID_CD` int(2) NOT NULL DEFAULT '0',
  `ID_TRACK` int(11) NOT NULL AUTO_INCREMENT,
  `Family` varchar(14) DEFAULT NULL,
  `Category` varchar(14) DEFAULT NULL,
  `Position1` varchar(9) DEFAULT NULL,
  `Position2` varchar(30) DEFAULT NULL,
  `REP_Album` varchar(140) DEFAULT NULL,
  `REP_Track` varchar(140) DEFAULT NULL,
  `FIL_Track` varchar(140) DEFAULT NULL,
  `TAG_Exten` varchar(33) DEFAULT NULL,
  `TAG_Album` varchar(63) DEFAULT NULL,
  `TAG_Albumartists` varchar(30) DEFAULT NULL,
  `TAG_Year` varchar(4) DEFAULT NULL,
  `TAG_Disc` int(1) DEFAULT NULL,
  `TAG_Track` int(2) DEFAULT NULL,
  `ODR_Track` varchar(6) DEFAULT NULL,
  `TAG_Artists` varchar(40) DEFAULT NULL,
  `TAG_Title` varchar(70) DEFAULT NULL,
  `TAG_Genres` varchar(50) DEFAULT NULL,
  `TAG_Duration` varchar(8) DEFAULT NULL,
  `TAG_length` varchar(11) DEFAULT NULL,
  `Score` int(2) NOT NULL DEFAULT '0',
  `Date_Insert` datetime DEFAULT NULL,
  `Statut` varchar(7) DEFAULT NULL,
  PRIMARY KEY (`ID_TRACK`),
  UNIQUE KEY `ID_TRACK` (`ID_TRACK`),
  KEY `ID_CD` (`ID_CD`),
  KEY `Family` (`Family`),
  KEY `Category` (`Category`),
  KEY `FIL_Track` (`FIL_Track`),
  KEY `TAG_Title` (`TAG_Title`),
  KEY `TAG_Artists` (`TAG_Artists`)
) ENGINE=InnoDB AUTO_INCREMENT=62763 DEFAULT CHARSET=utf8;

-- Views
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
	
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
