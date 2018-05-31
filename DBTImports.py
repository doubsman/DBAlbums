#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
from time import time, sleep
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import (Qt, qDebug, pyqtSignal, qInstallMessageHandler,
						pyqtSlot, QSettings, QThread)
from PyQt5.QtWidgets import QApplication, QWidget, QLCDNumber,	QMenu, QStyle
from DBFunction import (buildCommandPowershell, centerWidget, qtmymessagehandler,
						displayCounters, openFolder, ThemeColors)
from DBDatabase import connectDatabase, getrequest, buildTabFromRequest
from DBTProcess import DBProcessGui
from DBModelAbs import ModelTableUpdatesABS
from DBTImpFunc import BuildInvent
from Ui_DBUPDATE import Ui_UpdateWindows


class timerThread(QThread):
	timeElapsed = pyqtSignal(int)

	def __init__(self, parent=None):
		super(timerThread, self).__init__(parent)
		self.timeStart = None

	def start(self, timeStart):
		self.timeStart = timeStart
		return super(timerThread, self).start()

	def run(self):
		while self.parent().isRunning():
			self.timeElapsed.emit(time() - self.timeStart)
			sleep(1)


class myThreadTimer(QThread):
	timeElapsed = pyqtSignal(int)
	
	def __init__(self, parent=None):
		super(myThreadTimer, self).__init__(parent)
		self.timerThread = timerThread(self)
		self.timerThread.timeElapsed.connect(self.timeElapsed.emit)

	def run(self):
		self.timerThread.start(time())
		iterations = 10000
		while iterations:
			#print("Running {0}".format(self.__class__.__name__))
			iterations -= 1
			sleep(1)


class InventGui(QWidget, Ui_UpdateWindows):
	PATH_PROG = path.dirname(path.abspath(__file__))
	PWSH_SCRU = path.join(PATH_PROG, 'PS1', "UPDATE_ALBUMS.ps1")
	PWSH_SCRA = path.join(PATH_PROG, 'PS1', "ADD_ALBUMS.ps1")
	# Read File DBAlbums.ini
	qDebug('read ini file')
	FILE__INI = 'DBAlbums.ini'
	configini = QSettings(FILE__INI, QSettings.IniFormat)
	configini.beginGroup('dbalbums')
	VERS_PROG = configini.value('prog_build')
	TITL_PROG = "♫ DBAlbums v{v} (2017)".format(v=VERS_PROG)
	TITL_PROG = TITL_PROG + " : Update Database"
	WIDT_MAIN = int(configini.value('wgui_width'))
	HEIG_MAIN = int(configini.value('wgui_heigh'))
	WINS_ICO = path.join(PATH_PROG, 'IMG', configini.value('wins_icone'))
	UNIX_ICO = path.join(PATH_PROG, 'IMG', configini.value('unix_icone'))
	THEM_COL = configini.value('name_theme')
	configini.endGroup()
	
	def __init__(self, list_albums, list_category, typeupdate, modsql, envt, themecolor, parent=None):
		"""Init Gui, start invent"""
		super(InventGui, self).__init__(parent)
		self.setupUi(self)
		self.parent = parent
		self.resize(self.WIDT_MAIN, self.HEIG_MAIN-500)
		self.setWindowIcon(QIcon(self.WINS_ICO))
		self.setWindowTitle(self.TITL_PROG + " Environment : " + envt + " mode : " + typeupdate)
		centerWidget(self)
		self.show()
		
		self.menua = QMenu()
		self.action_OPF = self.menua.addAction(self.style().standardIcon(QStyle.SP_DialogOpenButton),
							"Open Folder...", self.getFolder)
		self.total_p = None
		self.envits = envt
		self.curthe = themecolor
		font = QFont()
		font.setFamily("Courrier New")
		font.setFixedPitch(True)
		font.setPointSize(10)
		self.lab_result.setFont(font)
		self.lab_advance.setFont(font)
		
		self.btn_quit.clicked.connect(lambda e: self.destroy())
		self.btn_action.clicked.connect(self.realiseActions)
		self.btn_action.setEnabled(False)
		self.lcdTime.setSegmentStyle(QLCDNumber.Flat)
		self.applyTheme()
		
		self.seconds = 0
		self.myThreadtime = myThreadTimer(self)
		self.myThreadtime.timeElapsed.connect(self.showlcd)
		self.myThreadtime.start()
		
		self.tbl_update.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tbl_update.customContextMenuRequested.connect(self.popUpTreeUpdate)
		self.tableMdlUpd = ModelTableUpdatesABS(self, [[]*5])
		self.tbl_update.setModel(self.tableMdlUpd)
		for i in range(len(self.tableMdlUpd.U_C_WIDTH)):
			self.tbl_update.setColumnWidth(i, self.tableMdlUpd.U_C_WIDTH[i])
		self.tbl_update.verticalHeader().setDefaultSectionSize(self.tableMdlUpd.C_HEIGHT)

		qDebug('Start BuildInvent')
		self.setCursor(Qt.WaitCursor)
		self.prepareInvent = BuildInvent(list_albums,
									list_category,
									typeupdate,
									modsql, 
									envt)
		self.prepareInvent.signalthunchgt.connect(self.onBuild)
		self.prepareInvent.inventDatabase()
		self.setCursor(Qt.ArrowCursor)
		self.lab_result.setText('Analyse completed in '+self.total_p)
		qDebug('End BuildInvent')
		
		self.btn_quit.setText('Quit')
		if len(self.prepareInvent.list_action) > 0:
			self.btn_action.setEnabled(True)
			if self.checkBoxStart.isChecked():
				self.realiseActions()
	
	def onBuild(self, percent, message):
		"""Display advance browsinf folders."""
		self.lab_result.setText(message)
		self.progressBar.setValue(percent)
		mesresu =  'PRESENT : ' + format(self.prepareInvent.apresent + self.prepareInvent.alupdate - self.prepareInvent.aldelete, '05d')
		mesresu += '\nADD     : ' + format(self.prepareInvent.albumnew, '05d')
		mesresu += '\nUPDATE  : ' + format(self.prepareInvent.alupdate, '05d')
		mesresu += '\nDELETE  : ' + format(self.prepareInvent.aldelete, '05d')
		self.lab_advance.setText(mesresu)
		self.tableMdlUpd.update(self.prepareInvent.list_action)
		self.tbl_update.scrollToBottom()
		QApplication.processEvents()
	
	def realiseActions(self):
		"""Execute Actions Update."""
		self.btn_action.setEnabled(False)
		listactions = self.prepareInvent.getListIds()
		# release Actions
		if listactions:
			lstcate = []
			lstfami = []
			lstacti = []
			lstpath = []
			for pathadd in listactions:
				lstcate.append(pathadd[0])
				lstfami.append(pathadd[1])
				lstacti.append(pathadd[2])
				lstpath.append(pathadd[3])
			exeprocess, params = buildCommandPowershell(self.PWSH_SCRU,
														'-Envt', self.envits, 
														'-TypeOpe', '"' + '|'.join(lstacti) + '"',
														'-AlbumInfos', '"' + '|'.join(lstpath) + '"',
														'-Category', '"' + '|'.join(lstcate) + '"',
														'-Family', '"' + '|'.join(lstfami) + '"',
														'-Force')
			DBProcessGui(exeprocess, params, 'Add ' + displayCounters(len(lstacti), "Album "), self.WIDT_MAIN, self.HEIG_MAIN-150)
			#pro.signalend.connect(lambda: self.parent.connectEnvt(True))

	def getFolder(self):
		"""Open album folder."""
		indexes = self.tbl_update.selectedIndexes()
		self.currow = indexes[0].row()
		albumpath = self.tableMdlUpd._array[self.currow][5]
		openFolder(albumpath)

	def popUpTreeUpdate(self, position):
		self.menua.exec_(self.tbl_update.viewport().mapToGlobal(position))
	
	@pyqtSlot(int)
	def showlcd(self, seconds):
		minutes = seconds // 60
		self.total_p = "%02d:%02d" % (minutes, seconds % 60)
		self.lcdTime.display(str(self.total_p))
		QApplication.processEvents()

	def applyTheme(self):
		"""Apply color Theme to main Gui."""
		# main
		mainstyle = 'QWidget{{background-color: {col1};}}' \
					'QLCDNumber{{border: none;color: black; background-color: {col1};}}' \
					'QScrollBar:vertical{{width: 14px;}}' \
					'QScrollBar:horizontal{{height: 14px;}}' \
					'QTableView::item:selected{{ background-color:{col5}; color:white;}}'
		mainstyle = mainstyle.format(col1 = self.curthe.listcolors[0],
									col2 = self.curthe.listcolors[1], 
									col5 = self.curthe.listcolors[4])
		self.setStyleSheet(mainstyle)
		gridstyle = 'alternate-background-color: {col3};background-color: {col4};'
		gridstyle = gridstyle.format(col3 = self.curthe.listcolors[2], 
									col4 = self.curthe.listcolors[3])
		self.tbl_update.setStyleSheet(gridstyle)


if __name__ == '__main__':
	app = QApplication(argv)
	# debug
	qInstallMessageHandler(qtmymessagehandler)
	envt = 'LOSSLESS'
	boolconnect, dbbase, modsql, rootDk, listcategory = connectDatabase(envt)
	req = getrequest('albumslist', modsql)
	list_albums = buildTabFromRequest(req)
	curthe = ThemeColors('brown')
	prepareInvent = InventGui(list_albums,
								listcategory,
								"NEW",
								modsql, 
								envt, 
								curthe)
	rc = app.exec_()
	exit(rc)
