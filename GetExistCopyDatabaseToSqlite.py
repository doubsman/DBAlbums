#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import system, path, getcwd, name, remove
from base64 import b64decode, decodestring
from pymysql import connect
from sqlite3 import connect as connectsqlite3
import logging

SERV_TEST = 'doubbigstation'
USER_TEST = 'admInvent'
PASS_TEST = 'MwRbBR2HA8PFQjuu'
BASE_TEST = 'Invent'
TEXT_NCO = 'No Picture'
C_REQUEST = """SELECT MD5, Cover64 FROM DBCOVERS WHERE MD5='{MD5}'"""

def ConnectInvent(envt="TEST"):
	"""Connect sur la base Invent."""
	server = SERV_TEST
	userdb = USER_TEST
	namedb = BASE_TEST
	passdb = PASS_TEST
	con = connect(  host=server, 
					user=userdb, 
					passwd=passdb, 
					db=namedb,
					charset='utf8',
					use_unicode=True)
	#con.autocommit(True)
	return con

def SelectTOTab(con, req):
	"""Select Mysql dans un tableau en mémoire."""
	cur = con.cursor()    
	cur.execute(req)
	rows = cur.fetchall()
	cur.close()
	return rows

def BuildFileCover(con, namefile, pathcover, md5):
	"""Gestion cover base64/mysql to file"""
	#no cover
	if pathcover != TEXT_NCO: 
		#mysql
		req = C_REQUEST.format(MD5=md5)
		Tableau = SelectTOTabCon(con, req)
		extension = path.splitext(pathcover)[1][1:]
		filecover = namefile+'.'+extension
		cover = open(filecover, "wb")
		content = decodestring(Tableau[0][1])
		cover.write(content)
		cover.close()
#md5="0954302C5556878C5AD353D0AE605EB1"
#BuildFileCover(con, 'essai2', '\\kdjfkdjf\gfkhj\cover.jpg', md5)

def CopyDatabaseInvent(conMySQL, BaseNameSQLite, logname):
	logging.basicConfig(filename=logname,
							filemode='a',
							format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
							datefmt='%H:%M:%S',
							level=logging.DEBUG)
	logging.info ('Create/Update Database '+BaseNameSQLite)
	con = connectsqlite3(BaseNameSQLite)
	NAME_TABL = "DBALBUMS"
	logging.info ('Create '+NAME_TABL)
	Tabs =  SelectTOTab(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()    
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE DBALBUMS(ID_CD INT PRIMARY KEY, MD5 TEXT, Family TEXT, Category TEXT, Position1 TEXT, Position2 TEXT, Name TEXT, Label TEXT, ISRC TEXT, Year TEXT, Qty_CD INT,Qty_Cue INT,Qty_CueERR INT, Qty_repMusic INT, Qty_Tracks INT, Qty_audio INT, Typ_Audio TEXT, Qty_repCover, Qty_covers, Cover TEXT, Path TEXT, Size INT, Duration TEXT, Length TEXT, Typ_Tag TEXT, Date_Insert DATETIME, Date_Modifs DATETIME, RHDD_Modifs DATETIME, Score INT, Statut TEXT)")
		cur.executemany("INSERT INTO DBALBUMS VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", Tabs)
		cur.execute("CREATE UNIQUE INDEX DBALBUMS_ndx_idcd ON DBALBUMS(ID_CD)")
		cur.execute("CREATE INDEX DBALBUMS_ndx_Date_Insert ON DBALBUMS(Date_Insert)")
		con.commit() 

	NAME_TABL = "DBTRACKS"
	logging.info ('Create '+NAME_TABL)
	Tabs =  SelectTOTab(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()    
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE DBTRACKS(ID_CD INT,ID_TRACK INT PRIMARY KEY, Family TEXT, Category TEXT, Position1 TEXT, Position2 TEXT, REP_Album TEXT, REP_Track TEXT,FIL_Track TEXT,TAG_Exten TEXT,TAG_Album TEXT, TAG_Albumartists TEXT, TAG_Year TEXT,TAG_Disc INT, TAG_Track INT,ODR_Track TEXT, TAG_Artists TEXT,TAG_Title TEXT,TAG_Genres TEXT,TAG_Duration TEXT,TAG_length TEXT,Score INT,Date_Insert DATETIME, Statut TEXT, FOREIGN KEY(ID_CD) REFERENCES DBALBUMS(ID_CD))")
		cur.executemany("INSERT INTO DBTRACKS VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", Tabs)	
		cur.execute("CREATE UNIQUE INDEX DBTRACKS_ndx_idtrack ON DBTRACKS(ID_TRACK)")
		cur.execute("CREATE INDEX DBTRACKS_ndx_idcd ON DBTRACKS(ID_CD)")
	con.commit() 

	NAME_TABL = "DBCOVERS"
	logging.info ('Create '+NAME_TABL)
	Tabs =  SelectTOTab(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE {t}(MD5 TEXT, Cover64 BLOB)".format(t=NAME_TABL))
		cur.executemany("INSERT INTO {t} VALUES(?, ?)".format(t=NAME_TABL), Tabs)	
		cur.execute("CREATE UNIQUE INDEX DBCOVERS_ndx_md5 ON DBCOVERS(MD5)")
	con.commit() 

	NAME_TABL = "VW_DBCOMPLETION"
	logging.info ('Create '+NAME_TABL)
	Tabs =  SelectTOTab(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE {t}(Synthax TEXT)".format(t=NAME_TABL))
		cur.executemany("INSERT INTO {t} VALUES(?)".format(t=NAME_TABL), Tabs)	
	con.commit() 
	
	logging.info("test")
	with con:
		cur = con.cursor()    
		cur.execute("SELECT * FROM VW_DBCOMPLETION;")
	con.commit()
	row = cur.fetchall()
	logging.info (row[0])
	
	con.close()

###################################################################
# START
if __name__ == "__main__":
	ENVT = "TEST"
	BASE_SQLI = "Invent_{envt}.db".format(envt=ENVT)
	conmysql = ConnectInvent(ENVT)
	CopyDatabaseInvent(conmysql, BASE_SQLI)
	conmysql.close()
