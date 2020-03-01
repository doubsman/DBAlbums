#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from sys import platform
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QTableWidgetItem, QAbstractScrollArea, QHeaderView, 
							QMessageBox, QStyle, QInputDialog, QLineEdit, QMenu)
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
					'mask_audio' : 'list extensions audio files ({v})'.format(v=group_dbalbums['mask_audio']),
					'mask_cover' : 'list extensions pictures files ({v})'.format(v=group_dbalbums['mask_cover']),
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
		
		# list + combo envt
		self.envits = envt
		self.NAME_EVT, self.CURT_EVT = self.Json_params.buildListEnvt(self.envits)
		self.CURT_EVT = 0 
		for item in self.NAME_EVT:
			if item == self.envits:
				break
			self.CURT_EVT += 1
		self.comboBox_Envt.addItems(self.NAME_EVT)
		self.comboBox_Envt.setCurrentIndex(self.CURT_EVT)
		
		# list + combo category
		self.listcategory = self.Json_params.getMember('categories')
		self.comboBox_cate.addItems(self.listcategory)

		# font
		self.label_libgeneral.setFont(self.parent.fontbig)
		self.label_libcate.setFont(self.parent.fontbig)
		self.label_libenvt.setFont(self.parent.fontbig)

		# decos
		self.btn_save.setEnabled(False)
		self.btn_save.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
		self.btn_open.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
		self.btn_quit.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
		
		# tbl General init
		self.updateTable(self.tableWidget_general, self.Json_params.getMember('dbalbums') , ['Group', 'Parameters', 'Values', 'Informations'], False, False, 'dbalbums')
		self.updateTable(self.tableWidget_general, self.Json_params.getMember('programs') , None, True, False, 'programs')
		self.updateTable(self.tableWidget_general, self.Json_params.getMember('score') , None, True, False, 'score')
		self.updateTable(self.tableWidget_general, self.Json_params.getMember('scripts') , None, True, False, 'scripts')
		self.updateTable(self.tableWidget_general, self.Json_params.getMember('themes') , None, True, False, 'themes')
		
		# complete column help
		self.textEdit.append(self.HELP_TXT)
		row = 0
		while row < self.tableWidget_general.rowCount():
			nameitem = QTableWidgetItem(self.HELP_LST.get(self.tableWidget_general.item(row,1).text()))
			nameitem.setFlags(Qt.ItemIsEditable)
			self.tableWidget_general.setItem(row,3,nameitem)
			row += 1

		# pop up
		self.menua = QMenu()
		self.action2 = self.menua.addAction("add line", self.addLineCategory)
		self.action3 = self.menua.addAction("del line", self.delLineCategory)

		# events
		self.comboBox_cate.currentIndexChanged.connect(self.updateCategory)
		self.comboBox_Envt.currentIndexChanged.connect(self.updateEnvt)
		self.tableWidget_category.cellChanged.connect(self.changeCategory)
		self.tableWidget_category.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tableWidget_category.customContextMenuRequested.connect(self.popUpcate)
		self.tableWidget_envt.cellChanged.connect(self.changeEnvironment)
		self.tableWidget_general.cellChanged.connect(self.changeGeneral)
		self.btn_open.clicked.connect(self.openJson)
		self.btn_open.clicked.connect(self.openJson)
		self.btn_quit.clicked.connect(self.closeParams)
		self.btn_save.clicked.connect(self.writeFileJson)
		self.btn_addcate.clicked.connect(self.addCategory)
		self.btn_delcate.clicked.connect(self.delCategory)
		self.btn_addenvt.setEnabled(False)
		self.btn_delenvt.setEnabled(False)

		# run
		self.updateEnvt(True)
		self.applyTheme()
		self.show()

	def popUpcate(self, position):
		self.menua.exec_(self.tableWidget_category.viewport().mapToGlobal(position))

	def openJson(self):
		"""Open json file with text editor."""
		self.parent.execute_command(self.EDIT_TEXT, self.FILE__INI)
	
	def writeFileJson(self):
		self.Json_params.saveJson()
		self.parent.execute_command(self.EDIT_TEXT, self.FILE__INI)

	def getText(self, tittle, text):
		text, okPressed = QInputDialog.getText(self, tittle, text, QLineEdit.Normal, "")
		if okPressed and text != '':
			return text
		return None

	def addCategory(self):
		# demand new name
		self.btn_save.setEnabled(True)
		newcate = self.getText('Add Categories', 'Name :')
		if newcate is not None:
			if newcate in self.listcategory:
				QMessageBox.information(self, 'Add Categories', newcate + ' already present')
			else:
				row = len(self.listcategory)
				# add new / add list json  auto ?
				self.listcategory.append(newcate)
				# modify link category to connexion
				nameitem = QTableWidgetItem(str(newcate))
				self.tableWidget_envt.setItem(1, 1, nameitem)
				self.Json_params.data[self.comboBox_Envt.currentText()]['cate'] = newcate
				# add virgin json var
				self.Json_params.addLineCategory(newcate)
				# modify combo and new position
				self.comboBox_cate.currentIndexChanged.disconnect() 
				self.comboBox_cate.addItem(newcate)
				self.comboBox_cate.currentIndexChanged.connect(self.updateCategory)
				self.selectComboCategory(newcate)
	
	def addLineCategory(self):
		self.btn_save.setEnabled(True)
		cate = self.comboBox_cate.currentText()
		self.Json_params.addLineCategory(cate)
		self.updateCategory()

	def delCategory(self):
		self.btn_save.setEnabled(True)
		delcate = self.comboBox_cate.currentText()
		buttonReply = QMessageBox.question(self, 'Delete Category', "Delete category : " + delcate, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if buttonReply == QMessageBox.Yes:
			# modify combo and new position
			self.comboBox_cate.currentIndexChanged.disconnect() 
			self.deleteComboCategory(delcate)
			# del category json var
			del(self.Json_params.data[delcate])
			self.listcategory.remove(delcate)
			# modify link category to connexion
			self.Json_params.data[self.comboBox_Envt.currentText()]['cate'] = self.listcategory[0]
			self.comboBox_cate.currentIndexChanged.connect(self.updateCategory)
			self.comboBox_cate.setCurrentIndex(0)

	def delLineCategory(self):
		self.btn_save.setEnabled(True)
		cate = self.comboBox_cate.currentText()
		row = self.tableWidget_category.selectedIndexes()[0].row()
		self.Json_params.delLineCategory(cate, row + 1)
		self.updateCategory()
		
	def changeGeneral(self, row, col):
		"""Modify params."""
		self.btn_save.setEnabled(True)
		curItem = self.tableWidget_general.currentItem()
		# colum family param
		familypa = self.tableWidget_general.item(row,0).text()
		# column name param
		namepara = self.tableWidget_general.item(row,1).text()
		# old value param
		oldvalue = self.Json_params.getMember(familypa)[namepara]
		# value
		if isinstance(oldvalue, int):
			newvalue = int(curItem.text())
		elif isinstance(oldvalue, list):
			newvalue = curItem.text().replace('[','').replace(']','').replace("'",'').split(', ')
		else:
			newvalue = curItem.text()
		# modify param
		self.Json_params.data[familypa][namepara] = newvalue

	def changeEnvironment(self, row, col):
		"""Modify params envt."""
		self.btn_save.setEnabled(True)
		curItem = self.tableWidget_envt.currentItem()
		# value
		newvalue = curItem.text()
		# name envt
		currenvt = self.comboBox_Envt.currentText()
		# column name param
		namepara = self.tableWidget_envt.item(row,0).text()
		# envt json
		environt = self.Json_params.getMember(currenvt)
		# old value param
		oldvalue = self.Json_params.getMember(currenvt)[namepara]
		# modify param
		self.Json_params.data[currenvt][namepara] = newvalue

	def changeCategory(self, row, col):
		"""Modify Category."""
		self.btn_save.setEnabled(True)
		curItem = self.tableWidget_category.currentItem()
		# value
		newvalue = curItem.text()
		# column name
		namecolu = self.tableWidget_category.horizontalHeaderItem(self.tableWidget_category.currentItem().column()).text().lower()
		# category json
		category = self.Json_params.data[self.comboBox_cate.currentText()]['FOLDER'+format(row + 1, '03d')]
		# backup value
		oldvalue = category[namecolu]
		# modify category
		self.Json_params.data[self.comboBox_cate.currentText()]['FOLDER'+format(row + 1, '03d')][namecolu] = newvalue

	def updateEnvt(self, refresh):
		"""Change table lists content envt."""
		if self.envits != self.comboBox_Envt.currentText() or refresh:
			self.envits = self.comboBox_Envt.currentText()
			# Environment
			self.group_envt = self.Json_params.getMember(self.envits)
			self.tableWidget_envt.cellChanged.disconnect()
			self.updateTable(self.tableWidget_envt, self.group_envt, ['Parameters', 'Values'])
			# Category
			currentcate = self.tableWidget_envt.item(1,1).text()
			self.tableWidget_envt.cellChanged.connect(self.changeEnvironment)
			# select combo catergory
			self.selectComboCategory(currentcate)

	def selectComboCategory(self, cate):
		# select combo catergory
		indexcate = 0 
		for item in self.listcategory:
			if item == cate:
				break
			indexcate += 1
		self.comboBox_cate.setCurrentIndex(indexcate)
		if indexcate == 0:
			self.updateCategory()

	def deleteComboCategory(self, cate):
		# select combo catergory
		indexcate = 0 
		for item in self.listcategory:
			if item == cate:
				break
			indexcate += 1
		self.comboBox_cate.removeItem(indexcate)

	def updateCategory(self):
		"""Change table lists content category."""
		self.tableWidget_category.cellChanged.disconnect()
		self.tableWidget_category.setRowCount(0)
		# lien envt cate
		for envt in self.NAME_EVT:
			if self.comboBox_cate.currentText() == self.Json_params.getMember(envt)['cate']:
				break
		self.content_category = self.Json_params.buildListcategory(envt)
		listcat = []
		for itemd in self.content_category:
			for item in itemd:
				listcat.append(item)
		self.updateTable(self.tableWidget_category, listcat, ['Style', 'Mode', 'Folder', 'Family'])#, False, True)
		self.tableWidget_category.cellChanged.connect(self.changeCategory)

	def updateTable(self, table, listitems, listcolumns, add = False, ajustlastcolumn = False, groupjson = None):
		"""generic insert QtableWidget data"""
		if not add:
			# init table
			#table.clear()
			table.setRowCount(0)
			table.setColumnCount(0)
			table.verticalHeader().setDefaultSectionSize(self.C_HEIGHT)
			table.verticalHeader().setVisible(False)
			if listcolumns:
				table.setColumnCount(len(listcolumns))
				table.setHorizontalHeaderLabels(listcolumns)
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
				# column no editable
				nameitem.setFlags(Qt.ItemIsEditable)
				codeitem = QTableWidgetItem(str(value))
				if groupjson:
					grpsitem = QTableWidgetItem(str(groupjson))
					grpsitem.setFlags(Qt.ItemIsEditable)
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
				if value is None:
					value= ''
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
		self.tableWidget_general.setStyleSheet(gridstyle)
		self.tableWidget_envt.setStyleSheet(gridstyle)
		self.tableWidget_category.setStyleSheet(gridstyle)

	def closeParams(self):
		"""Close Windows."""
		self.destroy()
