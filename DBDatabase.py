#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import  path, chdir
from PyQt5.QtCore import Qt, QSettings, qDebug, QObject, QByteArray, QIODevice, QBuffer
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QPixmap
from DBFunction import buildlistcategory

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


def getrequest(name, MODE_SQLI=None):
	"""Store requests."""
	# autocompletion VW_DBCOMPLETION
	if name == 'autocompletion':
		if MODE_SQLI == 'mssql':
			request = "SELECT TOP 1000 Synthax FROM VW_AUTOCOMPLETION GROUP BY Synthax ORDER BY COUNT(*) DESC;"
		else:
			request = "SELECT Synthax FROM VW_AUTOCOMPLETION GROUP BY Synthax ORDER BY COUNT(*) DESC LIMIT 1000;"
	# date modification base
	elif name == 'datedatabase':
		request = "SELECT MAX(datebase) FROM (SELECT MAX(Date_insert) AS datebase FROM DBALBUMS UNION SELECT MAX(Date_Modifs) FROM DBALBUMS ) FUS;"
	# list albums DBALBUMS
	elif name == 'albumslist':
		request = "SELECT Category, Family, Name, Label, ISRC, " \
				"Qty_Tracks, Qty_CD, Year, Length, Size, " \
				"Score, Qty_covers, Date_Insert, Date_Modifs, "
		if MODE_SQLI == 'sqlite':
			request = request + "Position1 || '\\' || Position2 AS Position, "
		if MODE_SQLI == 'mysql':
			request = request + "CONCAT(Position1,'\\\\',Position2) AS Position, "
		if MODE_SQLI == 'mssql':
			request = request + "Position1+'\'+Position2 AS Position, "
		request = request + " Typ_Tag, Path, Cover, MD5, ID_CD " \
							"FROM DBALBUMS WHERE 1=1 ORDER BY Date_Insert DESC"
	# list tracks
	elif name == 'trackslist':
		request = "SELECT ODR_Track, TAG_Artists, TAG_Title, TAG_length, " \
					"Score, TAG_Genres, FIL_Track, REP_Track, ID_TRACK  " \
					"FROM DBTRACKS WHERE ID_CD={id} ORDER BY REP_Track, ODR_Track"
	# search in track
	elif name == 'tracksinsearch':
		request = "SELECT ID_CD AS ID FROM DBTRACKS AS TRK WHERE TAG_Artists like '%{search}%' OR TAG_Title like '%{search}%' GROUP BY ID_CD"
	# search genres/style
	elif name == 'tracksgesearch':
		request = "SELECT ID_CD AS ID FROM DBTRACKS AS TRK WHERE REPLACE(TAG_Genres,'-','') like '{search}' GROUP BY ID_CD"
	# cover
	elif name == 'coverpix':
		request = "SELECT Cover FROM DBPIXMAPS WHERE ID_CD={id}"
	elif name == 'thumbnailpix':
		request = "SELECT Thumbnail FROM DBPIXMAPS WHERE ID_CD={id}"
	# update Sore Album
	elif name == 'updatescorealbum':
		request = "UPDATE DBALBUMS SET Score={score} WHERE ID_CD={id}"
	# update Sore Track
	elif name == 'updatescoretrack':
		request = "UPDATE DBTRACKS SET Score={score} WHERE ID_TRACK={id}"
	# insert playlist foobar
	elif name == 'playlistfoobar':
		request = "INSERT INTO DBFOOBAR (Playlist, Path, FIL_Track, Name , MD5, TAG_Album, TAG_Artists, TAG_Title) " \
					"VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
	# combobox style
	elif name == 'listgenres':
		request = "SELECT DISTINCT ID_CD, TAG_Genres FROM DBTRACKS;"
	if MODE_SQLI == 'mssql':
		request = request.replace(' `', ' [').replace('` ', '] ')
	return request



class DBFuncBase(QObject):
	def __init__(self, parent=None):
		"""Init."""
		super(DBFuncBase, self).__init__(parent)
		self.parent = parent

	def arrayToSql(self, operation, arraydata, tablename, columnnamekey):    # TEST
		listcolumns = self.getListColumnsTable(tablename)
		numberscolumns = len(listcolumns)	
		
		if operation == 'INSERT':
			# build query insert
			request = 'INSERT INTO ' + tablename + '('
			request += ', '.join(listcolumns) + ') VALUES '
			request += '(' + ', '.join( ['?'] * numberscolumns) +')' 
		elif operation == 'UPDATE':
			# build query update
			request = 'UPDATE ' + tablename + ' SET ('
			request += ' = ? ,'.join(listcolumns[1:]) + ' = ?)'
			request += 'WHERE ' + listcolumns[1] + ' = ?'	
		else:
			return False
		print(request)
		return False     # TEST
		
		# repeat query insert 
		queryoperation = QSqlQuery()
		for row in arraydata:
			queryoperation.prepare(request)
			for column in range(numberscolumns):
				# first column : primary key
				if listcolumns[column] == columnnamekey:
					if operation == 'INSERT':
						queryoperation.bindValue(column, 'NULL')
					elif operation == 'UPDATE':
						id = row[column]
				# last column column : primary key
				elif column == numberscolumns - 1 and operation == 'UPDATE':
					queryoperation.bindValue(column, id)
				else:
					queryoperation.bindValue(column, row[column])
			if not queryoperation.exec_():
				qDebug(tablename+"10*' ' "+queryoperation.lastError().text())
				listparam = list(queryoperation.boundValues().values())
				for i in range(len(listparam)):
					qDebug(10*' ', i, listparam[i])
				return False
		return True
	
	def getListColumnsTable(self, tablename):
		"""Get list columns from table."""
		request = 'SELECT * FROM ' + tablename + ' LIMIT 0'
		query = QSqlQuery(request)
		query.exec_()
		listcolumns = self.getListColumns(query)
		query.clear
		return listcolumns

	def getListColumns(self, query):
		"""Get list columns from QsqlQuery."""
		listcolumns = []
		numberscolumns = query.record().count()		
		for column in range(numberscolumns):
			listcolumns.append(query.record().fieldName(column))
		return listcolumns

	def sqlToArray(self, request):
		"""Select to array data."""
		arraydata = []
		query = QSqlQuery(request)
		query.exec_(request)
		indexes = query.record().count()
		while query.next():
			if indexes == 1:
				arraydata.append(query.value(0))
			else:
				row = [query.value(index) for index in range(indexes)]
				arraydata.append(row)
		query.clear
		return arraydata

	def execSqlFile(self, sql_file, nbop):
		"""Exec script SQL file..."""
		#cur = con.cursor()
		statement = ""
		counter = 0
		self.parent.updateGaugeBar(0, "Exececution script SQL file"+sql_file)
		for line in open(sql_file):
			if line[0:2] == '--':
				if line[0:3] == '-- ':
					self.parent.updateGaugeBar((counter/nbop)*100, "Exec :"+line.replace('--', ''))
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
		self.parent.updateGaugeBar(100)

	def imageToSql(self, pathimage, idcd, minisize):
		"""Write image and thunbnail to database."""
		# just file
		#file = QFile(pathimage)
		#file.open(QIODevice.ReadOnly)
		#inByteArray = QByteArray(file.readAll())
		
		# image big
		inPixmap = QPixmap(pathimage)
		inByteArray = QByteArray()
		inBuffer = QBuffer(inByteArray)
		if not inBuffer.open(QIODevice.WriteOnly):
			return False
		inPixmap.save(inBuffer,"JPG");
		
		# image mini
		inPixmap = inPixmap.scaled(minisize, minisize, Qt.IgnoreAspectRatio, Qt.FastTransformation)
		inByteArraymini = QByteArray()
		inBuffer = QBuffer(inByteArraymini)
		inBuffer.open(QIODevice.WriteOnly);
		inPixmap.save(inBuffer,"JPG");
		
		# mssql
		# https://stackoverflow.com/questions/108403/solutions-for-insert-or-update-on-sql-server
		
		# UPDATE data or INSERT : https://en.wikipedia.org/wiki/Merge_(SQL)
		query = QSqlQuery()
		query.prepare( "REPLACE INTO DBPIXMAPS(ID_CD, NamePix, Cover, Thumbnail) VALUES (?, ?, ?, ?)")
		query.bindValue(0, idcd)
		query.bindValue(1, pathimage)
		query.bindValue(2, inByteArray)
		query.bindValue(3, inByteArraymini)
		if not query.exec_():
			qDebug(10*' '+":index "+query.lastError().text())
			return False
		return True

	def sqlToPixmap(self, idcd, blankcover, typecover = 'coverpix'):
		"""Read database image, return Blank Pixmap else."""
		request = (getrequest(typecover)).format(id=idcd)
		try:
			cover = self.sqlToArray(request)
			if len(cover) > 0:
				coverpixmap = QPixmap()
				coverpixmap.loadFromData(cover[0])
			else:
				coverpixmap = QPixmap(blankcover)
		except:
			pass
			qDebug('err thumbnail read : '+str(idcd))
			coverpixmap = QPixmap(blankcover)
		return coverpixmap
	
	def sqlImageToFile(self, idcd, savepathfile, typecover = 'coverpix'):
		"""Read database image, build file image."""
		request = (getrequest(typecover)).format(id=idcd)
		cover = self.sqlToArray(request)[0]
		savefile = open(savepathfile, "wb")
		savefile.write(cover[0])
		savefile.close()

	def buildReqTCD(self, group, column, tableName, TDCName='TDC', TDCSum=1, LineSum=True, MODE_SQLI='mysql'):
		"""build request Pivot table compatible sqlite, mysql, SQLserver."""
		# Collections
		req = "SELECT `{column}` FROM {tableName} GROUP BY `{column}` ;".format(tableName=tableName, column=column)
		if MODE_SQLI == 'mssql':
			req = req.replace(' `', ' [').replace('` ', '] ')
		col_names = self.sqlToArray(req)
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


class DBCreateSqLite(QObject):
	def __init__(self, parent=None):
		"""Init."""
		super(DBCreateSqLite, self).__init__(parent)
		self.parent = parent
		
	def copytable(self, dbsrc, dbdes, tablename, reqcreate, reqinsert, reqindexe=None):
		"""Copy table. Create+Datas+Index."""
		querylite = QSqlQuery(self, dbdes)
		query = QSqlQuery(self, dbsrc)
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

	def copyDatabaseInvent(self, db, basename, logname):
		"""create SqlLite Database."""
		qDebug('Process Creation Database Sqlite '+basename)
		self.parent.updateGaugeBar(0, 'Process Creation Database Sqlite '+basename)
		# create sqlite database
		cnxlite = 'CREA'
		dblite = QSqlDatabase.addDatabase("QSQLITE", cnxlite)
		dblite.setDatabaseName(basename)
		if dblite.isValid():
			boolcon = dblite.open()
			if boolcon:
				self.parent.updateGaugeBar(5)
				tablename = "DBALBUMS"
				qDebug('Create '+tablename)
				reqcreate = "CREATE TABLE DBALBUMS(ID_CD INTEGER PRIMARY KEY AUTOINCREMENT, MD5 TEXT, Family TEXT, " \
							"Category TEXT, Position1 TEXT, Position2 TEXT, Name TEXT, Label TEXT, ISRC TEXT, " \
							"Year TEXT, Qty_CD INT, Qty_Cue INT, Qty_CueERR INT, Qty_repMusic INT, Qty_Tracks INT, " \
							"Qty_audio INT, Typ_Audio TEXT, Qty_repCover, Qty_covers, Cover TEXT, Path TEXT, Size INT, " \
							"Duration TEXT, Length TEXT, Typ_Tag TEXT, Date_Insert DATETIME, Date_Modifs DATETIME, RHDD_Modifs DATETIME, Score INT, Statut TEXT)"
				reqinsert = "INSERT INTO DBALBUMS VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
				reqindexe = "CREATE INDEX DBALBUMS_ndx_Date_Insert ON DBALBUMS(Date_Insert)"
				self.copytable(db, dblite, tablename, reqcreate, reqinsert, reqindexe)
				self.parent.updateGaugeBar(15)
				tablename = "DBTRACKS"
				qDebug('Create '+tablename)
				reqcreate = "CREATE TABLE DBTRACKS(ID_CD INT,ID_TRACK INTEGER PRIMARY KEY AUTOINCREMENT, Family TEXT, " \
							"Category TEXT, Position1 TEXT, Position2 TEXT, REP_Album TEXT, REP_Track TEXT,FIL_Track TEXT, " \
							"TAG_Exten TEXT,TAG_Album TEXT, TAG_Albumartists TEXT, TAG_Year TEXT,TAG_Disc INT, TAG_Track INT, " \
							"ODR_Track TEXT, TAG_Artists TEXT,TAG_Title TEXT,TAG_Genres TEXT,TAG_Duration TEXT,TAG_length TEXT, " \
							"Score INT,Date_Insert DATETIME, Statut TEXT, FOREIGN KEY(ID_CD) REFERENCES DBALBUMS(ID_CD))"
				reqinsert = "INSERT INTO DBTRACKS VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )"
				reqindexe = "CREATE INDEX DBTRACKS_ndx_idcd ON DBTRACKS(ID_CD)"
				self.copytable(db, dblite, tablename, reqcreate, reqinsert, reqindexe)
				self.parent.updateGaugeBar(30)
				tablename = "DBFOOBAR"
				qDebug('Create '+tablename)
				reqcreate = "CREATE TABLE {t}(ID_FOO INTEGER PRIMARY KEY AUTOINCREMENT, MD5 TEXT, Name TEXT, Path TEXT, " \
							"FIL_Track TEXT, Playlist TEXT, TAG_Album TEXT, TAG_Artists TEXT, TAG_Title TEXT, " \
							"Date_insert TIMESTAMP DEFAULT CURRENT_TIMESTAMP)".format(t=tablename)
				reqinsert = "INSERT INTO {t} VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(t=tablename)
				reqindexe = "CREATE INDEX DBFOOBAR_ndx_FIL_Track ON DBFOOBAR(FIL_Track)"
				self.copytable(db, dblite, tablename, reqcreate, reqinsert, reqindexe)
				self.parent.updateGaugeBar(45)
				tablename = "DBFOOBOR"
				qDebug('Create '+tablename)
				reqcreate = "CREATE TABLE {t}(FIL_Track TEXT, FIL_TrackM TEXT)".format(t=tablename)
				reqinsert = "INSERT INTO {t} VALUES( ?, ?)".format(t=tablename)
				self.copytable(db, dblite, tablename, reqcreate, reqinsert)
				self.parent.updateGaugeBar(60)
				tablename = "DBCOVERS"
				qDebug('Create '+tablename)
				reqcreate = "CREATE TABLE {t}(MD5 TEXT, Cover64 BLOB, MiniCover64 BLOB)".format(t=tablename)
				reqinsert = "INSERT INTO {t} VALUES( ?, ?, ?)".format(t=tablename)
				reqindexe = "CREATE UNIQUE INDEX DBCOVERS_ndx_md5 ON DBCOVERS(MD5)"
				self.copytable(db, dblite, tablename, reqcreate, reqinsert, reqindexe)
				self.parent.updateGaugeBar(75)
				tablename = "VW_AUTOCOMPLETION"
				qDebug('Create '+tablename)
				reqcreate = "CREATE TABLE {t}(ID_CD INT, Synthax TEXT)".format(t=tablename)
				reqinsert = "INSERT INTO {t} VALUES( ?, ?)".format(t=tablename)
				self.copytable(db, dblite, tablename, reqcreate, reqinsert)
				# remove database sqlite
				db.removeDatabase(cnxlite)
				self.parent.updateGaugeBar(100)
			else:
				qDebug('no create', basename)
