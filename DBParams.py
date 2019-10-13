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
	C_HEIGHT = 25
	# Read File DBAlbums.json
	qDebug('read json params file')
	FILE__INI = 'DBAlbums.json'
	Json_params = JsonParams(FILE__INI)
	
	group_programs = Json_params.getMember('programs')
	group_dbalbums = Json_params.getMember('dbalbums')
	group_scorealb = Json_params.buildDictScore()
	VERS_PROG = group_dbalbums['prog_build']
	TITL_PROG = "DBAlbums v{v} (2019)".format(v=VERS_PROG)
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
				'text_nocov' : 'Define text for no covers ({v})'.format(v=TEXT_NCO),
				'progr_logo' : 'filename logo program ({v})'.format(v=group_dbalbums['progr_logo']),
				'wins_icone' : 'filename icone program ({v})'.format(v=group_dbalbums['wins_icone']),
				'pict_blank' : 'filename cover blank ({v})'.format(v=group_dbalbums['pict_blank']),
				'picm_endof' : 'last thunbnails display ({v})'.format(v=group_dbalbums['picm_endof']),
				'envt_deflt' : 'default environment loading at start ({v})'.format(v=group_dbalbums['envt_deflt']),
				'covers_siz' : 'size pixels of cover display ({v})'.format(v=group_dbalbums['covers_siz']),
				'thun_csize' : 'size pixels scare thunbnails ({v})'.format(v=group_dbalbums['thun_csize']),
				'thnail_dis' : 'number of thunbnails displaying ({v})'.format(v=group_dbalbums['thnail_dis']),
				'thnail_nbl' : 'number of lines thunbnails displaying ({v})'.format(v=group_dbalbums['thnail_nbl']),
				'thnail_nod' : 'display covers thunbnails 1 or 0 ({v})'.format(v=group_dbalbums['thnail_nod']),
				'font00_ttx' : 'name font general text ({v})'.format(v=group_dbalbums['font00_ttx']),
				'font01_ttx' : 'name font consol execution ({v})'.format(v=group_dbalbums['font01_ttx']),
				'name_theme' : 'style colors (blue, green, brown, grey, pink) ({v})'.format(v=group_dbalbums['name_theme']),
				'txt_win' : '<program> text editor Windows',
				'txt_lin' : '<program> text editor Debian',
				'tagscan' : '<program> program extern for tags',
				'foobarP' : '<program> folder playlists foobar2000',
				'discogs' : '<program> url search album from discogs',
				'0' : '<score> label notation display',
				'1' : '<score> label notation display',
				'2' : '<score> label notation display',
				'3' : '<score> label notation display'
				}
				
	def __init__(self, envt, themecolor, parent=None):
		"""Init Gui, start invent"""
		super(ParamsGui, self).__init__(parent)
		self.parent = parent
		self.setupUi(self)
		self.resize(self.WIDT_MAIN, self.HEIG_MAIN - 250)
		self.setWindowIcon(QIcon(self.WINS_ICO))
		self.setWindowTitle(self.TITL_PROG + path.join(self.PATH_PROG, self.FILE__INI))
		centerWidget(self)
		
		self.envits = envt
		self.ENVT_DEF = self.envits
		self.curthe = themecolor
		self.NAME_EVT, self.CURT_EVT = self.Json_params.buildListEnvt(self.envits)
		self.comboBox_Envt.addItems(self.NAME_EVT)
		self.comboBox_Envt.setCurrentIndex(self.CURT_EVT)
		
		# events
		self.comboBox_Envt.currentIndexChanged.connect(self.updateEnvt)
		self.tableWidget_category.cellChanged.connect(self.changeCategory)
		self.btn_quit.clicked.connect(self.closeParams)
		#self.tableWidget_category.itemSelectionChanged.connect(self.updateListcategory)
		
		# General init
		self.updateTable(self.tableWidget_general, self.group_dbalbums , ['Parameters', 'Values', 'Informations'])
		self.updateTable(self.tableWidget_general, self.group_programs , None, True)
		self.updateTable(self.tableWidget_general, self.group_scorealb , None, True)
		
		# complete column help
		row = 0
		while row < self.tableWidget_general.rowCount():
			nameitem = QTableWidgetItem(self.HELP_LST.get(self.tableWidget_general.item(row,0).text()))
			self.tableWidget_general.setItem(row,2,nameitem)
			row += 1
	
		# run
		self.updateEnvt(True)
		self.applyTheme()
		self.show()
	
	def changeCategory(self, row, col):
		"""Modify Category"""
		curItem = self.tableWidget_category.currentItem()
		QMessageBox.warning(None, "Modified Category", "albums already scanned will remain with the old name\n"
								+ "row:"+str(row)+" col:"+str(col)+' txt:'+curItem.text())
		print("row:"+str(row)+" col:"+str(col)+' txt:'+curItem.text())
		self.btn_save.setEnabled(True)

	def updateEnvt(self, refresh):
		"""change table lists content envt"""
		if self.envits != self.comboBox_Envt.currentText() or refresh:
			self.envits = self.comboBox_Envt.currentText()
			# Environment
			self.group_envt = self.Json_params.getMember(self.envits)
			self.updateTable(self.tableWidget_envt, self.group_envt, ['Parameters', 'Values'], False, True)
			# Category
			currentcate = self.tableWidget_envt.item(1,1).text()
			self.label_cate.setText("Category : " + currentcate + " ")
			self.tableWidget_category.cellChanged.disconnect()
			self.list_category = []
			self.list_category += self.Json_params.buildCategories(self.envits)
			listcat = []
			for itemd in self.list_category:
				for item in itemd:
					listcat.append(item)
			self.updateTable(self.tableWidget_category, listcat, ['Category', 'Mode', 'Folder Name', 'Family'])
			self.tableWidget_category.cellChanged.connect(self.changeCategory)
		
	def updateTable(self, table, listitems, listcolumns, add=False, ajustlastcolumn=False):
		"""generic insert QtableWidget data"""
		if not add:
			# init table
			#table.clear()
			table.setColumnCount(0)
			table.verticalHeader().setDefaultSectionSize(self.C_HEIGHT)
			table.verticalHeader().setVisible(False)
			if listcolumns:
				table.setColumnCount(len(listcolumns))
				table.setHorizontalHeaderLabels(listcolumns)
			else:
				qDebug('First create table desire liscolumns')
			row = 0
		else:
			# add rows
			row = table.rowCount()
			if listcolumns:
				listcolumns = [[] * table.columnCount()]
		if isinstance(listitems,dict):
			# dict format
			table.setRowCount(len(listitems) + row)
			for key, value in listitems.items():
				nameitem = QTableWidgetItem(str(key))
				codeitem = QTableWidgetItem(str(value))
				table.setItem(row,0,nameitem)			
				table.setItem(row,1,codeitem)
				row += 1
		else:
			# array format
			table.setRowCount(len(listitems) / len(listcolumns) + row)
			col = 0
			for value in listitems:
				nameitem = QTableWidgetItem(str(value))			
				table.setItem(row,col,nameitem)
				if col < len(listcolumns) -1:
					col +=1
				else:
					row += 1
					col = 0
		if ajustlastcolumn:
			table.horizontalHeader().setStretchLastSection(True)
		table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
		table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
		table.selectRow(0)
	
	def applyTheme(self):
		"""Apply color Theme to main Gui."""
		# main
		mainstyle = 'QWidget{{background-color: {col1};}}' \
					'QLCDNumber{{border: none;color: black; background-color: {col1};}}' \
					'QComboBox{{background-color: {col2};}}' \
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

	def closeParams(self):
		self.destroy()
