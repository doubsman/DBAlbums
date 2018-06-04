#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from codecs import open
from time import time, sleep
from PyQt5.QtGui import QFont, QIcon, QColor, QTextCursor
from PyQt5.QtCore import (Qt, qDebug, pyqtSignal,
						pyqtSlot, QSettings, QThread, QDateTime)
from PyQt5.QtWidgets import QApplication, QWidget, QLCDNumber,	QMenu, QStyle, QMessageBox, QTextEdit, QScrollBar
from PyQt5.QtSql import QSqlQuery
from DBFunction import centerWidget, openFolder
from DBDatabase import DBFuncBase
from DBModelAbs import ModelTableUpdatesABS
from DBTImpoANA import BuildInvent
from DBTImpoRUN import ReleaseInvent
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
	
	def stop(self):
		self.timerThread.terminate()
		self.terminate()
		
	def run(self):
		self.timerThread.start(time())
		iterations = 10000
		while iterations:
			#print("Running {0}".format(self.__class__.__name__))
			iterations -= 1
			sleep(1)


class InventGui(QWidget, Ui_UpdateWindows):
	signalend = pyqtSignal()
	
	PATH_PROG = path.dirname(path.abspath(__file__))
	LOGS_PROG = path.join(PATH_PROG, 'LOG')
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
	WIDT_PICM = int(configini.value('thun_csize'))
	TEXT_NCO = configini.value('text_nocov')
	FONT_CON = configini.value('font01_ttx')
	WINS_ICO = path.join(PATH_PROG, 'IMG', configini.value('wins_icone'))
	THEM_COL = configini.value('name_theme')
	configini.endGroup()
	
	def __init__(self, list_albums, list_columns, list_category, typeupdate, modsql, envt, themecolor, parent=None):
		"""Init Gui, start invent"""
		super(InventGui, self).__init__(parent)
		self.setupUi(self)
		self.resize(self.WIDT_MAIN, self.HEIG_MAIN-300)
		self.setWindowIcon(QIcon(self.WINS_ICO))
		self.setWindowTitle(self.TITL_PROG + " Environment : " + envt + " mode : " + typeupdate)
		centerWidget(self)
		
		self.parent = parent
		self.list_albums = list_albums
		self.list_category = list_category
		self.list_columns = list_columns
		self.modsql = modsql
		self.envits = envt
		self.typeupdate = typeupdate
		self.curthe = themecolor
		self.logname = QDateTime.currentDateTime().toString('yyMMddhhmmss') + "_UPDATE_DATABASE_" + self.envits + ".log"
		self.logname = path.join(self.LOGS_PROG, self.logname)
		self.total_p = None
		self.albumnew = 0
		self.alupdate = 0
		self.aldelete = 0
		self.apresent = 0
		self.actionerror = 0
		self.selecttrowg = 0
		self.list_actions = []
		
		font = QFont()
		font.setFamily("Courrier New")
		font.setFixedPitch(True)
		font.setPointSize(10)
		fontconsol = QFont()
		fontconsol.setFamily(self.FONT_CON)
		fontconsol.setFixedPitch(True)
		fontconsol.setPointSize(8)
		self.levelcolors = [Qt.white, Qt.green, Qt.magenta, Qt.red]
		
		self.menua = QMenu()
		self.action_OPF = self.menua.addAction(self.style().standardIcon(QStyle.SP_DialogOpenButton),
							"Open Folder...", self.getFolder)
							
		self.lab_result.setFont(font)
		self.lab_release.setFont(font)
		self.lab_advance.setFont(font)
		self.lab_releaseadvance.setFont(font)
		
		self.textEditrelease.setStyleSheet("background-color: black;color:white;")
		self.textEditrelease.setLineWrapMode(QTextEdit.NoWrap)
		self.textEditrelease.setReadOnly(True)
		self.textEditrelease.setFont(fontconsol)
		self.vScrollBar = QScrollBar(self.textEditrelease.verticalScrollBar())
		self.vScrollBar.sliderPressed.connect(self.onScrollPressed)
	
		self.btn_action.clicked.connect(self.realiseActions)
		self.btn_action.setEnabled(False)
		self.btn_quit.clicked.connect(self.closeImpoort)
		self.lcdTime.setSegmentStyle(QLCDNumber.Flat)
		
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
		self.tbl_update.horizontalHeader().setStretchLastSection(True)
		
		self.applyTheme()
		self.show()

	def startAnalyse(self):
		qDebug('Start BuildInvent')
		self.setCursor(Qt.WaitCursor)
		self.prepareInvent = BuildInvent(self.list_albums,
									self.list_columns,
									self.list_category,
									self.typeupdate,
									self.modsql, 
									self.envits)
		self.prepareInvent.signalchgt.connect(self.onBuild)
		self.prepareInvent.signaltext.connect(self.updateInfos)
		self.prepareInvent.inventDatabase()
		self.setCursor(Qt.ArrowCursor)
		self.lab_result.setText('Completed Analyse in '+self.total_p)
		qDebug('End BuildInvent')
		
		self.btn_quit.setText('Close')
		if len(self.prepareInvent.list_action) > 0 and not self.checkBoxStart.isChecked():
				self.btn_action.setEnabled(True)
		self.realiseActions()
	
	def onBuild(self, percent, message):
		"""Display advance browsing folders."""
		self.lab_result.setText(message)
		self.progressBar.setValue(percent)
		mesresu =  'PRESENT : ' + format(self.prepareInvent.apresent + self.prepareInvent.alupdate - self.prepareInvent.aldelete, '05d')
		mesresu += '\nADD     : ' + format(self.prepareInvent.albumnew, '05d')
		mesresu += '\nUPDATE  : ' + format(self.prepareInvent.alupdate, '05d')
		mesresu += '\nDELETE  : ' + format(self.prepareInvent.aldelete, '05d')
		self.lab_advance.setText(mesresu)
		self.lab_releaseadvance.setText(mesresu)
		self.tableMdlUpd.update(self.prepareInvent.list_action)
		self.tbl_update.scrollToBottom()
		QApplication.processEvents()
	
	def realiseActions(self, list_actions=None):
		"""Execute Actions Update."""
		if list_actions is None:
			self.list_actions = self.prepareInvent.list_action
			self.apresent = self.prepareInvent.apresent
			self.albumnew = self.prepareInvent.albumnew
			self.alupdate = self.prepareInvent.alupdate
			self.aldelete = self.prepareInvent.aldelete
		else:
			# no analyse
			self.btn_quit.setText('Close')
			self.list_actions = list_actions
			self.lab_result.setText('No Analyse')
			self.lab_advance.setText('')
			self.progressBar.setValue(100)
			self.tableMdlUpd.update(self.list_actions)
			self.apresent = len(self.list_albums)
			for action in self.list_actions:
				if action[2] == 'DELETE':
					self.aldelete += 1
				elif action[2] == 'UPDATE':
					self.alupdate += 1
				elif action[2] == 'ADD':
					self.albumnew += 1
		run = ReleaseInvent(self.list_actions, self.modsql)
		run.signalrun.connect(self.updateRun)
		run.signalend.connect(self.updateEnd)
		run.signaltxt.connect(self.updateInfos)
		run.executeActions()

	def updateRun(self, percent, text):
		"""Display run operations update database."""
		index = self.tableMdlUpd.index(self.selecttrowg, 0)
		self.tbl_update.selectRow(index.row())
		index = self.tbl_update.currentIndex()
		self.tbl_update.scrollTo(index)
		self.selecttrowg += 1
		self.progressBarrelease.setValue(percent)
		if text == 'DELETE':
			self.aldelete -= 1
			self.apresent -= 1
		elif text == 'UPDATE':
			self.alupdate -= 1
		elif text == 'ADD':
			self.albumnew -= 1
			self.apresent += 1
		elif text == 'ERROR':
			self.actionerror += 1 
		mesresu =  'ERROR   : ' + format(self.actionerror, '05d')
		mesresu += '\nADD     : ' + format(self.albumnew, '05d')
		mesresu += '\nUPDATE  : ' + format(self.alupdate, '05d')
		mesresu += '\nDELETE  : ' + format(self.aldelete, '05d')
		self.lab_releaseadvance.setText(mesresu)
		QApplication.processEvents()
		
	@pyqtSlot()	
	def updateEnd(self):
		"""Operations finished."""
		QApplication.processEvents()
		self.lab_release.setText('Completed Operations in '+self.total_p)
		if len(self.list_actions) > 0:
			# create log file
			self.textEditrelease.append('\n- Completed Operations in '+self.total_p)
			self.textEditrelease.append('\n- Create log file : ' + self.logname)
			text_file = open(self.logname, "w", 'utf-8')
			text_file.write(self.textEditrelease.toPlainText())
			text_file.close()
			self.textEditrelease.moveCursor(QTextCursor.Start) ;
			self.textEditrelease.ensureCursorVisible()
			# refresh
			self.signalend.emit()
			QMessageBox.information(self,'Update Database', 'Completed Operations in '+self.total_p)
	
	def updateInfos(self, line, level=None):
		"""Write Reception signal run update."""
		if not level:
			if line.startswith('-'):
				level = 1
			elif line.startswith('WARNING'):
				level = 2
			elif line.startswith('ERROR'):
				level = 3
			else:
				level = 0
		# set color
		self.textEditrelease.setTextColor(QColor(self.levelcolors[level]))
		if self.focusWidget() != self.vScrollBar:
			# display
			cursor = self.textEditrelease.textCursor()
			cursor.movePosition(QTextCursor.End)
		#cursor.insertText(line)
		self.textEditrelease.append(line.rstrip())
		self.textEditrelease.setTextCursor(cursor)
		if self.focusWidget() != self.vScrollBar:
			self.textEditrelease.ensureCursorVisible()
		self.textEditrelease.horizontalScrollBar().setValue(0)
	
	def golbalInsertCovers(self):
		request = "SELECT ALBUMS.ID_CD, ALBUMS.Cover FROM ALBUMS " \
					"LEFT JOIN COVERS ON ALBUMS.ID_CD = COVERS.ID_CD " \
					"WHERE COVERS.ID_CD IS NULL AND ALBUMS.Cover<>'{textnopic}'"
		request = request.format(textnopic = self.TEXT_NCO)
		query = QSqlQuery(request)
		query.exec_()
		while query.next():
			DBFuncBase().imageToSql(query.value(1), query.value(0), self.WIDT_PICM)

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
		hours, seconds =  seconds // 3600, seconds % 3600
		minutes, seconds = seconds // 60, seconds % 60
		self.total_p = "%02d:%02d:%02d" % (hours, minutes, seconds)
		self.lcdTime.display(self.total_p)
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

	def closeImpoort(self):
		"""Close Windows."""
		self.myThreadtime.stop()
		self.destroy()

	def onScrollPressed(self):
		pass
