#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import  path, chdir, remove
from copy import deepcopy
from time import sleep
from PyQt5.QtCore import Qt, qDebug, QObject, QByteArray, QIODevice, QBuffer, pyqtSignal
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QPixmap
from DBReadJson import JsonParams

PATH_PROG = path.dirname(path.abspath(__file__))
chdir(PATH_PROG)
BASE_SQLI = path.join(PATH_PROG, 'LOC', "DBALBUMS_{envt}.db")

def connectDatabase(envt):
	"""Connect base MySQL/Sqlite."""
	FILE__INI = 'DBAlbums.json'
	Json_params = JsonParams(FILE__INI)
	group_envt = Json_params.getMember(envt)
	MODE_SQLI = group_envt['typb']
	BASE_RAC = r'' + group_envt['raci']
	RACI_DOU = group_envt['cate']
	boolcon = False
	if MODE_SQLI == 'sqlite':
		db = QSqlDatabase.addDatabase("QSQLITE")
		db.setDatabaseName(BASE_SQLI.format(envt=envt))
		if not db.isValid():
			qDebug(envt+' problem no valid database')
	else:
		BASE_SEV = group_envt['serv']
		BASE_USR = group_envt['user']
		BASE_PAS = group_envt['pass']
		BASE_NAM = group_envt['base']
		BASE_PRT = group_envt['port']
		if MODE_SQLI == 'mysql':
			db = QSqlDatabase.addDatabase("QMYSQL")
			db.setHostName(BASE_SEV)
			db.setDatabaseName(BASE_NAM)
			db.setUserName(BASE_USR)
			db.setPassword(BASE_PAS)
			db.setPort(BASE_PRT)
		elif MODE_SQLI == 'mssql':
			db = QSqlDatabase.addDatabase("QODBC3")
			driver = "DRIVER={SQL Server Native Client 11.0};Server=" + BASE_SEV + ";Database=" + BASE_NAM
			driver += ";Uid=" + BASE_USR + ";Port=" + str(BASE_PRT) + ";Pwd=" + BASE_PAS + ";Trusted_connection=yes"
			#print(driver)
			db.setDatabaseName(driver);
	list_category = []
	if RACI_DOU is not None:
		list_category += Json_params.buildCategories(envt)
	if db.isValid():
		boolcon = db.open()
	else:
		qDebug(envt+' problem for open database : '+db.lastError().text())
	return boolcon, db, MODE_SQLI, BASE_RAC, list_category


def getrequest(name, MODE_SQLI=None):
	"""Store requests."""
	# autocompletion VW_DBCOMPLETION
	if name == 'autocompletion':
		if MODE_SQLI == 'mssql':
			request = "SELECT TOP 1000 Synthax FROM VW_COMPLETION GROUP BY Synthax ORDER BY COUNT(*) DESC;"
		else:
			request = "SELECT Synthax FROM VW_COMPLETION GROUP BY Synthax ORDER BY COUNT(*) DESC LIMIT 1000;"
	# date modification base
	elif name == 'datedatabase':
		request = "SELECT MAX(datebase) FROM (SELECT MAX( `ADD` ) AS datebase FROM ALBUMS UNION SELECT MAX( `ADD` ) FROM ALBUMS ) FUS;"
	# list albums DBALBUMS
	elif name == 'albumslist':
		request = 	"SELECT " \
					" `CATEGORY` , `FAMILY` , `NAME` , `ARTIST` , `STYLE` , " \
					" `LABEL` , `TAGLABEL` , `ISRC` , `TAGISRC` , `TRACKS` , " \
					" `CD` , `YEAR` , `LENGTHDISPLAY` , `SIZE` , `SCORE` , " \
					" `PIC` , `COUNTRY` , `ADD` , `MODIFIED` , `POSITIONHDD` , " \
					" `PATHNAME` , `COVER` , `TAGMETHOD` , `ID_CD` " \
					" FROM ALBUMS ORDER BY `ADD` DESC";
	# list tracks
	elif name == 'trackslist':
		request = 	"SELECT " \
					" `TRACKORDER` , `ARTIST` , `TITLE` , `LENGTHDISPLAY` , `SCORE` ," \
					" `GENRE` , `FILENAME` , `INDEX` , `POS_START_SAMPLES` , `POS_END_SAMPLES` ," \
					" `PATHNAME` , `TYPEMEDIA` , `ID_TRACK` " \
					" FROM TRACKS WHERE ID_CD={id} ORDER BY `TRACKORDER` ";
	# search in track
	elif name == 'tracksinsearch':
		request = 	"SELECT ALBUMS.ID_CD FROM ALBUMS " \
					"INNER JOIN TRACKS " \
					"ON ALBUMS.ID_CD=TRACKS.ID_CD " \
					"WHERE TRACKS.ARTIST like '%{search}%' OR TRACKS.TITLE like '%{search}%' OR ALBUMS.NAME like '%{search}%'  " \
					"GROUP BY ALBUMS.ID_CD"
	# last ID
	if name == 'lastid':
		if MODE_SQLI == 'mssql':
			request = "SELECT IDENT_CURRENT(‘tablename’)"
		if MODE_SQLI == 'mysql':
			request = "SELECT LAST_INSERT_ID() as lastid;"
		if MODE_SQLI == 'sqlite':
			request = "SELECT last_insert_rowid();"
	# cover
	elif name == 'coverpix':
		request = "SELECT COVER FROM COVERS WHERE ID_CD={id}"
	elif name == 'thumbnailpix':
		request = "SELECT THUMBNAIL FROM COVERS WHERE ID_CD={id}"
	elif name == 'insertcover':
		request = "REPLACE INTO COVERS(ID_CD, NAME, COVER, THUMBNAIL) VALUES (?, ?, ?, ?)"
	# update Sore Album
	elif name == 'updatescorealbum':
		request = "UPDATE ALBUMS SET SCORE={score} WHERE ID_CD={id}"
	# update Sore Track
	elif name == 'updatescoretrack':
		request = "UPDATE TRACKS SET SCORE={score} WHERE ID_TRACK={id}"
	# insert playlist foobar
	elif name == 'playlistfoobar':
		request = "INSERT INTO FOOBAR (PLAYLIST, PATH, FILENAME, ALBUM, NAME, ARTIST, TITLE, `ADD` ) " \
					"VALUES (?, ?, ?, ?, ?, ?, ?,  NOW())"
	# combobox style
	elif name == 'listgenres':
		request = "SELECT ID_CD, STYLE FROM ALBUMS;"
		
	if MODE_SQLI == 'mssql':
		request = request.replace(' `', ' [').replace('` ', '] ').replace("'", '"')
	return request



class DBFuncBase(QObject):
	signalchgt = pyqtSignal(int, str)		# signal browse
	
	def __init__(self, parent=None):
		"""Init."""
		super(DBFuncBase, self).__init__(parent)
		self.parent = parent

	def arrayCardsToSql(self, operation, arraydata, tablename, columnnamekey):
		listcolumns = self.getListColumnsTable(tablename)
		if len(listcolumns) == 0:
			qDebug(tablename)
			return False
		
		numberscolumns = len(listcolumns)
		if operation == 'INSERT':
			# build query insert
			request = 'INSERT INTO ' + tablename + '('
			request += ', '.join('`{0}`'.format(w) for w in listcolumns) + ') VALUES '
			request += '(' + ', '.join( ['?'] * numberscolumns) +')' 
		elif operation == 'UPDATE':
			# build query update
			listcolumns.remove(columnnamekey)
			numberscolumns = len(listcolumns)
			request = 'UPDATE ' + tablename + ' SET '
			request += '= ?, '.join('`{0}`'.format(w) for w in listcolumns) + '= ? '
			request += ' WHERE ' + columnnamekey + ' = ? ;'
		else:
			qDebug(operation)
			return False
	
		# repeat query insert 
		if isinstance(arraydata, list):
			# multi card
			for row in arraydata:
				if not self.arrayCardToSql(operation, row, columnnamekey, request, listcolumns):
					return False
		else:
			# one card
			if not self.arrayCardToSql(operation, arraydata, columnnamekey, request, listcolumns):
				return False
		return True
	
	def arrayCardToSql(self, operation, arraydata, columnnamekey, request, listcolumns):
		# one card
		numberscolumns = len(listcolumns)
		queryoperation = QSqlQuery()
		queryoperation.prepare(request)
		for column in range(numberscolumns):
			# first column : primary key
			if listcolumns[column] == columnnamekey and operation == 'INSERT':
				queryoperation.bindValue(column, None)
			else:
				queryoperation.bindValue(column, arraydata[listcolumns[column]])
		if operation == 'UPDATE':
			# primary key for update
			queryoperation.bindValue(column + 1, arraydata[columnnamekey])
		if not queryoperation.exec_():
			qDebug(request + ' ' + queryoperation.lastError().text())
			qDebug(','.join(list(queryoperation.boundValues().values())))
			return False
		queryoperation.clear
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
		if not query.exec_():
			errorText = query.lastError().text()
			qDebug(query.lastQuery())
			qDebug(ascii(errorText))
		indexes = query.record().count()
		while query.next():
			if indexes == 1:
				arraydata.append(query.value(0))
			else:
				row = [query.value(index) for index in range(indexes)]
				arraydata.append(row)
		query.clear
		return arraydata

	def sqlToArrayDict(self, tablename, columnnamekey, columnvalue):
		"""Select to array/ line format dict data."""
		request = 'SELECT * FROM {tbl} WHERE {col}={colv};'
		request = request.format(tbl = tablename, col = columnnamekey,  colv = str(columnvalue))
		arraydata = []
		cardline = {}
		query = QSqlQuery(request)
		query.exec_(request)
		numberscolumns = query.record().count()
		while query.next():
			mycardline = deepcopy(cardline)
			for column in range(numberscolumns):
				mycardline[query.record().fieldName(column)] =	query.value(column)
			arraydata.append(mycardline)
		return arraydata

	def execSqlFile(self, sql_file, dbcnx=None):
		"""Exec script SQL file..."""
		counter = 0
		request = ''
		for line in open(sql_file, 'r'):
			request += line
			if line.endswith(';\n'):
				counter = counter + 1
				request = request.rstrip('\n')
				qDebug(request)
				query = QSqlQuery(request, dbcnx)
				if not query.exec_():
					errorText = query.lastError().text()
					qDebug(query.lastQuery())
					qDebug(errorText)
				query.clear
				request = ''

	def imageToSql(self, pathimage, idcd, minisize):
		"""Write image and thunbnail to database."""
		# just file
		#file = QFile(pathimage)
		#file.open(QIODevice.ReadOnly)
		#inByteArray = QByteArray(file.readAll())
		
		# image big
		#print(path.getsize(pathimage))
		inPixmap = QPixmap(pathimage)
		inByteArray = QByteArray()
		inBuffer = QBuffer(inByteArray)
		if not inBuffer.open(QIODevice.WriteOnly):
			return False
		inPixmap.save(inBuffer,"JPG");
		
		# image mini # Qt.FastTransformation
		inPixmap = inPixmap.scaled(minisize, minisize, Qt.IgnoreAspectRatio, Qt.SmoothTransformation) 
		inByteArraymini = QByteArray()
		inBuffer = QBuffer(inByteArraymini)
		inBuffer.open(QIODevice.WriteOnly);
		inPixmap.save(inBuffer,"JPG");
		
		# mssql
		# https://stackoverflow.com/questions/108403/solutions-for-insert-or-update-on-sql-server
		# UPDATE data or INSERT : https://en.wikipedia.org/wiki/Merge_(SQL)
		query = QSqlQuery()
		request = getrequest('insertcover')
		query.prepare(request)
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
		ReqTDC = "(SELECT `{group}` AS `{TDCName}` ,\n".format(group=group, TDCName=TDCName)
		for col_name in col_names:
			ReqTDC += "    SUM(CASE WHEN `{column}` = '{col_name}' THEN {TDCSum} ELSE 0 END) AS `{col_name}` ,\n".format(column=column, TDCSum=TDCSum, col_name=col_name)
			lstcols += " `{col_name}` ,".format(col_name=col_name)
		ReqTDC += "    SUM({TDCSum}) AS `TOTAL` FROM {tableName} GROUP BY `{group}`\n".format(tableName=tableName, TDCSum=TDCSum, group=group)
		# sum global
		if LineSum:
			ReqTDC += " UNION \nSELECT '➔TOTAL', \n"
			for col_name in col_names:
				ReqTDC += "    SUM(CASE WHEN `{column}` = '{col_name}' THEN {TDCSum} ELSE 0 END),\n".format(column=column, TDCSum=TDCSum, col_name=col_name)
			ReqTDC += "    SUM({TDCSum}) FROM {tableName}\n".format(tableName=tableName, TDCSum=TDCSum)
		# order by total is last line
		ReqTDC += ") tdc ORDER BY 1;"
		# select column
		ReqTDC = "SELECT `"+TDCName+"` ,"+lstcols+" `TOTAL` FROM \n" + ReqTDC
		# replace ` for [] sqlserver
		if MODE_SQLI == 'mssql':
			ReqTDC = ReqTDC.replace(' `', ' [').replace('` ', '] ')
		return ReqTDC

	def deleteTable(self, tableName, columnnamekey, idvalue):
		"""Delete enr table."""
		request = ('DELETE FROM ' + tableName + ' WHERE ' + columnnamekey + ' =' + str(idvalue))
		qDebug(request)
		query = QSqlQuery()	
		return query.exec_(request)


class DBCreateSqLite(QObject):
	signalchgt = pyqtSignal(int, str)		# signal browse
	
	def __init__(self, basename, parent=None):
		"""Init."""
		super(DBCreateSqLite, self).__init__(parent)
		self.parent = parent
		self.basename = basename
		if path.isfile(basename):
			remove(basename)
	
	def createObjSqlLite(self, dbsource, filerequestcreate):
		"""create SqlLite Database."""
		qDebug('Process Creation Database Sqlite ' + self.basename)
		# create sqlite database
		cnxlite = 'CREA'
		dblite = QSqlDatabase.addDatabase("QSQLITE", cnxlite)
		dblite.setDatabaseName(self.basename)
		if dblite.isValid():
			boolcon = dblite.open()
			if boolcon:	
				# create objects database
				DBFuncBase().execSqlFile(filerequestcreate, dblite)
				# copy table
				self.signalchgt.emit((1/5)*100, 'Create ALBUMS...')
				self.copytable(dbsource, dblite, 'ALBUMS')
				self.signalchgt.emit((2/5)*100, 'Create TRACKS...')
				self.copytable(dbsource, dblite, 'TRACKS')
				self.signalchgt.emit((3/5)*100, 'Create COVERS...')
				self.copytable(dbsource, dblite, 'COVERS')
				self.signalchgt.emit((4/5)*100, 'Create FOOBAR...')
				self.copytable(dbsource, dblite, 'FOOBAR')
				self.signalchgt.emit((5/5)*100, 'Operations completed')
		else:
			qDebug('no create', self.basename)
	
	def copytable(self, dbsrc, dbdes, tablename):
		listcolumns =  DBFuncBase().getListColumnsTable(tablename)
		numberscolumns = len(listcolumns)
		# build query insert
		request = 'INSERT INTO ' + tablename + '('
		request += ', '.join('`{0}`'.format(w) for w in listcolumns) + ') VALUES '
		request += '(' + ', '.join(['?'] * numberscolumns) + ')' 
		# query 
		querylite = QSqlQuery(dbdes)
		query = QSqlQuery(dbsrc)
		query.exec_("SELECT * FROM "+tablename)
		while query.next():
			querylite.prepare(request)
			for indcol in range(query.record().count()):
				querylite.bindValue(indcol, query.value(indcol))
			if not querylite.exec_():
				qDebug(tablename+10*' '+querylite.lastError().text())
				listparam = list(querylite.boundValues().values())
				for i in range(len(listparam)):
					qDebug(10*' '+ str(i) + ' ' + str(listparam[i].decode('ascii', 'ignore')))
			# Waiting problem Disk I/O error
			sleep(0.1)


class DBCcopyTable(QObject):
	
	def __init__(self, parent=None):
		"""Init."""
		super(DBCcopyTable, self).__init__(parent)
		self.parent = parent
	
	def execSqlFile(self, sql_file, dbcnx=None):
		"""Exec script SQL file..."""
		counter = 0
		request = ''
		for line in open(sql_file, 'r'):
			request += line
			if line.endswith(';\n'):
				counter = counter + 1
				request = request.rstrip('\n')
				qDebug(request)
				query = QSqlQuery(request, dbcnx)
				if not query.exec_():
					errorText = query.lastError().text()
					qDebug(query.lastQuery())
					qDebug(errorText)
				query.clear
				request = ''

	def copyCovers(self, dbdes):
		dbsrc = QSqlDatabase.addDatabase("QMYSQL")
		dbsrc.setHostName('homerstation')
		dbsrc.setDatabaseName('InventMP3')
		dbsrc.setUserName('admInventMP3')
		dbsrc.setPassword('nuDbC6spVZxtkKC8')
		dbsrc.setPort(3306)
		if dbsrc.isValid():
			dbsrc.open()
		self.copytable(dbsrc, dbdes, 'COVERS')

if __name__ == '__main__':
#//2005 db.setDatabaseName(DRIVER={SQL Server};SERVER=localhost\SQLExpress;DATABASE=secundaria;UID=sa;PWD=contraseña;WSID=.;Trusted_connection=yes)
#//2008 db.setDatabaseName("DRIVER={SQL Server Native Client 10.0};SERVER=localhost\SQLExpress;DATABASE=myDbName;UID=user;PWD=userPwd;WSID=.;Trusted_connection=yes")
#//2012 db.setDatabaseName("DRIVER={SQL Server Native Client 11.0};SERVER=localhost\SQLExpress;DATABASE=myDbName;UID=user;PWD=userPwd;WSID=.;Trusted_connection=yes")
	boolconnect, dbbase, modsql, rootDk, lstcat = connectDatabase('MP3')
	print(boolconnect, dbbase, modsql, rootDk, lstcat)
	copytable = DBCcopyTable()
	copytable.execSqlFile("E:\Download\InventMP3_old.sql", dbbase)
	#createsqllite = DBCreateSqLite(r'\\Homerstation\_pro\Projets\DBALBUMSQT5\SQL\TEXT.DB')
	#createsqllite.createObjSqlLite(dbbase, r'\\Homerstation\_pro\Projets\DBALBUMSQT5\SQL\Create_sqllite_database.sql')
