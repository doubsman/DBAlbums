#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from PyQt5.QtGui import QFont, QMovie, QIcon
from PyQt5.QtCore import Qt, pyqtSlot, QDateTime
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtWidgets import QWidget
from Ui_DBLOADING import Ui_LoadingWindow


class DBloadingGui(QWidget, Ui_LoadingWindow):
	"""Loading."""
	
	def __init__(self, parent, title):
		super(DBloadingGui, self).__init__()
		self.setupUi(self)
		self.parent = parent
		self.setToolTip('[F1] Exit')
		#self.setWindowFlags(Qt.WindowStaysOnTopHint)
		#self.setWindowFlags(Qt.SplashScreen)
		self.setWindowIcon(QIcon(self.parent.WINS_ICO))
		self.setWindowTitle(self.parent.TITL_PROG + ' : SplashScreen')

		# font
		font = QFont()
		font.setFamily(self.parent.FONT_MAI)
		font.setFixedPitch(True)
		font.setPointSize(self.parent.FONT_SIZE + 2)
		self.lab_text.setFont(font)
		self.tabWidget.currentChanged.connect(self.chgtLogo)
		# logo gif
		self.numlogo = 1
		self.movielogo = QMovie(path.join(self.parent.RESS_LOGO,"logo1.gif"))
		self.lab_logo.setMovie(self.movielogo)
		self.movielogo.start()
		# tab1
		req = self.parent.CnxConnect.buildRequestTCD("CATEGORY", "FAMILY", "ALBUMS", "ALBUM", "1", True)
		self.buildTab(req, self.tableWid1)
		# tab2
		req = self.parent.CnxConnect.buildRequestTCD("CATEGORY", "FAMILY", "ALBUMS", "SIZE (GO)", "ROUND(( `Size` * 1.00) /1024 , 1)", True)
		self.buildTab(req, self.tableWid2)
		# tab3
		req = self.parent.CnxConnect.buildRequestTCD("YEAR", "CATEGORY", "ALBUMS", "YEAR", "1", True)
		self.buildTab(req, self.tableWid3)
		# center widget
		self.parent.centerWidget(self)
		# message
		basedate = self.parent.CnxConnect.sqlToArray(self.parent.CnxConnect.getrequest('datedatabase'))
		txt_message = self.parent.CnxConnect.MODE_SQLI
		if len(basedate) == 0:
			txt_message += " Base \nlast modified :\nnever"
		elif isinstance(basedate[0], QDateTime):
			txt_message += " Base \nlast modified :\n"+basedate[0].toString('dd/MM/yyyy hh:mm:ss')	
		else:
			txt_message += " Base \nlast modified :\n"+basedate[0].replace('T',' ')
		self.lab_text.setText(title+"\nConnected "+txt_message)
		# theme
		self.applyTheme()

	@pyqtSlot()
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape or event.key() == Qt.Key_F1:
			self.hide()

	def buildTab(self, req, tab):
		model = QSqlQueryModel(self)
		model.setQuery(req, self.parent.dbbase)
		tab.setModel(model)
		tab.resizeColumnsToContents()
		tab.verticalHeader().setVisible(False)
		tab.horizontalHeader().setStretchLastSection(True)
		tab.verticalHeader().setDefaultSectionSize(self.parent.C_HEIGHT)
		tab.setFont(QFont(self.parent.FONT_CON, self.parent.FONT_SIZE - 2))
	
	def chgtLogo(self):
		self.movielogo.stop()
		self.numlogo += 1
		self.numlogo = self.numlogo % 3
		logo = path.join(self.parent.RESS_LOGO, "logo" +str(self.numlogo) + ".gif")
		self.movielogo = QMovie(logo)
		self.lab_logo.setMovie(self.movielogo)
		self.movielogo.start()
			
	def applyTheme(self):
		"""Apply color Theme to main Gui."""
		# main
		mainstyle = 'QWidget{{background-color: {col2};}}' \
					'QScrollBar:vertical{{width: 14px;}}' \
					'QScrollBar:horizontal{{height: 14px;}}'
		mainstyle = mainstyle.format(col2 = self.parent.listcolors[1])
		self.setStyleSheet(mainstyle)
		gridstyle = 'alternate-background-color: {col3};background-color: {col4};'
		gridstyle = gridstyle.format(col3 = self.parent.listcolors[2],
									col2 = self.parent.listcolors[1],
									col4 = self.parent.listcolors[3])
		self.tableWid1.setStyleSheet(gridstyle)
		self.tableWid2.setStyleSheet(gridstyle)
		self.tableWid3.setStyleSheet(gridstyle)
