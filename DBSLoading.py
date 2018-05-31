#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, chdir
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtCore import Qt, pyqtSlot, QSettings, QDateTime
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtWidgets import QWidget
from DBDatabase import getrequest, buildTabFromRequest, buildReqTCD
from DBFunction import centerWidget
from Ui_DBLOADING import Ui_LoadingWindow


class DBloadingGui(QWidget, Ui_LoadingWindow):
	PATH_PROG = path.dirname(path.abspath(__file__))
	RESS_LOGO = path.join(PATH_PROG, 'IMG')
	chdir(PATH_PROG)
	FILE__INI = 'DBAlbums.ini'
	configini = QSettings(FILE__INI, QSettings.IniFormat)
	configini.beginGroup('dbalbums')
	FONT_MAI = configini.value('font00_ttx')
	configini.endGroup()	
	
	def __init__(self, modsql, title, parent):
		super(DBloadingGui, self).__init__(parent)
		self.setupUi(self)
		self.parent = parent
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags(Qt.SplashScreen)
		centerWidget(self)
		# font
		font = QFont()
		font.setFamily(self.FONT_MAI)
		font.setFixedPitch(True)
		font.setPointSize(14)
		self.lab_text.setFont(font)
		self.tabWidget.currentChanged.connect(self.chgtLogo)
		# logo gif
		self.numlogo = 1
		self.movielogo = QMovie(path.join(self.RESS_LOGO,"logo1.gif"))
		self.lab_logo.setMovie(self.movielogo)
		self.movielogo.start()
		# tab1
		req = buildReqTCD("Category", "Family", "DBALBUMS", "ALBUM", "1", True, modsql)
		self.buildTab(req, self.tableWid1)
		# tab2
		req = buildReqTCD("Category", "Family", "DBALBUMS", "SIZE (GO)", "ROUND( `Size` /1024,1)", True, modsql)
		self.buildTab(req, self.tableWid2)
		# tab3
		req = buildReqTCD("Year", "Category", "DBALBUMS", "YEAR", "1", True, modsql)
		self.buildTab(req, self.tableWid3)
		# message
		basedate = buildTabFromRequest(getrequest('datedatabase', modsql))
		if len(basedate) == 0:
			txt_message = modsql + " Base \nlast modified :\nnever"
		elif isinstance(basedate[0], QDateTime):
			txt_message = modsql + " Base \nlast modified :\n"+basedate[0].toString('dd/MM/yyyy hh:mm:ss')	
		else:
			txt_message = modsql + " Base \nlast modified :\n"+basedate[0].replace('T',' ')
		self.lab_text.setText(title+"\nConnected "+txt_message)
		# quit
		self.btn_quit.clicked.connect(lambda: self.hide())
		# theme
		self.applyTheme()

	@pyqtSlot()
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape or event.key() == Qt.Key_F1:
			self.hide()

	def buildTab(self,  req, tab):
		model = QSqlQueryModel(self)
		model.setQuery(req)
		tab.setModel(model)
		tab.resizeColumnsToContents()
		tab.verticalHeader().setVisible(False)
		tab.horizontalHeader().setStretchLastSection(True)
		tab.verticalHeader().setDefaultSectionSize(self.parent.C_HEIGHT)
	
	def chgtLogo(self):
		self.movielogo.stop()
		self.numlogo += 1
		self.numlogo = self.numlogo % 3
		logo = path.join(self.RESS_LOGO, "logo" +str(self.numlogo) + ".gif")
		self.movielogo = QMovie(logo)
		self.lab_logo.setMovie(self.movielogo)
		self.movielogo.start()		

	def applyTheme(self):
		"""Apply color Theme to main Gui."""
		# main
		mainstyle = 'QWidget{{background-color: {col2};}}' \
					'QScrollBar:vertical{{width: 14px;}}' \
					'QScrollBar:horizontal{{height: 14px;}}'
		mainstyle = mainstyle.format(col2 = self.parent.curthe.listcolors[1])
		self.setStyleSheet(mainstyle)
		gridstyle = 'alternate-background-color: {col3};background-color: {col4};'
		gridstyle = gridstyle.format(col3 = self.parent.curthe.listcolors[2], 
									col4 = self.parent.curthe.listcolors[3])
		self.tableWid1.setStyleSheet(gridstyle)
		self.tableWid2.setStyleSheet(gridstyle)
		self.tableWid3.setStyleSheet(gridstyle)
