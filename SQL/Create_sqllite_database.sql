CREATE TABLE `ALBUMS` (
	`ID_CD` INTEGER PRIMARY KEY AUTOINCREMENT,
	`CATEGORY` TEXT,
	`FAMILY` TEXT,
	`NAME` TEXT,
	`ARTIST` TEXT,
	`PATHNAME` TEXT,
	`POSITION` TEXT,
	`SUBPOSITION` TEXT,
	`POSITIONHDD` TEXT,
	`AUDIOTRACKS` INT,
	`TRACKS` INT,
	`CUE` INT,
	`COVER` TEXT,
	`PIC` INT,
	`SIZE` INT,
	`CD` INT,
	`YEAR` TEXT,
	`ISRC` TEXT,
	`LABEL` TEXT,
	`TAGISRC` TEXT,
	`TAGLABEL` TEXT,
	`STYLE` TEXT,
	`COUNTRY` TEXT,
	`LENGTHSECONDS` INT,
	`LENGTHDISPLAY` TEXT,
	`TYPEMEDIA` TEXT,
	`SCORE` INT,
	`TAGMETHOD` TEXT,
	`ADD` DATETIME,
	`MODIFIED` DATETIME);

CREATE INDEX ALBUMS_ndx_ADD ON ALBUMS(`ADD`);
CREATE INDEX ALBUMS_ndx_NAME ON ALBUMS(`NAME`);
CREATE INDEX ALBUMS_ndx_FAMILY ON ALBUMS (`FAMILY`);
CREATE INDEX ALBUMS_ndx_CATEGORY ON ALBUMS (`CATEGORY`);
CREATE INDEX ALBUMS_ndx_STYLE ON ALBUMS (`STYLE`);


CREATE TABLE `TRACKS` (
	`ID_TRACK` INTEGER PRIMARY KEY AUTOINCREMENT,
	`ID_CD` INT,
	`FILENAME` TEXT,
	`PATHNAME` TEXT,
	`LENGTHSECONDS` INT,
	`LENGTHDISPLAY` TEXT,
	`TYPEMEDIA` TEXT,
	`TITLE` TEXT,
	`ARTIST` TEXT,
	`ALBUM` TEXT,
	`DATE` TEXT,
	`GENRE` TEXT,
	`TRACKNUMBER` TEXT,
	`ALBUMARTIST` TEXT,
	`COMPOSER` TEXT,
	`DISCNUMBER` TEXT,
	`DISC` INT,
	`TRACKORDER` TEXT,
	`ISRC` TEXT,
	`ORGANIZATION` TEXT,
	`COUNTRY` TEXT,
	`INDEX` TEXT,
	`POS_START_SAMPLES` INT,
	`POS_END_SAMPLES` INT,
	`SCORE` INT);

CREATE INDEX TRACKS_ndx_IDCD ON TRACKS(`ID_CD`);
CREATE INDEX TRACKS_ndx_ARTIST ON TRACKS(`ARTIST`);
CREATE INDEX TRACKS_ndx_TITLE ON TRACKS(`TITLE`);


CREATE TABLE FOOBAR(
	ID_FOO INTEGER PRIMARY KEY AUTOINCREMENT,
	`ID_TRACK` INT,
	`PLAYLIST` TEXT, 
	`PATH` TEXT, 
	`ALBUM` TEXT,
	`FILENAME` TEXT, 
	`NAME` TEXT,
	`ARTIST` TEXT, 
	`TITLE` TEXT, 
	`ADD` DATETIME);

CREATE INDEX FOOBAR_ndx_FILENAME ON FOOBAR(FILENAME);


CREATE TABLE `COVERS` (
	`ID_CD` INT,
	`NAME` TEXT,
	`COVER` BLOB,
	`THUMBNAIL` BLOB);
CREATE INDEX COVERS_ndx_IDCD ON COVERS(`ID_CD`);


CREATE VIEW VW_COMPLETION AS 
	SELECT `ALBUMS`.`ID_CD` AS `ID_CD`,`ALBUMS`.`ARTIST` AS `SYNTHAX` 
		FROM `ALBUMS` 
		WHERE `ALBUMS`.`ARTIST` <> '' AND `ALBUMS`.`ARTIST` <> 'Various' 
	UNION 
	SELECT `ALBUMS`.`ID_CD` AS `ID_CD`,`ALBUMS`.`SUBPOSITION` AS `SUBPOSITION` 
		FROM `ALBUMS` 
		WHERE `ALBUMS`.`FAMILY` = 'Artists';
