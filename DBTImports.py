#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from codecs import open
from PyQt5.QtGui import QFont, QIcon, QColor, QTextCursor, QCursor
from PyQt5.QtCore import Qt, qDebug, pyqtSignal, pyqtSlot, QDateTime, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLCDNumber, QMenu, QStyle, QMessageBox, QTextEdit
from DBModelAbs import ModelTableUpdatesABS
from DBTImpoANA import ThreadAnalyseInvent
from DBTImpoRUN import ThreadReleaseInvent
from DBChrono import DBChrono
from Ui_DBUPDATE import Ui_UpdateWindows


class InventGui(QWidget, Ui_UpdateWindows):
	signalend = pyqtSignal()
	
	def __init__(self, parent, list_albums, list_columns, list_category, typeupdate, envt):
		"""Init Gui, start invent"""
		super(InventGui, self).__init__()
		self.setupUi(self)
		self.parent = parent
		self.resize(self.parent.WIDT_MAIN, self.parent.HEIG_MAIN-300)
		self.setWindowIcon(QIcon(self.parent.WINS_ICO))
		self.setWindowTitle(self.parent.TITL_PROG + ' : Update Database (Environment : ' + envt + ' mode : ' + typeupdate + ')')
		self.parent.centerWidget(self)
		
		self.list_albums = list_albums
		self.list_category = list_category
		self.list_columns = list_columns
		self.envits = envt
		self.typeupdate = typeupdate

		self.prepareInvent = None	# Class Analyse
		self.runActions = None		# Class Actions
		self.logname = QDateTime.currentDateTime().toString('yyMMddhhmmss') + "_UPDATE_DATABASE_" + self.envits + ".log"
		self.logname = path.join(self.parent.LOGS_PROG, self.logname)
		self.albumnew = 0
		self.alupdate = 0
		self.aldelete = 0
		self.apresent = 0
		self.actionerror = 0
		self.selecttrowg = 0
		self.list_actions = []
		
		font = QFont()
		font.setFamily("Courier New")
		font.setFixedPitch(True)
		font.setPointSize(10)
		fontconsol = QFont()
		fontconsol.setFamily(self.parent.FONT_CON)
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
	
		self.btn_action.clicked.connect(self.realiseActions)
		self.btn_action.setEnabled(False)
		self.btn_quit.clicked.connect(self.close)
		self.lcdTime.setSegmentStyle(QLCDNumber.Flat)
		
		self.tbl_update.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tbl_update.customContextMenuRequested.connect(self.popUpTreeUpdate)
		self.tableMdlUpd = ModelTableUpdatesABS(self, [[]*5])
		self.tbl_update.setModel(self.tableMdlUpd)
		for i in range(len(self.tableMdlUpd.U_C_WIDTH)):
			self.tbl_update.setColumnWidth(i, self.tableMdlUpd.U_C_WIDTH[i])
		self.tbl_update.verticalHeader().setDefaultSectionSize(self.tableMdlUpd.C_HEIGHT)
		self.tbl_update.horizontalHeader().setStretchLastSection(True)
		
		self.MyChrono = DBChrono()
		self.MyChrono.signalnow.connect(self.updateDisplaytimer)
		self.MyChrono.start_timer()
		
		self.applyTheme()
		self.show()

	def startAnalyse(self):
		qDebug('Start Analyse')
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
		self.prepareInvent = ThreadAnalyseInvent(self.list_albums,
												self.list_columns,
												self.list_category,
												self.typeupdate,
												self.envits,
												self.parent.MASKAUDIO,
												self.parent.FAMILIES)
		self.prepareInvent.signalchgt.connect(self.updateAnalyse)
		self.prepareInvent.signaltext.connect(self.updateConsole)
		self.prepareInvent.finished.connect(self.endAnalyse)
		self.prepareInvent.start()
	
	def updateAnalyse(self, percent, message):
		"""Display Analyse advance browsing folders."""
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

	@pyqtSlot()	
	def endAnalyse(self):
		"""End Analyse."""
		QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
		# actions ?
		if len(self.prepareInvent.list_action) > 0:
			self.list_actions = self.prepareInvent.list_action
			# relase manuel ?
			if self.checkBoxStart.isChecked():
				# release
				self.realiseActions()
			else:
				self.btn_action.setEnabled(True)
		else:
			self.MyChrono.stop_timer()
			self.lab_release.setText('no action')
			self.progressBarrelease.setValue(0)
			self.btn_quit.setText('Close')
		qDebug('End Analyse BuildInvent')
		self.lab_result.setText('Completed Analyse in ' + self.runtime)

	def realiseManualsActions(self, list_Manualsactions):
		"""Execute Actions Manuals."""
		qDebug('Start Realise Manuals Actions')
		# no analyse
		self.list_actions = list_Manualsactions
		self.lab_result.setText('No Analyse')
		self.lab_advance.setText('')
		self.progressBar.setValue(0)
		self.tableMdlUpd.update(self.list_actions)
		# maj counters
		self.apresent = len(self.list_albums)
		for action in self.list_actions:
			if action[2] == 'DELETE':
				self.aldelete += 1
			elif action[2] == 'UPDATE':
				self.alupdate += 1
			elif action[2] == 'ADD':
				self.albumnew += 1
		mesresu =  'PRESENT : ' + format(self.apresent + self.alupdate - self.aldelete, '05d')
		mesresu += '\nADD     : ' + format(self.albumnew, '05d')
		mesresu += '\nUPDATE  : ' + format(self.alupdate, '05d')
		mesresu += '\nDELETE  : ' + format(self.aldelete, '05d')
		self.lab_advance.setText(mesresu)
		self.aldelete = self.albumnew = self.alupdate = 0
		self.realiseActions()

	def realiseActions(self):
		"""Execute Actions Analyse."""
		self.btn_quit.setText('Close')
		qDebug('Start Realise Actions')
		self.runActions = ThreadReleaseInvent(self.parent, self.list_actions)
		self.runActions.signalrun.connect(self.updateActions)
		self.runActions.signaltxt.connect(self.updateConsole)
		self.runActions.finished.connect(self.endActions)
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
		self.runActions.start()

	def updateActions(self, percent, text):
		"""Display run operations update database."""
		index = self.tableMdlUpd.index(self.selecttrowg, 0)
		self.tbl_update.selectRow(index.row())
		index = self.tbl_update.currentIndex()
		self.tbl_update.scrollTo(index)
		self.selecttrowg += 1
		self.progressBarrelease.setValue(percent)
		if text == 'DELETE':
			self.aldelete += 1
		elif text == 'UPDATE':
			self.alupdate += 1
		elif text == 'ADD':
			self.albumnew += 1
		elif text == 'ERROR':
			self.actionerror += 1 
		mesresu =  'ERROR   : ' + format(self.actionerror, '05d')
		mesresu += '\nADD     : ' + format(self.albumnew, '05d')
		mesresu += '\nUPDATE  : ' + format(self.alupdate, '05d')
		mesresu += '\nDELETE  : ' + format(self.aldelete, '05d')
		self.lab_releaseadvance.setText(mesresu)
	
	@pyqtSlot()
	def endActions(self):
		"""Operations finished."""
		QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
		self.lab_release.setText('Completed Operations in ' + self.runtime)
		self.MyChrono.stop_timer()
		if len(self.list_actions) > 0:
			# create log file
			self.updateConsole('\n- Completed Operations in ' + self.runtime)
			self.updateConsole('\n- Create log file : ' + self.logname)
			self.textEditrelease.moveCursor(QTextCursor.Start)
			self.textEditrelease.ensureCursorVisible()
			# refresh datas
			self.signalend.emit()
			QMessageBox.information(self,'Update Database', 'Completed Operations in ' + self.runtime)
	
	def updateConsole(self, line, level=None):
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
		#if self.focusWidget() != self.vScrollBar:
		if self.focusWidget() != self.textEditrelease.verticalScrollBar():
			# display
			cursor = self.textEditrelease.textCursor()
			cursor.movePosition(QTextCursor.End)
		#cursor.insertText(line)
		self.textEditrelease.append(line.rstrip())
		self.textEditrelease.setTextCursor(cursor)
		#if self.focusWidget() != self.vScrollBar:
		if self.focusWidget() != self.textEditrelease.verticalScrollBar():
			self.textEditrelease.ensureCursorVisible()
		self.textEditrelease.horizontalScrollBar().setValue(0)
		text_file = open(self.logname, "a", 'utf-8')
		text_file.write(line+"\n")
		text_file.close()

	def getFolder(self):
		"""Open album folder."""
		indexes = self.tbl_update.selectedIndexes()
		self.currow = indexes[0].row()
		albumpath = self.tableMdlUpd._array[self.currow][5]
		self.parent.folder_open(albumpath)

	def popUpTreeUpdate(self, position):
		self.menua.exec_(self.tbl_update.viewport().mapToGlobal(position))

	def updateDisplaytimer(self, nowdisplay):
		"""display signal CLass Chrono."""
		self.runtime = nowdisplay
		self.lcdTime.display(nowdisplay)

	@pyqtSlot()
	def closeEvent(self, event):
		"""Cancel Processus Analyse + Actions."""
		# analyse in progress ?
		runana = runact = False
		if self.prepareInvent is not None:
			if self.prepareInvent.isRunning():
				runana = True
			else:
				self.prepareInvent.terminate()
		# actions in pogress ?
		if self.runActions is not None:
			if self.runActions.isRunning():
				runact = True
			else:
				self.runActions.terminate()
		# confirmation
		if runana or runact:
			response = QMessageBox.question(self, "Confirmation", "Stop Update Database in progress ?", QMessageBox.Yes, QMessageBox.No)
			if response == QMessageBox.Yes:
				self.MyChrono.stop_timer()
				if runana:
					# stop thread
					self.prepareInvent.stopAnalyse()
					qDebug('close Analyse in progress')
					self.prepareInvent.terminate()
					self.updateConsole('\n- close Analyse in progress')
				if runact:
					# stop thread
					self.runActions.stopActions()
					qDebug('close Actions in progress')
					self.runActions.terminate()
					self.updateConsole('\n- close Actions in progress')
				QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
				event.accept()
			else:
				event.ignore()
		QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
		self.MyChrono.timer.stop()
		event.accept()

	def applyTheme(self):
		"""Apply color Theme to main Gui."""
		# main
		mainstyle = 'QWidget{{background-color: {col1};}}' \
					'QLCDNumber{{border: none;color: black; background-color: {col1};}}' \
					'QScrollBar:vertical{{width: 14px;}}' \
					'QScrollBar:horizontal{{height: 14px;}}' \
					'QTableView{{alternate-background-color: {col3};background-color: {col4};}}' \
					'QTableView::item:selected{{ background-color:{col5}; color:white;}}'
		mainstyle = mainstyle.format(col1 = self.parent.listcolors[0],
									col3 = self.parent.listcolors[2],
									col4 = self.parent.listcolors[3],
									col5 = self.parent.listcolors[4])
		self.setStyleSheet(mainstyle)
		gridstyle = 'QHeaderView::section{{background-color: {col2};border-radius:1px;margin: 1px;padding: 2px;}}' \
					'alternate-background-color: {col3};background-color: {col4};'
		gridstyle = gridstyle.format(col2 = self.parent.listcolors[1],
									col3 = self.parent.listcolors[2], 
									col4 = self.parent.listcolors[3])
		self.tbl_update.setStyleSheet(gridstyle)
