#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from PyQt5.QtCore import Qt, QVariant, QModelIndex, pyqtSignal, QSortFilterProxyModel, QAbstractTableModel
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtGui import QColor


# MODEL ABSTRACT generique
class ModelDBAbstract(QAbstractTableModel):
	"""Abstract model for qtableview."""
	signalthubuild = pyqtSignal(float, str)		# build base
	
	def __init__(self, parent, colsname, req):
		"""Init Model Abstract."""
		super(ModelDBAbstract, self).__init__(parent)
		self.parent = parent
		self.columns = colsname
		self.request = req
		self.arraydata = []
		self.myindex = []
		# fill array
		self.refresh()
	
	def refresh(self):
		"""build Array from request."""
		query = QSqlQuery(self.parent.dbbase)
		query.setForwardOnly(True)
		query.exec_(self.request)
		self.myindex = self.parent.CnxConnect.getListColumns(query)
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
		if self.rowCount() > 0:
			if col is None:
				return self.arraydata[row][self.myindex.index(colname)]
			elif colname is None:
				return self.arraydata[row][col]
		return QVariant()
	
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
			if isinstance(itemlist, int) is False and len(itemlist) > 0:
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
		self.filtcoun = None
		self.listidtxt = []
		self.cpt_siz = 0
		self.cpt_len = 0
		self.cpt_trk = 0
		self.listcat = []
		self.listfam = []
		self.listlab = []
		self.listyea = []
		self.listcou = []
		self.listthun = []
		self.listiddi = []

	def updateFilters(self, filttext, filtcate=None, filtfami=None, filtyear=None, filtlabl=None, filtgenr=None, filtcoun=None, filtintk=False):
		"""Update vars filter."""
		if filtintk and filttext != '':
			print((self.parent.CnxConnect.getrequest('tracksinsearch')).format(search=filttext))
			self.listidtxt = self.parent.CnxConnect.sqlToArray((self.parent.CnxConnect.getrequest('tracksinsearch')).format(search=filttext))
			print(self.listidtxt)
		else:
			self.listidtxt = []
		self.filttext = filttext
		self.filtcate = filtcate
		self.filtfami = filtfami
		self.filtyear = filtyear
		self.filtlabl = filtlabl
		self.filtintk = filtintk
		self.filtgenr = filtgenr
		self.filtcoun = filtcoun
		self.cpt_siz = 0
		self.cpt_len = 0
		self.cpt_trk = 0
		self.listcat = []
		self.listfam = []
		self.listlab = []
		self.listyea = []
		self.listcou = []
		self.listthun = []
		self.listiddi = []
		self.invalidate()
		
	def filterAcceptsRow(self, sourceRow, sourceParent):
		"""Filter data model."""
		# category
		if self.filtcate:
			index = self.parent.index(sourceRow, self.parent.myindex.index('CATEGORY'), sourceParent)
			if self.filtcate != self.parent.data(index).value():
				return False
		# family
		if self.filtfami:
			index = self.parent.index(sourceRow, self.parent.myindex.index('FAMILY'), sourceParent)
			if self.filtfami != self.parent.data(index).value():
				return False
		# year
		if self.filtyear:
			index = self.parent.index(sourceRow, self.parent.myindex.index('YEAR'), sourceParent)
			if self.filtyear != self.parent.data(index).value():
				return False
		# label
		if self.filtlabl:
			index = self.parent.index(sourceRow, self.parent.myindex.index('LABEL'), sourceParent)
			if self.filtlabl != self.parent.data(index):
				return False
		# style
		if self.filtgenr:
			index = self.parent.index(sourceRow, self.parent.myindex.index('STYLE'), sourceParent)
			if not (self.filtgenr == 'Unknown' and self.parent.data(index).value() == ''):
				if self.filtgenr not in self.parent.data(index).value():
					return False
		# country
		if self.filtcoun:
			index = self.parent.index(sourceRow, self.parent.myindex.index('COUNTRY'), sourceParent)
			if self.filtcoun not in self.parent.data(index).value():
				return False
		# text search
		if self.filtintk and self.filttext != '':
			index = self.parent.index(sourceRow, self.parent.myindex.index('ID_CD'), sourceParent)
			if self.parent.data(index).value() not in self.listidtxt:
				return False
		# find in name and label
		elif self.filttext != '':
			index = self.parent.index(sourceRow, self.parent.myindex.index('NAME'), sourceParent)
			indexArtist = self.parent.index(sourceRow, self.parent.myindex.index('POSITIONHDD'), sourceParent)
			if self.filttext.lower() not in self.parent.data(index).value().lower() and self.filttext.lower() not in self.parent.data(indexArtist).value().lower():
				return False
		# cumuls
		index = self.parent.index(sourceRow, self.parent.myindex.index('SIZE'), sourceParent)
		self.cpt_siz += self.parent.data(index).value()
		index = self.parent.index(sourceRow, self.parent.myindex.index('TRACKS'), sourceParent)
		self.cpt_trk += self.parent.data(index).value()
		index = self.parent.index(sourceRow, self.parent.myindex.index('LENGTHDISPLAY'), sourceParent)
		lethval = self.parent.data(index).value()
		if isinstance(lethval, int) is False:
			if len(lethval.split(':')) > 1:
				lethval = sum(int(x) * 60 ** i for i, x in enumerate(reversed(lethval.split(':'))))
		self.cpt_len += int(lethval)
		# list id
		index = self.parent.index(sourceRow, self.parent.myindex.index('ID_CD'), sourceParent)
		self.listiddi.append(self.parent.data(index).value())
		# build combos list
		index = self.parent.index(sourceRow, self.parent.myindex.index('CATEGORY'), sourceParent)
		if self.parent.data(index).value() not in self.listcat:
			self.listcat.append(self.parent.data(index).value())
		index = self.parent.index(sourceRow, self.parent.myindex.index('FAMILY'), sourceParent)
		if self.parent.data(index).value() not in self.listfam:
			self.listfam.append(self.parent.data(index).value())
		# label only for family Label/Physique
		if self.parent.data(index).value() == 'Label/Physique':
			index = self.parent.index(sourceRow, self.parent.myindex.index('LABEL'), sourceParent)
			if self.parent.data(index) not in self.listlab:
				self.listlab.append(self.parent.data(index))
		index = self.parent.index(sourceRow, self.parent.myindex.index('YEAR'), sourceParent)
		if self.parent.data(index).value() not in self.listyea:
			self.listyea.append(self.parent.data(index).value())
		index = self.parent.index(sourceRow, self.parent.myindex.index('COUNTRY'), sourceParent)
		if self.parent.data(index).value() not in self.listcou:
			self.listcou.append(self.parent.data(index).value())
		# validate rows display ok
		return True


# TABLE DBALBUMS ABSTRACT
class ModelTableAlbumsABS(ModelDBAbstract):
	PATH_PROG = path.dirname(path.abspath(__file__))
	RESS_FLAG = path.join(PATH_PROG, 'IMG' , 'FLAG')
	# ## definition list albums
	# columns grid name
	A_COLNAME = (	'Category', 'Family', 'Name', 'Artist', 'Style',
					'Label', 'TLabel', 'ISRC', 'TISRC', 'Trk', 
					'CD', 'Year', 'Time', 'Size', 'Score', 
					'Pic', 'Country', 'Add', 'Modified', 'Position',
					'Path', 'Cover', 'Tag', 'ID_CD')
	# treeview columns width
	A_C_WIDTH = (	60, 90, 250, 0, 110,
					120, 0, 100, 0, 30,
					30, 40, 50, 40,	50,
					30, 60, 77, 77, 250,
					200, 200, 30, 40)
	C_HEIGHT = 21
	
	def __init__(self, parent, *args):
		"""Init model."""
		super(ModelTableAlbumsABS, self).__init__(parent, self.A_COLNAME, *args)
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
			if index.column() == self.myindex.index('SCORE'):
				return QVariant(QColor("yellow"))	
		elif role != Qt.DisplayRole:
			# TextAlignmentRole
			# if role == Qt.TextAlignmentRole:
			#	if index.column() == self.myindex.index('Qty_CD'):
			#		return Qt.AlignCenter
			return QVariant()
		# DisplayRole
		if index.column() == self.myindex.index('SCORE'):
			return (self.arraydata[index.row()][index.column()]*'★')
		if index.column() == self.myindex.index('LABEL'):
			if self.arraydata[index.row()][index.column()]:
				return (self.arraydata[index.row()][index.column()]).title()
			else:
				return (self.arraydata[index.row()][self.myindex.index('TAGLABEL')]).title()
		if index.column() == self.myindex.index('ISRC'):
			if self.arraydata[index.row()][index.column()]:
				return (self.arraydata[index.row()][index.column()]).upper()
			else:
				return (self.arraydata[index.row()][self.myindex.index('TAGISRC')]).upper()
		if index.column() == self.myindex.index('COVER') or index.column() == self.myindex.index('PATHNAME'):
				return self.parent.Json_params.convertUNC(self.arraydata[index.row()][index.column()])
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
			pathcover = self.getData(index.row(), 'COVER')
			albumname = self.getData(index.row(), 'NAME')
			albumname = albumname.replace(' - ', '\n')
			# no cover or no display thunbnails covers (thnail_nod = 1)
			if self.parent.THUN_NOD == 0 or pathcover == self.parent.TEXT_NCO:
				idcd = None
			else:
				idcd = self.getData(index.row(), 'ID_CD')
			listthun.append([idcd, index.row(), albumname])
		# add thunnails add
		return listthun
	
	def updateScore(self, row, score, namereq='updatescorealbum'):
		"""Maj Mysql table Albums."""
		idkey = self.arraydata[row][self.myindex.index('ID_CD')]
		# update score mysql
		req =  self.parent.CnxConnect.getrequest(namereq)
		req = req.format(score=score, id=idkey)
		query = QSqlQuery(self.parent.dbbase)
		query.exec_(req)
		query.clear
		# change value to array
		self.arraydata[row][self.myindex.index('SCORE')]= score


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
	# columns grid name
	T_COLNAME = (	'N°', 'Artist', 'Title', 'Time', 'Score',
					'Style', 'File', 'index', 'start', 'end',
					'Path', 'format', 'ID_TRACK')
	# treeview columns width
	C_HEIGHT = 21
	T_C_WIDTH = (	50, 200, 200, 50, 50,
					90, 250, 60, 70, 70,
					250, 70, 70)
					
	def __init__(self, parent, txtsearch, *args):
		"""Init model."""
		super(ModelTableTracksABS, self).__init__(parent, self.T_COLNAME, *args)
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
			if index.column() == self.myindex.index('SCORE'):
				return QVariant(QColor("yellow"))
		elif role == Qt.BackgroundRole:				
			if self.txtsearch != '':
				row = index.row()
				value1 = self.arraydata[row][self.myindex.index('ARTIST')]
				value2 = self.arraydata[row][self.myindex.index('TITLE')]
				if self.txtsearch.lower() in value1.lower() or self.txtsearch.lower() in value2.lower():
					return QVariant(QColor("lightsteelblue"))
		elif role != Qt.DisplayRole:
			return QVariant()
		# DisplayRole
		if index.column() == self.myindex.index('SCORE'):
			return (self.arraydata[index.row()][index.column()]*'★')
		if index.column() == self.myindex.index('PATHNAME'):
				return self.parent.Json_params.convertUNC(self.arraydata[index.row()][index.column()])
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
				file = path.join(self.arraydata[index.row()][self.myindex.index('PATHNAME')], self.arraydata[index.row()][self.myindex.index('FILENAME')])
				listmedia.append(file)
			return listmedia

	def updateScore(self, row, score, namereq='updatescoretrack'):
		"""Maj Mysql table Albums."""
		# update score mysql
		idkey = self.arraydata[row][self.myindex.index('ID_TRACK')]
		req =  self.parent.CnxConnect.getrequest(namereq)
		req = req.format(score=score, id=idkey)
		query = QSqlQuery(self.parent.dbbase)
		query.exec_(req)
		query.clear
		# change value to array
		self.arraydata[row][self.myindex.index('SCORE')] = score


# TABLE DBTRACKS SQLQUERY
class ModelTableUpdatesABS(QAbstractTableModel):
	# columns position 0-8 wrapper
	U_POSITIO = ('Category', 'Family', 'Action', 'ID', 'Name', 'Folder')
	# columns grid name
	U_COLNAME = U_POSITIO
	# treeview columns width
	C_HEIGHT = 21
	U_C_WIDTH = (70, 120, 70, 50, 300, 800)
					
	def __init__(self, parent, arraydata):
		"""Init model."""
		super(ModelTableUpdatesABS, self).__init__(parent)
		self._array = arraydata
	
	def update(self, arraydata):
		self._array = arraydata
		self.layoutChanged.emit()
		
	def headerData(self, section, orientation, role=Qt.DisplayRole):
		"""Set the name list to column name."""
		if role != Qt.DisplayRole:
			return QVariant()
		if orientation == Qt.Horizontal:
			return self.U_POSITIO[section]
		return QVariant()	
		
	def rowCount(self, parent=None):
		return len(self._array)

	def columnCount(self, parent=None):
		return len(self.U_POSITIO)
		
	def data(self, index, role=Qt.DisplayRole):
		if index.isValid():
			if role == Qt.DisplayRole:
				return QVariant(self._array[index.row()][index.column()])

		return QVariant()
