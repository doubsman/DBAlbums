#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from PyQt5.QtCore import (Qt, QVariant, qDebug, QSettings, QAbstractTableModel, QModelIndex,
						QSortFilterProxyModel, pyqtSignal)
from PyQt5.QtSql import QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from PyQt5.QtGui import QColor
from DBDatabase import connectDatabase, getrequest, buildTabFromRequest
from DBFunction import displayCounters
#from DBModeldat import ModelTableAlbums

FILE__INI = 'DBAlbums.ini'
configini = QSettings(FILE__INI, QSettings.IniFormat)
configini.beginGroup('dbalbums')
TEXT_NCO = configini.value('text_nocov')
THUN_NOD = int(configini.value('thnail_nod'))
DISP_CJOKER = configini.value('text_joker')
configini.endGroup()


# MODEL TABLE, no production
class ModelDBTable(QSqlTableModel):
	"""Model generique."""
	def __init__(self, parent, table):
		super(ModelDBTable, self).__init__(parent)
		self.parent = parent
		self.setTable(table)
		
	def headerData(self, section, orientation, role=Qt.DisplayRole):
		"""Set the name list to column name."""
		if role==Qt.SizeHintRole and orientation == Qt.Vertical:
			pass
		if role != Qt.DisplayRole:
			return QVariant()
		if orientation == Qt.Horizontal:
			return (self.record().fieldName(section))
			#return str(self.columns[section])
		return QVariant()
		
	def getData(self, row, colname):
		if self.rowCount() > 0:
			return self.data(self.index(row, self.myindex.index(colname)))
		return QVariant()
	
	def getSum(self, colname):
		if self.rowCount() > 0:
			total = 0
			for row in range(self.rowCount()):
				value = self.data(self.index(row, self.myindex.index(colname)))
				if isinstance(value, int) is False:
					if len(value.split(':')) > 1:
						value = sum(int(x) * 60 ** i for i, x in enumerate(reversed(value.split(':'))))
				total += int(value)
			return total
		return QVariant()


class ProxyModel(QSortFilterProxyModel):
	
	def __init__(self, parent):
		"""Init proxy model."""
		super(ProxyModel, self).__init__(parent)
		self.parent = parent
		self.filttext = ''
		self.filtcate = ''
		self.filtfami = ''
		self.filtyear = ''
		self.filtlabl = ''
		self.filtintk = ''
		self.listid = []
		self.cpt_siz = 0
		self.cpt_len = 0
		self.cpt_cds = 0
		self.cpt_trk = 0
		self.listcat = []
		self.listfam = []
		self.listlab = []
		self.listyea = []
		
	def updateFilters(self, filttext, filtcate, filtfami, filtyear, filtlabl, filtintk):
		"""Update vars filter."""
		if filtintk and filttext != '':
			self.listid = buildTabFromRequest((getrequest('tracksinsearch')).format(search=filttext))
		else:
			self.listid = []
		self.filttext = filttext
		self.filtcate = filtcate
		self.filtfami = filtfami
		self.filtyear = filtyear
		self.filtlabl = filtlabl
		self.filtintk = filtintk
		self.cpt_siz = 0
		self.cpt_len = 0
		self.cpt_cds = 0
		self.cpt_trk = 0
		self.invalidate()
		
	def filterAcceptsRow(self, sourceRow, sourceParent):
		"""Filter data model."""
		# category
		if self.filtcate != '' and self.filtcate != self.parent.DISP_CJOKER:
			index = self.parent.index(sourceRow, self.parent.myindex.index('Category'), sourceParent)
			if self.filtcate != self.parent.data(index).value():
				return False
		# family
		if self.filtfami != '' and self.filtfami != self.parent.DISP_CJOKER:
			index = self.parent.index(sourceRow, self.parent.myindex.index('Family'), sourceParent)
			if self.filtfami != self.parent.data(index).value():
				return False
		# year
		if self.filtyear != '' and self.filtyear != self.parent.DISP_CJOKER:
			index = self.parent.index(sourceRow, self.parent.myindex.index('Year'), sourceParent)
			if self.filtyear != self.parent.data(index).value():
				return False
		# label
		if self.filtlabl != '' and self.filtlabl != self.parent.DISP_CJOKER:
			index = self.parent.index(sourceRow, self.parent.myindex.index('Label'), sourceParent)
			if self.filtlabl != self.parent.data(index).value():
				return False
		# text search
		if self.filtintk and self.filttext != '':
			index = self.parent.index(sourceRow, self.parent.myindex.index('ID_CD'), sourceParent)
			if  self.parent.data(index).value() not in self.listid:
				return False
		elif self.filttext != '':
			index = self.parent.index(sourceRow, self.parent.myindex.index('Name'), sourceParent)
			if self.filttext.lower() not in self.parent.data(index).value().lower():
				return False
		# cumuls
		index = self.parent.index(sourceRow, self.parent.myindex.index('Qty_CD'), sourceParent)
		self.cpt_cds += self.parent.data(index).value()
		index = self.parent.index(sourceRow, self.parent.myindex.index('Size'), sourceParent)
		self.cpt_siz += self.parent.data(index).value()
		index = self.parent.index(sourceRow, self.parent.myindex.index('Qty_CD'), sourceParent)
		self.cpt_cds += self.parent.data(index).value()
		index = self.parent.index(sourceRow, self.parent.myindex.index('Qty_Tracks'), sourceParent)
		self.cpt_trk += self.parent.data(index).value()
		index = self.parent.index(sourceRow, self.parent.myindex.index('Length'), sourceParent)
		lethval = self.parent.data(index).value()
		if isinstance(lethval, int) is False:
			if len(lethval.split(':')) > 1:
				lethval = sum(int(x) * 60 ** i for i, x in enumerate(reversed(lethval.split(':'))))
		self.cpt_len += int(lethval)
		# combos list
		index = self.parent.index(sourceRow, self.parent.myindex.index('Category'), sourceParent)
		if self.parent.data(index).value() not in self.listcat:
			self.listcat.append(self.parent.data(index).value())
		index = self.parent.index(sourceRow, self.parent.myindex.index('Family'), sourceParent)
		if self.parent.data(index).value() not in self.listfam:
			self.listfam.append(self.parent.data(index).value())
		index = self.parent.index(sourceRow, self.parent.myindex.index('Label'), sourceParent)
		if self.parent.data(index) not in self.listlab:
			self.listlab.append(self.parent.data(index))
		index = self.parent.index(sourceRow, self.parent.myindex.index('Year'), sourceParent)
		if self.parent.data(index).value() not in self.listyea:
			self.listyea.append(self.parent.data(index).value())
		# validate rows display ok
		return True
		
	

# MODEL ABSTRACT no production : slow init
class ModelDBAbstract(QAbstractTableModel):
	"""Abstract model for qtableview."""
	signalthubuild = pyqtSignal(float, str)		# build base
	
	def __init__(self, parent, colsname, colswrapper, req):
		"""Init Model Abstract."""
		super(ModelDBAbstract, self).__init__(parent)
		self.parent = parent
		self.myindex = colswrapper
		self.columns = colsname
		self.request = req
		self.arraydata = None
		
		# fill
		self.refresh()
	
	def refresh(self):
		"""build Array from request."""
		print('debut')
		query = QSqlQuery()
		query.setForwardOnly(True)
		query.exec_(self.request)
		self.arraydata = []
		cpt = 1
		tot = query.size() 
		while query.next():
			row = []
			for i in range(len(self.columns)):
				row.append(query.value(i))
			self.arraydata.append(row)
			if tot % 100 == 0:
				self.signalthubuild.emit((cpt/tot), 'Read Database')
				print(cpt/tot)
			cpt += 1
		query.clear
		print('fin')
	
	def headerData(self, section, orientation, role=Qt.DisplayRole):
		"""Set the name list to column name."""
		if role != Qt.DisplayRole:
			return QVariant()
		if orientation == Qt.Horizontal:
			return self.columns[section]
		return QVariant()
	
	def rowCount(self, parent=QModelIndex()):
		"""Get total rows."""
		return len(self.arraydata) 
	
	def columnCount(self, parent=QModelIndex()):
		"""Get total columns."""
		return len(self.columns) 
	
	def data(self, index, role=Qt.DisplayRole):
		"""Get datas."""
		if not index.isValid(): 
			return QVariant() 
		elif role == Qt.TextAlignmentRole:
			# TextAlignmentRole
			return QVariant()
		elif role != Qt.DisplayRole:
			return QVariant()
		return QVariant(self.arraydata[index.row()][index.column()])
	
	def getData(self, row, colname=None, col=None):
		if col is None:
			return self.arraydata[row][self.myindex.index(colname)]
		elif colname is None:
			return self.arraydata[row][col]

	def getList(self, colname, desc=True):
		"""Build list column."""
		mylist = []
		for row in range(self.rowCount()):
			itemlist = self.arraydata[row][self.myindex.index(colname)]
			if itemlist not in mylist:
				mylist.append(itemlist)
		mylist.sort(reverse=desc)
		return mylist
	
	def getSum(self, colname):
		"""Calcul sum of columns."""
		total = 0
		for row in range(self.rowCount()):
			itemlist = self.arraydata[row][self.myindex.index(colname)]
			if isinstance(itemlist, int) is False:
				if len(itemlist.split(':')) > 1:
					itemlist = sum(int(x) * 60 ** i for i, x in enumerate(reversed(itemlist.split(':'))))
			total += int(itemlist)
		return total
		return QVariant()


# #########################
# TABLE DBALBUM ABSTRACT : no production
class ModelTableAlbumsABS(ModelDBAbstract):
	# ## definition list albums
	# columns position 0-19 wrapper
	A_POSITIO = (	'Category', 'Family', 'Name', 'Label', 'ISRC',
					'Qty_Tracks', 'Qty_CD', 'Year', 'Length', 'Size',
					'Score', 'Qty_covers', 'Date_Insert', 'Date_Modifs', 'Position',
					'Typ_Tag', 'Path', 'Cover', 'MD5', 'ID_CD')
	# columns grid name
	A_COLNAME = (	'Category', 'Family', 'Name', 'Label', 'ISRC',
					'Trk', 'CD', 'Year', 'Time', 'Size',
					'Score', 'Pic', 'Add', 'Modified', 'Position',
					'Tag', 'Path', 'Cover', 'MD5', 'ID_CD')
	# treeview columns width
	A_C_WIDTH = (	60, 90, 250, 120, 110,
					30, 30, 40, 50, 40,
					45, 30, 77, 77, 250,
					30, 200, 200, 200, 40)
	C_HEIGHT = 20
	DISP_CJOKER = DISP_CJOKER 
	
	def __init__(self, parent, *args):
		"""Init model."""
		super(ModelTableAlbumsABS, self).__init__(parent, self.A_COLNAME, self.A_POSITIO, *args)
		# init sums
		self.parent = parent
		
				# sorting
		self.SortFilterProxy = ProxyModel(self)
		self.SortFilterProxy.setSortRole(Qt.UserRole)
		self.SortFilterProxy.setDynamicSortFilter(True)
		self.SortFilterProxy.setSourceModel(self)
	
	def data(self, index,  role=Qt.DisplayRole):
		"""Sum and display data."""
		if not index.isValid(): 
			return QVariant() 
		elif role == Qt.TextColorRole:
			if index.column() == self.myindex.index('Score'):
				return QVariant(QColor("yellow"))	
		elif role != Qt.DisplayRole:
			# TextAlignmentRole
			# if role == Qt.TextAlignmentRole:
			#	if index.column() == self.myindex.index('Qty_CD'):
			#		return Qt.AlignCenter
			return QVariant()
		# DisplayRole
		if index.column() == self.myindex.index('Score'):
			return (self.arraydata[index.row()][index.column()]*'★')
		if index.column() == self.myindex.index('Label') or index.column() == self.myindex.index('ISRC'):
			return ((self.arraydata[index.row()][index.column()]).upper())
		return QVariant(self.arraydata[index.row()][index.column()])
		
	def listCombo(self, colname, desc=True):
		mylist = self.getList(colname, desc)
		mylist = [self.DISP_CJOKER] + mylist
		return mylist

	def builListThunbnails(self, new=True, deb=0, fin=100):
		"""Build list Thunbnails"""
		listthun = []
		numAlb = self.rowCount()
		fin = min(fin,numAlb)
		for row in range(deb, fin):
			pathcover = self.arraydata[row][self.myindex.index('Cover')]
			albumname = self.arraydata[row][self.myindex.index('Name')]
			albumname = albumname.replace(' - ', '\n')
			# no cover or no display thunbnails covers (thnail_nod = 1)
			if THUN_NOD == 0 or pathcover == TEXT_NCO:
				Curalbmd5 = None
			else:
				Curalbmd5 = self.arraydata[row][self.myindex.index('MD5')]
			listthun.append([Curalbmd5, row, albumname])
		# add thunnails add
		return listthun
	
	def updateScore(self, idkey, score, namereq='updatescorealbum'):
		"""Maj Mysql table Albums."""
		# update score mysql
		req =  getrequest(namereq)
		req = req.format(score=score, id=idkey)
		query = QSqlQuery()
		query.exec_(req)
		query.clear
		# change value to array
		for i in range(self.rowCount()):
			if self.arraydata[i][self.myindex.index('ID_CD')]==idkey:
				self.arraydata[i][self.myindex.index('Score')] = score
				break


# ################################################
# MODEL SQLQUERY MODEL
class ModelSqlTbl2(QSqlQueryModel):
	"""Model generique."""
	signalthubuild = pyqtSignal(float, str)		# build base
	
	def __init__(self, parent, colsname, colswrapper, req):
		"""Init Model."""
		super(ModelSqlTbl2, self).__init__(parent)
		self.parent = parent
		self.myindex = colswrapper
		self.columns = colsname
		self.reqbase = req
		self.req = req
		self.setQuery(self.req)
		
	def headerData(self, section, orientation, role=Qt.DisplayRole):
		"""Set the headers to be displayed."""
		# get the column name self.model.headerData(0, Qt.Horizontal, Qt.DisplayRole).toString()
		if role != Qt.DisplayRole:
			return QVariant()
		if orientation == Qt.Horizontal:
			return str(self.columns[section])
		return QVariant()
	
	def refresh(self):
		self.setQuery(self.req)
	
	def columnCount(self, parent=QModelIndex()):
		return len(self.columns)
	
	def getData(self, row, colname):
		if self.rowCount() > 0:
			return self.data(self.index(row, self.myindex.index(colname)))
		return QVariant()
	
	def getSum(self, colname):
		if self.rowCount() > 0:
			total = 0
			for row in range(self.rowCount()):
				value = self.data(self.index(row, self.myindex.index(colname)))
				if isinstance(value, int) is False:
					if len(value.split(':')) > 1:
						value = sum(int(x) * 60 ** i for i, x in enumerate(reversed(value.split(':'))))
				total += int(value)
			return total
		return QVariant()
		
	def getList(self, colname, desc=True):
		"""Build list for the combos box."""
		mylist = []
		for row in range(self.rowCount()):
			index = self.index(row, self.columns.index(colname))
			curItem = self.data(index)
			if curItem not in mylist:
				mylist.append(str(curItem))
		mylist.sort(reverse=desc)
		return mylist
		
	def listmodel(self):
		if self.rowCount() > 0:
			for index in range(len(self.columns)):
				curItem = self.data(self.index(0, index))
				qDebug("{nd} {co} : {va}".format(nd=index, co=self.myindex[index], va=curItem))


# TABLE DBALBUMS SQLQUERY
class ModelTableAlbums2(ModelSqlTbl2):
	signallistalbchanged = pyqtSignal(int)		# list changed
	
	# ## definition list albums
	# columns position 0-19 wrapper
	A_POSITIO = (	'Category', 'Family', 'Name', 'Label', 'ISRC',
					'Qty_Tracks', 'Qty_CD', 'Year', 'Length', 'Size',
					'Score', 'Qty_covers', 'Date_Insert', 'Date_Modifs', 'Position',
					'Typ_Tag', 'Path', 'Cover', 'MD5', 'ID_CD')
	# columns grid name
	A_COLNAME = (	'Category', 'Family', 'Name', 'Label', 'ISRC',
					'Trk', 'CD', 'Year', 'Time', 'Size',
					'Score', 'Pic', 'Add', 'Modified', 'Position',
					'Tag', 'Path', 'Cover', 'MD5', 'ID_CD')
	DISP_CJOKER = DISP_CJOKER 
	
	def __init__(self, parent, *args):
		"""Init model."""
		super(ModelTableAlbums2, self).__init__(parent, self.A_COLNAME, self.A_POSITIO, *args)
		self.parent = parent
		self.currentfilter = '1=1'
		self.currentsearch = ''
		self.listcat = []
		self.listfam = []
		self.listlab = []
		self.listyea = [] 		
		self.cpt_siz = 0
		self.cpt_len = 0
		self.cpt_cds = 0
		self.cpt_trk = 0
		
	def data(self, index, role=Qt.DisplayRole):
		"""column Score decoration."""
		# color txt
		if index.isValid() and role==Qt.TextColorRole:
			if index.column() == self.myindex.index('Score'):
				return QVariant(QColor("#F6F503"))
		if index.isValid() and role==Qt.DisplayRole:
			# display column
			if index.column() == self.myindex.index('Score'):
				row = index.row()
				value = QSqlQueryModel.data(self, self.index(row, self.myindex.index('Score')))
				if value == None: value = 0
				return (value*'★')
			# build combos list
			if index.column() == self.myindex.index('Category'):
				row = index.row()
				itemlist = QSqlQueryModel.data(self, self.index(row, self.myindex.index('Category')))
				if itemlist not in self.listcat:
					self.listcat.append(itemlist)
			if index.column() == self.myindex.index('Family'):
				row = index.row()
				itemlist = QSqlQueryModel.data(self, self.index(row, self.myindex.index('Family')))
				if itemlist not in self.listfam:
					self.listfam.append(itemlist)
			if index.column() == self.myindex.index('Label'):
				row = index.row()
				itemlist = QSqlQueryModel.data(self, self.index(row, self.myindex.index('Label')))
				if itemlist not in self.listlab:
					self.listlab.append(itemlist)
			if index.column() == self.myindex.index('Year'):
				row = index.row()
				itemlist = QSqlQueryModel.data(self, self.index(row, self.myindex.index('Year')))
				if itemlist not in self.listyea:
					self.listyea.append(itemlist)
		return QSqlQueryModel.data(self, index, role)
	
	def sort(self, section, orientation):
		"""Sort Select request."""
		orderby = 'ORDER BY ' + self.myindex[section]
		if orientation == 0:
			orderby += ' DESC'
		self.req = self.reqbase.replace('ORDER BY Date_Insert DESC', orderby)
		self.setQuery(self.req)
		# signal list changed
		self.signallistalbchanged.emit(1)
	
	def setFilter(self, filttext, filtcate, filtfami, filtyear, filtlabl, filtintk):
		"""Filter request."""
		wheretxt = '1=1'
		if filtintk and filttext != '':
			self.currentsearch = filttext
			listid = buildTabFromRequest((getrequest('tracksinsearch')).format(search=filttext))
			idtxt = ', '.join(str(x) for x in listid)
			wheretxt += " AND ID_CD IN ("+idtxt+")"
		else:
			self.currentsearch = ''
			if filttext is not None and filttext != '':
				wheretxt += " AND Name LIKE '%" + filttext + "%'"
		if filtcate != '' and filtcate != self.DISP_CJOKER:
			wheretxt += " AND Category =  '" + filtcate + "'"
		if filtfami != '' and filtfami != self.DISP_CJOKER:
			wheretxt += " AND Family =  '" + filtfami + "'"
		if filtyear != '' and filtyear != self.DISP_CJOKER:
		 	wheretxt += " AND Year =  '" + filtyear + "'"
		if filtlabl != '' and filtlabl != self.DISP_CJOKER:
			wheretxt += " AND Label =  '" + filtlabl + "'"
		boolchgt = (wheretxt != self.currentfilter)
		if boolchgt:
			self.currentfilter = wheretxt
			self.req = self.reqbase.replace('1=1', self.currentfilter)
			self.setQuery(self.req)
			# signal list changed
			self.signallistalbchanged.emit(1)
		return boolchgt
			
	def getAlbumsSums(self):
		if self.rowCount() > 0:
			self.cpt_siz = 0
			self.cpt_len = 0
			self.cpt_cds = 0
			self.cpt_trk = 0
			for row in range(self.rowCount()):
				self.cpt_siz += self.data(self.index(row, self.myindex.index('Size')))
				self.cpt_cds += self.data(self.index(row, self.myindex.index('Qty_CD')))
				self.cpt_trk += self.data(self.index(row, self.myindex.index('Qty_Tracks')))
				lethval = self.data(self.index(row, self.myindex.index('Length')))
				if isinstance(lethval, int) is False:
					if len(lethval.split(':')) > 1:
						lethval = sum(int(x) * 60 ** i for i, x in enumerate(reversed(lethval.split(':'))))
				self.cpt_len += int(lethval)
	
	def builListThunbnails(self, new=True, deb=0, fin=100):
		"""Build list Thunbnails"""
		listthun = []
		numAlb = self.rowCount()
		fin = min(fin,numAlb)
		for row in range(deb, fin):
			pathcover = self.data(self.index(row, self.myindex.index('Cover')))
			albumname = self.data(self.index(row, self.myindex.index('Name')))
			albumname = albumname.replace(' - ', '\n')
			# no cover or no display thunbnails covers (thnail_nod = 1)
			if THUN_NOD == 0 or pathcover == TEXT_NCO:
				Curalbmd5 = None
			else:
				Curalbmd5 = self.data(self.index(row, self.myindex.index('MD5')))
			listthun.append([Curalbmd5, row, albumname])
		# add thunnails add
		return listthun
	
	def updateScore(self, row, score, namereq='updatescorealbum'):
		"""Maj Mysql table Albums."""
		# update score mysql
		idkey = self.data(self.index(row, self.myindex.index('ID_CD')))
		req =  getrequest(namereq)
		req = req.format(score=score, id=idkey)
		query = QSqlQuery()
		query.exec_(req)
		query.clear



# #####################
# test model
# #####################
class MainExempleModelDBTable(QMainWindow):
	"""Exemple model TABLE."""
	def __init__(self, parent=None):
		super(MainExempleModelDBTable, self).__init__(parent)
		self.resize(1200, 500)
		boolconnect, self.dbbase, self.modsql, self.rootDk = connectDatabase('LOSSLESS_TEST')
		self.mytable = QTableView(self)
		# sql table model 
		self.model = ModelDBTable(self, 'DBALBUMS')
		self.mytable.setModel(self.model)
		#self.model.setFilter("Category = 'TRANCE'");
		self.model.setSort(12, Qt.DescendingOrder)
		self.model.select()
		print (self.model.record(4).value("Name"))
		
		self.mytable.setAlternatingRowColors(True)
		self.mytable.resizeColumnsToContents()
		self.mytable.resizeRowsToContents()
		self.mytable.setSortingEnabled(True)
		self.mytable.setSelectionBehavior(QTableView.SelectRows)
		
		self.setCentralWidget(self.mytable)
		self.show()


class MainExempleSqlQuery(QMainWindow):
	"""Exemple model SQLQUERY."""
	def __init__(self, parent=None):
		super(MainExempleSqlQuery, self).__init__(parent)
		self.resize(1200, 500)
		boolconnect, self.dbbase, self.modsql, self.rootDk = connectDatabase('LOSSLESS_TEST')
		
		self.mytable = QTableView(self)
		
		print('Fill list albums start')
		req = getrequest('albumslist', self.modsql)
		self.model = ModelTableAlbums2(self, req)
		self.mytable.setSortingEnabled(True)
		self.mytable.setModel(self.model)
		self.mytable.setAlternatingRowColors(True)
		self.mytable.resizeColumnsToContents()
		self.mytable.resizeRowsToContents()
		self.mytable.setSelectionBehavior(QTableView.SelectRows)
		self.setCentralWidget(self.mytable)
		self.show()


class MainExempleAbstractTable(QMainWindow):
	"""Exemple model ABSTRACT."""
	def __init__(self, parent=None):
		super(MainExempleAbstractTable, self).__init__(parent)
		self.resize(1200, 500)
		boolconnect, self.dbbase, self.modsql, self.rootDk = connectDatabase('LOSSLESS')
		self.mytable = QTableView(self)
		self.mytable.setAlternatingRowColors(True)
		self.mytable.setSortingEnabled(True)
		self.mytable.setSelectionBehavior(QTableView.SelectRows)
		self.mytable.clicked.connect(self.onSelect)
		
		
		# abstract model
		req = getrequest('albumslist', self.modsql)
		self.model = ModelTableAlbumsABS(self, req)
		self.model.SortFilterProxy.layoutChanged.connect(self.listChanged)
		self.mytable.setModel(self.model.SortFilterProxy)
		
		# width columns
		for i in range(len(self.model.A_C_WIDTH)):
			self.mytable.setColumnWidth(i, self.model.A_C_WIDTH[i])
		# height rows
		self.mytable.verticalHeader().setDefaultSectionSize(self.model.C_HEIGHT)
		
		self.setCentralWidget(self.mytable)
		self.show()

		self.model.SortFilterProxy.sort(-1)
		#self.model.SortFilterProxy.updateFilters('', '', '', '', '', False)
		self.model.SortFilterProxy.updateFilters('', 'TRANCE', 'Physique', '', '', False)
		
		print(self.model.SortFilterProxy.listcat)
		
		self.displayTitle()
	
	def onSelect(self):
		indexes = self.mytable.selectedIndexes()
		print(indexes[0].row())
		indexes = self.model.SortFilterProxy.mapToSource(indexes[0])
		print(indexes.row())

	def listChanged(self):
		print('list change')

	def displayTitle(self):
		if int(((self.model.SortFilterProxy.cpt_len/60/60)/24)*10)/10 < 1:
			# seoncd -> Hours
			txt_len = str(int(((self.model.SortFilterProxy.cpt_len/60/60))*10)/10) + ' Hours'
		else:
			# seoncd -> Days
			txt_len = str(int(((self.model.SortFilterProxy.cpt_len/60/60)/24)*10)/10) + ' Days'
		if int(self.model.SortFilterProxy.cpt_siz/1024) == 0:
			txt_siz =  str(self.model.SortFilterProxy.cpt_siz) + ' Mo'
		else:
			txt_siz = str(int(self.model.SortFilterProxy.cpt_siz/1024)) + ' Go'
		message = "Search Result \"{sch}\" :  {alb} | {trk} | {cds} | {siz} | {dur}".format(alb=displayCounters(self.model.SortFilterProxy.rowCount(), 'Album'),
																							cds=displayCounters(self.model.SortFilterProxy.cpt_cds, 'CD'),
																							trk=displayCounters(self.model.SortFilterProxy.cpt_trk, 'Track'),
																							siz=txt_siz,
																							dur=txt_len,
																							sch='{sch}')
		self.setWindowTitle(message)

if __name__ == '__main__':
	app = QApplication(argv)
	MainExempleAbstractTable()
	#MainExempleModelDBTable()
	#MainExempleSqlQuery()
	rc = app.exec_()
	exit(rc)
