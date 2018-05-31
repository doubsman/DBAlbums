#! /usr/bin/python
# coding: utf-8

from sys import argv, exit
from os import path
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QHBoxLayout)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest


class QLabeldnd(QLabel):
	# signal
	signalcoverchgt = pyqtSignal(int)		# cover changed
	
	def __init__ (self, parent, pathcover, coversize):
		"""Init QLabel Dnd."""
		super(QLabel, self).__init__(parent)
		self.pathcover = pathcover
		self.size = coversize
		self.setMaximumSize(QSize(self.size, self.size))
		self.setMinimumSize(QSize(self.size, self.size))
	
	def dragEnterEvent (self, event):
		"""Accept url and image."""
		if event.mimeData().hasImage() or event.mimeData().hasUrls():
			event.acceptProposedAction()	

	def dropEvent (self, event):
		"""Build Qpixmap/cover and display in label."""
		event.setAccepted(True)
		if event.mimeData().hasImage():
			mimeQImage = QImage(event.mimeData().imageData())
			mypixmap = QPixmap.fromImage(mimeQImage)
			mypixmap.save(path.join(self.pathcover,"cover.jpg"))
			mypixlab = mypixmap.scaled(self.size, self.size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
			self.setPixmap(mypixlab)
			self.signalcoverchgt.emit(1)
		elif event.mimeData().hasUrls():
			url = event.mimeData().urls()[0]
			nam = QNetworkAccessManager(self)
			nam.finished.connect(self.finishRequest)
			nam.get(QNetworkRequest(url))
		QLabel.dropEvent(self, event)

	def finishRequest(self, reply):
		"""Download image from url."""
		mimeQImage = QImage()
		mimeQImage.loadFromData(reply.readAll())
		mypixmap = QPixmap(mimeQImage)
		mypixmap.save(path.join(self.pathcover,"cover.jpg"))
		mypixlab = mypixmap.scaled(self.size, self.size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
		self.setPixmap(mypixlab)
		self.signalcoverchgt.emit(1)
	
	def updateLabel(self, pathcover):
		"""Active or not DnD only no cover."""
		self.pathcover = pathcover
		if pathcover is None:
			self.setAcceptDrops(False)
		else:
			self.setAcceptDrops(True)


class QCustomQWidget(QWidget):
	def __init__ (self, parentQWidget = None):
		super(QCustomQWidget, self).__init__(parentQWidget)
		self.mimeQLabel = QLabel()
		allQHBoxLayout = QHBoxLayout()
		allQHBoxLayout.addWidget(self.mimeQLabel)
		self.setLayout(allQHBoxLayout)
		self.setAcceptDrops(True)

	def dragEnterEvent (self, event):
		if event.mimeData().hasImage() or event.mimeData().hasUrls():
			event.acceptProposedAction()

	def dropEvent (self, event):
		self.mimeQLabel.clear()
		event.setAccepted(True)
		if event.mimeData().hasImage():
			print('image')
			mimeQImage = QImage(event.mimeData().imageData())
			mypixmap = QPixmap.fromImage(mimeQImage)
			mypixmap.save("E:\cover.jpg")
			mypixmap = mypixmap.scaled(400, 400, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
			self.mimeQLabel.setPixmap(mypixmap)
		elif event.mimeData().hasUrls():
			print('urls')
			url = event.mimeData().urls()[0]
			nam = QNetworkAccessManager(self)
			nam.finished.connect(self.finishRequest)
			nam.get(QNetworkRequest(url))
		QWidget.dropEvent(self, event)

	def finishRequest(self, reply):
		print('fin')
		mimeQImage = QImage()
		mimeQImage.loadFromData(reply.readAll())
		self.mimeQLabel.setPixmap(QPixmap(mimeQImage))


if __name__ == '__main__':
	app = QApplication(argv)
	myQCustomQWidget = QCustomQWidget()
	myQCustomQWidget.show()
	exit(app.exec_())
