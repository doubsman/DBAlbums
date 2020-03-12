#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import path
from PyQt5.QtWidgets import (QTableView, QVBoxLayout, QHBoxLayout, QWidget, QStyle,
							QComboBox, QSpacerItem, QSizePolicy, QPushButton, QApplication)
from PyQt5.QtSql import QSqlQuery, QSqlRelationalTableModel, QSqlRelationalDelegate, QSqlTableModel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from Ui_DBVIEWTBL import Ui_ViewTablesDatas

class ViewsDatabaseTablesGUI(QWidget, Ui_ViewTablesDatas):
	"""Display GUI Tables Database view and modify datas."""

	def __init__(self, parent):
		super(ViewsDatabaseTablesGUI, self).__init__()
		self.setupUi(self)

		self.parent = parent
		self.setWindowIcon(QIcon(self.parent.WINS_ICO))
		self.setWindowTitle(self.parent.TITL_PROG + ' : View Database Tables')
		sizescreen = QApplication.primaryScreen()
		tol = 50
		self.resize(sizescreen.size().width() - tol, self.parent.HEIG_MAIN - tol)

		# buttons
		self.btnsav.setIcon(QIcon(path.join(self.parent.RESS_ICOS, 'database.png')))
		self.btnsav.clicked.connect(self.saveModifications)
		self.btncan.setIcon(QIcon(path.join(self.parent.RESS_ICOS, 'database.png')))
		self.btncan.clicked.connect(self.cancelModifications)
		self.btnclo.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
		self.btnclo.clicked.connect(self.closeViewTables)

		# create combo model
		self.modelcombo = QSqlTableModel(self)
		query = QSqlQuery(self.parent.CnxConnect.getrequest('listtables'), self.parent.CnxConnect.qtdbdb)
		self.modelcombo.setQuery(query)
		self.modelcombo.select()
		query.clear
		self.comboboxlist.setModel(self.modelcombo)
		self.comboboxlist.setModelColumn(self.modelcombo.fieldIndex("name"))
		self.comboboxlist.currentIndexChanged.connect(self.fillTableView)

		# column table to combo exemple
		# self.comboboxlist = QComboBox()
		# request = "SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
		# self.modelcombo = QSqlTableModel(self)
		# self.modelcombo.setTable("sqlite_master")
		# self.modelcombo.select()
		# self.comboboxlist.setModel(self.modelcombo)
		# self.comboboxlist.setModelColumn(self.modelcombo.fieldIndex("name"))

		# create table model 
		self.modeltable = QSqlRelationalTableModel(self, self.parent.CnxConnect.qtdbdb)
		# stratégy user modify
		self.modeltable.setEditStrategy(QSqlTableModel.OnManualSubmit)
		#QSqlTableModel::OnFieldChange	: All changes to the model will be applied immediately to the database.
		#QSqlTableModel::OnRowChange	: Changes to a row will be applied when the user selects a different row.
		#QSqlTableModel::OnManualSubmit	: All changes will be cached in the model until either submitAll() or revertAll() is called.

		# apply model in table
		self.viewtable.setAlternatingRowColors(True)
		self.viewtable.setModel(self.modeltable)
		self.viewtable.setItemDelegate(QSqlRelationalDelegate(self.viewtable))
		# columns sort
		self.viewtable.setSortingEnabled(True)

		# display GUI
		self.parent.centerWidget(self)
		self.applyTheme()
		self.show()
		# display datas
		self.fillTableView()

	def fillTableView(self):
		table = self.comboboxlist.currentText()
		if table:
			print('fill')
			self.modeltable.setTable(table)
			self.modeltable.select()
			# ajust size
			self.viewtable.resizeColumnsToContents()
			# sort first column DescendingOrder
			self.modeltable.sort(0, Qt.DescendingOrder)

	def saveModifications(self):
		self.modeltable.submitAll()

	def cancelModifications(self):
		self.modeltable.revertAll()

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.closeViewTables()

	def closeViewTables(self):
		"""Close Windows."""
		self.modeltable.clear()
		self.modelcombo.clear()
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
		self.viewtable.setStyleSheet(gridstyle)
