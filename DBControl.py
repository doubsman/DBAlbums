#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import path
from PyQt5.QtWidgets import QApplication,  QWidget, QStyle, QTextEdit
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtGui import QIcon, QFont, QColor, QTextCursor
from PyQt5.QtCore import Qt
from Ui_DBCONTROL import Ui_ViewControlDatas

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
		self.resize(sizescreen.size().width() - tol, self.parent.HEIG_MAIN - tol)

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
		self.btngo.setIcon(QIcon(path.join(self.parent.RESS_ICOS, 'sql.png')))
		self.btngo.clicked.connect(self.runControl)

		# define file control script
		self.PATH_PROG = path.dirname(path.abspath(__file__))
		self.RESS_ICOS = path.join(self.PATH_PROG, 'ICO')
		namescript = self.parent.Json_params.getMember('scripts')["control_integrity"]
		script = path.join(self.PATH_PROG, 'SQL', namescript)

		# prepare list requests and fill combo
		self.listrequests = []
		self.listnames = []
		self.comboboxlist.addItem('All')
		request = ' '
		for line in open(script, 'r'):
			if line.startswith('--'):
				item = line.replace('-- ', '').replace('\n', ' ').replace('\r', '')
				self.comboboxlist.addItem(item)
				self.listnames.append(item)
			else:
				request += ' ' + line.rstrip('\n').lstrip('\t')
				if line.endswith(';\n'):
					self.listrequests.append(request)
					request = ' '
		#self.comboboxlist.currentIndexChanged.connect()

		# display GUI
		self.parent.centerWidget(self)
		self.applyTheme()
		self.show()

	def runControl(self):
		self.updateConsole('\nStart', 0)
		if self.comboboxlist.currentText() == 'All':
			# all requests
			for counter in range(0, len(self.listnames)):
				result = self.parent.CnxConnect.sqlToArray(self.listrequests[counter])
				self.writeRequest(self.listnames[counter], self.listrequests[counter], result)
		else:
			# one request
			result = self.parent.CnxConnect.sqlToArray(self.listrequests[self.comboboxlist.currentIndex() - 1])
			self.writeRequest(self.comboboxlist.currentText(), self.listrequests[self.comboboxlist.currentIndex() - 1], result)
		self.updateConsole('\nEnd', 0)
	
	def writeRequest(self, textname, request, result):
		self.updateConsole('\n' + textname, 1)
		self.updateConsole(request, 0)
		self.updateConsole(' '*3 + str(result), 2)

	def updateConsole(self, line, level):
		"""Write Reception signal run update."""
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
