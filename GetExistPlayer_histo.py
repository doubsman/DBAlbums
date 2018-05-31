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
WINS_ICO = "GetExist.ico"

class PlayerAudio(QWidget):
	def __init__(self, filePath, fileName, x=0, y=0):
		super(PlayerAudio, self).__init__()
		
		# media
		self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.LowLatency)
		
		# windows
		self.setFixedSize(400, 40)
		self.setWindowIcon(QIcon(WINS_ICO))
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowTitle(TITL_PROG+fileName)
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
		# histo
		self.histogram = HistogramWidget()
		# order display
		PlayerLayout = QHBoxLayout()
		PlayerLayout.setContentsMargins(5, 5, 5, 5)
		PlayerLayout.addWidget(self.playButton)
		PlayerLayout.addWidget(self.lcd)
		PlayerLayout.addWidget(self.positionSlider)
		PlayerLayout.addWidget(self.labelHistogram)
		PlayerLayout.addWidget(self.histogram, 1)
		self.setLayout(PlayerLayout)
		# display
		self.show()
		
		# link media
		self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
		self.mediaPlayer.positionChanged.connect(self.positionChanged)
		self.mediaPlayer.durationChanged.connect(self.durationChanged)
		#link histogram
		self.probe = QAudioProbe()
		self.probe.videoFrameProbed.connect(self.histogram.processFrame)
		self.probe.setSource(self.player)
		
		self.histogram.audioBufferProbed.connect(self.histogram.processFrame)
		# autoplay
		self.insertMedia(path.join(filePath,fileName))
	
	def insertMedia(self, media):
		self.mediaPlayer.pause()
		self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(media)))
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

class HistogramWidget(QWidget):

	def __init__(self, parent=None):
		super(HistogramWidget, self).__init__(parent)

		self.m_levels = 128
		self.m_isBusy = False
		self.m_histogram = []
		self.m_processor = FrameProcessor()
		self.m_processorThread = QThread()

		self.m_processor.moveToThread(self.m_processorThread)
		self.m_processor.histogramReady.connect(self.setHistogram)

	def __del__(self):
		self.m_processorThread.quit()
		self.m_processorThread.wait(10000)

	def setLevels(self, levels):
		self.m_levels = levels

	def processFrame(self, frame):
		print("In processFrame()")
		if self.m_isBusy:
			return

		self.m_isBusy = True
		print("Invoking method")
		QMetaObject.invokeMethod(self.m_processor, 'processFrame',
				Qt.QueuedConnection, Q_ARG(QVideoFrame, frame),
				Q_ARG(int, self.m_levels))

	def setHistogram(self, histogram):
		self.m_isBusy = False
		self.m_histogram = list(histogram)
		self.update()

	def paintEvent(self, event):
		painter = QPainter(self)

		if len(self.m_histogram) == 0:
			painter.fillRect(0, 0, self.width(), self.height(),
					QColor.fromRgb(0, 0, 0))
			return

		barWidth = self.width() / float(len(self.m_histogram))

		for i, value in enumerate(self.m_histogram):
			h = value * height()
			# Draw the level.
			painter.fillRect(barWidth * i, height() - h, barWidth * (i + 1),
					height(), Qt.red)
			# Clear the rest of the control.
			painter.fillRect(barWidth * i, 0, barWidth * (i + 1), height() - h,
					Qt.black)

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
	PlayerProcess("E:\ZTest","Morten Granau.flac")
	
	# thread
	#player = Thread(target = PlayerProcess, args = ("E:\ZTest","Morten Granau.flac",50,50))
	#player.daemon = True
	#player.start()
	#t1.join()

