#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, getcwd
from sys import platform
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QTableWidgetItem, QAbstractScrollArea, QHeaderView, 
							QMessageBox, QFileDialog, QStyle, QInputDialog, QLineEdit, QMenu)
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
		self.RESS_ICOS = path.join(self.PATH_PROG, 'ICO')
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
		self.HELP_GENE = {'prog_build' : 'version program ({v})'.format(v=self.VERS_PROG),
					'wgui_width' : 'width pixels main windows ({v})'.format(v=self.WIDT_MAIN),
					'wgui_heigh' : 'height pixels main windows ({v})'.format(v=self.HEIG_MAIN),
					'text_nocov' : 'Define text for no covers ({v})'.format(v=self.TEXT_NCO),
					'progr_logo' : 'filename logo program ({v})'.format(v=group_dbalbums['progr_logo']),
					'wins_icone' : 'filename icone program ({v})'.format(v=group_dbalbums['wins_icone']),
					'pict_blank' : 'filename cover blank ({v})'.format(v=group_dbalbums['pict_blank']),
					'envt_deflt' : 'default environment ({v})'.format(v=group_dbalbums['envt_deflt']),
					'covers_siz' : 'size pixels of cover display ({v})'.format(v=group_dbalbums['covers_siz']),
					'thun_csize' : 'size pixels scare thunbnails ({v})'.format(v=group_dbalbums['thun_csize']),
					'thnail_dis' : 'number of thunbnails displaying ({v})'.format(v=group_dbalbums['thnail_dis']),
					'thnail_nbl' : 'number of max lines thunbnails displaying ({v})'.format(v=group_dbalbums['thnail_nbl']),
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
		self.HELP_CATE = "Category\n"
		self.HELP_CATE +="- Style : name (rock, classic...)\n"
		self.HELP_CATE +="- Mode S/D : Simple or Double tree folder\n"
		self.HELP_CATE +="           define column family\n"
		self.HELP_CATE +="- Mode T : Triple tree folder\n"
		self.HELP_CATE +="           define table family\n"
		self.HELP_CATE +="           raci [T]\n"
		self.HELP_CATE +="             └subfolders : family tab filter\n"
		self.HELP_CATE +="               └subfolders\n"
		self.HELP_CATE +="                 └folders albums\n"
		self.HELP_CATE +="- Folder : parameter[raci] + [Folder]\n"
		self.HELP_CATE +="- Family : name (physique, web, vinyls)\n"
		self.resize(self.WIDT_MAIN, self.HEIG_MAIN - 250)
		self.setWindowIcon(QIcon(self.WINS_ICO))
		self.setWindowTitle(self.TITL_PROG + path.join(self.PATH_PROG, self.FILE__INI))
		self.parent.centerWidget(self)
		
		# list + combo envt
		self.envits = envt
		self.NAME_EVT, self.CURT_EVT = self.Json_params.buildListEnvt(self.envits)
		self.CURT_EVT = self.parent.CURT_EVT
		self.comboBox_Envt.addItems(self.NAME_EVT)
		self.comboBox_Envt.setCurrentIndex(self.CURT_EVT)
		
		# list + combo category
		self.listcategory = self.Json_params.jsonlistcategories
		self.comboBox_cate.addItems(self.listcategory)

		# font
		font = QFont()
		font.setFamily("Calibri")
		font.setFixedPitch(True)
		font.setPointSize(8)
		self.label_libgeneral.setFont(self.parent.fontbig)
		self.label_libcate.setFont(self.parent.fontbig)
		self.label_libenvt.setFont(self.parent.fontbig)
		self.label_libfamily.setFont(self.parent.fontbig)
		self.textEdit_cate.setFont(font)

		# decos
		self.btn_save.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
		self.btn_load.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
		self.btn_open.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
		self.btn_quit.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
		self.btn_delenvt.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))
		self.btn_delcate.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))
		self.btn_addenvt.setIcon(self.style().standardIcon(QStyle.SP_TitleBarNormalButton))
		self.btn_addcate.setIcon(self.style().standardIcon(QStyle.SP_TitleBarNormalButton))
		
		# pop up
		self.menua = QMenu()
		self.action2 = self.menua.addAction(QIcon(path.join(self.RESS_ICOS, 'more.png')),"add line", self.addLineCategory)
		self.action3 = self.menua.addAction(QIcon(path.join(self.RESS_ICOS, 'less.png')),"del line", self.delLineCategory)
		self.menub = QMenu()
		self.action4 = self.menub.addAction(QIcon(path.join(self.RESS_ICOS, 'more.png')),"add line", self.addLineFamily)
		self.action5 = self.menub.addAction(QIcon(path.join(self.RESS_ICOS, 'less.png')),"del line", self.delLineFamily)

		# events
		self.comboBox_cate.currentIndexChanged.connect(self.updateCategory)
		self.comboBox_Envt.currentIndexChanged.connect(self.updateEnvt)
		self.tableWidget_category.cellChanged.connect(self.changeCategory)
		self.tableWidget_category.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tableWidget_category.customContextMenuRequested.connect(self.popUpcate)
		self.tableWidget_envt.cellChanged.connect(self.changeEnvironment)
		self.tableWidget_general.cellChanged.connect(self.changeGeneral)
		self.tableWidget_family.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tableWidget_family.customContextMenuRequested.connect(self.popUpfami)
		self.tableWidget_family.cellChanged.connect(self.changeFamily)
		self.btn_open.clicked.connect(self.openJson)
		self.btn_open.clicked.connect(self.openJson)
		self.btn_quit.clicked.connect(self.closeParams)
		self.btn_save.clicked.connect(self.writeFileJson)
		self.btn_load.clicked.connect(self.loadFileJson)
		self.btn_addcate.clicked.connect(self.addCategory)
		self.btn_delcate.clicked.connect(self.delCategory)
		self.btn_addenvt.clicked.connect(self.addEnvironment)
		self.btn_delenvt.clicked.connect(self.delEnvironment)

		# run
		self.updateFamily()
		self.updateGeneral()
		self.updateEnvt(True)
		self.applyTheme()
		self.show()

	def popUpcate(self, position):
		self.menua.exec_(self.tableWidget_category.viewport().mapToGlobal(position))

	def popUpfami(self, position):
		self.menub.exec_(self.tableWidget_family.viewport().mapToGlobal(position))

	def openJson(self):
		"""Open json file with text editor."""
		self.parent.execute_command(self.EDIT_TEXT, self.FILE__INI)
	
	def writeFileJson(self):
		buttonReply = QMessageBox.question(self, 'Save modifications', "Create new file configuration ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if buttonReply == QMessageBox.Yes:
			oldjson, newjson = self.Json_params.saveJson()
			QMessageBox.information(self, 'Save Configuration', 'Configuration succes write to :' + newjson + '\nOld file config backup to : ' + oldjson)

	def loadFileJson(self):
		file_json = QFileDialog.getOpenFileName(self,
								"Load file configuration Json format",
								getcwd(),
								"Json (*.json)")
		file_json = file_json[0]
		if path.isfile(str(file_json)):
			self.Json_params.reloadJson(file_json)
			self.updateFamily()
			self.updateGeneral()
			self.updateEnvt(False)
			QMessageBox.information(self, 'Load Configuration', 'Configuration succes from :' + file_json)

	def getText(self, tittle, text):
		text, okPressed = QInputDialog.getText(self, tittle, text, QLineEdit.Normal, "")
		if okPressed and text != '':
			return text
		return None

	def addEnvironment(self):
		# demand new name
		newenvt = self.getText('Add Environment', 'Name :')
		if newenvt is not None:
			if newenvt in self.NAME_EVT:
				QMessageBox.information(self, 'No Add, Environment', newenvt + ' already present')
			else:
				# add virgin json var
				self.Json_params.addEnvt(newenvt)
				# add category default
				self.Json_params.modJsonEnvt(newenvt, 'cate', self.comboBox_cate.currentText())
				# modify combo and new position
				self.comboBox_Envt.currentIndexChanged.disconnect() 
				self.comboBox_Envt.addItem(newenvt)
				self.NAME_EVT.append(newenvt)
				self.envits = newenvt
				self.comboBox_Envt.currentIndexChanged.connect(self.updateEnvt)
				self.selectComboEnvt(newenvt)

	def delEnvironment(self):
		delenvt = self.comboBox_Envt.currentText()
		buttonReply = QMessageBox.question(self, 'Delete Environment', "Delete Environment : " + delenvt, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if buttonReply == QMessageBox.Yes:
			# modify combo and new position
			self.comboBox_Envt.currentIndexChanged.disconnect() 
			self.deleteComboEnvironment(delenvt)
			self.Json_params.delEnvt(delenvt)
			self.comboBox_Envt.currentIndexChanged.connect(self.updateEnvt)
			self.comboBox_Envt.setCurrentIndex(0)

	def addCategory(self):
		# demand new name
		newcate = self.getText('Add Categories', 'Name :')
		if newcate is not None:
			if newcate in self.listcategory:
				QMessageBox.information(self, 'Add Categories', newcate + ' already present')
			else:
				row = len(self.listcategory)
				# modify link category to connexion tablewidget
				nameitem = QTableWidgetItem(str(newcate))
				self.tableWidget_envt.setItem(1, 1, nameitem)
				self.Json_params.modJsonEnvt(self.comboBox_Envt.currentText(), 'cate', newcate)
				# add virgin json var
				self.Json_params.addCategory(newcate)
				# add list category
				self.listcategory.append(newcate)
				# modify combo and new position
				self.comboBox_cate.currentIndexChanged.disconnect() 
				self.comboBox_cate.addItem(newcate)
				self.comboBox_cate.currentIndexChanged.connect(self.updateCategory)
				self.selectComboCategory(newcate)
	
	def addLineCategory(self):
		cate = self.comboBox_cate.currentText()
		self.Json_params.addLineCategory(cate)
		self.updateCategory()

	def delCategory(self):
		delcate = self.comboBox_cate.currentText()
		buttonReply = QMessageBox.question(self, 'Delete Category', "Delete category : " + delcate, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if buttonReply == QMessageBox.Yes:
			# modify combo and new position
			self.comboBox_cate.currentIndexChanged.disconnect() 
			self.deleteComboCategory(delcate)
			self.Json_params.delCategory(delcate)
			# modify link category to connexion tablewidget
			newcate = self.listcategory[0]
			nameitem = QTableWidgetItem(str(newcate))
			self.tableWidget_envt.setItem(1, 1, nameitem)
			# modify  category json var
			self.Json_params.modJsonEnvt(self.comboBox_Envt.currentText(), 'cate', newcate)
			self.comboBox_cate.currentIndexChanged.connect(self.updateCategory)
			self.comboBox_cate.setCurrentIndex(0)

	def delLineCategory(self):
		cate = self.comboBox_cate.currentText()
		try:
			row = self.tableWidget_category.selectedIndexes()[0].row()
			self.Json_params.delLineCategory(cate, row + 1)
			self.updateCategory()
		except:
			pass

	def addLineFamily(self):
		self.Json_params.addFami('<family name>')
		self.updateFamily()

	def delLineFamily(self):
		try:
			row = self.tableWidget_family.selectedIndexes()[0].row()
			# key
			key = self.tableWidget_family.item(row,0).text()
			self.Json_params.delFami(key)
			self.updateFamily()
		except:
			pass

	def changeGeneral(self, row, col):
		"""Modify params."""
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
		self.Json_params.modJsonGeneral(familypa, namepara, newvalue)

	def changeEnvironment(self, row, col):
		"""Modify params envt."""
		curItem = self.tableWidget_envt.currentItem()
		# value
		newvalue = curItem.text()
		# name envt
		currenvt = self.comboBox_Envt.currentText()
		# column name param
		namepara = self.tableWidget_envt.item(row,0).text()
		# modify param
		self.Json_params.modJsonEnvt(currenvt, namepara, newvalue)

	def changeCategory(self, row, col):
		"""Modify Category."""
		curItem = self.tableWidget_category.currentItem()
		# value
		newvalue = curItem.text()
		# column name
		namecolu = self.tableWidget_category.horizontalHeaderItem(self.tableWidget_category.currentItem().column()).text().lower()
		# category json
		category = self.Json_params.getContentMember('categories', self.comboBox_cate.currentText())['folder'+format(row + 1, '03d')]
		# backup value
		# oldvalue = category[namecolu]
		# modify category
		self.Json_params.modJsonCate(self.comboBox_cate.currentText(), 'folder'+format(row + 1, '03d'), namecolu, newvalue)

	def changeFamily(self, row, col):
		"""Modify Family."""
		curItem = self.tableWidget_family.currentItem()
		# value
		newvalue = curItem.text()
		# backup value
		oldvalue = self.Json_params.getContentMember('family')
		# modify family
		self.Json_params.modJsonFami(row, col, newvalue, oldvalue)

	def selectComboEnvt(self, envt):
		"""Select combo environment."""
		indexenvt = self.NAME_EVT.index(envt)
		self.comboBox_Envt.setCurrentIndex(indexenvt)
		if indexenvt == 0:
			self.updateEnvt()

	def selectComboCategory(self, cate):
		"""Select combo catergory."""
		indexcate = self.listcategory.index(cate)
		self.comboBox_cate.setCurrentIndex(indexcate)
		if indexcate == 0:
			self.updateCategory()

	def deleteComboCategory(self, cate):
		"""Select combo catergory."""
		indexcate = self.listcategory.index(cate)
		self.comboBox_cate.removeItem(indexcate)

	def deleteComboEnvironment(self, envt):
		"""Select combo catergory."""
		indexenvt = self.NAME_EVT.index(envt)
		self.comboBox_Envt.removeItem(indexenvt)

	def updateGeneral(self):
		self.tableWidget_general.cellChanged.disconnect()
		self.tableWidget_general.setRowCount(0)		
		# tbl General init
		self.updateTable(self.tableWidget_general, self.Json_params.getMember('dbalbums') , ['Group', 'Parameters', 'Values', 'Informations'], False, False, 'dbalbums')
		self.updateTable(self.tableWidget_general, self.Json_params.getMember('programs') , None, True, False, 'programs')
		self.updateTable(self.tableWidget_general, self.Json_params.getMember('score') , None, True, False, 'score')
		self.updateTable(self.tableWidget_general, self.Json_params.getMember('scripts') , None, True, False, 'scripts')
		self.updateTable(self.tableWidget_general, self.Json_params.getMember('themes') , None, True, False, 'themes')
		# complete column help
		self.textEdit_cate.append(self.HELP_CATE)
		row = 0
		while row < self.tableWidget_general.rowCount():
			nameitem = QTableWidgetItem(self.HELP_GENE.get(self.tableWidget_general.item(row,1).text()))
			nameitem.setFlags(Qt.ItemIsEditable)
			self.tableWidget_general.setItem(row, 3, nameitem)
			row += 1
		self.tableWidget_general.cellChanged.connect(self.changeGeneral)

	def updateEnvt(self, refresh):
		"""Change table lists content envt."""
		if self.envits != self.comboBox_Envt.currentText() or refresh:
			self.envits = self.comboBox_Envt.currentText()
			# Environment
			self.group_envt = self.Json_params.getContentMember('environments', self.envits)
			self.tableWidget_envt.cellChanged.disconnect()
			self.updateTable(self.tableWidget_envt, self.group_envt, ['Parameters', 'Values'], False, True)
			# Category
			currentcate = self.tableWidget_envt.item(1,1).text()
			self.tableWidget_envt.cellChanged.connect(self.changeEnvironment)
			# select combo catergory
			self.selectComboCategory(currentcate)

	def updateCategory(self):
		"""Change table lists content category."""
		self.tableWidget_category.cellChanged.disconnect()
		self.tableWidget_category.setRowCount(0)
		listcat = []
		#listcolumns = ['Style', 'Mode', 'Folder', 'Family']
		listcolumns = list(self.Json_params.getContentMember('categories', self.comboBox_cate.currentText())['folder001'].keys())
		row = 0
		for col in listcolumns:
			listcolumns[row] = listcolumns[row].title()
			row += 1
		self.content_category =	self.Json_params.getContentMember('categories', self.comboBox_cate.currentText())
		for key, value in self.content_category.items():
			for key in listcolumns:
				listcat.append(value[key.lower()])
		self.updateTable(self.tableWidget_category, listcat, listcolumns, False, True)
		self.tableWidget_category.cellChanged.connect(self.changeCategory)

	def updateFamily(self):
		"""Change table lists content family."""
		listcolumns = ['Family Name', 'Folder content']
		self.tableWidget_family.cellChanged.disconnect()
		listcat = []
		self.tableWidget_family.setRowCount(0)
		for key, value in self.Json_params.getMember('families').items():
			listcat.append(key)
			listcat.append(value)
		self.updateTable(self.tableWidget_family, listcat, listcolumns, False, True)
		self.tableWidget_family.cellChanged.connect(self.changeCategory)

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

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.closeParams()

	def closeParams(self):
		"""Close Windows."""
		self.destroy()
