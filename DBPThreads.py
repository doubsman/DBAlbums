#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv,  exit
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget
from DBDatabase import DBFuncBase, connectDatabase, getrequest

class DBPThreadsListStyle(QThread):
	finished = pyqtSignal(list)
	
	def __init__(self, parent, listgenres):
		super(DBPThreadsListStyle, self).__init__(parent)
		self.listgenres = listgenres
	
	def __del__(self):
		self.wait()
	
	def run(self):
		# build list styles albums
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


# test Qthread
class FormTest(QWidget):
	def __init__(self):
		super().__init__()
		self.lstcat = None
		boolconnect, self.dbbase, self.modsql, self.rootDk, self.lstcat = connectDatabase('LOSSLESS_TEST')
		request = getrequest('listgenres')
		listgenres = DBFuncBase().sqlToArray(request)
		#print(listgenres)
		self.obj = DBPThreadsListStyle(self, listgenres)
		self.obj.finished.connect(self.listprint)
		self.obj.start()
	
	def listprint(self, listgenres):
		print('kk', len(listgenres), listgenres)


if __name__ == '__main__':
	app = QApplication(argv)
	form = FormTest()
	exit(app.exec_())
