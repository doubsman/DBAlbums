#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal


class DBPThreadsListStyle(QThread):
	finished = pyqtSignal(list)
	
	def __init__(self, parent, envt, jsondataini, baseqli):
		super(DBPThreadsListStyle, self).__init__()
		self.parent = parent
		self.envt = envt
		self.Json_params = jsondataini
		self.baseqli = baseqli
		self.CnxDat = None
	
	def __del__(self):
		self.wait()
	
	def run(self):
		# build list styles albums
		request = self.parent.CnxConnect.getrequest('listgenres')
		self.listgenres = self.parent.CnxConnect.sqlToArray(request)
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

