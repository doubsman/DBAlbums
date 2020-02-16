#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPixmap, QPainter, QFont
from PyQt5.QtCore import Qt, pyqtSlot, QSize, pyqtSignal, QRect, qDebug
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QScrollArea, QLayout, QLabel


class TNLabel(QLabel):
	"""Build label from thunbnail."""
	def __init__(self, parent, labelpixmap, labelid, labelsize, labelname, labeltext='', booltxt=False):
		super(TNLabel,  self).__init__(parent)
		self.parent = parent
		# build picture
		if labelid is None and labelpixmap is None:
			# no cover : blank
			labelpixmap = QPixmap(self.parent.PICM_NCO)
			booltxt = True
		elif labelid is not None:
			# extract picture
			labelpixmap, booltxt = self.extractCover(labelid)
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
		painter.setFont(QFont(self.parent.FONT_MAI, 8))
		painter.drawText(QRect(0, 0, labelsize, labelsize), Qt.AlignCenter, labeltext)
		painter.end()
		return labelpixmap

	def extractCover(self, idcd, namerequest='thumbnailpix'):
		"""Get base picture cover."""
		booltxt = True
		request = (self.parent.CnxConnect.getrequest(namerequest)).format(id=idcd)
		try:
			cover = self.parent.CnxConnect.sqlToArray(request)
			if len(cover) > 0:
				labelpixmap = QPixmap()
				labelpixmap.loadFromData(cover[0])
				booltxt = False
			else:
				labelpixmap = QPixmap(self.parent.PICM_NCO)
		except:
			pass
			qDebug('err thunbnail read : '+str(idcd))
			labelpixmap = QPixmap(self.parent.PICM_NCO)
		return labelpixmap, booltxt


# ##################################################################
class DBThunbnails(QWidget):
	"""Widget Thunbnails for main & artworks viewers."""
	# signal
	signalthunchgt = pyqtSignal(int)		# select thunbnail
	signalthunadds = pyqtSignal(int)		# add thunbnails
	signalthubuild = pyqtSignal(float, str)	# build thunbnails
	
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
		self.stopbuild = False
		self.isbuilder = False
		self.currow = 0
		self.curcol = 0
		
		self.setMinimumSize(QSize((self.thunmaxco * self.thunwidth) + self.thunmarge ,(self.thunmaxli * self.thunwidth) + self.thunmarge))
		self.scrollArea = QScrollArea()
		self.scrollArea.setContentsMargins(0, 0, 0, 0)
		self.scrollArea.scrollContentsBy(self.thunwidth, self.thunwidth)
		self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scrollArea.setMinimumSize(QSize((self.thunmaxco * self.thunwidth) + self.thunmarge ,(self.thunmaxli * self.thunwidth) + self.thunmarge))
		self.scrollArea.setSizeIncrement(QSize(self.thunwidth, self.thunwidth))
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
		
		self.scrollBarevent = self.scrollArea.verticalScrollBar()
		self.scrollBarevent.valueChanged.connect(self.endScroobarVertical)

		self.booladdthub = False
		self.isbuilder = False

		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(self.scrollArea)
		self.setLayout(layout)
	
	def endScroobarVertical(self, value):
		# max scroll + no total display thumbnails + not build thumbail 
		if value == self.scrollArea.verticalScrollBar().maximum() and self.booladdthub and not(self.isbuilder):
			# emit signal add thunbnails
			self.signalthunadds.emit(self.getTotalThunbnails())

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
		"""Build thunbails. list = [id, rowgrid, albumname] or list = [image]."""
		qDebug("Start Add Thunbnails")
		self.stopbuild = False
		self.isbuilder = True
		fin = max(self.getTotalThunbnails(), fin)
		# init grid
		if new:
			self.delThunbails()
			self.currow = 0
			self.curcol = 0
			self.thunbncur = 0
		#else:
			#self.delThunbailsEndof()
		# init new size
		if sizetn is not None:
			self.thunbsize = sizetn
			self.thunwidth = self.getTotalWidth(sizetn)
			self.thunmaxco = self.getTotalColumns(sizetn)
			self.scrollArea.scrollContentsBy(self.thunwidth, self.thunwidth)
		cpt = 0
		end = min(len(listthunbnails)+deb, fin)
		for _ in range(deb, end):
			thundesc = listthunbnails[cpt]
			if self.stopbuild:
				self.isbuilder = False
				qDebug("Break Add Thunbnails")
				break
			# 2 modes : list or pathcover
			if isinstance(thundesc, list):
				# build cover
				albumid = thundesc[0]
				albumrow = thundesc[1]
				albumname = (thundesc[2]).replace(' - ', '\n')
				label = TNLabel(self.parent, None, albumid, self.thunbsize,  albumrow, albumname)
			else:
				# only path cover
				mythunb = QPixmap(listthunbnails[cpt])
				label = TNLabel(self.parent, mythunb, None, self.thunbsize, listthunbnails[cpt])
			label.mousePressEvent = (lambda event, n=cpt+deb: self.onSelectThunbnail(n))
			self.gridthunbnails.addWidget(label, self.currow, self.curcol)
			# signal gauge
			#qDebug('onAddThunbnail EMIT add '+str(self.thunbncur))
			self.signalthubuild.emit((cpt/(len(listthunbnails) + deb))*100, 'Create thunbnails')
			cpt += 1
			# position
			self.curcol += 1
			if self.curcol == self.thunmaxco:
				self.curcol = 0
				self.currow += 1
		self.booladdthub = False
		if total > fin:
			self.booladdthub = True
		self.signalthubuild.emit(100, 'end Create thunbnails')
		self.isbuilder = False
		qDebug('Start End Thunbnails (' + str(self.getTotalThunbnails()) + ')')
	
	def delThunbails(self):
		"""Remove thunbnails."""
		while self.getTotalThunbnails() > 0:
			layoutitem = self.gridthunbnails.takeAt(0)
			self.gridthunbnails.removeWidget(layoutitem.widget())
			layoutitem.widget().deleteLater()

	@pyqtSlot()
	def resizeEvent(self, event):
		"""Widget size move."""
		self.replaceThunbnails(self.parent.sizeTN)
		
	def replaceThunbnails(self, sizetn=None):
		"""Replace Thunbails."""
		numCov = self.getTotalThunbnails()
		if numCov > 1:
			self.stopbuild = False
			self.isbuilder = True
			thunoldco = self.thunmaxco
			if sizetn is not None:
				self.thunwidth = self.getTotalWidth(sizetn)
				self.scrollArea.scrollContentsBy(self.thunwidth, self.thunwidth)
			else:
				sizetn = self.thunbsize
			self.thunmaxco = self.getTotalColumns(sizetn)
			curRow = curCol = oldcurRow = oldcurCol = 0
			for _ in range(numCov):
				if self.stopbuild:
					self.isbuilder = False
					break
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
				oldcurCol += 1
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
			self.isbuilder = False
	
	def selectThunbnail(self, tunhnum):
		"""Select."""
		if tunhnum != self.thunbncur and self.thunbncur is not None:
			self.unselectThunbnail(self.thunbncur)
		if tunhnum <= self.getTotalThunbnails() and tunhnum is not None:
			self.thunbncur = tunhnum
			if self.gridthunbnails.itemAt(tunhnum) is not None:
				thunitem = self.gridthunbnails.itemAt(tunhnum).widget()
				thunitem.setStyleSheet("border: 2px solid red;")
				self.scrollArea.ensureWidgetVisible(thunitem)
		
	def unselectThunbnail(self, tunhnum):
		"""No select."""
		if self.gridthunbnails.itemAt(tunhnum) is not None:
			thunitem = self.gridthunbnails.itemAt(tunhnum).widget()
			thunitem.setStyleSheet("border: 2px solid white;")

	def onSelectThunbnail(self, tunhnum):
		"""Select thunbnail, send signal."""
		if tunhnum != self.thunbncur:
			# emit signal select thunbnails
			qDebug('onSelectThunbnail EMIT sel '+str(self.thunbncur))
			self.signalthunchgt.emit(tunhnum)
			self.selectThunbnail(tunhnum)
