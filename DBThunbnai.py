#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv, executable
from os import system, path
from base64 import b64decode
from PyQt5.QtGui import QPixmap, QPainter, QFont
from PyQt5.QtCore import Qt, pyqtSlot, QSize, pyqtSignal, QRect, QSettings, qDebug
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QScrollArea, QLayout, QLabel
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
TEXT_NCO = configini.value('text_nocov')
PICM_NCO = path.join(PATH_PROG, 'IMG', configini.value('pict_blank'))
THUN_DBA = path.join(PATH_PROG, 'IMG', configini.value('picm_endof'))
FONT_MAI = configini.value('font00_ttx')
configini.endGroup()


# ##################################################################
class TNLabel(QLabel):
	"""Build label from thunbnail."""
	def __init__(self, parent, labelpixmap, labelmd5, labelsize, labelname, labeltext='', booltxt=False):
		super(TNLabel,  self).__init__(parent)
		self.parent = parent
		# build picture
		if labelmd5 is None and labelpixmap is None:
			# no cover : blank
			labelpixmap = QPixmap(PICM_NCO)
			booltxt = True
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
		#self.setFrameStyle(QFrame.Box | QFrame.Panel)

	@pyqtSlot()
	def leaveEvent(self, QEvent):
		self.setStyleSheet("border: 2px solid white")
		#self.setFrameStyle(QFrame.Plain)

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
			labelpixmap = QPixmap(PICM_NCO)
			booltxt = True
		return (labelpixmap, booltxt)


# ##################################################################
class DBThunbnails(QWidget):
	"""Widget Thunbnails for main & artworks viewers."""
	# signal
	signalthunchgt = pyqtSignal(int)		# select thunbnail
	signalthunadds = pyqtSignal(int)		# add thunbnails
	signalthubuild = pyqtSignal(float, str)		# build thunbnails
	
	def __init__(self, parent, sizetn, lintn):
		super(DBThunbnails, self).__init__(parent)
		
		# 1 [1 tn 1] 1 [1 tn 1] = (tn+3 * nb)
		self.parent = parent
		self.thunmarge = 1
		self.thunbncur = 0
		self.thunspace = thunspace = 0
		self.thunbsize = sizetn
		self.thunwidth = self.getTotalWidth(self.thunbsize)
		self.thunmaxco = self.getTotalColumns(sizetn)
		self.thunmaxli = lintn
		self.currow = 0
		self.curcol = 0
		
		self.setMinimumSize(QSize((self.thunmaxco * self.thunwidth) + self.thunmarge ,(self.thunmaxli * self.thunwidth) + self.thunmarge))
		self.scrollArea = QScrollArea()
		self.scrollArea.setContentsMargins(0, 0, 0, 0)
		self.scrollArea.setSizeIncrement(QSize(self.thunwidth, self.thunwidth))
		self.scrollArea.scrollContentsBy(self.thunwidth, self.thunwidth)
		self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scrollArea.setMinimumSize(QSize((self.thunmaxco * self.thunwidth) + self.thunmarge ,(self.thunmaxli * self.thunwidth) + self.thunmarge))
		
		self.gridthunbnails = QGridLayout()
		self.gridthunbnails.setContentsMargins(thunspace, thunspace, thunspace, thunspace)
		self.gridthunbnails.setSpacing(0)
		
		self.scrollAreaWidgetthunbnails = QWidget(self)
		self.scrollAreaWidgetthunbnails.setContentsMargins(0, 0, 0, 0)
		self.gridscrollarea = QGridLayout(self.scrollAreaWidgetthunbnails)
		self.gridscrollarea.addLayout(self.gridthunbnails, 0, 0, 1, 1)
		self.gridscrollarea.setSizeConstraint(QLayout.SetFixedSize)
		self.gridscrollarea.setContentsMargins(0, 0, 0, 0)
		self.gridscrollarea.setSpacing(0)
		self.scrollArea.setWidget(self.scrollAreaWidgetthunbnails)
		self.scrollArea.keyPressEvent = self.keyPressEvent
		
		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(self.scrollArea)
		self.setLayout(layout)
	
	def getTotalWidth(self, sizetn):
		"""Apply margin to size."""
		return (sizetn + (2 * self.thunmarge) + self.thunspace)
	
	def getTotalColumns(self, sizetn):
		"""Get number of columns possible."""
		return (int((self.parent.width() - 10) / self.thunwidth))
	
	def getTotalThunbnails(self):
		"""total thunbnails present."""
		return (self.gridthunbnails.count())
		
	def addthunbails(self, listthunbnails, sizetn=None,  new=True, deb=0, fin=100, total=9999):
		"""Build thunbails. list = [md5, id, labelname] or list = [image]."""
		# init grid
		if new:
			self.delThunbails()
			self.currow = 0
			self.curcol = 0
		else:
			self.delThunbailsEndof()
		# init new size
		if sizetn is not None:
			self.thunbsize = sizetn
			self.thunwidth = self.getTotalWidth(sizetn)
			self.thunmaxco = self.getTotalColumns(sizetn)
			self.scrollArea.scrollContentsBy(self.thunwidth, self.thunwidth)
		cpt = 0
		end = min(len(listthunbnails)+deb, fin)
		for row in range(deb, end):
			thundesc = listthunbnails[cpt]
			# 2 modes : list or pathcover
			if isinstance(thundesc, list):
				# build cover b64 from md5
				albummd5 = thundesc[0]
				albumrow = thundesc[1]
				albumname = (thundesc[2]).replace(' - ', '\n')
				label = TNLabel(self.parent, None, albummd5, self.thunbsize,  albumrow, albumname)
			else:
				# only path cover
				mythunb = QPixmap(listthunbnails[cpt])
				label = TNLabel(self, mythunb, None, self.thunbsize, listthunbnails[cpt])
			label.mousePressEvent = (lambda event, n=cpt+deb: self.onSelectThunbnail(n))
			self.gridthunbnails.addWidget(label, self.currow, self.curcol)
			# signal gauge
			#qDebug('onAddThunbnail EMIT add '+str(self.thunbncur))
			self.signalthubuild.emit(cpt/len(listthunbnails), 'Create thunbnails')
			cpt += 1
			# position
			self.curcol += 1
			if self.curcol == self.thunmaxco:
				self.curcol = 0
				self.currow += 1
		if total > fin:
			# add for add more thunbnails
			monimage = QPixmap(THUN_DBA)
			mmessage = "{n} covers displaying \n Click for more...".format(n=str(fin))
			label = TNLabel(self.parent, monimage, None, self.thunbsize, 999999, mmessage, True)
			label.mousePressEvent = (lambda event, n=999999: self.onSelectThunbnail(n))
			self.gridthunbnails.addWidget(label, self.currow, self.curcol)
		if new:
			self.thunbncur = 0
		self.signalthubuild.emit(1, 'end Create thunbnails')
	
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
		self.replaceThunbnails(None)
		
	def replaceThunbnails(self, sizetn=None):
		"""Replace Thunbails."""
		numCov = self.getTotalThunbnails()
		if numCov > 1:
			thunoldco = self.thunmaxco
			if sizetn is not None:
				self.thunwidth = self.getTotalWidth(sizetn)
				self.scrollArea.scrollContentsBy(self.thunwidth, self.thunwidth)
			else:
				sizetn = self.thunbsize
			self.thunmaxco = self.getTotalColumns(sizetn)
			curRow = curCol = oldcurRow = oldcurCol = 0
			for row in range(numCov):
				if self.gridthunbnails.itemAtPosition(oldcurRow, oldcurCol) != 0:
					# capture and clear label gridlayout
					layoutitem = self.gridthunbnails.takeAt(0)
					label = layoutitem.widget()
					self.gridthunbnails.removeWidget(label)
					# resize
					label.setFixedSize(sizetn, sizetn)
					mypixmap = label.pixmap()
					if sizetn is not None:
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
			# save position -1 for add
			curCol -= 1
			if curCol == -1:
				curCol = self.thunmaxco
				curRow -= 1
			self.currow = curRow
			self.curcol = curCol

	
	def selectThunbnail(self, tunhnum):
		"""Select."""
		if tunhnum != self.thunbncur and self.thunbncur is not None:
			self.unselectThunbnail(self.thunbncur)
		if tunhnum <= self.getTotalThunbnails() and tunhnum is not None:
			self.thunbncur = tunhnum
			thunitem = self.gridthunbnails.itemAt(tunhnum).widget()
			thunitem.setStyleSheet("border: 2px solid red;")
			self.scrollArea.ensureWidgetVisible(thunitem)
		
	def unselectThunbnail(self, tunhnum):
		"""No select."""
		thunitem = self.gridthunbnails.itemAt(tunhnum).widget()
		thunitem.setStyleSheet("border: 2px solid white;")

	def onSelectThunbnail(self, tunhnum):
		"""Select thunbnail, send signal."""
		if tunhnum == 999999:
			qDebug('onSelectThunbnail EMIT add '+str(self.getTotalThunbnails()))
			# emit signal add thunbnails
			self.signalthunadds.emit(self.getTotalThunbnails()-1)
		elif tunhnum != self.thunbncur and tunhnum != 999999:
			# emit signal select thunbnails
			qDebug('onSelectThunbnail EMIT sel '+str(self.thunbncur))
			self.signalthunchgt.emit(tunhnum)
			self.selectThunbnail(tunhnum)
