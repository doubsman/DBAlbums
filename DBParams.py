#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import qDebug
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QAbstractScrollArea, QHeaderView, QMessageBox
from DBFunction import centerWidget
from DBReadJson import JsonParams
from Ui_DBPARAMS import Ui_ParamsJson


class ParamsGui(QWidget, Ui_ParamsJson):
	"""Display GUI file Json parameters."""
	PATH_PROG = path.dirname(path.abspath(__file__))
	LOGS_PROG = path.join(PATH_PROG, 'LOG')
	# Read File DBAlbums.ini
	qDebug('read json params file')
	FILE__INI = 'DBAlbums.json'
	Json_params = JsonParams(FILE__INI)
	
	group_dbalbums = Json_params.getMember('dbalbums')
	VERS_PROG = group_dbalbums['prog_build']
	TITL_PROG = "DBAlbums v{v} (2017)".format(v=VERS_PROG)
	TITL_PROG = TITL_PROG + " : Environments Parameters "
	WIDT_MAIN = group_dbalbums['wgui_width']
	HEIG_MAIN = group_dbalbums['wgui_heigh']
	WIDT_PICM = group_dbalbums['thun_csize']
	WINS_ICO = path.join(PATH_PROG, 'IMG', group_dbalbums['wins_icone'])
	THEM_COL = group_dbalbums['name_theme']
	TEXT_NCO = group_dbalbums['text_nocov']
	FONT_CON = group_dbalbums['font01_ttx']
	HELP_LST = {'prog_build' : 'version program ({v})'.format(v=VERS_PROG),
				'wgui_width' : 'width pixels main windows ({v})'.format(v=WIDT_MAIN),
				'wgui_heigh' : 'height pixels main windows ({v})'.format(v=HEIG_MAIN),
				'text_nocov' : 'Define text for no covers, define before create base ({v})'.format(v=TEXT_NCO),
				'progr_logo' : 'filename logo program ({v})'.format(v=group_dbalbums['wins_icone']), 
				'pict_blank' : 'filename cover blank ({v})'.format(v=group_dbalbums['pict_blank'])
				}
				
	def __init__(self, envt, themecolor, parent=None):
		"""Init Gui, start invent"""
		super(ParamsGui, self).__init__(parent)
		self.parent = parent
		self.setupUi(self)
		self.resize(self.WIDT_MAIN, self.HEIG_MAIN-300)
		self.setWindowIcon(QIcon(self.WINS_ICO))
		self.setWindowTitle(self.TITL_PROG + path.join(self.PATH_PROG, self.FILE__INI))
		centerWidget(self)
		
		self.envits = envt
		self.ENVT_DEF = self.envits
		self.curthe = themecolor
		self.NAME_EVT, self.CURT_EVT = self.Json_params.buildListEnvt(self.envits)
		self.comboBox_Envt.addItems(self.NAME_EVT)
		self.comboBox_Envt.setCurrentIndex(self.CURT_EVT)
		self.comboBox_Envt.currentIndexChanged.connect(self.updateEnvt)
		self.tableWidget_category.cellChanged.connect(self.changeCategory)

		# General init
		self.updateTable(self.tableWidget_general, self.group_dbalbums, ['Parameters', 'Value'])
		self.tableWidget_infos.setShowGrid(False)
		self.updateTable(self.tableWidget_infos, self.HELP_LST, ['Parameters', 'Informations'])
		self.tableWidget_category.itemSelectionChanged.connect(self.updateListcategory)
		
		# run
		self.updateEnvt(True)
		self.applyTheme()
		self.show()
	
	def changeCategory(self, row, col):
		"""Modify Category"""
		QMessageBox.warning(None, "Modified Category", "albums already scanned will remain with the old name")
		#print(str(item))
		self.btn_save.setEnabled(True)

	def updateEnvt(self, refresh):
		"""change table lists content envt"""
		if self.envits != self.comboBox_Envt.currentText() or refresh:
			self.envits = self.comboBox_Envt.currentText()
			# Environment
			self.group_envt = self.Json_params.getMember(self.envits)
			self.updateTable(self.tableWidget_envt, self.group_envt, ['Parameters', 'Value'])
			# Category
			self.tableWidget_category.cellChanged.disconnect()
			self.list_category = []
			self.list_category += self.Json_params.buildCategories(self.envits)
			listcat = []
			for item in self.list_category:
				listcat.append(item[0])
			self.updateTable(self.tableWidget_category, listcat, ['Category'])
			self.tableWidget_category.cellChanged.connect(self.changeCategory)
			# list category
			self.updateListcategory()
	
	def updateListcategory(self):
		"""Insert table list content category."""
		self.curcat = self.tableWidget_category.currentRow()
		listcontent = []
		for item in self.list_category[self.curcat]:
			listcontent.append(item)
		del listcontent[0]
		self.updateTable(self.tableWidget_listcategory, listcontent, ['Mode', 'Folder Name', 'Family'])
		
	def updateTable(self, table, listitems, listcolumns):
		"""generic insert QtableWidget data"""
		#table.clear()
		table.setColumnCount(0)
		table.verticalHeader().setVisible(False)
		if listcolumns:
			table.setColumnCount(len(listcolumns))
			table.setHorizontalHeaderLabels(listcolumns)
		table.setRowCount(len(listitems))
		row = 0
		if isinstance(listitems,dict):
			for key, value in listitems.items():
				nameitem = QTableWidgetItem(key)
				codeitem = QTableWidgetItem(str(value))
				table.setItem(row,0,nameitem)			
				table.setItem(row,1,codeitem)
				row += 1
		else:
			col = 0
			for value in listitems:
				nameitem = QTableWidgetItem(str(value))			
				table.setItem(row,col,nameitem)
				if col < len(listcolumns) -1:
					col +=1
				else:
					row += 1
		table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
		table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
		table.selectRow(0)
		
	def applyTheme(self):
		"""Apply color Theme to main Gui."""
		# main
		mainstyle = 'QWidget{{background-color: {col1};}}' \
					'QLCDNumber{{border: none;color: black; background-color: {col1};}}' \
					'QScrollBar:vertical{{width: 14px;}}' \
					'QScrollBar:horizontal{{height: 14px;}}' \
					'QTableWidget::item:selected{{ background-color:{col5}; color:white;}}'
		mainstyle = mainstyle.format(col1 = self.curthe.listcolors[0],
									col2 = self.curthe.listcolors[1], 
									col5 = self.curthe.listcolors[4])
		self.setStyleSheet(mainstyle)
		gridstyle = 'alternate-background-color: {col3};background-color: {col4};'
		gridstyle = gridstyle.format(col3 = self.curthe.listcolors[2], 
									col4 = self.curthe.listcolors[3])
									
		self.tableWidget_general.setStyleSheet(gridstyle)
		self.tableWidget_envt.setStyleSheet(gridstyle)
		self.tableWidget_category.setStyleSheet(gridstyle)
		self.tableWidget_listcategory.setStyleSheet(gridstyle)

