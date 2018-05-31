#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import executable, argv
from os import path, system
from base64 import b64decode
from PyQt5.QtGui import QPixmap, QPainter, QFont
from PyQt5.QtCore import Qt, QVariant, pyqtSlot, QRect, qDebug, QSettings, QDir
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtWidgets import QLabel, QMessageBox
from DBFunction import convertUNC
from DBDatabase import getrequest, buildTabFromRequest


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
THUN_DBA = configini.value('picm_endof')
PICM_NCO = configini.value('picm_blank')
PICT_NCO = configini.value('pict_blank')
FONT_MAI = configini.value('font00_ttx')
DISP_CJOKER = configini.value('text_joker')


# ##################################################################
class TNLabel(QLabel):
	"""Build label from thunbnail"""
	def __init__(self, parent, monimage,  size,  row, **kwargs):
		super(TNLabel,  self).__init__(parent, **kwargs)
		self.parent = parent
		# label
		self.setPixmap(monimage)
		self.setFixedSize(size, size)
		self.setStyleSheet("border: 2px solid white")
		self.Name = row

	@pyqtSlot()
	def enterEvent(self, QEvent):
		# here the code for mouse hover
		self.setStyleSheet("border: 2px solid black")

	@pyqtSlot()
	def leaveEvent(self, QEvent):
		# here the code for mouse leave
		self.setStyleSheet("border: 2px solid white")


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
				# no cover or no display thunbnails covers (thnail_nod = 1)
				if THUN_NOD == 0 or pathcover == TEXT_NCO:
					if THUN_NOD == 0:
						pathcover = TEXT_NCO
					monimage = QPixmap(PICM_NCO)
					monimage = self.buildTextThunbnail(pathcover, albumname.replace(' - ', '\n'), monimage, sizeTN)
				else:
					index = self.index(row, self.myindex.index('MD5'))
					Curalbmd5 = self.data(index)
					monimage = self.buildCover(pathcover, Curalbmd5, sizeTN, 'minicover')
				label = TNLabel(self.parent, monimage, sizeTN,  row)
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
				monimage = self.buildTextThunbnail(THUN_DBA, "{n} covers display max \n Click for more +{f}...".format(n=str(fin), f=str(fin+fin) if (fin+fin) < (numAlb-fin) else str(numAlb-fin)), monimage, sizeTN)
				label = TNLabel(self.parent, monimage, sizeTN,  999999)
				label.mousePressEvent = (lambda e, d=fin, f=fin+fin: self.displayThunbnails(False, d, f))
				self.grid.addWidget(label, curRow, curCol)
				# add for all thunbnails
				curCol = curCol + 1
				if curCol == maxCol:
					curCol = 0
					curRow = curRow + 1
				monimage = QPixmap(THUN_DBA)
				monimage = self.buildTextThunbnail(THUN_DBA, "{n} covers display max \n Click for all +{f}...".format(n=str(fin), f=str(numAlb-fin)), monimage, sizeTN)
				label = TNLabel(self.parent, monimage, sizeTN,  999999)
				label.mousePressEvent = (lambda e, d=fin, f=numAlb-fin+1: self.displayThunbnails(False, d, f))
				self.grid.addWidget(label, curRow, curCol)
				self.parent.updateGaugeBar(1)
				break
		self.parent.updateGaugeBar(1)

	def buildTextThunbnail(self, pathcover, texte, monimage, sizeTN):
		"""Add text to cover if is blank."""
		# no cover, add blank
		if pathcover[0:len(TEXT_NCO)] == TEXT_NCO or pathcover == THUN_DBA:
			# add text infos
			painter = QPainter(monimage)
			painter.setRenderHint(QPainter.Antialiasing)
			painter.drawPixmap(QRect(0, 0, monimage.width(), monimage.width()), monimage)
			painter.fillRect(QRect(5, sizeTN/3, sizeTN-5, sizeTN/3), Qt.black)
			painter.setPen(Qt.white)
			painter.setFont(QFont(FONT_MAI, 8))
			painter.drawText(QRect(0, 0, sizeTN, sizeTN), Qt.AlignCenter, texte)
			painter.end()
		return monimage

	def buildCover(self, pathcover, md5, sizeTN, namerequest='cover'):
		"""Get base64 picture cover."""
		request = (getrequest(namerequest)).format(MD5=md5)
		if pathcover[0:len(TEXT_NCO)] == TEXT_NCO:
			# no cover : blank
			monimage = QPixmap(PICT_NCO)
		else:
			# cover base64/mysql
			try:
				coverb64 = buildTabFromRequest(request)[0]
				cover = b64decode(coverb64)
				monimage = QPixmap()
				monimage.loadFromData(cover)
			except:
				pass
				QMessageBox(self, TITL_PROG, ' : err thunbnail read :'+pathcover)
				monimage = QPixmap(PICT_NCO)
		if monimage.width() != sizeTN or monimage.height() != sizeTN:
			qDebug('resize picture')
			monimage = monimage.scaled(sizeTN, sizeTN, Qt.IgnoreAspectRatio, Qt.FastTransformation)
		return (monimage)

