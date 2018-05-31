#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, chdir
from PyQt5.QtGui import QIcon, QFont, QTextCursor, QColor, QMovie
from PyQt5.QtCore import Qt, QProcess, QIODevice, pyqtSlot, pyqtSignal, QSettings, QDateTime
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtWidgets import QPushButton, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout
from DBDatabase import getrequest, buildTabFromRequest, buildReqTCD
from DBFunction import centerWidget
from Ui_DBLOADING import Ui_LoadingWindow


PATH_PROG = path.dirname(path.abspath(__file__))
RESS_LOGO = path.join(PATH_PROG, 'IMG')
chdir(PATH_PROG)
FILE__INI = 'DBAlbums.ini'
configini = QSettings(FILE__INI, QSettings.IniFormat)
configini.beginGroup('dbalbums')
FONT_MAI = configini.value('font00_ttx')
FONT_CON = configini.value('font01_ttx')
THEM_COL = configini.value('name_theme')
WINS_ICO = path.join(PATH_PROG, 'IMG', configini.value('wins_icone'))
configini.endGroup()


# ##################################################################
class ProcessGui(QWidget):
	signalend = pyqtSignal(int)
	def __init__(self, process, params, title, w, h, parent=None):
		super(ProcessGui, self).__init__(parent)
		self.title = title
		self.resize(w, h)
		self.setWindowIcon(QIcon(WINS_ICO))
		self.setWindowTitle(title+' : waiting...')
		self.plainTextOut = QTextEdit(self)
		self.plainTextOut.setStyleSheet("background-color: black;color:white;")
		self.plainTextOut.setReadOnly(True)
		self.btn_quit = QPushButton('Kill')
		self.btn_quit.setMaximumWidth(80)
		self.btn_quit.clicked.connect(lambda e: self.destroy())
		font = QFont()
		font.setFamily(FONT_CON)
		font.setFixedPitch(True)
		font.setPointSize(8)
		self.levelcolors = [Qt.white, Qt.green, Qt.magenta, Qt.red]
		self.plainTextOut.setFont(font)
		labtn = QHBoxLayout()
		labtn.addStretch()
		labtn.addWidget(self.btn_quit)
		layout = QVBoxLayout()
		layout.addWidget(self.plainTextOut)
		layout.addLayout(labtn)
		self.setLayout(layout)
		centerWidget(self)
		self.show()
		# run process
		self.normalOutputWritten('|'+process+' '+' '.join(params) + '\n')
		self.process = QProcess()
		self.process.setProcessChannelMode(QProcess.MergedChannels)
		self.process.readyReadStandardOutput.connect(self.WorkReply)
		self.process.finished.connect(self.WorkFinished)
		self.process.start(process, params, QIODevice.ReadWrite)
		self.process.waitForStarted()

	def normalOutputWritten(self, line):
		# set level line
		if line.startswith('*') or ('****' in line):
			level = 1
		elif (line.lstrip()).startswith('|') or ('(U)' in line) or ('(N)' in line):
			level = 2
		elif 'error:' in line:
			level = 3
		else:
			level = 0
		# set color
		self.plainTextOut.setTextColor(QColor(self.levelcolors[level]))
		# display
		cursor = self.plainTextOut.textCursor()
		cursor.movePosition(QTextCursor.End)
		#cursor.insertText(line)
		self.plainTextOut.append(line.rstrip())
		self.plainTextOut.setTextCursor(cursor)
		self.plainTextOut.ensureCursorVisible()

	@pyqtSlot()
	def WorkReply(self):
		"""Outpout to Gui."""
		data = self.process.readAllStandardOutput().data()
		ch = data.decode('cp850').rstrip()
		self.normalOutputWritten(ch)

	@pyqtSlot()
	def WorkFinished(self):
		"""End of processus."""
		if self.process is not None:
			self.process.readyReadStandardOutput.disconnect()
			self.process.finished.disconnect()
			self.normalOutputWritten('Process Finished...')
			self.setWindowTitle(self.title+' : Finished...')
			self.btn_quit.setText('Quit')
			self.signalend.emit(1)


# ##################################################################
class DBloadingGui(QWidget, Ui_LoadingWindow):
	def __init__(self, modsql, title, parent=None):
		super(DBloadingGui, self).__init__(parent)
		self.setupUi(self)
		self.parent = parent
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags(Qt.SplashScreen)
		centerWidget(self)
		# font
		font = QFont()
		font.setFamily(FONT_MAI)
		font.setFixedPitch(True)
		font.setPointSize(14)
		self.lab_text.setFont(font)
		self.tabWidget.currentChanged.connect(self.chgtLogo)
		# logo gif
		self.numlogo = 1
		self.movielogo = QMovie(path.join(RESS_LOGO,"logo1.gif"))
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
		basedate = buildTabFromRequest(getrequest('datedatabase', modsql))[0]
		if isinstance(basedate, QDateTime):
			txt_message = modsql + " Base \nlast modified :\n"+basedate.toString('dd/MM/yyyy hh:mm:ss')	
		else:
			txt_message = modsql + " Base \nlast modified :\n"+basedate.replace('T',' ')
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
		logo = path.join(RESS_LOGO, "logo" +str(self.numlogo) + ".gif")
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
