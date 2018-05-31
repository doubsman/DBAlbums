#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import system, path, getcwd, name, remove
from base64 import b64decode, decodestring
from pymysql import connect
from sqlite3 import connect as connectsqlite3
from logging import DEBUG, basicConfig, info

SERV_TEST = 'doubbigstation'
USER_TEST = 'admInvent'
PASS_TEST = 'MwRbBR2HA8PFQjuu'
BASE_TEST = 'Invent'
TEXT_NCO = 'No Picture'
C_REQUEST = """SELECT MD5, Cover64 FROM DBCOVERS WHERE MD5='{MD5}'"""

def ConnectInvent(envt="LOSSLESS_TEST"):
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

# false bar status
class Object(object):
	pass
	def update(sefl,n):
		pass
	def settitle(sefl,n):
		pass
	def open(sefl):
		pass
	def close(sefl):
		pass

def CopyDatabaseInvent(conMySQL, BaseNameSQLite, BarGauge, logname):
	basicConfig(filename=logname,
							filemode='a',
							format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
							datefmt='%H:%M:%S',
							level=DEBUG)
	info ('Create/Update Database '+BaseNameSQLite)
	BarGauge.open()
	con = connectsqlite3(BaseNameSQLite)
	NAME_TABL = "DBALBUMS"
	BarGauge.update(0.05)
	BarGauge.settitle('Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  SelectTOTab(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()    
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE DBALBUMS(ID_CD INTEGER PRIMARY KEY AUTOINCREMENT, MD5 TEXT, Family TEXT, Category TEXT, Position1 TEXT, Position2 TEXT, Name TEXT, Label TEXT, ISRC TEXT, Year TEXT, Qty_CD INT,Qty_Cue INT,Qty_CueERR INT, Qty_repMusic INT, Qty_Tracks INT, Qty_audio INT, Typ_Audio TEXT, Qty_repCover, Qty_covers, Cover TEXT, Path TEXT, Size INT, Duration TEXT, Length TEXT, Typ_Tag TEXT, Date_Insert DATETIME, Date_Modifs DATETIME, RHDD_Modifs DATETIME, Score INT, Statut TEXT)")
		cur.executemany("INSERT INTO DBALBUMS VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", Tabs)
		cur.execute("CREATE INDEX DBALBUMS_ndx_Date_Insert ON DBALBUMS(Date_Insert)")
		con.commit() 
	
	NAME_TABL = "DBTRACKS"
	BarGauge.update(0.25)
	BarGauge.settitle('Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  SelectTOTab(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()    
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE DBTRACKS(ID_CD INT,ID_TRACK INTEGER PRIMARY KEY AUTOINCREMENT, Family TEXT, Category TEXT, Position1 TEXT, Position2 TEXT, REP_Album TEXT, REP_Track TEXT,FIL_Track TEXT,TAG_Exten TEXT,TAG_Album TEXT, TAG_Albumartists TEXT, TAG_Year TEXT,TAG_Disc INT, TAG_Track INT,ODR_Track TEXT, TAG_Artists TEXT,TAG_Title TEXT,TAG_Genres TEXT,TAG_Duration TEXT,TAG_length TEXT,Score INT,Date_Insert DATETIME, Statut TEXT, FOREIGN KEY(ID_CD) REFERENCES DBALBUMS(ID_CD))")
		cur.executemany("INSERT INTO DBTRACKS VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", Tabs)
		cur.execute("CREATE INDEX DBTRACKS_ndx_idcd ON DBTRACKS(ID_CD)")
	con.commit() 
	
	NAME_TABL = "DBFOOBAR"
	BarGauge.update(0.5)
	BarGauge.settitle('Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  SelectTOTab(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE {t}(ID_FOO INTEGER PRIMARY KEY AUTOINCREMENT, MD5 TEXT, Name TEXT, Path TEXT, FIL_Track TEXT, Playlist TEXT, TAG_Album TEXT, TAG_Artists TEXT, TAG_Title TEXT, Date_insert TIMESTAMP DEFAULT CURRENT_TIMESTAMP)".format(t=NAME_TABL))
		cur.executemany("INSERT INTO {t} VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(t=NAME_TABL), Tabs)
		cur.execute("CREATE INDEX DBFOOBAR_ndx_FIL_Track ON DBFOOBAR(FIL_Track)")
	con.commit() 
	
	NAME_TABL = "DBFOOBOR"
	BarGauge.update(0.6)
	BarGauge.settitle('Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  SelectTOTab(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE {t}(FIL_Track TEXT, FIL_TrackM TEXT)".format(t=NAME_TABL))
		cur.executemany("INSERT INTO {t} VALUES(?, ?)".format(t=NAME_TABL), Tabs)
	con.commit() 
	
	NAME_TABL = "DBCOVERS"
	BarGauge.update(0.75)
	BarGauge.settitle('Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  SelectTOTab(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE {t}(MD5 TEXT, Cover64 BLOB, MiniCover64 BLOB)".format(t=NAME_TABL))
		cur.executemany("INSERT INTO {t} VALUES(?, ?, ?)".format(t=NAME_TABL), Tabs)
		cur.execute("CREATE UNIQUE INDEX DBCOVERS_ndx_md5 ON DBCOVERS(MD5)")
	con.commit() 
	
	NAME_TABL = "VW_DBCOMPLETLISTPUB"
	BarGauge.update(0.9)
	BarGauge.settitle('Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  SelectTOTab(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE {t}(Synthax TEXT)".format(t=NAME_TABL))
		cur.executemany("INSERT INTO {t} VALUES(?)".format(t=NAME_TABL), Tabs)
	con.commit() 
	
	BarGauge.update(1)
	BarGauge.settitle('Create DataBase Completed: '+BaseNameSQLite)
	info("test")
	with con:
		cur = con.cursor()    
		cur.execute("SELECT * FROM VW_DBCOMPLETLISTPUB;")
	con.commit()
	row = cur.fetchall()
	info (row[0])
	
	con.close()
	BarGauge.close()

###################################################################
# START
if __name__ == "__main__":
	ENVT = "LOSSLESS_TEST"
	BASE_SQLI = "Invent_{envt}.db".format(envt=ENVT)
	conmysql = ConnectInvent(ENVT)
	bar = Object()
	CopyDatabaseInvent(conmysql, BASE_SQLI, bar, "E:\ZTest\essai.log")
	conmysql.close()
