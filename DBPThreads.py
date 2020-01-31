#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import  path, chdir
from PyQt5.QtCore import QThread, pyqtSignal, qDebug
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from DBDatabase import getrequest
from DBReadJson import JsonParams

PATH_PROG = path.dirname(path.abspath(__file__))
BASE_SQLI = path.join(PATH_PROG, 'LOC', "DBALBUMS_{envt}.db")
#chdir(PATH_PROG)

class DBPThreadsListStyle(QThread):
	finished = pyqtSignal(list)
	
	def __init__(self, parent, envt):
		super(DBPThreadsListStyle, self).__init__(parent)
		self.envt = envt
		self.dbthread = None
	
	def __del__(self):
		self.wait()
	
	def run(self):
		# build list styles albums
		boolcon, self.dbthread = self.connectDatabase(self.envt, 'dbthread')
		request = getrequest('listgenres')
		self.listgenres = self.sqlToArray(request)
		self.dbthread.close()
		liststyles = []
		for row in self.listgenres:
			id_cd = row[0]
			genres = row[1].replace(';', '/')
			genres = genres.replace(',', '/')
			genres = genres.replace('"', '')
			genres = genres.replace('-', '')
			genres = genres.replace('  ', ' ')
			for genre in genres.split('/'):
				genre = genre.strip()
				genre = genre.title()
				if genre == '':
					genre = 'Unknown'
				liststyles.append([id_cd, genre])
		liststyles.sort(reverse=False)
		self.finished.emit(liststyles)
		self.quit()

	def connectDatabase(self, envt, connexionName):
		"""Connect base MySQL/Sqlite."""
		FILE__INI = path.join(PATH_PROG, 'DBAlbums.json')
		Json_params = JsonParams(FILE__INI)
		group_envt = Json_params.getMember(envt)
		MODE_SQLI = group_envt['typb']
		boolcon = False
		if MODE_SQLI == 'sqlite':
			db = QSqlDatabase.addDatabase("QSQLITE", connexionName)
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
				db = QSqlDatabase.addDatabase("QMYSQL", connexionName)
				db.setHostName(BASE_SEV)
				db.setDatabaseName(BASE_NAM)
				db.setUserName(BASE_USR)
				db.setPassword(BASE_PAS)
				db.setPort(BASE_PRT)
			elif MODE_SQLI == 'mssql':
				db = QSqlDatabase.addDatabase("QODBC3", connexionName)
				driver = "DRIVER={SQL Server Native Client 11.0};Server=" + BASE_SEV + ";Database=" + BASE_NAM
				driver += ";Uid=" + BASE_USR + ";Port=" + str(BASE_PRT) + ";Pwd=" + BASE_PAS + ";Trusted_connection=yes"
				#print(driver)
				db.setDatabaseName(driver);
		if db.isValid():
			boolcon = db.open()
		else:
			qDebug(envt+' problem for open database : '+db.lastError().text())
		return boolcon, db

	def sqlToArray(self, request):
		"""Select to array data."""
		arraydata = []
		query = QSqlQuery(self.dbthread)
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

# test Qthread
#from sys import argv,  exit
#from PyQt5.QtWidgets import QApplication, QWidget
#
#class FormTest(QWidget):
#	def __init__(self):
#		super(FormTest, self).__init__()
#		self.obj = DBPThreadsListStyle(self, 'LOSSLESS_TEST')
#		self.obj.finished.connect(self.listControl)
#		self.obj.start()
#	
#	def listControl(self, listgenres):
#		print(len(listgenres), listgenres)
#
#
#if __name__ == '__main__':
#	app = QApplication(argv)
#	form = FormTest()
#	exit(app.exec_())
