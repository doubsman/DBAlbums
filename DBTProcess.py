#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, chdir
from PyQt5.QtGui import QIcon, QFont, QTextCursor, QColor
from PyQt5.QtCore import Qt, QProcess, QIODevice, pyqtSlot, pyqtSignal, QSettings
from PyQt5.QtWidgets import QPushButton, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout
from DBFunction import centerWidget


class DBProcessGui(QWidget):
	signalend = pyqtSignal(int)

	PATH_PROG = path.dirname(path.abspath(__file__))
	RESS_LOGO = path.join(PATH_PROG, 'IMG')
	chdir(PATH_PROG)
	FILE__INI = 'DBAlbums.ini'
	configini = QSettings(FILE__INI, QSettings.IniFormat)
	configini.beginGroup('dbalbums')
	FONT_CON = configini.value('font01_ttx')
	WINS_ICO = path.join(PATH_PROG, 'IMG', configini.value('wins_icone'))
	configini.endGroup()

	def __init__(self, process, params, title, w, h, parent=None):
		super(DBProcessGui, self).__init__(parent)
		self.title = title
		self.resize(w, h)
		self.setWindowIcon(QIcon(self.WINS_ICO))
		self.setWindowTitle(title+' : waiting...')
		self.plainTextOut = QTextEdit(self)
		self.plainTextOut.setStyleSheet("background-color: black;color:white;")
		self.plainTextOut.setReadOnly(True)
		self.btn_quit = QPushButton('Kill')
		self.btn_quit.setMaximumWidth(80)
		self.btn_quit.clicked.connect(lambda e: self.destroy())
		font = QFont()
		font.setFamily(self.FONT_CON)
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
		ch = data.decode('cp850').rstrip().replace("\r", "")
		if len(ch) != 1:
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
