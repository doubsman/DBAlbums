#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QTableView, QFrame, QVBoxLayout, QHBoxLayout, QMainWindow, 
							QComboBox, QSpacerItem, QSizePolicy, QPushButton, QApplication)
from PyQt5.QtSql import QSqlQuery, QSqlRelationalTableModel, QSqlRelationalDelegate, QSqlTableModel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class ViewTablesSqlGUI(QMainWindow):
 
	def __init__(self, parent):
		super(ViewTablesSqlGUI, self).__init__()

		self.parent = parent
		self.setWindowIcon(QIcon(self.parent.WINS_ICO))
		self.setWindowTitle(self.parent.TITL_PROG + ' : View Datas')
		sizescreen = QApplication.primaryScreen()

		self.resize(sizescreen.size().width(), self.parent.HEIG_MAIN)
		self.parent.centerWidget(self)

		# buttons
		self.btnsav = QPushButton('Save')
		self.btnsav.clicked.connect(self.saveModifications)
		self.btncan = QPushButton('Cancel')
		self.btncan.clicked.connect(self.cancelModifications)

		# create combo model
		self.comboboxlist = QComboBox()
		self.modelcombo = QSqlTableModel(self)
		request = QSqlQuery(self.parent.CnxConnect.getrequest('listtables'), self.parent.CnxConnect.qtdbdb)
		self.modelcombo.setQuery(request)
		self.modelcombo.select()
		self.comboboxlist.setModel(self.modelcombo)
		self.comboboxlist.setModelColumn(self.modelcombo.fieldIndex("name"))
		self.comboboxlist.currentIndexChanged.connect(self.fillTableView)

		# # column table to combo
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
		self.viewtable = QTableView(self)
		self.viewtable.setAlternatingRowColors(True)
		self.viewtable.setModel(self.modeltable)
		self.viewtable.setItemDelegate(QSqlRelationalDelegate(self.viewtable))
		# columns sort
		self.viewtable.setSortingEnabled(True)

		# position GUI
		spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
		
		posco = QHBoxLayout()
		posco.addWidget(self.comboboxlist)
		posco.addItem(spacerItem)
				
		posbt = QHBoxLayout()
		posbt.addItem(spacerItem)
		posbt.addWidget(self.btnsav)
		posbt.addWidget(self.btncan)

		posit = QVBoxLayout()
		posit.addItem(posco)
		posit.addWidget(self.viewtable)
		posit.addItem(posbt)

		self.setCentralWidget(QFrame())
		self.centralWidget().setLayout(posit)

		self.show()
		self.applyTheme()
		# display datas
		self.fillTableView()
		

	def fillTableView(self):
		table = self.comboboxlist.currentText()
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
