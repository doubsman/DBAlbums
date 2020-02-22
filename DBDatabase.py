#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import  path, remove
from codecs import open
from PyQt5.QtCore import Qt, qDebug, QByteArray, QIODevice, QBuffer, pyqtSignal
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtGui import QPixmap
from LIBDatabase import LibDatabase


class ConnectDatabase(LibDatabase):
	signalchgt = pyqtSignal(int, str)		# signal browse

	def __init__(self, parent, envt, basesqli, jsondataini, connexionName): # = 'qt_sql_default_connection'):
		"""Init invent, build list albums exists in database."""
		super(ConnectDatabase, self).__init__(parent)
		self.parent = parent
		self.envt = envt					# current environnement
		self.basesqli = basesqli			# name base sqllite
		self.buildbase = False				# build objets in new database
		self.connexionName = connexionName	# QT name connection
		self.Json_params = jsondataini		# params Json file ini 

		self.group_envt = self.Json_params.getMember(envt)
		self.MODE_SQLI = self.group_envt['typb']
		self.BASE_RAC = r'' + self.group_envt['raci']
		self.RACI_DOU = self.group_envt['cate']
		self.dbcrea = self.Json_params.getMember('scripts')	# scripts creation database
		# open Database
		if self.MODE_SQLI == 'sqlite':
			basename = self.basesqli.format(envt = self.envt)
			# file exist ?
			self.buildbase = path.exists(basename)
			self.openDatabase(self.MODE_SQLI, '', '', '', '', '', basename , connexionName)
		else:
			BASE_SEV = self.group_envt['serv']
			BASE_USR = self.group_envt['user']
			BASE_PAS = self.group_envt['pass']
			BASE_NAM = self.group_envt['base']
			BASE_PRT = self.group_envt['port']
			self.openDatabase(self.MODE_SQLI, BASE_SEV, BASE_USR, BASE_PAS, BASE_NAM, BASE_PRT, self.basesqli , connexionName)
		# Create Objects in database
		self.boolcon = self.boolcn
		self.db = self.qtdbdb
		self.createObjetsDatabase(self.MODE_SQLI, self.buildbase, self.qtdbdb)

	def createDBAlbumsSqlLite(self, basesqli):
		"""create SqlLite Database."""
		qDebug('Process Creation Database Sqlite ' + basesqli)
		if path.isfile(basesqli):
			remove(basesqli)
		qtdblite = self.createDatabaseSqlLite(basesqli, 'DBCREA')
		# create objects database
		self.createObjetsDatabase('sqlite', True, qtdblite)
		# copy table
		listtable =  ['ALBUMS', 'TRACKS', 'COVERS', 'FOOBAR']
		counter = 1
		for tablename in listtable:
			self.signalchgt.emit((counter/len(listtable))*100, 'Copy datas table ' + tablename)
			self.copyDatasTable(tablename, self.qtdbdb, qtdblite)
			counter += 1 
		self.signalchgt.emit(100, 'Operations completed')

	def createObjetsDatabase(self, modesql, boolbuild, qtdblite):
		"""Create Objects in new database."""
		self.PATH_PROG = path.dirname(path.abspath(__file__))
		self.dbcrea = path.join(self.PATH_PROG, 'SQL', self.dbcrea['create_' + modesql])
		if self.boolcon:
			if modesql == 'sqlite':
				if not(boolbuild):
					# build database tables/view
					self.execSqlFile(self.dbcrea)
			else:
				# table album exist ?
				request = self.getrequest('tableexist')
				boolbuild = (len(self.sqlToArray(request, qtdblite)) > 0)
				if not(boolbuild):
					# build database tables/view
					self.execSqlFile(self.dbcrea)
		if boolbuild is None:
			self.buildbase = False

	def getrequest(self, name):
		"""Store requests."""
		# autocompletion VW_DBCOMPLETION
		if name == 'autocompletion':
			if self.MODE_SQLI == 'mssql':
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
			if self.MODE_SQLI == 'mssql':
				request = "SELECT IDENT_CURRENT('ALBUMS')"
			if self.MODE_SQLI == 'mysql':
				request = "SELECT LAST_INSERT_ID() as lastid;"
			if self.MODE_SQLI == 'sqlite':
				request = "SELECT last_insert_rowid();"
		# cover
		elif name == 'coverpix':
			request = "SELECT COVER FROM COVERS WHERE ID_CD={id}"
		elif name == 'thumbnailpix':
			request = "SELECT THUMBNAIL FROM COVERS WHERE ID_CD={id}"
		elif name == 'insertcover':
			if self.MODE_SQLI == 'mssql':
				request = "INSERT INTO COVERS(ID_CD, NAME, COVER, THUMBNAIL) VALUES (?, ?, ?, ?)"
			else:
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
		# table exist
		elif name == 'tableexist':
			if self.MODE_SQLI == 'mysql':
				request = "'SELECT * FROM information_schema.tables WHERE table_schema = 'DBALUMS' AND table_name = 'ALBUMS' LIMIT 1;"
			if self.MODE_SQLI == 'mssql':
				request = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND  TABLE_NAME = 'ALBUMS';"
		# compatibilité mutli-base	
		return self.translateRequest(request)

	def imagesToSql(self, pathimage, idcd, minisize):
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
		query = QSqlQuery(self.qtdbdb)
		request = self.getrequest('insertcover')
		query.prepare(request)
		query.bindValue(0, idcd)
		query.bindValue(1, pathimage)
		query.bindValue(2, inByteArray)
		query.bindValue(3, inByteArraymini)
		if not query.exec_():
			qDebug(10*' '+":index "+ascii(query.lastError().text()))
			return False
		return True

	def sqlToPixmap(self, idcd, blankcover, typecover = 'coverpix'):
		"""Read database image, return Blank Pixmap else."""
		request = (self.getrequest(typecover)).format(id=idcd)
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
		request = (self.getrequest(typecover)).format(id=idcd)
		cover = self.sqlToArray(request)[0]
		savefile = open(savepathfile, "wb")
		savefile.write(cover[0])
		savefile.close()

