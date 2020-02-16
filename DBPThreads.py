#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
from DBDatabase import ConnectDatabase


class DBPThreadsListStyle(QThread):
	finished = pyqtSignal(list)
	
	def __init__(self, parent, envt, fileini, baseqli):
		super(DBPThreadsListStyle, self).__init__(parent)
		self.parent = parent
		self.envt = envt
		self.fileini = fileini
		self.baseqli = baseqli
		self.CnxDat = None
	
	def __del__(self):
		self.wait()
	
	def run(self):
		# build list styles albums
		self.CnxDat = ConnectDatabase(None, self.envt, self.fileini, self.baseqli, 'dbthread')
		request = self.CnxDat.getrequest('listgenres')
		self.listgenres = self.CnxDat.sqlToArray(request)
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
		self.CnxDat.closeDatabase()
		self.quit()

