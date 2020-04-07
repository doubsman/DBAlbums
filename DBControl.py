#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import path
from PyQt5.QtWidgets import QApplication,  QWidget, QStyle, QTextEdit, QFileDialog
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtGui import QIcon, QFont, QColor, QTextCursor
from PyQt5.QtCore import Qt, QDateTime
from Ui_DBCONTROL import Ui_ViewControlDatas
from json import load, dumps

class ControlDatabaseGUI(QWidget, Ui_ViewControlDatas):
	"""Display GUI Tables Database view and modify datas."""

	def __init__(self, parent):
		super(ControlDatabaseGUI, self).__init__()
		self.setupUi(self)

		self.parent = parent
		self.setWindowIcon(QIcon(self.parent.WINS_ICO))
		self.setWindowTitle(self.parent.TITL_PROG + ' : Control Database Integrity')
		sizescreen = QApplication.primaryScreen()
		tol = 50
		self.resize(self.parent.WIDT_MAIN + (tol*2), self.parent.HEIG_MAIN - tol)

		# json file
		self.logname = None

		# font
		font = QFont()
		font.setFamily("Courier New")
		font.setFixedPitch(True)
		font.setPointSize(10)
		fontconsol = QFont()
		fontconsol.setFamily(self.parent.FONT_CON)
		fontconsol.setFixedPitch(True)
		fontconsol.setPointSize(8)
		self.levelcolors = [Qt.white, Qt.green, Qt.magenta, Qt.red]
		self.textEdit.setStyleSheet("background-color: black;color:white;")
		self.textEdit.setLineWrapMode(QTextEdit.NoWrap)
		self.textEdit.setReadOnly(True)
		self.textEdit.setFont(fontconsol)

		# buttons
		self.btnclo.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
		self.btnclo.clicked.connect(self.closeControl)
		self.btnctr.setIcon(QIcon(path.join(self.parent.RESS_ICOS, 'sql.png')))
		self.btnctr.clicked.connect(self.runControl)
		self.btncor.setIcon(QIcon(path.join(self.parent.RESS_ICOS, 'sql.png')))
		self.btncor.clicked.connect(self.runCorrection)
		self.btnload.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
		self.btnload.clicked.connect(self.loadControl)

		# define file control script
		self.PATH_PROG = path.dirname(path.abspath(__file__))
		self.RESS_ICOS = path.join(self.PATH_PROG, 'ICO')
		namescriptctr = self.parent.Json_params.getMember('scripts')["control_integrity"]
		namescriptcor = self.parent.Json_params.getMember('scripts')["correction_integrity"]

		# prepare list controls requests and fill combo control
		script = path.join(self.PATH_PROG, 'SQL', namescriptctr)
		self.listjson = []
		self.listctrnames, self.listctrrequests = self.loadScript(script, self.comboboxlistctr)

		# prepare list corrections requests and fill combo control
		script = path.join(self.PATH_PROG, 'SQL', namescriptcor)
		self.listcornames, self.listcorrequests = self.loadScript(script, self.comboboxlistcor)

		# display GUI
		self.parent.centerWidget(self)
		self.applyTheme()
		self.show()

	def loadScript(self, script, combo):
		"""Fill Combo with listname, reutrn two lists."""
		listname = []
		listrequest = []
		combo.addItem('All')
		request = ' '
		for line in open(script, 'r'):
			if line.startswith('--'):
				item = line.replace('-- ', '').replace('\n', ' ').replace('\r', '')
				combo.addItem(item)
				listname.append(item)
			else:
				request += ' ' + line.rstrip('\n').lstrip('\t')
				if line.endswith(';\n'):
					listrequest.append(request)
					request = ' '
		return listname, listrequest

	def runCorrection(self):
		# execute request(s)
		self.execRequests(self.comboboxlistcor, self.listcornames, self.listcorrequests, 'correction')

	def runControl(self, type):
		# define json file
		self.logname = QDateTime.currentDateTime().toString('yyMMddhhmmss') + "_CONTROL_DATABASE_" + self.parent.envits + ".json"
		self.logname = path.join(self.PATH_PROG, 'CTR', self.logname)
		# execute request(s)
		self.execRequests(self.comboboxlistctr, self.listctrnames, self.listctrrequests, 'control')
			# write file json
		self.listjson = {"Control_Integrity_Database" : self.listjson}
		data_file = open(self.logname, 'w+')
		data_file.write(dumps(self.listjson, indent=4))
		data_file.close()
		self.updateConsole('\nsave results to json file : ' + self.logname, 0)
	
	def execRequests(self, combo, listnames, listrequests, typeop):
		"""Execute query(s) and display result to textedit."""
		self.listjson = []
		self.updateConsole('\n' + '-^'*60, 0)
		self.updateConsole('Start ' + typeop + ' at ' + QDateTime.currentDateTime().toString('hh:mm:ss dd/MM/yy'), 0)
		if combo.currentText() == 'All':
			# all requests
			for counter in range(0, len(listnames)):
				result = self.parent.CnxConnect.sqlToArray(listrequests[counter])
				self.writeRequest(listnames[counter], listrequests[counter], result)
		else:
			# one request
			result = self.parent.CnxConnect.sqlToArray(listrequests[combo.currentIndex() - 1])
			self.writeRequest(combo.currentText(), listrequests[combo.currentIndex() - 1], result)
		self.updateConsole('\nEnd ' + typeop + ' at ' + QDateTime.currentDateTime().toString('hh:mm:ss dd/MM/yy'), 0)

	def loadControl(self):
		"""Load old controls file json."""
		file_json = QFileDialog.getOpenFileName(self,
							"Select file Control Itegrity database Result",
							path.join(self.PATH_PROG, 'CTR'),
							"Json (*.json)")
		file_json = file_json[0]
		if path.isfile(str(file_json)):
			self.updateConsole('\n' + '^-'*60, 0)
			self.updateConsole('Load File Control at ' + QDateTime.currentDateTime().toString('hh:mm:ss dd/MM/yy'), 0)
			data_file = open(file_json, 'r')
			self.datajson = load(data_file)
			self.listjson = []
			data_file.close()
			self.updateConsole('\nload results to json file : ' + file_json, 0)
			# display results json
			for control in self.datajson['Control_Integrity_Database']:
				self.writeRequest(control['name'], control['request'], control['result'])
			self.updateConsole('\nEnd at ' + QDateTime.currentDateTime().toString('hh:mm:ss dd/MM/yy'), 0)

	def writeRequest(self, textname, request, result):
		"""Display consol text."""
		self.listjson.append({"name" : textname, "request": request,"result": result})
		self.updateConsole('\n' + textname, 1)
		self.updateConsole(request, 0)
		str_l = 10
		for row in result:
			line = " ".join(['{:<{length}s}'.format(str(x), length = str_l) for x in row])
			self.updateConsole(' '*3 + line, 2)

	def updateConsole(self, line, level):
		"""Add line to QtextEdit."""
		# set color
		self.textEdit.setTextColor(QColor(self.levelcolors[level]))
		# display
		cursor = self.textEdit.textCursor()
		cursor.movePosition(QTextCursor.End)
		#cursor.insertText(line)
		self.textEdit.append(line.rstrip())
		self.textEdit.setTextCursor(cursor)

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.closeControl()

	def closeControl(self):
		"""Close Windows."""
		self.destroy()

	def applyTheme(self):
		"""Apply color Theme to main Gui."""
		# main
		mainstyle = 'QWidget{{background-color: {col1};}}' \
					'QComboBox{{background-color: {col2};}}' \
					'QScrollBar:vertical{{width: 14px;}}' \
					'QScrollBar:horizontal{{height: 14px;}}' \
					'QTableView{{alternate-background-color: {col3};background-color: {col4};}}' \
					'QTableWidget::item:selected{{ background-color:{col5}; color:white;}}'
		mainstyle = mainstyle.format(col1 = self.parent.listcolors[0],
									col2 = self.parent.listcolors[1],
									col3 = self.parent.listcolors[2],
									col4 = self.parent.listcolors[3], 
									col5 = self.parent.listcolors[4])
		self.setStyleSheet(mainstyle)
		gridstyle = 'QHeaderView::section{{background-color: {col2};border-radius:1px;margin: 1px;padding: 2px;}}'
		gridstyle = gridstyle.format(col2 = self.parent.listcolors[1])						
