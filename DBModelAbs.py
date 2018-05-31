#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from PyQt5.QtCore import Qt, QVariant, QSettings, QModelIndex, pyqtSignal, QSortFilterProxyModel, QAbstractTableModel
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtGui import QColor
from DBDatabase import getrequest, buildTabFromRequest
from DBFunction import convertUNC

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
			if cpt % (tot/max(tot, 10)) == 0:
				self.signalthubuild.emit((cpt/tot), 'Read Database')
			cpt += 1
		query.clear
	
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
class ProxyModelAlbums(QSortFilterProxyModel):
	def __init__(self, parent):
		"""Init proxy model."""
		super(ProxyModelAlbums, self).__init__(parent)
		self.parent = parent
		self.filttext = ''
		self.filtcate = None
		self.filtfami = None
		self.filtyear = None
		self.filtlabl = None
		self.filtintk = False
		self.filtgenr = None
		self.listidtxt = []
		self.listidsty = []
		self.cpt_siz = 0
		self.cpt_len = 0
		self.cpt_cds = 0
		self.cpt_trk = 0
		self.listcat = []
		self.listfam = []
		self.listlab = []
		self.listyea = []
		self.listthun = []
		self.listiddi = []

	def updateFilters(self, filttext, filtcate=None, filtfami=None, filtyear=None, filtlabl=None, filtgenr=None, filtintk=False):
		"""Update vars filter."""
		if filtintk and filttext != '':
			self.listidtxt = buildTabFromRequest((getrequest('tracksinsearch')).format(search=filttext))
		else:
			self.listidtxt = []
		if  filtgenr is not None:
			if filtgenr != '':
				filtsearch = '%'+filtgenr+'%'
			else:
				filtsearch = ''
			self.listidsty = buildTabFromRequest((getrequest('tracksgesearch')).format(search=filtsearch))
		else:
			self.listidsty = []
		self.filttext = filttext
		self.filtcate = filtcate
		self.filtfami = filtfami
		self.filtyear = filtyear
		self.filtlabl = filtlabl
		self.filtintk = filtintk
		self.filtgenr = filtgenr
		self.cpt_siz = 0
		self.cpt_len = 0
		self.cpt_cds = 0
		self.cpt_trk = 0
		self.listcat = []
		self.listfam = []
		self.listlab = []
		self.listyea = []
		self.listthun = []
		self.listiddi = []
		self.invalidate()
		
	def filterAcceptsRow(self, sourceRow, sourceParent):
		"""Filter data model."""
		# category
		if self.filtcate is not None and self.filtcate != self.parent.DISP_CJOKER:
			index = self.parent.index(sourceRow, self.parent.myindex.index('Category'), sourceParent)
			if self.filtcate != self.parent.data(index).value():
				return False
		# family
		if self.filtfami is not None and self.filtfami != self.parent.DISP_CJOKER:
			index = self.parent.index(sourceRow, self.parent.myindex.index('Family'), sourceParent)
			if self.filtfami != self.parent.data(index).value():
				return False
		# year
		if self.filtyear is not None and self.filtyear != self.parent.DISP_CJOKER:
			index = self.parent.index(sourceRow, self.parent.myindex.index('Year'), sourceParent)
			if self.filtyear != self.parent.data(index).value():
				return False
		# label
		if self.filtlabl is not None and self.filtlabl != self.parent.DISP_CJOKER:
			index = self.parent.index(sourceRow, self.parent.myindex.index('Label'), sourceParent)
			if self.filtlabl != self.parent.data(index):
				return False
		# genres
		if self.filtgenr is not None and self.filtgenr != self.parent.DISP_CJOKER:
			index = self.parent.index(sourceRow, self.parent.myindex.index('ID_CD'), sourceParent)
			if  self.parent.data(index).value() not in self.listidsty:
				return False
		# text search
		if self.filtintk and self.filttext != '':
			index = self.parent.index(sourceRow, self.parent.myindex.index('ID_CD'), sourceParent)
			if  self.parent.data(index).value() not in self.listidtxt:
				return False
		elif self.filttext != '':
			index = self.parent.index(sourceRow, self.parent.myindex.index('Name'), sourceParent)
			if self.filttext.lower() not in self.parent.data(index).value().lower():
				return False
		# cumuls
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
		# list id
		index = self.parent.index(sourceRow, self.parent.myindex.index('ID_CD'), sourceParent)
		self.listiddi.append(self.parent.data(index).value())
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


# TABLE DBALBUMS ABSTRACT
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
					50, 30, 77, 77, 250,
					30, 200, 200, 200, 40)
	C_HEIGHT = 21
	DISP_CJOKER = DISP_CJOKER 
	
	def __init__(self, parent, *args):
		"""Init model."""
		super(ModelTableAlbumsABS, self).__init__(parent, self.A_COLNAME, self.A_POSITIO, *args)
		# init sums
		self.parent = parent
		
		# sorting
		self.SortFilterProxy = ProxyModelAlbums(self)
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
	
	def builListThunbnails(self, new=True, deb=0, fin=100):
		"""Build list Thunbnails"""
		listthun = []
		numAlb = self.rowCount()
		fin = min(fin,numAlb)
		for row in range(deb, fin):
			index = self.SortFilterProxy.index(row, 0)
			index = self.SortFilterProxy.mapToSource(index)
			if not index.isValid():
				continue
			pathcover = self.getData(index.row(), 'Cover')
			albumname = self.getData(index.row(), 'Name')
			albumname = albumname.replace(' - ', '\n')
			# no cover or no display thunbnails covers (thnail_nod = 1)
			if THUN_NOD == 0 or pathcover == TEXT_NCO:
				Curalbmd5 = None
			else:
				Curalbmd5 = self.getData(index.row(), 'MD5')
			listthun.append([Curalbmd5, index.row(), albumname])
		# add thunnails add
		return listthun
	
	def updateScore(self, row, score, namereq='updatescorealbum'):
		"""Maj Mysql table Albums."""
		idkey = self.arraydata[row][self.myindex.index('ID_CD')]
		# update score mysql
		req =  getrequest(namereq)
		req = req.format(score=score, id=idkey)
		query = QSqlQuery()
		query.exec_(req)
		query.clear
		# change value to array
		self.arraydata[row][self.myindex.index('Score')]= score


# MODEL ABSTRACT proxy model tbl albums
class ProxyModelTracks(QSortFilterProxyModel):
	def __init__(self, parent):
		"""Init proxy model."""
		super(ProxyModelTracks, self).__init__(parent)
		self.parent = parent
	
	def filterAcceptsRow(self, sourceRow, sourceParent):
		"""Filter data model."""
		# validate rows display ok
		return True


# TABLE DBTRACKS SQLQUERY
class ModelTableTracksABS(ModelDBAbstract):
	
	# ## definition list tracks
	# columns position 0-8 wrapper
	T_POSITIO = (	'ODR_Track', 'TAG_Artists', 'TAG_Title', 'TAG_length',
					'Score', 'TAG_Genres', 'FIL_Track', 'REP_Track', 'ID_TRACK')
	# columns grid name
	T_COLNAME = (	'N°', 'Artist', 'Title', 'Time',
					'Score', 'Style', 'File', 'Folder', 'ID_TRACK')
	# treeview columns width
	C_HEIGHT = 21
	T_C_WIDTH = (	50, 150, 200, 60,
					50, 90, 250, 250, 70)
					
	def __init__(self, parent, txtsearch, *args):
		"""Init model."""
		super(ModelTableTracksABS, self).__init__(parent, self.T_COLNAME, self.T_POSITIO, *args)
		self.parent = parent
		self.txtsearch = txtsearch	
		
		# sorting
		self.SortFilterProxy = ProxyModelTracks(self)
		self.SortFilterProxy.setDynamicSortFilter(True)
		self.SortFilterProxy.setSourceModel(self)
		
	def data(self, index,  role=Qt.DisplayRole):
		"""column Score decoration and color."""
		if not index.isValid(): 
			return QVariant() 
		elif role == Qt.TextColorRole:
			if index.column() == self.myindex.index('Score'):
				return QVariant(QColor("yellow"))
		elif role == Qt.BackgroundRole:				
			if self.txtsearch != '':
				row = index.row()
				value1 = self.arraydata[row][self.myindex.index('TAG_Artists')]
				value2 = self.arraydata[row][self.myindex.index('TAG_Title')]
				if self.txtsearch.lower() in value1.lower() or self.txtsearch.lower() in value2.lower():
					return QVariant(QColor("lightsteelblue"))
		elif role != Qt.DisplayRole:
			return QVariant()
		# DisplayRole
		if index.column() == self.myindex.index('Score'):
			return (self.arraydata[index.row()][index.column()]*'★')
		return QVariant(self.arraydata[index.row()][index.column()])

	def getMedias(self):
		"""Prepare list media for player audio."""
		if self.rowCount() > 0:
			listmedia = []
			for row in range(self.rowCount()):
				index = self.SortFilterProxy.index(row, 0)
				index = self.SortFilterProxy.mapToSource(index)
				if not index.isValid():
					continue
				file = path.join(self.arraydata[index.row()][self.myindex.index('REP_Track')], self.arraydata[index.row()][self.myindex.index('FIL_Track')])
				listmedia.append(convertUNC(file))
			return listmedia

	def updateScore(self, row, score, namereq='updatescoretrack'):
		"""Maj Mysql table Albums."""
		# update score mysql
		idkey = self.arraydata[row][self.myindex.index('ID_TRACK')]
		req =  getrequest(namereq)
		req = req.format(score=score, id=idkey)
		query = QSqlQuery()
		query.exec_(req)
		query.clear
		# change value to array
		self.arraydata[row][self.myindex.index('Score')] = score
