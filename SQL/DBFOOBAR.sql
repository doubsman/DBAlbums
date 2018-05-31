-- --------------------------------------------------------
-- Hôte :                        DOUBBIGSTATION
-- Version du serveur:           5.5.54-MariaDB - Source distribution
-- SE du serveur:                Linux
-- HeidiSQL Version:             9.4.0.5174
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Export de la structure de la base pour MP3
CREATE DATABASE IF NOT EXISTS `MP3` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `MP3`;

-- Export de la structure de la table MP3. DBFOOBAR
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
  KEY `TAG_Album` (`TAG_Album`),
  KEY `TAG_Artists` (`TAG_Artists`),
  KEY `TAG_Title` (`TAG_Title`)
) ENGINE=InnoDB AUTO_INCREMENT=9400 DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
