-- convert mysql script 
-- http://www.sqlines.com/online

CREATE TABLE ALBUMS (
	[ID_CD] INT NOT NULL IDENTITY,
	[CATEGORY] VARCHAR(32) NULL DEFAULT NULL,
	[FAMILY] VARCHAR(32) NULL DEFAULT NULL,
	[NAME] VARCHAR(255) NULL DEFAULT NULL,
	[ARTIST] VARCHAR(255) NULL DEFAULT NULL,
	[PATHNAME] VARCHAR(255) NULL DEFAULT NULL,
	[POSITION] VARCHAR(127) NULL DEFAULT NULL,
	[SUBPOSITION] VARCHAR(127) NULL DEFAULT NULL,
	[POSITIONHDD] VARCHAR(255) NULL DEFAULT NULL,
	[AUDIOTRACKS] INT NULL DEFAULT NULL,
	[TRACKS] INT NULL DEFAULT NULL,
	[CUE] INT NULL DEFAULT NULL,
	[COVER] VARCHAR(255) NULL DEFAULT NULL,
	[PIC] INT NULL DEFAULT NULL,
	[SIZE] INT NULL DEFAULT NULL,
	[CD] INT NULL DEFAULT NULL,
	[YEAR] VARCHAR(4) NULL DEFAULT NULL,
	[ISRC] VARCHAR(255) NULL DEFAULT NULL,
	[LABEL] VARCHAR(255) NULL DEFAULT NULL,
	[TAGISRC] VARCHAR(255) NULL DEFAULT NULL,
	[TAGLABEL] VARCHAR(255) NULL DEFAULT NULL,
	[STYLE] VARCHAR(255) NULL DEFAULT NULL,
	[COUNTRY] VARCHAR(32) NULL DEFAULT NULL,
	[LENGTHSECONDS] INT NULL DEFAULT NULL,
	[LENGTHDISPLAY] VARCHAR(16) NULL DEFAULT NULL,
	[TYPEMEDIA] VARCHAR(32) NULL DEFAULT NULL,
	[SCORE] INT NOT NULL DEFAULT 0,
	[TAGMETHOD] VARCHAR(3) NULL DEFAULT NULL,
	[ADD] DATETIME2(0) NULL DEFAULT NULL,
	[MODIFIED] DATETIME2(0) NULL DEFAULT NULL,
	PRIMARY KEY ([ID_CD]),
	CONSTRAINT [ID_CD] UNIQUE  ([ID_CD])
);

CREATE INDEX [FAMILY] ON ALBUMS ([FAMILY]);
CREATE INDEX [CATEGORY] ON ALBUMS ([CATEGORY]);
CREATE INDEX [STYLE] ON ALBUMS ([STYLE]);
CREATE INDEX [NAME] ON ALBUMS ([NAME]);
CREATE INDEX [ADD] ON ALBUMS ([ADD]);

CREATE TABLE TRACKS (
	[ID_TRACK] INT NOT NULL IDENTITY,
	[ID_CD] INT NOT NULL DEFAULT 0,
	[FILENAME] VARCHAR(255) NULL DEFAULT NULL,
	[PATHNAME] VARCHAR(255) NULL DEFAULT NULL,
	[LENGTHSECONDS] INT NULL DEFAULT NULL,
	[LENGTHDISPLAY] VARCHAR(16) NULL DEFAULT NULL,
	[TYPEMEDIA] VARCHAR(32) NULL DEFAULT NULL,
	[TITLE] VARCHAR(255) NULL DEFAULT NULL,
	[ARTIST] VARCHAR(255) NULL DEFAULT NULL,
	[ALBUM] VARCHAR(255) NULL DEFAULT NULL,
	[DATE] VARCHAR(32) NULL DEFAULT NULL,
	[GENRE] VARCHAR(255) NULL DEFAULT NULL,
	[TRACKNUMBER] VARCHAR(6) NULL DEFAULT NULL,
	[ALBUMARTIST] VARCHAR(255) NULL DEFAULT NULL,
	[COMPOSER] VARCHAR(255) NULL DEFAULT NULL,
	[DISCNUMBER] VARCHAR(16) NULL DEFAULT NULL,
	[DISC] INT NULL DEFAULT NULL,
	[TRACKORDER] VARCHAR(6) NULL DEFAULT NULL,
	[ISRC] VARCHAR(255) NULL DEFAULT NULL,
	[ORGANIZATION] VARCHAR(255) NULL DEFAULT NULL,
	[COUNTRY] VARCHAR(32) NULL DEFAULT NULL,
	[INDEX] VARCHAR(11) NULL DEFAULT NULL,
	[POS_START_SAMPLES] INT NULL DEFAULT NULL,
	[POS_END_SAMPLES] INT  NULL DEFAULT NULL,
	[SCORE] INT NOT NULL DEFAULT 0,
	PRIMARY KEY ([ID_TRACK]),
	CONSTRAINT [ID_TRACK] UNIQUE  ([ID_TRACK])
);

CREATE INDEX [TRACKS_ID_CD] ON TRACKS ([ID_CD]);

CREATE TABLE COVERS (
	[ID_CD] INT NOT NULL,
	[NAME] VARCHAR(255) NOT NULL,
	[COVER] VARBINARY(max) NOT NULL,
	[THUMBNAIL] VARBINARY(max) NOT NULL,
	PRIMARY KEY ([ID_CD]),
	CONSTRAINT [COVERS_ID_CD] UNIQUE  ([ID_CD])
);

CREATE TABLE FOOBAR (
	[ID_FOO] INT NOT NULL IDENTITY,
	[ID_TRACK] INT NULL,
	[PLAYLIST] VARCHAR(64) NOT NULL,
	[PATH] VARCHAR(255) NOT NULL,
	[FILENAME] VARCHAR(255) NOT NULL,
	[NAME] VARCHAR(255) NULL DEFAULT NULL,
	[ALBUM] VARCHAR(255) NULL DEFAULT NULL,
	[ARTIST] VARCHAR(255) NULL DEFAULT NULL,
	[TITLE] VARCHAR(255) NULL DEFAULT NULL,
	[ADD] DATETIME2(0) NULL DEFAULT NULL,
	PRIMARY KEY ([ID_FOO]),
	CONSTRAINT [ID_FOO] UNIQUE  ([ID_FOO])
);

CREATE INDEX [FILENAME] ON FOOBAR ([FILENAME]);
CREATE INDEX [TAG_Album] ON FOOBAR ([NAME], [ARTIST], [TITLE]);


CREATE VIEW VW_COMPLETION AS 
SELECT ID_CD, ARTIST AS SYNTHAX FROM ALBUMS WHERE ARTIST <> '' AND ARTIST <> 'Various'
UNION 
SELECT ID_CD, SUBPOSITION FROM ALBUMS WHERE FAMILY='Artists';



