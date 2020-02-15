#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot, QSize
from PyQt5.QtWidgets import QMenu, QWidget, QSizePolicy, QGridLayout, QVBoxLayout, QLabel
from DBFunction import openFolder, getListFiles, centerWidget
from DBThunbnai import DBThunbnails


class CoverViewGui(QWidget):
	"""Cover class."""
	def __init__(self, cover, namealbum, w, h, parent=None):
		super(CoverViewGui, self).__init__()
		self.parent = parent
		self.resize(w, h)
		self.setMaximumSize(w, h)
		self.setMinimumSize(cover.width(), cover.height())
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags(Qt.WindowTitleHint)
		self.setWindowFlags(Qt.WindowSystemMenuHint)
		self.setWindowFlags(Qt.WindowCloseButtonHint)
		self.setWindowIcon(QIcon(self.parent.WINS_ICO))
		centerWidget(self)
		self.namealbum = namealbum
		self.cover = cover
		self.label = QLabel(self)
		self.resizeEvent(None)
		self.label.mousePressEvent = lambda e: self.destroy()
		posit = QGridLayout(self)
		posit.setContentsMargins(0, 0, 0, 0)
		posit.addWidget(self.label, 0, 0)
		self.setLayout(posit)
		self.show()

	@pyqtSlot()
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.destroy()

	@pyqtSlot()
	def resizeEvent(self, event):
		"""Widget size move."""
		covdi = self.cover.scaled(self.width(), self.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
		self.label.setPixmap(covdi)
		self.setWindowTitle("{name} - displaying[{w}x{h}] orignal[{wo}x{ho}]".format(w = self.width(),
																					h = self.height(),
																					name = self.namealbum,
																					wo = str(self.cover.width()),
																					ho = str(self.cover.height())))


# ##################################################################
class ArtworksGui(QWidget):
	"""AcdSee lite."""
	def __init__(self, pathartworks, nametittle, createcover, w, h, sizeTN, parent=None):
		#super(ArtworksGui, self).__init__(parent)
		super(ArtworksGui, self).__init__()
		self.parent = parent
		self.resize(w, h)
		self.setWindowIcon(QIcon(self.parent.WINS_ICO))
		self.setWindowTitle(self.parent.TITL_PROG+" [view ArtWorks] : reading files covers...")
		self.setStyleSheet('QWidget{background-color: darkgray} '
							'QLabel{background-color: black;border: 1px solid black;}')
		
		# cover default
		self.mycover = None
		self.numpic = 0
		
		self.line = 1
		self.sizeTN = sizeTN
		self.thunbnails = DBThunbnails(self, self.sizeTN, self.line)
		self.thunbnails.signalthunchgt.connect(self.onSelectCover)
		self.thunbnails.setMaximumSize(QSize(16667, sizeTN+4))
		self.labelcover = QLabel(self)
		self.labelcover.setAlignment(Qt.AlignCenter)
		self.labelcover.setMinimumSize(QSize(self.width()-40, h-(self.line*(self.sizeTN+4))-70))
		self.labelcover.setContextMenuPolicy(Qt.CustomContextMenu)
		self.labelcover.customContextMenuRequested.connect(self.popUpMenu)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.labelcover.setSizePolicy(sizePolicy)
		self.labelcover.enterEvent = self.selectCover
		
		# popup albums
		self.menua = QMenu()
		self.action_OFC = self.menua.addAction("Open Folder...", lambda c=pathartworks: openFolder(c))
		self.action_COV = self.menua.addAction("Create cover file...", self.createFileCover)
		
		# create cover option only if no cover file
		if createcover[0:len(self.parent.TEXT_NCO)] != self.parent.TEXT_NCO:
			self.action_COV.setEnabled(False)

		layout = QVBoxLayout(self)
		
		lyaout = QGridLayout(self)
		lyaout.addWidget(self.thunbnails)
		lyaout.setContentsMargins(0, 0, 0, 0)
		lyaout.setSpacing(0)
		
		layout.addLayout(lyaout)
		layout.addWidget(self.labelcover)
		layout.setSpacing(5)
		layout.setContentsMargins(7, 7, 7, 7)
		self.setLayout(layout)
		centerWidget(self)
		self.show()

		# build list covers
		self.nametittle = nametittle
		self.fileslist = list(getListFiles(pathartworks, self.parent.MASKCOVER))
		self.filelist = self.fileslist[0]

		# build thunbnails
		self.thunbnails.addthunbails(self.fileslist, self.sizeTN,  True, 0, 100, len(self.fileslist))

		# build large cover
		self.displayCover(self.numpic)

	@pyqtSlot()
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.destroy()
		elif event.key() == Qt.Key_Left:
			self.displayCover((self.numpic-1) % len(self.fileslist))
		elif event.key() == Qt.Key_Right:
			self.displayCover((self.numpic+1) % len(self.fileslist))
	
	@pyqtSlot()
	def resizeEvent(self, event):
		if self.thunbnails.getTotalThunbnails() > 0:
			self.displayCover(self.numpic)

	def onSelectCover(self, numpic):
		"""Select thunbnail."""
		self.displayCover(numpic)

	def selectCover(self, event):
		"""Select thunbnail if select cover."""
		self.thunbnails.selectThunbnail(self.numpic)
		
	def popUpMenu(self,  position):
		"""Menu."""
		self.menua.exec_(self.labelcover.mapToGlobal(position))

	def displayCover(self, numpic):
		"""Display picture."""
		self.numpic = numpic
		self.filelist = self.fileslist[self.numpic]
		self.mycover = QPixmap(self.filelist)
		width, height, new_width, new_height = self.resizeImage(self.labelcover.size().width(), self.size().height()-self.thunbnails.size().height(), self.mycover)
		dicover = self.mycover.scaled(new_width, new_height, Qt.IgnoreAspectRatio, Qt.FastTransformation)
		self.labelcover.setPixmap(dicover)
		self.setWindowTitle(self.parent.TITL_PROG+" : [view ArtWorks: "+self.nametittle+'] {c}/{n} "{name}" A[{w}x{h}] O[{wo}x{ho}]'.format(c=str(self.numpic+1),
																	 n=str(len(self.fileslist)),
																	 w=new_width,
																	 h=new_height,
																	 name=path.basename(self.filelist),
																	 wo=str(width),
																	 ho=str(height)))
		self.thunbnails.selectThunbnail(numpic)
	
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


# # TEST
#from DBReadJson import JsonParams

# class TESTArtWork(QObject):
	# PATH_PROG = path.dirname(path.abspath(__file__))
	# FILE__INI = path.join(PATH_PROG, 'DBAlbums.json')
	# Json_params = JsonParams(FILE__INI)
	# group_dbalbums = Json_params.getMember('dbalbums')
	# VERS_PROG = group_dbalbums['prog_build']
	# TITL_PROG = "DBAlbums v{v} (2017)".format(v=VERS_PROG)
	# TITL_PROG = TITL_PROG + " : Artwork viewer"
	# WINS_ICO = path.join(PATH_PROG, 'IMG', group_dbalbums['wins_icone'])
	# TEXT_NCO = group_dbalbums['text_nocov']
	# MASKCOVER = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.bmp', '.tiff')

	# def __init__(self, filtername = '', PathDownload = '',  parent=None):
		# super(TESTArtWork, self).__init__(None)
		# self.parent = parent
		# ArtworksGui(r"D:\WorkDev\DBAlbumsTEST\ROCK\Download\Red Hot Chili Peppers - Californication (1999)", 
							# 'test', 
							# 'chocolat', 
							# 1250, 
							# 1060, 
							# 150, 
							# self)

# if __name__ == '__main__':
	# app = QApplication(argv)
	# run = TESTArtWork()
	# rc = app.exec_()
	# exit(rc)
