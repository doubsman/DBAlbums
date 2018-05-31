#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ############################################################################
# # Audio pyQT5 Player by SFI
# ############################################################################
from os import path
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot, QSize
from PyQt5.QtWidgets import (QMenu, QWidget, QSizePolicy, QGridLayout, QVBoxLayout, 
						 QScrollArea, QFrame, QLayout, QLabel)
from DBModeldat import TNLabel						 
from DBFunction import openFolder, getListFiles, centerWidget


VERS_PROG = '1.00'
TITL_PROG = "Player v{v} : ".format(v=VERS_PROG)
WINS_ICO = "DBAlbums-icone.ico"
WIDT_PICM = 1250
HEIG_MAIN = 1060
TEXT_NCO = 'No Picture'
MASKCOVER = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.bmp', '.tiff')


# ##################################################################
class CoverViewGui(QWidget):
	def __init__(self, cover, namealbum, w=HEIG_MAIN, h=HEIG_MAIN, parent=None):
		super(CoverViewGui, self).__init__(parent)
		self.resize(w, h)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags(Qt.WindowTitleHint)
		self.setWindowFlags(Qt.WindowSystemMenuHint)
		self.setWindowFlags(Qt.WindowCloseButtonHint)
		self.setWindowIcon(QIcon(WINS_ICO))
		self.setWindowTitle("{name} - [{w}x{h}] orignal size:[{wo}x{ho}]".format(w=w, h=h, name=namealbum, wo=str(cover.width()), ho=str(cover.height())))
		centerWidget(self)
		covdi = cover.scaled(w, h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
		label = QLabel(self)
		label.setPixmap(covdi)
		label.mousePressEvent = lambda e: self.destroy()
		posit = QGridLayout(self)
		posit.setContentsMargins(0, 0, 0, 0)
		posit.addWidget(label, 0, 0)
		self.setLayout(posit)
		self.show()

	@pyqtSlot()
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.destroy()


# ##################################################################
class ArtworksGui(QWidget):
	def __init__(self, pathartworks, nametittle, createcover, w, h, sizeTN=WIDT_PICM, parent=None):
		super(ArtworksGui, self).__init__(parent)
		self.resize(w, h)
		self.setWindowIcon(QIcon(WINS_ICO))
		self.setWindowTitle(TITL_PROG+" [view ArtWorks] : reading files covers...")
		self.setStyleSheet('QWidget{background-color: darkgray} '
							'QLabel{background-color: darkgray;}')
		self.height = h
		self.mycover = None
		self.sizethun = sizeTN
		self.scrollAreaWidgetthunbnails = QWidget(self)
		self.scrollArea = QScrollArea()
		self.scrollArea.setSizeIncrement(QSize(sizeTN+4, sizeTN+4))
		self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scrollArea.setMinimumSize(QSize(8*(self.sizethun+4), 155))
		self.gridthunbnails = QGridLayout()
		self.gridthunbnails.setContentsMargins(5, 5, 5, 5)
		self.labelcover = QLabel()
		self.labelcover.setAlignment(Qt.AlignCenter)
		self.labelcover.setMinimumSize(QSize(self.width()-40, self.height-(self.gridthunbnails.rowCount()*(self.sizethun+4))-70))
		self.labelcover.enterEvent = self.onSelectCover
		self.labelcover.setContextMenuPolicy(Qt.CustomContextMenu)
		self.labelcover.customContextMenuRequested.connect(self.popUpMenu)
		# popup albums
		self.menua = QMenu()
		self.action_OFC = self.menua.addAction("Open Folder...", lambda c=pathartworks: openFolder(c))
		self.action_COV = self.menua.addAction("Create cover file...", self.createFileCover)
		# create cover option only if no cover file
		if createcover[0:len(TEXT_NCO)] != TEXT_NCO:
			self.action_COV.setEnabled(False)
		self.line = QFrame(self)
		self.line.setFrameShape(QFrame.HLine)
		self.line.setFrameShadow(QFrame.Sunken)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.labelcover.setSizePolicy(sizePolicy)
		labelcgrid = QGridLayout()
		labelcgrid.setContentsMargins(5, 5, 5, 5)
		labelcgrid.addWidget(self.labelcover)
		labelcgrid.setSizeConstraint(QLayout.SetFixedSize)
		self.gridthunbnails.setContentsMargins(3, 5, -1, 5)
		self.gridthunbnails.setSpacing(2)
		self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetthunbnails)
		self.gridLayout_2.addLayout(self.gridthunbnails, 0, 0, 1, 1)

		self.scrollArea.setWidget(self.scrollAreaWidgetthunbnails)
		layout = QVBoxLayout(self)
		layout.addWidget(self.scrollAreaWidgetthunbnails)
		layout.addWidget(self.line)
		layout.addStretch(1)
		layout.addLayout(labelcgrid)
		self.setLayout(layout)
		centerWidget(self)
		self.show()

		# build list covers
		self.nametittle = nametittle
		self.fileslist = list(getListFiles(pathartworks, MASKCOVER))
		self.pathartworks = pathartworks
		self.filelist = self.fileslist[0]

		maxCol = int(w/self.sizethun)
		curRow = curCol = 0
		# build thunbnails
		cpt = 0
		for filelist in self.fileslist:
			mycover = QPixmap(filelist)
			mythunb = mycover.scaled(sizeTN, sizeTN, Qt.IgnoreAspectRatio, Qt.FastTransformation)
			label = TNLabel(self, mythunb, sizeTN,  filelist)
			label.mousePressEvent = (lambda event,  n=cpt: self.onSelectThunbnailChanged(event, n))
			self.gridthunbnails.addWidget(label, curRow, curCol)
			cpt += 1
			# position
			curCol += 1
			if curCol == maxCol:
				curCol = 0
				curRow += 1
		# build large cover
		self.numpic = 0
		self.onSelectThunbnailChanged(None, self.numpic)

	@pyqtSlot()
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.destroy()
		elif event.key() == Qt.Key_Left:
			self.onSelectThunbnailChanged(None, (self.numpic-1) % len(self.fileslist))
		elif event.key() == Qt.Key_Right:
			self.onSelectThunbnailChanged(None, (self.numpic+1) % len(self.fileslist))

	@pyqtSlot()
	def resizeEvent(self, event):
		if self.gridthunbnails.count() > 0:
			self.replaceThunbnails(self.sizethun, self.sizethun)
			self.onSelectThunbnailChanged(None, self.numpic)

	def popUpMenu(self,  position):
		self.menua.exec_(self.labelcover.mapToGlobal(position))

	def onSelectThunbnailChanged(self, event, numpic):
		"""Display picture."""
		self.filelist = self.fileslist[numpic]
		self.numpic = numpic
		self.mycover = QPixmap(self.filelist)
		width, height, new_width, new_height = self.resizeImage(self.width()-40, self.height-(self.gridthunbnails.rowCount()*(self.sizethun+4))-70, self.mycover)
		dicover = self.mycover.scaled(new_width, new_height, Qt.IgnoreAspectRatio, Qt.FastTransformation)
		self.labelcover.setPixmap(dicover)
		self.setWindowTitle(TITL_PROG+" : [view ArtWorks: "+self.nametittle+'] {c}/{n} "{name}" A[{w}x{h}] O[{wo}x{ho}]'.format(c=str(numpic),
																	 n=str(len(self.fileslist)),
																	 w=new_width,
																	 h=new_height,
																	 name=path.basename(self.filelist),
																	 wo=str(width),
																	 ho=str(height)))
		self.onSelectCover()

	def onSelectCover(self,  event=None):
		# unselect/select thunbnail
		for i in range(self.gridthunbnails.count()):
			if self.gridthunbnails.itemAt(i).widget().Name == self.filelist:
				self.gridthunbnails.itemAt(i).widget().setStyleSheet("border: 2px solid red;")
			else:
				self.gridthunbnails.itemAt(i).widget().setStyleSheet("border: 2px solid white;")

	def replaceThunbnails(self, sizeTN, oldsizeTN):
		# replace labels thunbnails
		numCov = self.gridthunbnails.count()
		if numCov > 1:
			oldmaxCol = int(self.frameGeometry().width()/(oldsizeTN+4))
			maxCol = int(self.frameGeometry().width()/(sizeTN+4))
			curRow = curCol = cptIte = oldcurRow = oldcurCol = 0
			for row in range(numCov):
				if self.gridthunbnails.itemAtPosition(oldcurRow, oldcurCol) != 0:
					# capture and clear label gridlayout
					layoutitem = self.gridthunbnails.takeAt(cptIte)
					label = layoutitem.widget()
					self.gridthunbnails.removeWidget(label)
					# resize
					label.setFixedSize(sizeTN, sizeTN)
					mypixmap = label.pixmap()
					if mypixmap.size().width() != sizeTN or mypixmap.size().height() != sizeTN:
						mypixmap = mypixmap.scaled(sizeTN, sizeTN, Qt.IgnoreAspectRatio, Qt.FastTransformation)
					label.setPixmap(mypixmap)
					# replace
					self.gridthunbnails.addWidget(label, curRow, curCol)
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

	def resizeImage(self, wmax, hmax, pic):
		# measures
		width, height = pic.size().width(), pic.size().height()
		# resize
		if ((wmax/width) < (hmax/height)):
			new_width = wmax
			new_height = int(new_width * height / width)
		else:
			new_height = hmax
			new_width = int(new_height * width / height)
		return(width, height, new_width, new_height)

	def createFileCover(self):
		file_exten = path.splitext(self.filelist)[1][1:]
		path_cover = path.join(path.dirname(self.filelist), 'cover.' + file_exten)
		self.setWindowTitle("create file {name} ".format(name=path.basename(path_cover)))
		self.mycover.save(path_cover)
