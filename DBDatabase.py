#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import  path, chdir
from base64 import b64decode
from PyQt5.QtCore import QSettings, qDebug
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QPixmap


PATH_PROG = path.dirname(path.abspath(__file__))
chdir(PATH_PROG)
BASE_SQLI = path.join(PATH_PROG, 'LOC', "DBALBUMS_{envt}.db")

def connectDatabase(envt):
	"""Connect base MySQL/Sqlite."""
	FILE__INI = 'DBAlbums.ini'
	configini = QSettings(FILE__INI, QSettings.IniFormat)
	configini.beginGroup(envt)
	MODE_SQLI = configini.value('typb')
	BASE_RAC = r'' + configini.value('raci')
	RACI_DOU = configini.value('cate')
	RACI_SIM = configini.value('cats')
	boolcon = False
	if MODE_SQLI == 'sqlite':
		db = QSqlDatabase.addDatabase("QSQLITE")
		db.setDatabaseName(BASE_SQLI.format(envt=envt))
		if not db.isValid():
			qDebug(envt+' problem no valid database')
	else:
		BASE_SEV = configini.value('serv')
		BASE_USR = configini.value('user')
		BASE_PAS = configini.value('pass')
		BASE_NAM = configini.value('base')
		BASE_PRT = int(configini.value('port'))
		configini.endGroup()
		if MODE_SQLI == 'mysql':
			db = QSqlDatabase.addDatabase("QMYSQL")
		elif MODE_SQLI == 'mssql':
			db = QSqlDatabase.addDatabase("QODBC")
		db.setHostName(BASE_SEV)
		db.setDatabaseName(BASE_NAM)
		db.setUserName(BASE_USR)
		db.setPassword(BASE_PAS)
		db.setPort(BASE_PRT)
	list_category = []
	if RACI_DOU is not None:
		list_category += buildlistcategory(configini, RACI_DOU, BASE_RAC, 'D')
	if RACI_SIM is not None:
		list_category += buildlistcategory(configini, RACI_SIM, BASE_RAC, 'S')	
	if db.isValid():
		boolcon = db.open()
	else:
		qDebug(envt+' problem for open database')
	return boolcon, db, MODE_SQLI, BASE_RAC, list_category


def buildlistcategory(configini, category, racine,  mode):
	# build racines doubles
	list_category = []
	configini.beginGroup(category)
	for cate in configini.allKeys():
		listracate = configini.value(cate)
		family = None
		if isinstance(listracate, list):
			for racate in listracate:
				if racate.find('|') > 0:
					family = racate.split('|')[1]
					racate = racate.split('|')[0]
				racate = path.join(racine, racate)
				list_category.append([cate, mode, racate, family])
		else:
			racate = listracate
			if racate.find('|') > 0:
				family = racate.split('|')[1]
				racate = racate.split('|')[0]
			racate = path.join(racine, racate)
			list_category.append([cate, mode, racate, family])
	configini.endGroup()
	return list_category


def getrequest(name, MODE_SQLI=None):
	"""Store requests."""
	# autocompletion VW_DBCOMPLETION
	if name == 'autocompletion':
		if MODE_SQLI == 'mssql':
			request = "SELECT TOP 1000 Synthax FROM VW_AUTOCOMPLETION GROUP BY Synthax ORDER BY COUNT(*) DESC;"
		else:
			request = "SELECT Synthax FROM VW_AUTOCOMPLETION GROUP BY Synthax ORDER BY COUNT(*) DESC LIMIT 1000;"
	# date modification base
	if name == 'datedatabase':
		request = "SELECT MAX(datebase) FROM (SELECT MAX(Date_insert) AS datebase FROM DBALBUMS UNION SELECT MAX(Date_Modifs) FROM DBALBUMS ) FUS;"
	# list albums DBALBUMS
	if name == 'albumslist':
		request = "SELECT Category, Family, Name, Label, ISRC, " \
				"Qty_Tracks, Qty_CD, Year, Length, Size, " \
				"Score, Qty_covers, Date_Insert, Date_Modifs, "
		if MODE_SQLI == 'sqlite':
			request = request + "Position1 || '\\' || Position2 AS Position, "
		if MODE_SQLI == 'mysql':
			request = request + "CONCAT(Position1,'\\\\',Position2) AS Position, "
		if MODE_SQLI == 'mssql':
			request = request + "Position1+'\'+Position2 AS Position, "
		request = request + " Typ_Tag, Path, Cover, MD5, ID_CD AS ID " \
							"FROM DBALBUMS WHERE 1=1 ORDER BY Date_Insert DESC"
	# list tracks
	if name == 'trackslist':
		request = "SELECT ODR_Track, TAG_Artists, TAG_Title, TAG_length, " \
					"Score, TAG_Genres, FIL_Track, REP_Track, ID_TRACK  " \
					"FROM DBTRACKS WHERE ID_CD={id} ORDER BY REP_Track, ODR_Track"
	# search in track
	if name == 'tracksinsearch':
		request = "SELECT ID_CD AS ID FROM DBTRACKS AS TRK WHERE TAG_Artists like '%{search}%' OR TAG_Title like '%{search}%' GROUP BY ID_CD"
	# search genres/style
	if name == 'tracksgesearch':
		request = "SELECT ID_CD AS ID FROM DBTRACKS AS TRK WHERE REPLACE(TAG_Genres,'-','') like '{search}' GROUP BY ID_CD"
	# cover base64
	if name == 'cover':
		request = "SELECT Cover64 FROM DBCOVERS WHERE MD5='{MD5}'"
	# minicover base64
	if name == 'minicover':
		request = "SELECT MiniCover64 FROM DBCOVERS WHERE MD5='{MD5}'"
	# update Sore Album
	if name == 'updatescorealbum':
		request = "UPDATE DBALBUMS SET Score={score} WHERE ID_CD={id}"
	# update Sore Track
	if name == 'updatescoretrack':
		request = "UPDATE DBTRACKS SET Score={score} WHERE ID_TRACK={id}"
	# insert playlist foobar
	if name == 'playlistfoobar':
		request = "INSERT INTO DBFOOBAR (Playlist, Path, FIL_Track, Name , MD5, TAG_Album, TAG_Artists, TAG_Title) " \
					"VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
	if name == 'listgenres':
		request = "SELECT DISTINCT ID_CD, TAG_Genres FROM DBTRACKS;"
	if MODE_SQLI == 'mssql':
		request = request.replace(' `', ' [').replace('` ', '] ')
	return request


def buildFileCover(filenamecover, md5):
	"""Build cover base64/mysql to file."""
	request = (getrequest('cover')).format(MD5=md5)
	coverb64 = buildTabFromRequest(request)[0]
	cover = b64decode(coverb64)
	filecover = open(filenamecover, "wb")
	filecover.write(cover)
	filecover.close()


def extractCoverb64(md5, blankcover, namerequest='cover'):
	"""Get base64 picture cover."""
	request = (getrequest(namerequest)).format(MD5=md5)
	try:
		coverb64 = buildTabFromRequest(request)[0]
		cover = b64decode(coverb64)
		labelpixmap = QPixmap()
		labelpixmap.loadFromData(cover)
	except:
		pass
		qDebug('err thunbnail read : '+str(md5))
		labelpixmap = QPixmap(blankcover)
	return labelpixmap


def updateBaseScore(score, idalb, req):
	"""Maj Mysql table Albums."""
	req = req.format(score=score, id=idalb)
	query = QSqlQuery()
	query.exec_(req)
	query.clear


def execSqlFile(parent, sql_file, nbop):
	"""Exec script SQL file..."""
	#cur = con.cursor()
	statement = ""
	counter = 0
	parent.updateGaugeBar(0, "Exececution script SQL file"+sql_file)
	for line in open(sql_file):
		if line[0:2] == '--':
			if line[0:3] == '-- ':
				parent.updateGaugeBar((counter/nbop)*100, "Exec :"+line.replace('--', ''))
			continue
		statement = statement + line
		if len(line) > 2 and line[-2] == ';':
			counter = counter + 1
			query = QSqlQuery()
			query.exec_(statement)
			if not query.exec_():
				errorText = query.lastError().text()
				qDebug(query.lastQuery())
				qDebug(errorText)
				break
			query.clear
			statement = ""
	parent.updateGaugeBar(100)


def buildTabFromRequest(req):
	"""Select to memory list."""
	autoList = []
	query = QSqlQuery(req)
	query.exec_(req)
	indexes = query.record().count()
	while query.next():
		if indexes == 1:
			autoList.append(query.value(0))
		else:
			row = [query.value(index) for index in range(indexes)]
			autoList.append(row)
	query.clear
	return autoList


def buildReqTCD(group, column, tableName, TDCName='TDC', TDCSum=1, LineSum=True, MODE_SQLI='mysql'):
	"""build request Pivot table compatible sqlite, mysql, SQLserver."""
	# Collections
	req = "SELECT `{column}` FROM {tableName} GROUP BY `{column}` ;".format(tableName=tableName, column=column)
	if MODE_SQLI == 'mssql':
		req = req.replace(' `', ' [').replace('` ', '] ')
	col_names = buildTabFromRequest(req)
	# sum/collections
	lstcols = ''
	ReqTDC = "(SELECT `{group}` AS '{TDCName}' ,\n".format(group=group, TDCName=TDCName)
	for col_name in col_names:
		ReqTDC += "    SUM(CASE WHEN `{column}` = '{col_name}' THEN {TDCSum} ELSE 0 END) AS `{col_name}` ,\n".format(column=column, TDCSum=TDCSum, col_name=col_name)
		lstcols += " `{col_name}` ,".format(col_name=col_name)
	ReqTDC += "    SUM({TDCSum}) AS 'TOTAL' FROM {tableName} GROUP BY `{group}` \n".format(tableName=tableName, TDCSum=TDCSum, group=group)
	# sum global
	if LineSum:
		ReqTDC += " UNION \nSELECT 'TOTAL', \n"
		for col_name in col_names:
			ReqTDC += "    SUM(CASE WHEN `{column}` = '{col_name}' THEN {TDCSum} ELSE 0 END),\n".format(column=column, TDCSum=TDCSum, col_name=col_name)
		ReqTDC += "    SUM({TDCSum}) FROM {tableName}\n".format(tableName=tableName, TDCSum=TDCSum)
	# order by total is last line
	ReqTDC += ") tdc ORDER BY 'TOTAL';"
	# select column
	ReqTDC = "SELECT `"+TDCName+"` ,"+lstcols+" `TOTAL` FROM \n" + ReqTDC
	# replace ` for [] sqlserver
	if MODE_SQLI == 'mssql':
		ReqTDC = ReqTDC.replace(' `', ' [').replace('` ', '] ')
	return ReqTDC


def copytable(dbsrc, dbdes, tablename, reqcreate, reqinsert, reqindexe=None):
	"""Copy table. Create+Datas+Index."""
	querylite = QSqlQuery(None, dbdes)
	query = QSqlQuery(None, dbsrc)
	# drop
	querylite.exec_("DROP TABLE {t}".format(t=tablename))
	if not querylite.exec_():
		qDebug(10*' '+"drop "+querylite.lastError().text())
	# create
	querylite.exec_(reqcreate)
	if not querylite.exec_():
		qDebug(10*' '+"create "+querylite.lastError().text())
	# datas
	query.exec_("SELECT * FROM "+tablename)
	while query.next():
		querylite.prepare(reqinsert)
		for indcol in range(query.record().count()):
			querylite.bindValue(indcol, query.value(indcol))
		if not querylite.exec_():
			qDebug(tablename+"10*' ' "+querylite.lastError().text())
			listparam = list(querylite.boundValues().values())
			for i in range(len(listparam)):
				qDebug(10*' ', i, listparam[i])
	# index
	if reqindexe is not None:
		querylite.exec_(reqindexe)
		if not querylite.exec_():
			qDebug(10*' '+":index "+querylite.lastError().text())
	querylite.clear
	query.clear


def copyDatabaseInvent(parent, db, basename, logname):
	"""create SqlLite Database."""
	qDebug('Process Creation Database Sqlite '+basename)
	parent.updateGaugeBar(0, 'Process Creation Database Sqlite '+basename)
	# create sqlite database
	cnxlite = 'CREA'
	dblite = QSqlDatabase.addDatabase("QSQLITE", cnxlite)
	dblite.setDatabaseName(basename)
	if dblite.isValid():
		boolcon = dblite.open()
		if boolcon:
			parent.updateGaugeBar(5)
			tablename = "DBALBUMS"
			qDebug('Create '+tablename)
			reqcreate = "CREATE TABLE DBALBUMS(ID_CD INTEGER PRIMARY KEY AUTOINCREMENT, MD5 TEXT, Family TEXT, " \
						"Category TEXT, Position1 TEXT, Position2 TEXT, Name TEXT, Label TEXT, ISRC TEXT, " \
						"Year TEXT, Qty_CD INT, Qty_Cue INT, Qty_CueERR INT, Qty_repMusic INT, Qty_Tracks INT, " \
						"Qty_audio INT, Typ_Audio TEXT, Qty_repCover, Qty_covers, Cover TEXT, Path TEXT, Size INT, " \
						"Duration TEXT, Length TEXT, Typ_Tag TEXT, Date_Insert DATETIME, Date_Modifs DATETIME, RHDD_Modifs DATETIME, Score INT, Statut TEXT)"
			reqinsert = "INSERT INTO DBALBUMS VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
			reqindexe = "CREATE INDEX DBALBUMS_ndx_Date_Insert ON DBALBUMS(Date_Insert)"
			copytable(db, dblite, tablename, reqcreate, reqinsert, reqindexe)
			parent.updateGaugeBar(15)
			tablename = "DBTRACKS"
			qDebug('Create '+tablename)
			reqcreate = "CREATE TABLE DBTRACKS(ID_CD INT,ID_TRACK INTEGER PRIMARY KEY AUTOINCREMENT, Family TEXT, " \
						"Category TEXT, Position1 TEXT, Position2 TEXT, REP_Album TEXT, REP_Track TEXT,FIL_Track TEXT, " \
						"TAG_Exten TEXT,TAG_Album TEXT, TAG_Albumartists TEXT, TAG_Year TEXT,TAG_Disc INT, TAG_Track INT, " \
						"ODR_Track TEXT, TAG_Artists TEXT,TAG_Title TEXT,TAG_Genres TEXT,TAG_Duration TEXT,TAG_length TEXT, " \
						"Score INT,Date_Insert DATETIME, Statut TEXT, FOREIGN KEY(ID_CD) REFERENCES DBALBUMS(ID_CD))"
			reqinsert = "INSERT INTO DBTRACKS VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )"
			reqindexe = "CREATE INDEX DBTRACKS_ndx_idcd ON DBTRACKS(ID_CD)"
			copytable(db, dblite, tablename, reqcreate, reqinsert, reqindexe)
			parent.updateGaugeBar(30)
			tablename = "DBFOOBAR"
			qDebug('Create '+tablename)
			reqcreate = "CREATE TABLE {t}(ID_FOO INTEGER PRIMARY KEY AUTOINCREMENT, MD5 TEXT, Name TEXT, Path TEXT, " \
						"FIL_Track TEXT, Playlist TEXT, TAG_Album TEXT, TAG_Artists TEXT, TAG_Title TEXT, " \
						"Date_insert TIMESTAMP DEFAULT CURRENT_TIMESTAMP)".format(t=tablename)
			reqinsert = "INSERT INTO {t} VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(t=tablename)
			reqindexe = "CREATE INDEX DBFOOBAR_ndx_FIL_Track ON DBFOOBAR(FIL_Track)"
			copytable(db, dblite, tablename, reqcreate, reqinsert, reqindexe)
			parent.updateGaugeBar(45)
			tablename = "DBFOOBOR"
			qDebug('Create '+tablename)
			reqcreate = "CREATE TABLE {t}(FIL_Track TEXT, FIL_TrackM TEXT)".format(t=tablename)
			reqinsert = "INSERT INTO {t} VALUES( ?, ?)".format(t=tablename)
			copytable(db, dblite, tablename, reqcreate, reqinsert)
			parent.updateGaugeBar(60)
			tablename = "DBCOVERS"
			qDebug('Create '+tablename)
			reqcreate = "CREATE TABLE {t}(MD5 TEXT, Cover64 BLOB, MiniCover64 BLOB)".format(t=tablename)
			reqinsert = "INSERT INTO {t} VALUES( ?, ?, ?)".format(t=tablename)
			reqindexe = "CREATE UNIQUE INDEX DBCOVERS_ndx_md5 ON DBCOVERS(MD5)"
			copytable(db, dblite, tablename, reqcreate, reqinsert, reqindexe)
			parent.updateGaugeBar(75)
			tablename = "VW_AUTOCOMPLETION"
			qDebug('Create '+tablename)
			reqcreate = "CREATE TABLE {t}(ID_CD INT, Synthax TEXT)".format(t=tablename)
			reqinsert = "INSERT INTO {t} VALUES( ?, ?)".format(t=tablename)
			copytable(db, dblite, tablename, reqcreate, reqinsert)
			# remove database sqlite
			db.removeDatabase(cnxlite)
			parent.updateGaugeBar(100)
		else:
			qDebug('no create', basename)
