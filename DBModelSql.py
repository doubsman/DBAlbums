#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from PyQt5.QtCore import Qt, QVariant, qDebug, QSettings, QModelIndex, pyqtSignal
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from PyQt5.QtGui import QBrush, QColor
from DBFunction import convertUNC
from DBDatabase import getrequest, buildTabFromRequest

FILE__INI = 'DBAlbums.ini'
configini = QSettings(FILE__INI, QSettings.IniFormat)
configini.beginGroup('dbalbums')
TEXT_NCO = configini.value('text_nocov')
THUN_NOD = int(configini.value('thnail_nod'))
FONT_MAI = configini.value('font00_ttx')
DISP_CJOKER = configini.value('text_joker')
configini.endGroup()


# MODEL SQLQUERY MODEL
class ModelSqlTbl(QSqlQueryModel):
	"""Model generique."""
	signalthubuild = pyqtSignal(float, str)		# build base
	
	def __init__(self, parent, colsname, colswrapper, req):
		"""Init Model."""
		super(ModelSqlTbl, self).__init__(parent)
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
		"""Build list for the column name."""
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
class ModelTableAlbums(ModelSqlTbl):
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
	# treeview columns width
	A_C_WIDTH = (	60, 90, 250, 120, 110,
					30, 30, 40, 50, 40,
					45, 30, 77, 77, 250,
					30, 200, 200, 200, 40)
	C_HEIGHT = 20
	DISP_CJOKER = DISP_CJOKER 
	
	def __init__(self, parent, *args):
		"""Init model."""
		super(ModelTableAlbums, self).__init__(parent, self.A_COLNAME, self.A_POSITIO, *args)
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
				return QVariant(QColor("yellow"))
		if index.isValid() and role==Qt.DisplayRole:
			# display column
			if index.column() == self.myindex.index('Score'):
				row = index.row()
				value = QSqlQueryModel.data(self, self.index(row, self.myindex.index('Score')))
				if value == None: value = 0
				return (''+value*'★')
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


# TABLE DBTRACKS SQLQUERY
class ModelTableTracks(ModelSqlTbl):
	# ## definition list tracks
	# columns position 0-8 wrapper
	T_POSITIO = (	'ODR_Track', 'TAG_Artists', 'TAG_Title', 'TAG_length',
					'Score', 'TAG_Genres', 'FIL_Track', 'REP_Track', 'ID_TRACK')
	# columns grid name
	T_COLNAME = (	'N°', 'Artist', 'Title', 'Time',
					'Score', 'Style', 'File', 'Folder', 'ID_TRACK')
					
	def __init__(self, parent, txtsearch, *args):
		"""Init model."""
		super(ModelTableTracks, self).__init__(parent, self.T_COLNAME, self.T_POSITIO, *args)
		self.parent = parent
		self.txtsearch = txtsearch
	
	def data(self, index, role=Qt.DisplayRole):
		"""column Score decoration and search color lines."""
		# color txt
		if index.isValid() and role==Qt.TextColorRole:
			if index.column() == self.myindex.index('Score'):
				return QVariant(QColor("yellow"))
		if index.isValid() and role==Qt.BackgroundRole and self.txtsearch != '':
			row = index.row()
			value1 = QSqlQueryModel.data(self, self.index(row, self.myindex.index('TAG_Artists')))
			value2 = QSqlQueryModel.data(self, self.index(row, self.myindex.index('TAG_Title')))
			if self.txtsearch.lower() in value1.lower() or self.txtsearch.lower() in value2.lower():
				return QBrush(Qt.darkGray)
		if index.isValid() and role==Qt.DisplayRole:
			if index.column() == self.myindex.index('Score'):
				row = index.row()
				value = QSqlQueryModel.data(self, self.index(row, self.myindex.index('Score')))
				if value == None: value = 0
				return (''+value*'★')
		return QSqlQueryModel.data(self, index, role)
		
	def sort(self, section, orientation):
		"""Sort Select request."""
		orderby = 'ORDER BY ' + self.myindex[section]
		if orientation == 0:
			orderby += ' DESC'
		self.req = self.reqbase.replace('ORDER BY REP_Track, ODR_Track', orderby)
		self.setQuery(self.req)
	
	def getMedias(self):
		"""Prepare list media for player audio."""
		if self.rowCount() > 0:
			listmedia = []
			for row in range(self.rowCount()):
				file = path.join(self.data(self.index(row, self.myindex.index('REP_Track'))), self.data(self.index(row, self.myindex.index('FIL_Track'))))
				listmedia.append(convertUNC(file))
		return listmedia

	def updateScore(self, row, score, namereq='updatescoretrack'):
		"""Maj Mysql table Albums."""
		# update score mysql
		idkey = self.data(self.index(row, self.myindex.index('ID_TRACK')))
		req =  getrequest(namereq)
		req = req.format(score=score, id=idkey)
		query = QSqlQuery()
		query.exec_(req)
		query.clear
