#! /usr/bin/python
# coding: utf-8
from sys import argv
from os import path, chdir
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QLineEdit
from DBDatabase import connectDatabase, getrequest, extractCoverb64
from DBFunction import displayCounters, centerWidget
from DBModelAbs import ModelTableAlbumsABS		# model tables
from DBArtworks import CoverViewGui				# viewer image b64 and hdd

PATH_PROG = path.dirname(path.abspath(__file__))
chdir(PATH_PROG)
VERS_PROG = '1.00'
TITL_PROG = "♫ DBAlbums mini v{v} (2017)".format(v=VERS_PROG)

FILE__INI = 'DBAlbums.ini'
configini = QSettings(FILE__INI, QSettings.IniFormat)
configini.beginGroup('dbalbums')
WINS_ICO = path.join(PATH_PROG, 'IMG', configini.value('wins_icone'))
PICM_NCO = path.join(PATH_PROG, 'IMG', configini.value('pict_blank'))
ENVT_DEF = configini.value('envt_deflt')
configini.endGroup()


class DBAlbumsQT5Mini(QMainWindow):
	"""Exemple model ABSTRACT."""
	def __init__(self, parent=None):
		super(DBAlbumsQT5Mini, self).__init__(parent)
		self.setWindowIcon(QIcon(WINS_ICO))
		self.setWindowTitle(TITL_PROG + ' : [' + ENVT_DEF + ']')
		self.h_main = 400
		self.resize(self.h_main + 300, self.h_main)
		centerWidget(self)
		
		self.setStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid black;}' \
							'QTableView{alternate-background-color: lightgray;background-color: silver;}')
		
		self.textsearch = QLineEdit()
		self.textsearch.setFixedSize(170,22)
		self.statusBar().addPermanentWidget(self.textsearch)
		self.textsearch.textChanged.connect(self.onFiltersChanged)
		
		boolconnect, self.dbbase, self.modsql, self.rootDk = connectDatabase(ENVT_DEF)
		self.mytable = QTableView(self)
		self.mytable.setAlternatingRowColors(True)
		self.mytable.setSortingEnabled(True)
		self.mytable.setSelectionBehavior(QTableView.SelectRows)
		self.mytable.doubleClicked.connect(self.onSelect)
			
		# abstract model
		req = getrequest('albumslist', self.modsql)
		self.model = ModelTableAlbumsABS(self, req)
		self.model.SortFilterProxy.layoutChanged.connect(self.listChanged)
		self.model.SortFilterProxy.sort(-1)
		self.mytable.setModel(self.model.SortFilterProxy)
		
		# width columns
		for i in range(len(self.model.A_C_WIDTH)):
			self.mytable.setColumnWidth(i, self.model.A_C_WIDTH[i])
		# height rows
		self.mytable.verticalHeader().setDefaultSectionSize(self.model.C_HEIGHT)
		
		# status bar
		self.displayTitle()
		
		self.setCentralWidget(self.mytable)
	
	def onFiltersChanged(self):
		self.model.SortFilterProxy.updateFilters(self.textsearch.text())
		self.displayTitle()
		
	def onSelect(self):
		indexes = self.mytable.selectedIndexes()
		indexes = self.model.SortFilterProxy.mapToSource(indexes[0])
		self.currow = indexes.row()
		albumname = self.model.getData(self.currow, 'Name')
		curMd5 = self.model.getData(self.currow, 'MD5')
		coveral = extractCoverb64(curMd5, PICM_NCO)
		CoverViewGui(coveral, albumname, self.h_main, self.h_main)

	def listChanged(self):
		pass

	def displayTitle(self):
		if int(((self.model.SortFilterProxy.cpt_len/60/60)/24)*10)/10 < 1:
			# seoncd -> Hours
			txt_len = str(int(((self.model.SortFilterProxy.cpt_len/60/60))*10)/10) + ' Hours'
		else:
			# seoncd -> Days
			txt_len = str(int(((self.model.SortFilterProxy.cpt_len/60/60)/24)*10)/10) + ' Days'
		if int(self.model.SortFilterProxy.cpt_siz/1024) == 0:
			txt_siz =  str(self.model.SortFilterProxy.cpt_siz) + ' Mo'
		else:
			txt_siz = str(int(self.model.SortFilterProxy.cpt_siz/1024)) + ' Go'
		txt_sch = (self.textsearch.text() if len(self.textsearch.text()) > 0 else 'all')
		message = "Search Result \"{sch}\" :  {alb} | {trk} | {cds} | {siz} | {dur}"
		message = message.format(alb=displayCounters(self.model.SortFilterProxy.rowCount(), 'Album'),
								cds=displayCounters(self.model.SortFilterProxy.cpt_cds, 'CD'),
								trk=displayCounters(self.model.SortFilterProxy.cpt_trk, 'Track'),
								siz=txt_siz,
								dur=txt_len,
								sch=txt_sch)
		self.statusBar().showMessage(message) # setsetWindowTitle(message)


if __name__ == '__main__':
	app = QApplication(argv)
	DB = DBAlbumsQT5Mini()
	DB.show()
	rc = app.exec_()
	exit(rc)
