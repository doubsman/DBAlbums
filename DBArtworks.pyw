#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ############################################################################
# # Audio pyQT5 Player by SFI
# ############################################################################
from sys import argv, executable
from os import system, path
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot, QSize
from PyQt5.QtWidgets import (QMenu, QWidget, QSizePolicy, QGridLayout, QVBoxLayout, 
						 QFrame, QLabel, QApplication)
from DBFunction import openFolder, getListFiles, centerWidget
from DBThunbnail import DBThunbnails


# path
if getattr(system, 'frozen', False):
	# frozen
	PATH_PROG = path.dirname(executable)
else:
	# unfrozen
	PATH_PROG = path.realpath(path.dirname(argv[0]))
	
VERS_PROG = '1.00'
TITL_PROG = "Artwork viewer v{v} : ".format(v=VERS_PROG)
WINS_ICO = path.join(PATH_PROG, 'IMG', 'icone.ico')
TEXT_NCO = 'No Picture'
MASKCOVER = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.bmp', '.tiff')


# ##################################################################
class CoverViewGui(QWidget):
	def __init__(self, cover, namealbum, w, h, parent=None):
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
	def __init__(self, pathartworks, nametittle, createcover, w, h, sizeTN, parent=None):
		super(ArtworksGui, self).__init__(parent)
		self.resize(w, h)
		self.setWindowIcon(QIcon(WINS_ICO))
		self.setWindowTitle(TITL_PROG+" [view ArtWorks] : reading files covers...")
		self.setStyleSheet('QWidget{background-color: darkgray} '
							'QLabel{background-color: black;border: 1px solid black;}')
		
		# cover default
		self.mycover = None
		self.numpic = 0
		
		self.line = 1
		self.sizethun = sizeTN
		self.thunbnails = DBThunbnails(self, self.sizethun, self.line)
		self.thunbnails.signalthunchgt.connect(self.onSelectCover)
		
		self.labelcover = QLabel()
		self.labelcover.setAlignment(Qt.AlignCenter)
		self.labelcover.setMinimumSize(QSize(self.width()-40, h-(self.line*(self.sizethun+4))-70))
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
		if createcover[0:len(TEXT_NCO)] != TEXT_NCO:
			self.action_COV.setEnabled(False)
		self.line = QFrame(self)
		self.line.setFrameShape(QFrame.HLine)
		self.line.setFrameShadow(QFrame.Sunken)
		self.line.setContentsMargins(0, 0, 0, 0)
		
		layout = QVBoxLayout(self)
		lyaout = QGridLayout()
		lyaout.addWidget(self.thunbnails)
		layout.addLayout(lyaout)
		layout.addWidget(self.line)
		layout.addStretch(1)
		layout.addWidget(self.labelcover)
		self.setLayout(layout)
		centerWidget(self)
		self.show()

		# build list covers
		self.nametittle = nametittle
		self.fileslist = list(getListFiles(pathartworks, MASKCOVER))
		self.filelist = self.fileslist[0]

		# build thunbnails
		self.thunbnails.addthunbails(self.fileslist)

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
		self.thunbnails.onSelectThunbnail(numpic)
		self.displayCover(numpic)

	def selectCover(self, event):
		"""Select thunbnail if select cover."""
		self.thunbnails.onSelectThunbnail(self.numpic)
		
	def popUpMenu(self,  position):
		"""Menu."""
		self.menua.exec_(self.labelcover.mapToGlobal(position))

	def displayCover(self, numpic):
		"""Display picture."""
		self.numpic = numpic
		self.filelist = self.fileslist[self.numpic]
		self.mycover = QPixmap(self.filelist)
		width, height, new_width, new_height = self.resizeImage(self.labelcover.size().width(), self.size().height()-self.thunbnails.size().height()-30, self.mycover)
		dicover = self.mycover.scaled(new_width, new_height, Qt.IgnoreAspectRatio, Qt.FastTransformation)
		self.labelcover.setPixmap(dicover)
		self.setWindowTitle(TITL_PROG+" : [view ArtWorks: "+self.nametittle+'] {c}/{n} "{name}" A[{w}x{h}] O[{wo}x{ho}]'.format(c=str(self.numpic+1),
																	 n=str(len(self.fileslist)),
																	 w=new_width,
																	 h=new_height,
																	 name=path.basename(self.filelist),
																	 wo=str(width),
																	 ho=str(height)))
		self.thunbnails.onSelectThunbnail(numpic)
	
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


if __name__ == '__main__':
	app = QApplication(argv)
	ART = ArtworksGui(r"E:\Work\ZTest\TAG_bluid\TECHNO\Download\Caia - The Magic Dragon (2003)", 
						'test', 
						'chocolat', 
						1250, 
						1060, 
						150)
	rc = app.exec_()
	exit(rc)
