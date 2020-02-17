#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import  path, remove
from copy import deepcopy
from time import sleep
from codecs import open
from PyQt5.QtCore import Qt, qDebug, QObject, QByteArray, QIODevice, QBuffer, pyqtSignal
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QPixmap
from DBReadJson import JsonParams


class LibDatabase(QObject):

	def __init__(self, parent):
		"""Init params class connexion."""
		super(LibDatabase, self).__init__(parent)
		self.parent = parent
		self.dbtype = None	# database mysql/mssql/sqlite
		self.dbserv = None	# cnx: server name
		self.dbuser = None	# cnx: user login
		self.dbpass = None	# cnx: user password
		self.dbbase = None	# cnx: database name
		self.dbport = None	# cnx: port instance
		self.dbsqli = None	# database file name for sqlite
		self.qtname = None	# connexion QT name
		self.qtdbdb = None  # ID QT5 cnx
		self.boolcn = False	# connexion database succes TRUE/FLASE

	def openDatabase(self, dbtype, dbserv, dbuser, dbpass, dbbase, dbport, dbsqli , qtname):
		"""Connect database."""
		self.dbtype = dbtype
		self.dbserv = dbserv
		self.dbuser = dbuser
		self.dbpass = dbpass
		self.dbbase = dbbase
		self.dbport = dbport
		self.dbsqli = dbsqli
		self.qtname = qtname
		if self.dbtype == 'sqlite':
			self.qtdbdb = QSqlDatabase.addDatabase("QSQLITE", self.qtname)
			self.qtdbdb.setDatabaseName(self.dbsqli)
		elif self.dbtype == 'mysql':
			self.qtdbdb = QSqlDatabase.addDatabase("QMYSQL", self.qtname)
			self.qtdbdb.setHostName(self.dbserv)
			self.qtdbdb.setDatabaseName(self.dbbase)
			self.qtdbdb.setUserName(self.dbuser)
			self.qtdbdb.setPassword(self.dbpass)
			self.qtdbdb.setPort(self.dbport)			
		elif self.dbtype == 'mssql':
			self.qtdbdb = QSqlDatabase.addDatabase("QODBC3", self.qtname)
			driver = "DRIVER={SQL Server Native Client 11.0};Server=" + self.dbserv + ";Database=" + self.dbbase
			driver += ";Uid=" + self.dbuser + ";Port=" + str(self.dbport) + ";Pwd=" + self.dbpass + ";Trusted_connection=yes"
			self.qtdbdb.setDatabaseName(driver)		
		# validation
		if self.qtdbdb.isValid():
			self.boolcn = self.qtdbdb.open()
		else:
			qDebug('Problem for open database : ' + self.qtdbdb.lastError().text())

	def closeDatabase(self):
		self.qtdbdb.close()
		QSqlDatabase.removeDatabase(self.qtname)

	def buildRequestTCD(self, group, column, tableName, TDCName='TDC', TDCSum=1, LineSum=True):
		"""build request Pivot table compatible sqlite, mysql, SQLserver."""
		# Collect list columns
		req = "SELECT `{column}` FROM {tableName} GROUP BY `{column}` ;".format(tableName=tableName, column=column)
		req = self.translateRequest(req)
		col_names = self.sqlToArray(req)
		# sum/collections
		lstcols = ''
		ReqTDC = "(SELECT `{group}` AS `{TDCName}` , 0 as `lineOder` , \n".format(group=group, TDCName=TDCName)
		for col_name in col_names:
			ReqTDC += "    SUM(CASE WHEN `{column}` = '{col_name}' THEN {TDCSum} ELSE 0 END) AS `{col_name}` ,\n".format(column=column, TDCSum=TDCSum, col_name=col_name)
			lstcols += " `{col_name}` ,".format(col_name=col_name)
		ReqTDC += "    SUM({TDCSum}) AS `TOTAL` FROM {tableName} GROUP BY `{group}` \n".format(tableName=tableName, TDCSum=TDCSum, group=group)
		# sum global
		if LineSum:
			ReqTDC += " UNION \nSELECT 'TOTAL', 1 as `lineOder` , \n"
			for col_name in col_names:
				ReqTDC += "    SUM(CASE WHEN `{column}` = '{col_name}' THEN {TDCSum} ELSE 0 END),\n".format(column=column, TDCSum=TDCSum, col_name=col_name)
			ReqTDC += "    SUM({TDCSum}) FROM {tableName}\n".format(tableName=tableName, TDCSum=TDCSum)
		# order by total is last line
		ReqTDC += ") tdc ORDER BY `lineOder` , 1;"
		# select column
		ReqTDC = "SELECT `"+TDCName+"` ,"+lstcols+" `TOTAL` FROM \n" + ReqTDC
		ReqTDC = self.translateRequest(ReqTDC)
		return ReqTDC

	def buildRequest(self, operation, tablename, columnnamekey=None):
		# build list columns table
		listcolumns = self.getListColumnsTable(tablename)
		if columnnamekey is not None:
			# remove primary key
			listcolumns.remove(columnnamekey)
		if len(listcolumns) == 0:
			qDebug('problem read columns table :' + tablename)
			return False
		else:
			numberscolumns = len(listcolumns)
			if operation == 'INSERT':
				# build query insert
				request = 'INSERT INTO ' + tablename + '( '
				request += ', '.join('`{0}` '.format(w) for w in listcolumns) + ') VALUES '
				request += '(' + ', '.join( ['?'] * numberscolumns) +')' 
			elif operation == 'UPDATE':
				# build query update
				request = 'UPDATE ' + tablename + ' SET '
				request += '= ?, '.join('`{0}` '.format(w) for w in listcolumns) + '= ? '
				request += ' WHERE ' + columnnamekey + ' = ? ;'
		return self.translateRequest(request), listcolumns

	def translateRequest(self, requestname):
		"""Corection path windows-linux."""
		if self.dbtype == 'mssql':
			requestname = requestname.replace(' `', ' [').replace('` ', '] ')#.replace("`,", '],')
		return requestname

	def arrayCardsToSql(self, operation, arraydata, tablename, columnnamekey):
		request, listcolumns = self.buildRequest(operation, tablename, columnnamekey)
		# repeat query insert 
		if isinstance(arraydata, list):
			# multi cards
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
		queryoperation = QSqlQuery(self.qtdbdb)
		queryoperation.prepare(request)
		for column in range(numberscolumns):
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
		if self.MODE_SQLI == 'mssql':
			request = 'SELECT TOP 0 * FROM ' + tablename 
		else:
			request = 'SELECT * FROM ' + tablename + ' LIMIT 0'
		query = QSqlQuery(self.qtdbdb)
		query.exec_(request)
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
		query = QSqlQuery(self.qtdbdb)
		if not query.exec_(request):
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
		query = QSqlQuery(self.qtdbdb)
		query.exec_(request)
		numberscolumns = query.record().count()
		while query.next():
			mycardline = deepcopy(cardline)
			for column in range(numberscolumns):
				mycardline[query.record().fieldName(column)] =	query.value(column)
			arraydata.append(mycardline)
		return arraydata

	def deleteLineTable(self, tableName, columnnamekey, idvalue):
		"""Delete enr table."""
		request = ('DELETE FROM ' + tableName + ' WHERE ' + columnnamekey + ' =' + str(idvalue))
		qDebug(request)
		query = QSqlQuery(self.qtdbdb)	
		return query.exec_(request)	

	def execSqlFile(self, sql_file, dbcnx=None):
		"""Exec script SQL file..."""
		if dbcnx is None:
			dbcnx = self.qtdbdb
		counter = 0
		request = ''
		for line in open(sql_file, 'r'):
			request += line.rstrip('\n').lstrip('\t')
			if line.endswith(';\n'):
				counter = counter + 1
				qDebug(request)
				query = QSqlQuery(request, dbcnx)
				if not query.exec_():
					errorText = query.lastError().text()
					qDebug(query.lastQuery())
					qDebug(errorText)
				query.clear
				request = ''

	def copytable(self, dbsrc, dbdes, tablename):
		listcolumns =  self.parent.CnxConnect.getListColumnsTable(tablename)
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

	def imageToSql(self, pathimage):
		"""Prepare buffer image for sql."""
		# just file
		#file = QFile(pathimage)
		#file.open(QIODevice.ReadOnly)
		#inByteArray = QByteArray(file.readAll())
		# prepare picture
		inPixmap = QPixmap(pathimage)
		inByteArray = QByteArray()
		inBuffer = QBuffer(inByteArray)
		if not inBuffer.open(QIODevice.WriteOnly):
			return False
		inPixmap.save(inBuffer,"JPG");
		return inByteArray