#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv, executable
from os import system, path
from base64 import b64decode
from PyQt5.QtGui import QPixmap, QPainter, QFont
from PyQt5.QtCore import Qt, pyqtSlot, QSize, pyqtSignal, QRect, QSettings, qDebug
from PyQt5.QtWidgets import (QWidget, QGridLayout, QVBoxLayout, 
						 QScrollArea, QLayout, QLabel)
from DBDatabase import getrequest, buildTabFromRequest

# path
if getattr(system, 'frozen', False):
	# frozen
	PATH_PROG = path.dirname(executable)
else:
	# unfrozen
	PATH_PROG = path.realpath(path.dirname(argv[0]))
	
VERS_PROG = '1.00'
TITL_PROG = "Artwork viewer v{v} : ".format(v=VERS_PROG)

FILE__INI = 'DBAlbums.ini'
configini = QSettings(FILE__INI, QSettings.IniFormat)
configini.beginGroup('dbalbums')
WINS_ICO = path.join(PATH_PROG, 'IMG', configini.value('wins_icone'))
TEXT_NCO = configini.value('text_nocov')
PICT_NCO = path.join(PATH_PROG, 'IMG', configini.value('pict_blank'))
THUN_DBA = path.join(PATH_PROG, 'IMG', configini.value('picm_endof'))
FONT_MAI = configini.value('font00_ttx')
MASKCOVER = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.bmp', '.tiff')


# ##################################################################
class TNLabel(QLabel):
	"""Build label from thunbnail."""
	def __init__(self, parent, labelpixmap, labelmd5, labelsize, labelname, labeltext='', booltxt=False):
		super(TNLabel,  self).__init__(parent)
		self.parent = parent
		# build picture
		if labelmd5 is None and labelpixmap is None:
			# no cover : blank
			labelpixmap = QPixmap(PICT_NCO)
		elif labelmd5 is not None:
			# extract b64 picture
			labelpixmap, booltxt = self.extractCoverb64(labelmd5)
		# resize 
		if labelpixmap.width() != labelsize or labelpixmap.height() != labelsize:
			qDebug('resize picture')
			labelpixmap = labelpixmap.scaled(labelsize, labelsize, Qt.IgnoreAspectRatio, Qt.FastTransformation)
		# write text
		if booltxt: 
			labelpixmap = self.writeText(labelpixmap, labelsize, labeltext)
		# label
		self.setPixmap(labelpixmap)
		self.setFixedSize(labelsize, labelsize)
		self.setStyleSheet("border: 2px solid white")
		self.Name = labelname

	@pyqtSlot()
	def enterEvent(self, QEvent):
		self.setStyleSheet("border: 2px solid black")

	@pyqtSlot()
	def leaveEvent(self, QEvent):
		self.setStyleSheet("border: 2px solid white")

	def writeText(self, labelpixmap, labelsize, labeltext):
		"""Add text to cover if is blank."""
		# add text infos
		painter = QPainter(labelpixmap)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.drawPixmap(QRect(0, 0, labelpixmap.width(), labelpixmap.width()), labelpixmap)
		painter.fillRect(QRect(5, labelsize/3, labelsize-5, labelsize/3), Qt.black)
		painter.setPen(Qt.white)
		painter.setFont(QFont(FONT_MAI, 8))
		painter.drawText(QRect(0, 0, labelsize, labelsize), Qt.AlignCenter, labeltext)
		painter.end()
		return labelpixmap

	def extractCoverb64(self, md5, namerequest='minicover'):
		"""Get base64 picture cover."""
		request = (getrequest(namerequest)).format(MD5=md5)
		try:
			coverb64 = buildTabFromRequest(request)[0]
			cover = b64decode(coverb64)
			labelpixmap = QPixmap()
			labelpixmap.loadFromData(cover)
			booltxt = False
		except:
			pass
			qDebug('err thunbnail read : '+str(md5))
			labelpixmap = QPixmap(PICT_NCO)
			booltxt = True
		return (labelpixmap, booltxt)


# ##################################################################
class DBThunbnails(QWidget):
	"""Widget Thunbnails."""
	# signal
	signalthunchgt = pyqtSignal(int)
	signalthubuild = pyqtSignal(int)
	
	def __init__(self, parent, sizetn, lintn):
		super(DBThunbnails, self).__init__(parent)
		
		# 1 [2 tn 2] 1 [2 tn 2] 1 [2 tn 2] 1 [2 tn 2] = (tn+5 * nb)
		self.parent = parent
		self.thunmarge = 2
		self.thunbncur = None
		self.thunspace = thunspace = 2
		self.thunbsize = sizetn
		self.thunwidth = self.getTotalWidth(self.thunbsize)
		self.thunmaxco = self.getTotalColumns()
		self.thunmaxli = lintn
		self.currow = 0
		self.curcol = 0
		
		self.scrollArea = QScrollArea()
		self.scrollArea.setSizeIncrement(QSize(self.thunwidth, self.thunwidth))
		self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scrollArea.setMinimumSize(QSize((self.thunmaxco * self.thunwidth) + self.thunmarge ,(self.thunmaxli * self.thunwidth) + self.thunmarge))
		
		self.gridthunbnails = QGridLayout()
		self.gridthunbnails.setContentsMargins(thunspace, thunspace, thunspace, thunspace)
		self.gridthunbnails.setSpacing(thunspace)
		
		self.scrollAreaWidgetthunbnails = QWidget(self)
		self.gridscrollarea = QGridLayout(self.scrollAreaWidgetthunbnails)
		self.gridscrollarea.addLayout(self.gridthunbnails, 0, 0, 1, 1)
		self.gridscrollarea.setSizeConstraint(QLayout.SetFixedSize)
		self.gridscrollarea.setContentsMargins(thunspace, thunspace, thunspace, thunspace)
		
		self.scrollArea.setWidget(self.scrollAreaWidgetthunbnails)
		self.scrollArea.keyPressEvent = self.keyPressEvent
		
		layout = QVBoxLayout()
		layout.addWidget(self.scrollArea)
		self.setLayout(layout)
	
	def getTotalWidth(self, sizetn):
		"""Apply margin to size."""
		return (sizetn + (2 * self.thunmarge) + self.thunspace)
	
	def getTotalColumns(self):
		"""Get number of columns possible."""
		return (int((self.parent.width() - 10) / self.thunwidth))
	
	def getTotalThunbnails(self):
		"""total thunbnails present."""
		return (self.gridthunbnails.count())
		
	def addthunbails(self, listthunbnails, new=True, deb=0, fin=100):
		"""Build thunbails. list = [md5, id, labelname] or list = [image]."""
		if new:
			self.delThunbails()
			self.currow = 0
			self.curcol = 0
		else:
			self.delThunbailsEndof()
		cpt = 0
		end = min(len(listthunbnails), fin)
		for row in range(deb, end):
			thundesc = listthunbnails[row]
			if isinstance(thundesc, list):
				# build cover b64 from md5
				albummd5 = thundesc[0]
				albumrow = thundesc[1]
				albumname = (thundesc[2]).replace(' - ', '\n')
				label = TNLabel(self.parent, None, albummd5, self.thunwidth,  albumrow, albumname)
			else:
				# only path cover
				mythunb = QPixmap(listthunbnails[row])
				label = TNLabel(self, mythunb, None, self.thunbsize, listthunbnails[row])
				label.mousePressEvent = (lambda event, n=cpt: self.onSelectThunbnail(n))
			self.gridthunbnails.addWidget(label, self.currow, self.curcol)
			cpt += 1
			# position
			self.curcol += 1
			if self.curcol == self.thunmaxco:
				self.curcol = 0
				self.currow += 1
		if cpt == fin:
			# add for add more thunbnails
			monimage = QPixmap(THUN_DBA)
			mmessage = "{n} covers display max \n Click for more +{f}...".format(n=str(fin), 
										f=str(fin+fin) if (fin+fin) < (end-fin) else str(end-fin))
			label = TNLabel(self.parent, monimage, None, self.thunwidth,  999999, mmessage, True)
			#label.mousePressEvent = (lambda e, d=fin, f=fin+fin: self.displayThunbnails(False, d, f))
			self.gridthunbnails.addWidget(label, self.currow, self.curcol)
		if new:
			self.thunbncur = 0
		self.selectThunbnail(self.thunbncur)
	
	def builThunbnail(self, thunpix ):
		"""Buil label thunbail."""
		pass
	
	def delThunbails(self):
		"""Remove thunbnails."""
		while self.getTotalThunbnails() > 0:
			layoutitem = self.gridthunbnails.takeAt(0)
			self.gridthunbnails.removeWidget(layoutitem.widget())
			layoutitem.widget().deleteLater()

	def delThunbailsEndof(self):
		"""Remove thunbnails EndOf."""
		if self.getTotalThunbnails() > 0:
			layoutitem = self.gridthunbnails.takeAt(self.getTotalThunbnails()-1)
			self.gridthunbnails.removeWidget(layoutitem.widget())
			layoutitem.widget().deleteLater()

	@pyqtSlot()
	def resizeEvent(self, event):
		"""Widget size move."""
		self.replaceThunbnail()
		
	def replaceThunbnail(self, sizetn=None):
		"""Replace Thunbails."""
		numCov = self.gridthunbnails.count()
		if numCov > 1:
			if sizetn is None:
				sizetn = self.thunwidth
			else:
				sizetn = self.getTotalWidth(sizetn)
			thunoldco = self.thunmaxco
			self.thunmaxco = self.getTotalColumns()
			curRow = curCol = cptIte = oldcurRow = oldcurCol = 0
			for row in range(numCov):
				if self.gridthunbnails.itemAtPosition(oldcurRow, oldcurCol) != 0:
					# capture and clear label gridlayout
					layoutitem = self.gridthunbnails.takeAt(cptIte)
					label = layoutitem.widget()
					self.gridthunbnails.removeWidget(label)
					# resize
					label.setFixedSize(sizetn, sizetn)
					mypixmap = label.pixmap()
					if mypixmap.size().width() != sizetn or mypixmap.size().height() != sizetn:
						mypixmap = mypixmap.scaled(sizetn, sizetn, Qt.IgnoreAspectRatio, Qt.FastTransformation)
					label.setPixmap(mypixmap)
					# replace
					self.gridthunbnails.addWidget(label, curRow, curCol)
				# position old next
				oldcurRow += 1
				if oldcurCol == thunoldco:
					oldcurCol = 0
					oldcurRow += 1
				# position next
				curCol += 1
				if curCol == self.thunmaxco:
					curCol = 0
					curRow += 1
	
	def selectThunbnail(self, tunhnum):
		"""Select."""
		thunitem = self.gridthunbnails.itemAt(tunhnum).widget()
		thunitem.setStyleSheet("border: 2px solid red;")
		self.scrollArea.ensureWidgetVisible(thunitem)

	def unselectThunbnail(self, tunhnum):
		"""No select."""
		thunitem = self.gridthunbnails.itemAt(tunhnum).widget()
		thunitem.setStyleSheet("border: 2px solid white;")

	def onSelectThunbnail(self, tunhnum):
		"""Select thunbnail, send signal"""
		if self.thunbncur is not None:
			if tunhnum != self.thunbncur:
				self.unselectThunbnail(self.thunbncur)
				self.thunbncur = tunhnum
				self.selectThunbnail(self.thunbncur)
				self.signalthunchgt.emit(self.thunbncur)
			else:
				self.selectThunbnail(self.thunbncur)
