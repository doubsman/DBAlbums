#! /usr/bin/python
# coding: utf-8
from sys import argv
from os import path
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableView, QPushButton,
							QMenu, QLineEdit, QStyle, QAbstractItemView, QCompleter)
from DBDatabase import ConnectDatabase
from DBFunction import displayCounters, centerWidget, openFolder
from DBGuiTheme import ThemeColors
from DBModelAbs import ModelTableAlbumsABS	# model tables
from DBArtworks import CoverViewGui			# viewer image b64
from DBFileJson import JsonParams


class DBAlbumsQT5Mini(QMainWindow):
	"""Init mini Gui constants."""
		
	def __init__(self, parent=None):
		super(DBAlbumsQT5Mini, self).__init__(parent)
		self.PATH_PROG = path.dirname(path.abspath(__file__))
		self.BASE_SQLI = path.join(self.PATH_PROG, 'LOC', "DBALBUMS_{envt}.db")
		self.RESS_ICOS = path.join(self.PATH_PROG, 'IMG' , 'ICO')
		self.VERS_PROG = '1.01'
		self.TITL_PROG = "♫ DBAlbums mini v{v} (2020)".format(v=VERS_PROG)
		self.FILE__INI = path.join(PATH_PROG, 'DBAlbums.json')
		Json_params = JsonParams(self.FILE__INI)
		group_dbalbums = Json_params.getMember('dbalbums')
		self.WINS_ICO = path.join(self.PATH_PROG, 'IMG', group_dbalbums['wins_icone'])
		self.PICM_NCO = path.join(self.PATH_PROG, 'IMG', group_dbalbums['pict_blank'])
		self.THEM_COL = group_dbalbums['name_theme']
		self.ENVT_DEF = group_dbalbums['envt_deflt']
		self.setWindowIcon(QIcon(self.WINS_ICO))
		self.setWindowTitle(self.TITL_PROG + ' : [' + self.ENVT_DEF + ']')
		self.h_main = 400
		self.resize(1248, self.h_main)
		centerWidget(self)
		
		self.menua = QMenu()
		self.action_OPF = self.menua.addAction(self.style().standardIcon(QStyle.SP_DialogOpenButton),
							"Open Folder...", self.getFolder)
		
		self.textsearch = QLineEdit()
		self.textsearch.setFixedSize(170,22)
		self.statusBar().addPermanentWidget(self.textsearch)
		self.textsearch.textChanged.connect(self.onFiltersChanged)

		self.btn_style = QPushButton()
		self.btn_style.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
		self.btn_style.setStyleSheet("border: none;")
		self.btn_style.clicked.connect(lambda: [self.curthe.nextTheme(), self.applyTheme()])
		self.statusBar().addPermanentWidget(self.btn_style)
		
		self.CnxConnect = ConnectDatabase(self, self.envits, self.FILE__INI, self.BASE_SQLI)
		boolconnect = self.CnxConnect.boolcon
		self.dbbase = self.CnxConnect.qtdbdb
		self.modsql = self.CnxConnect.MODE_SQLI
		self.rootDk = self.CnxConnect.BASE_RAC
		self.lstcat = self.Json_params.buildListcategory(self.envits)

		autoList = self.CnxConnect.sqlToArray(self.CnxConnect.getrequest('autocompletion'))
		self.com_autcom = QCompleter(autoList, self.textsearch)
		self.com_autcom.setCaseSensitivity(Qt.CaseInsensitive)
		self.textsearch.setCompleter(self.com_autcom)
		
		self.mytable = QTableView(self)
		self.mytable.setAlternatingRowColors(True)
		self.mytable.setSortingEnabled(True)
		self.mytable.setSelectionBehavior(QTableView.SelectRows)
		self.mytable.setSelectionMode(QAbstractItemView.SingleSelection)
		self.mytable.doubleClicked.connect(self.onSelect)
		self.mytable.setContextMenuPolicy(Qt.CustomContextMenu)
		self.mytable.customContextMenuRequested.connect(self.popUpTreeAlbums)
		
		self.curthe = ThemeColors(self.THEM_COL)
		self.applyTheme()
			
		req = self.CnxConnect.getrequest('albumslist', self.modsql)
		self.model = ModelTableAlbumsABS(self, req)
		self.model.SortFilterProxy.layoutChanged.connect(self.listChanged)
		self.model.SortFilterProxy.sort(-1)
		self.mytable.setModel(self.model.SortFilterProxy)
		
		# width columns
		for ind in range(len(self.model.A_C_WIDTH)):
			self.mytable.setColumnWidth(ind, self.model.A_C_WIDTH[ind])
		# height rows
		self.mytable.verticalHeader().setDefaultSectionSize(self.model.C_HEIGHT)
		
		self.displayTitle()
		self.setCentralWidget(self.mytable)
	
	def onFiltersChanged(self):
		self.model.SortFilterProxy.updateFilters(self.textsearch.text())
		self.displayTitle()
		
	def onSelect(self):
		indexes = self.mytable.selectedIndexes()
		indexes = self.model.SortFilterProxy.mapToSource(indexes[0])
		self.currow = indexes.row()
		albumname = self.model.getData(self.currow, 'NAME')
		idcd = self.model.getData(self.currow, 'ID_CD')
		coveral = self.CnxConnect.sqlToPixmap(idcd, self.PICM_NCO)
		CoverViewGui(coveral, albumname, self.h_main, self.h_main)
	
	def popUpTreeAlbums(self, position):
		self.menua.exec_(self.mytable.viewport().mapToGlobal(position))
	
	def getFolder(self):
		"""Open album folder."""
		indexes = self.mytable.selectedIndexes()
		indexes = self.model.SortFilterProxy.mapToSource(indexes[0])
		self.currow = indexes.row()
		albumpath = self.model.getData(self.currow, 'PATHNAME')
		openFolder(albumpath)

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
		
	def applyTheme(self):
		"""Apply color Theme to main Gui."""
		# main
		mainstyle = 'QMainWindow{{background-color: {col1};border: 1px solid black;}}' \
					'QLineEdit{{background-color: {col2};}}' \
					'QStatusBar{{background-color: {col1};border: 1px solid black;}}' \
					'QScrollBar:vertical{{width: 14px;}}' \
					'QScrollBar:horizontal{{height: 14px;}}' \
					'QTableView{{alternate-background-color: {col3};background-color: {col4};}}' \
					'QTableView::item:selected{{ background-color:{col5}; color:white;}}'
		mainstyle = mainstyle.format(col1 = self.curthe.listcolors[0], 
									col2 = self.curthe.listcolors[1], 
									col3 = self.curthe.listcolors[2], 
									col4 = self.curthe.listcolors[3],
									col5 = self.curthe.listcolors[4])
		self.setStyleSheet(mainstyle)
		# treeview
		gridstyle = 'QHeaderView::section{{background-color: {col2};border-radius:1px;margin: 1px;padding: 2px;}}'
		gridstyle = gridstyle.format(col2 = self.curthe.listcolors[1])
		self.mytable.setStyleSheet(gridstyle)


if __name__ == '__main__':
	app = QApplication(argv)
	DB = DBAlbumsQT5Mini()
	DB.show()
	rc = app.exec_()
	exit(rc)
