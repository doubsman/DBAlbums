#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
## Audio pyQT5 Player by SFI
#############################################################################
from sys import argv
from os import path
from threading import Thread
from PyQt5.QtCore import Qt, QUrl, QThread
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QPushButton, QSlider, QStyle, QWidget, QLCDNumber
from PyQt5.QtGui import QIcon

VERS_PROG = '1.00'
TITL_PROG = "Player v{v} : ".format(v=VERS_PROG)
WINS_ICO = "DBAlbums-icone.ico"

class PlayerAudio(QWidget):
	def __init__(self, filePath, fileName, x=0, y=0):
		super(PlayerAudio, self).__init__()
		
		# media
		self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.LowLatency)
		
		# windows
		self.setFixedSize(400, 40)
		self.setWindowIcon(QIcon(WINS_ICO))
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowTitle(TITL_PROG)
		self.move(x, y)
		# mm:ss
		self.lcd = QLCDNumber(self)
		self.lcd.display("00:00")
		# button
		self.playButton = QPushButton()
		self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
		self.playButton.clicked.connect(self.play)
		# slider position
		self.positionSlider = QSlider(Qt.Horizontal, self)
		self.positionSlider.setRange(0, 0)
		self.positionSlider.sliderMoved.connect(self.setPosition)
		self.positionSlider.valueChanged.connect(self.lcddisplay)
		# order display
		PlayerLayout = QHBoxLayout()
		PlayerLayout.setContentsMargins(5, 5, 5, 5)
		PlayerLayout.addWidget(self.playButton)
		PlayerLayout.addWidget(self.lcd)
		PlayerLayout.addWidget(self.positionSlider)
		self.setLayout(PlayerLayout)
		# display
		self.show()
		
		# link media
		self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
		self.mediaPlayer.positionChanged.connect(self.positionChanged)
		self.mediaPlayer.durationChanged.connect(self.durationChanged)
		
		# autoplay
		self.insertMedia(path.join(filePath,fileName))

	
	def insertMedia(self, media):
		self.mediaPlayer.pause()
		self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(media)))
		self.setWindowTitle('playing "'+path.basename(media)+'"')
		self.mediaPlayer.play()
	
	def play(self):
		if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
			self.mediaPlayer.pause()
		else:
			self.mediaPlayer.play()
	
	def mediaStateChanged(self, state):
		if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
			self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
		else:
			self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
	
	def positionChanged(self, position):
		self.positionSlider.setValue(position)
	
	def durationChanged(self, duration):
		self.positionSlider.setRange(0, duration)
	
	def setPosition(self, position):
		self.mediaPlayer.setPosition(position)
	
	def lcddisplay(self, position):
		seconds = position // 1000
		minutes = seconds // 60
		total_p = "%02d:%02d" % (minutes, seconds % 60)
		self.lcd.display(str(total_p))


class PlayerQThreadProcess(QThread):
	def __init__(self, filePath, fileName, x=0, y=0):
		super(PlayerTProcess, self).__init__()
		#QThread.__init__(self)
		self.filePath = filePath
		self.fileName = fileName
		self.x = x
		self.y = y
		
	def run(self):
		app = QApplication(argv)
		player = PlayerAudio(self.filePath, self.fileName, self.x, self.y)
		app.exec_()
		QThread.terminate()

def PlayerProcess(filePath, fileName, x=0, y=0):
	app = QApplication(argv)
	player = PlayerAudio(filePath, fileName, x, y)
	app.exec_()

	
if __name__ == "__main__":
	# Qthread
	#player  = PlayerQThreadProcess("E:\ZTest","Morten Granau.flac",50,50)
	#player.start()
	#player.wait()
	
	# no thread
	#PlayerProcess("E:\ZTest","Morten Granau.flac")
	
	# thread
	tplayer = Thread(target = PlayerProcess, args = ("E:\ZTest","Morten Granau.flac",50,50))
	tplayer.daemon = True
	tplayer.start()
	#tplayer(PlayerProcess.changemedia(PlayerThreadProcess, "E:\ZTest\SCSI-9.flac"))
	#t1.join()

