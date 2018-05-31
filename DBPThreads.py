#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv,  exit
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget
from DBDatabase import DBFuncBase, connectDatabase, getrequest

class DBPThreadsListStyle(QThread):
	finished = pyqtSignal(list)
	
	def __init__(self, parent):
		super(DBPThreadsListStyle, self).__init__(parent)

	def __del__(self):
		self.wait()
	
	def run(self):
		# your logic here
		request = getrequest('listgenres')
		listgenres = DBFuncBase().sqlToArray(request)
		liststyles = []
		for row in listgenres:
			id_cd = row[0]
			genres = row[1].replace(';', '/')
			genres = genres.replace(',', '/')
			genres = genres.replace('"', '')
			genres = genres.replace('-', '')
			genres = genres.replace('  ', ' ')
			for genre in genres.split('/'):
				genre = genre.strip()
				genre = genre.title()
				liststyles.append([id_cd, genre])
		liststyles.sort(reverse=False)
		self.finished.emit(liststyles)
		self.quit()


# test Qthread
class FormTest(QWidget):
	def __init__(self):
		super().__init__()
		boolconnect, self.dbbase, self.modsql, self.rootDk = connectDatabase('LOSSLESS_TEST')
		self.obj = DBPThreadsListStyle(self)
		self.obj.finished.connect(self.listprint)
		self.obj.start()
	
	def listprint(self, listgenres):
		print('kk', len(listgenres), listgenres)


if __name__ == '__main__':
	app = QApplication(argv)
	form = FormTest()
	exit(app.exec_())
