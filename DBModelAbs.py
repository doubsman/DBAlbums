#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QVariant, QSettings, QModelIndex, pyqtSignal, QSortFilterProxyModel, QAbstractTableModel
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtGui import QColor
from DBDatabase import getrequest, buildTabFromRequest

FILE__INI = 'DBAlbums.ini'
configini = QSettings(FILE__INI, QSettings.IniFormat)
configini.beginGroup('dbalbums')
TEXT_NCO = configini.value('text_nocov')
THUN_NOD = int(configini.value('thnail_nod'))
FONT_MAI = configini.value('font00_ttx')
DISP_CJOKER = configini.value('text_joker')
configini.endGroup()


# MODEL ABSTRACT generique
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
		# fill array
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


# MODEL ABSTRACT proxy model tbl albums
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
