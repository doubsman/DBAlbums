#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from sys import platform
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import qDebug
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QAbstractScrollArea, QHeaderView, QMessageBox, QStyle
from DBFileJson import JsonParams
from Ui_DBPARAMS import Ui_ParamsJson


class ParamsGui(QWidget, Ui_ParamsJson):
	"""Display GUI file Json parameters."""

	def __init__(self, parent, envt, fileini):
		"""Init Gui, start invent"""
		super(ParamsGui, self).__init__()
		self.parent = parent
		self.setupUi(self)

		# init Json VAR
		self.PATH_PROG = path.dirname(path.abspath(__file__))
		self.LOGS_PROG = path.join(self.PATH_PROG, 'LOG')
		self.C_HEIGHT = 25
		# Read File DBAlbums.json
		qDebug('ParamsGui: read json params file')
		self.FILE__INI = fileini
		self.Json_params = JsonParams(self.FILE__INI)
		
		group_programs = self.Json_params.getMember('programs')
		if platform == "darwin" or platform == 'linux':
			self.EDIT_TEXT = r'' + group_programs['txt_lin']
		else:
			self.EDIT_TEXT = r'' + group_programs['txt_win']
		group_dbalbums = self.Json_params.getMember('dbalbums')
		group_scorealb = self.Json_params.buildDictScore()
		self.VERS_PROG = group_dbalbums['prog_build']
		self.TITL_PROG = "DBAlbums v{v} (2020)".format(v=self.VERS_PROG)
		self.TITL_PROG += " : Environments Parameters "
		self.WIDT_MAIN = group_dbalbums['wgui_width']
		self.HEIG_MAIN = group_dbalbums['wgui_heigh']
		self.WIDT_PICM = group_dbalbums['thun_csize']
		self.WINS_ICO = path.join(self.PATH_PROG, 'IMG', group_dbalbums['wins_icone'])
		self.THEM_COL = group_dbalbums['name_theme']
		self.TEXT_NCO = group_dbalbums['text_nocov']
		self.FONT_CON = group_dbalbums['font01_ttx']
		self.HELP_LST = {'prog_build' : 'version program ({v})'.format(v=self.VERS_PROG),
					'wgui_width' : 'width pixels main windows ({v})'.format(v=self.WIDT_MAIN),
					'wgui_heigh' : 'height pixels main windows ({v})'.format(v=self.HEIG_MAIN),
					'text_nocov' : 'Define text for no covers ({v})'.format(v=self.TEXT_NCO),
					'progr_logo' : 'filename logo program ({v})'.format(v=group_dbalbums['progr_logo']),
					'wins_icone' : 'filename icone program ({v})'.format(v=group_dbalbums['wins_icone']),
					'pict_blank' : 'filename cover blank ({v})'.format(v=group_dbalbums['pict_blank']),
					'picm_endof' : 'last thunbnails display ({v})'.format(v=group_dbalbums['picm_endof']),
					'envt_deflt' : 'default environment ({v})'.format(v=group_dbalbums['envt_deflt']),
					'covers_siz' : 'size pixels of cover display ({v})'.format(v=group_dbalbums['covers_siz']),
					'thun_csize' : 'size pixels scare thunbnails ({v})'.format(v=group_dbalbums['thun_csize']),
					'thnail_dis' : 'number of thunbnails displaying ({v})'.format(v=group_dbalbums['thnail_dis']),
					'thnail_nbl' : 'number of lines thunbnails displaying ({v})'.format(v=group_dbalbums['thnail_nbl']),
					'thnail_nod' : 'display covers thunbnails 1 or 0 ({v})'.format(v=group_dbalbums['thnail_nod']),
					'font00_ttx' : 'name font general text for windows ({v})'.format(v=group_dbalbums['font00_ttx']),
					'font00_unx' : 'name font general text for linux ({v})'.format(v=group_dbalbums['font00_unx']),
					'font01_ttx' : 'name font consol execution ({v})'.format(v=group_dbalbums['font01_ttx']),
					'font00_siz' : 'size font main ({v})'.format(v=group_dbalbums['font00_siz']),
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
		self.HELP_TXT = "Category\n"
		self.HELP_TXT +="- Name : name (rock, classic...)\n"
		self.HELP_TXT +="- Mode : D (double tree folder) or S = (simple tree folder)\n"
		self.HELP_TXT +="- Folder : music location folder\n"
		self.HELP_TXT +="- Family : name (physique, web, vynils)\n"
	
		self.resize(self.WIDT_MAIN, self.HEIG_MAIN - 250)
		self.setWindowIcon(QIcon(self.WINS_ICO))
		self.setWindowTitle(self.TITL_PROG + path.join(self.PATH_PROG, self.FILE__INI))
		self.parent.centerWidget(self)
		
		self.envits = envt
		self.ENVT_DEF = self.envits
		self.NAME_EVT, self.CURT_EVT = self.Json_params.buildListEnvt(self.envits)
		self.CURT_EVT = self.parent.curthe
		self.comboBox_Envt.addItems(self.NAME_EVT)
		self.comboBox_Envt.setCurrentIndex(self.CURT_EVT)
		
		# decos
		self.btn_save.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
		self.btn_open.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
		self.btn_quit.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
		
		# events
		self.comboBox_Envt.currentIndexChanged.connect(self.updateEnvt)
		self.tableWidget_category.cellChanged.connect(self.changeCategory)
		self.btn_open.clicked.connect(self.openJson)
		self.btn_quit.clicked.connect(self.closeParams)
		self.btn_save.clicked.connect(self.writeFileJson)
		#self.tableWidget_category.itemSelectionChanged.connect(self.updateListcategory)
		
		# tbl General init
		self.updateTable(self.tableWidget_general, group_dbalbums , ['Group', 'Parameters', 'Values', 'Informations'], False, False, 'dbalbums')
		self.updateTable(self.tableWidget_general, group_programs , None, True, False, 'programs')
		self.updateTable(self.tableWidget_general, group_scorealb , None, True, False, 'score')
		
		# complete column help
		self.textEdit.append(self.HELP_TXT)
		row = 0
		while row < self.tableWidget_general.rowCount():
			nameitem = QTableWidgetItem(self.HELP_LST.get(self.tableWidget_general.item(row,1).text()))
			self.tableWidget_general.setItem(row,3,nameitem)
			row += 1

		self.modifydate = False

		# run
		self.updateEnvt(True)
		self.applyTheme()
		self.show()
		
	def openJson(self):
		"""Open json file with text editor."""
		self.parent.execute_command(self.EDIT_TEXT, self.FILE__INI)
	
	def writeFileJson(self):
		self.Json_params.saveJson()
		
	def changeCategory(self, row, col):
		"""Modify Category"""
		curItem = self.tableWidget_category.currentItem()
		QMessageBox.warning(None, "Modified Category", "albums already scanned will remain with the old name\n"
								+ "row:"+str(row)+" col:"+str(col)+' txt:'+curItem.text())
		print("row:"+str(row)+" col:"+str(col)+' txt:'+curItem.text())
		self.btn_save.setEnabled(True)

	def updateEnvt(self, refresh):
		"""Change table lists content envt + category"""
		if self.envits != self.comboBox_Envt.currentText() or refresh:
			self.envits = self.comboBox_Envt.currentText()
			# Environment
			self.group_envt = self.Json_params.getMember(self.envits)
			self.updateTable(self.tableWidget_envt, self.group_envt, ['Parameters', 'Values'])
			# Category
			currentcate = self.tableWidget_envt.item(1,1).text()
			self.label_cate.setText("Category : " + currentcate + " ")
			self.tableWidget_category.cellChanged.disconnect()
			self.list_category = []
			self.list_category += self.Json_params.buildListcategory(self.envits)
			listcat = []
			for itemd in self.list_category:
				for item in itemd:
					listcat.append(item)
			self.updateTable(self.tableWidget_category, listcat, ['Category', 'Mode', 'Folder Name', 'Family'])#, False, True)
			self.tableWidget_category.cellChanged.connect(self.changeCategory)
		
	def updateTable(self, table, listitems, listcolumns, add = False, ajustlastcolumn = False, groupjson = None):
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
				if groupjson:
					grpsitem = QTableWidgetItem(str(groupjson))
					table.setItem(row,0,grpsitem)
					table.setItem(row,1,nameitem)			
					table.setItem(row,2,codeitem)
				else:
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
					'QComboBox{{background-color: {col2};}}' \
					'QScrollBar:vertical{{width: 14px;}}' \
					'QScrollBar:horizontal{{height: 14px;}}' \
					'QTableWidget::item:selected{{ background-color:{col5}; color:white;}}'
		mainstyle = mainstyle.format(col1 = self.parent.listcolors[0],
									col2 = self.parent.listcolors[1], 
									col5 = self.parent.listcolors[4])
		self.setStyleSheet(mainstyle)
		gridstyle = 'alternate-background-color: {col3};background-color: {col4};'
		gridstyle = gridstyle.format(col3 = self.parent.listcolors[2], 
									col4 = self.parent.listcolors[3])
									
		self.tableWidget_general.setStyleSheet(gridstyle)
		self.tableWidget_envt.setStyleSheet(gridstyle)
		self.tableWidget_category.setStyleSheet(gridstyle)

	def closeParams(self):
		"""Close Windows."""
		self.destroy()
