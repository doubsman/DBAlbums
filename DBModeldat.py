#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import executable, argv
from os import path, system
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QVariant, qDebug, QSettings, QDir
from PyQt5.QtSql import QSqlQueryModel
from DBFunction import convertUNC
from DBThunbnail import TNLabel

if getattr(system, 'frozen', False):
	PATH_PROG = path.dirname(executable)
else:
	PATH_PROG = path.realpath(path.dirname(argv[0]))
QDir.setCurrent(PATH_PROG)
FILE__INI = 'DBAlbums.ini'
configini = QSettings(FILE__INI, QSettings.IniFormat)
configini.beginGroup('dbalbums')
VERS_PROG = configini.value('prog_build')
TITL_PROG = "♫ DBAlbums v{v} (2017)".format(v=VERS_PROG)

TEXT_NCO = configini.value('text_nocov')
THUN_DIS = int(configini.value('thnail_dis'))
THUN_NOD = int(configini.value('thnail_nod'))
THUN_DBA = path.join(PATH_PROG, 'IMG', configini.value('picm_endof'))
PICT_NCO = path.join(PATH_PROG, 'IMG', configini.value('pict_blank'))
PICM_NCO = path.join(PATH_PROG, 'IMG', configini.value('picm_blank'))
FONT_MAI = configini.value('font00_ttx')
DISP_CJOKER = configini.value('text_joker')


# ##################################################################
class ModelTbl(QSqlQueryModel):
	def __init__(self, parent, req, gridname,  colsname, colswrapper):
		super(ModelTbl, self).__init__(parent)
		self.parent = parent
		self.myindex = colswrapper
		self.columns = colsname
		self.req = req
		self.grid = gridname
		self.setQuery(self.req)
		# set columns name + size
		numcol = 0
		for colname in self.columns:
			self.setHeaderData(numcol, Qt.Horizontal, colname)
			numcol += 1

	def setFilter(self,  colname,  value):
		self.req = self.req.replace('1=1', '1=1 AND '+colname+"='"+value+"'")
		self.setQuery(self.req)
		#self.displayThunbnails()

	def refresh(self):
		self.setQuery(self.req)

	def datacombos(self, column):
		listcombo = []
		for row in range(self.rowCount()):
			index = self.index(row, self.columns.index(column))
			curItem = self.data(index)
			if curItem not in listcombo:
				listcombo.append(str(curItem))
		listcombo.sort(reverse=True)
		listcombo = [DISP_CJOKER] + listcombo
		return listcombo

	def listmodel(self):
		if self.rowCount() > 0:
			for index in range(len(self.columns)):
				curItem = self.data(self.index(0, index))
				qDebug(index, self.myindex[index], curItem)

	def getData(self, row, colname):
		if self.rowCount() > 0:
			return QVariant(self.data(self.index(row, self.myindex.index(colname))))
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

	def getMedias(self):
		if self.rowCount() > 0:
			listmedia = []
			for row in range(self.rowCount()):
				file = path.join(self.data(self.index(row, self.myindex.index('REP_Track'))), self.data(self.index(row, self.myindex.index('FIL_Track'))))
				listmedia.append(convertUNC(file))
		return listmedia

	def replaceThunbnails(self, sizeTN, oldsizeTN):
		"""Modify size thunbnails."""
		# replace labels thunbnails
		numCov = self.grid.count()
		if numCov > 1:
			oldmaxCol = int(self.parent.frameGeometry().width()/(oldsizeTN+4))
			maxCol = int(self.parent.frameGeometry().width()/(sizeTN+4))
			curRow = curCol = cptIte = oldcurRow = oldcurCol = 0
			for row in range(numCov):
				if self.grid.itemAtPosition(oldcurRow, oldcurCol) != 0:
					# capture and clear label gridlayout
					layoutitem = self.grid.takeAt(cptIte)
					label = layoutitem.widget()
					self.grid.removeWidget(label)
					# resize
					label.setFixedSize(sizeTN, sizeTN)
					mypixmap = label.pixmap()
					if mypixmap.size().width() != sizeTN or mypixmap.size().height() != sizeTN:
						mypixmap = mypixmap.scaled(sizeTN, sizeTN, Qt.IgnoreAspectRatio, Qt.FastTransformation)
					label.setPixmap(mypixmap)
					# replace
					self.grid.addWidget(label, curRow, curCol)
				# position old next
				oldcurRow += 1
				if oldcurCol == oldmaxCol:
					oldcurCol = 0
					oldcurRow += 1
				# position next
				curCol += 1
				if curCol == maxCol:
					curCol = 0
					curRow += 1
	
	def builListThunbnails2(self, new=True, deb=0, fin=100):
		"""Build list Thunbnails"""
		listthun = []
		numAlb = self.rowCount()
		fin = min(fin,numAlb)
		for row in range(deb, fin):
			index = self.index(row, self.myindex.index('Cover'))
			pathcover = self.data(index)
			index = self.index(row, self.myindex.index('Name'))
			albumname = self.data(index)
			albumname = albumname.replace(' - ', '\n')
			# no cover or no display thunbnails covers (thnail_nod = 1)
			if THUN_NOD == 0 or pathcover == TEXT_NCO:
				Curalbmd5 = None
			else:
				index = self.index(row, self.myindex.index('MD5'))
				Curalbmd5 = self.data(index)				
			listthun.append([pathcover, Curalbmd5, row, albumname])
		# add thunnails add
		print(listthun)
		
	def displayThunbnails(self, new=True, deb=0, fin=100):
		if new:
			# clear thunbnails
			while self.grid.count() > 0:
				layoutitem = self.grid.takeAt(0)
				self.grid.removeWidget(layoutitem.widget())
				layoutitem.widget().deleteLater()
		else:
			# delete 2 labels endof before add more
			if self.grid.count() > 0:
				layoutitem = self.grid.takeAt(self.grid.count()-1)
				self.grid.removeWidget(layoutitem.widget())
				layoutitem.widget().deleteLater()
				layoutitem = self.grid.takeAt(self.grid.count()-1)
				self.grid.removeWidget(layoutitem.widget())
				layoutitem.widget().deleteLater()
		sizeTN = self.parent.sizeTN
		self.parent.updateGaugeBar(0, "Create thunbnails...")
		numAlb = self.rowCount()
		numCov = min(fin, numAlb)-deb
		maxCol = int(self.parent.frameGeometry().width()/(sizeTN+4))
		curRow = 0
		curCol = 0
		cptIte = 0
		for row in range(numAlb):
			if cptIte >= deb and cptIte <= fin:
				index = self.index(row, self.myindex.index('Cover'))
				pathcover = self.data(index)
				index = self.index(row, self.myindex.index('Name'))
				albumname = self.data(index)
				albumname = albumname.replace(' - ', '\n')
				# no cover or no display thunbnails covers (thnail_nod = 1)
				if THUN_NOD == 0 or pathcover == TEXT_NCO:
					Curalbmd5 = None
				else:
					index = self.index(row, self.myindex.index('MD5'))
					Curalbmd5 = self.data(index)
				label = TNLabel(self.parent, None, Curalbmd5, sizeTN,  row, albumname)
				label.mousePressEvent = (lambda event, r=row: self.parent.onSelectThunbnailChanged(event,  r))
				self.grid.addWidget(label, curRow, curCol)
				self.parent.updateGaugeBar((cptIte-deb+1)/numCov)
			cptIte = cptIte + 1
			# position
			curCol = curCol + 1
			if curCol == maxCol:
				curCol = 0
				curRow = curRow + 1
				self.parent.update()
			# max display, labels for more
			if cptIte == fin:
				# add for add more thunbnails
				monimage = QPixmap(THUN_DBA)
				mmessage = "{n} covers display max \n Click for more +{f}...".format(n=str(fin), 
											f=str(fin+fin) if (fin+fin) < (numAlb-fin) else str(numAlb-fin))
				label = TNLabel(self.parent, monimage, None, sizeTN,  999999, mmessage, True)
				label.mousePressEvent = (lambda e, d=fin, f=fin+fin: self.displayThunbnails(False, d, f))
				self.grid.addWidget(label, curRow, curCol)
				# add for all thunbnails
				curCol = curCol + 1
				if curCol == maxCol:
					curCol = 0
					curRow = curRow + 1
				monimage = QPixmap(THUN_DBA)
				mmessage = "{n} covers display max \n Click for all +{f}...".format(n=str(fin),
											f=str(numAlb-fin))
				label = TNLabel(self.parent, monimage, None, sizeTN,  999999,  mmessage, True)
				label.mousePressEvent = (lambda e, d=fin, f=numAlb-fin+1: self.displayThunbnails(False, d, f))
				self.grid.addWidget(label, curRow, curCol)
				self.parent.updateGaugeBar(1)
				break
		self.parent.updateGaugeBar(1)
