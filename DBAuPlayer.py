#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ############################################################################
# # Audio pyQT5 Player by SFI
# ############################################################################
from os import path
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist#, QMediaMetaData
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QSlider, QStyleOptionSlider,
							QLabel, QStyle, QWidget, QMessageBox)

VERS_PROG = '1.00'
TITL_PROG = "Player v{v} : ".format(v=VERS_PROG)


class MySlider(QSlider):
	def mousePressEvent(self, event):
		super(MySlider, self).mousePressEvent(event)
		if event.button() == Qt.LeftButton:
			val = self.pixelPosToRangeValue(event.pos())
			self.setValue(val)

	def pixelPosToRangeValue(self, pos):
		opt = QStyleOptionSlider()
		self.initStyleOption(opt)
		gr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
		sr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)
		if self.orientation() == Qt.Horizontal:
			sliderLength = sr.width()
			sliderMin = gr.x()
			sliderMax = gr.right() - sliderLength + 1
		else:
			sliderLength = sr.height()
			sliderMin = gr.y()
			sliderMax = gr.bottom() - sliderLength + 1;
		pr = pos - sr.center() + sr.topLeft()
		p = pr.x() if self.orientation() == Qt.Horizontal else pr.y()
		return QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), p - sliderMin,
													sliderMax - sliderMin, opt.upsideDown)


# ##################################################################
# PLAYER PQT5 V2
class DBPlayer(QWidget):
	# signal
	signaltxt = pyqtSignal(str)
	signalnum = pyqtSignal(int)

	def __init__(self, parent):
		super(DBPlayer, self).__init__(parent)
		self.PATH_PROG = path.dirname(path.abspath(__file__))
		self.RESS_ICOS = path.join(self.PATH_PROG, 'ICO')

		self.setMaximumSize(16777215, 35)
		# Init Player
		self.messtitle = TITL_PROG
		self.namemedia = ''
		self.albumname = ''
		self.currentPlaylist = QMediaPlaylist()
		self.player = QMediaPlayer()
		self.player.stateChanged.connect(self.qmp_stateChanged)
		self.player.positionChanged.connect(self.qmp_positionChanged)
		self.player.volumeChanged.connect(self.qmp_volumeChanged)
		self.player.durationChanged.connect(self.qmp_durationChanged)
		self.player.setVolume(60)
		# Init GUI
		self.setLayout(self.addControls())
		self.infoBox = None

	def addControls(self):
		# buttons
		self.playBtn = QPushButton()
		self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
		self.playBtn.setStyleSheet('border: 0px;')
		self.stopBtn = QPushButton()
		self.stopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
		self.stopBtn.setStyleSheet('border: 0px;')
		self.prevBtn = QPushButton()
		self.prevBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
		self.prevBtn.setStyleSheet('border: 0px;')
		self.nextBtn = QPushButton()
		self.nextBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
		self.nextBtn.setStyleSheet('border: 0px;')
		self.volumeDescBtn = QPushButton('')
		self.volumeDescBtn.setIcon(QIcon(path.join(self.RESS_ICOS, 'decrease.png')))
		self.volumeDescBtn.setMaximumWidth(40)
		self.volumeDescBtn.setStyleSheet('border: 0px;')
		self.volumeIncBtn = QPushButton('')
		self.volumeIncBtn.setIcon(QIcon(path.join(self.RESS_ICOS, 'increase.png')))
		self.volumeIncBtn.setMaximumWidth(40)
		self.volumeIncBtn.setStyleSheet('border: 0px;')
		self.infoBtn = QPushButton()
		self.infoBtn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogContentsView))
		self.infoBtn.setStyleSheet('border: 0px;')

		# seek slider
		self.seekSlider = MySlider(Qt.Horizontal)
		self.seekSlider.setMinimum(0)
		self.seekSlider.setMaximum(100)
		self.seekSlider.setTracking(False)

		# labels position start/end
		self.seekSliderLabel1 = QLabel('0:00')
		self.seekSliderLabel2 = QLabel('0:00')

		# layout
		self.controlArea = QHBoxLayout(self)
		self.controlArea.addWidget(self.prevBtn)
		self.controlArea.addWidget(self.playBtn)
		self.controlArea.addWidget(self.stopBtn)
		self.controlArea.addWidget(self.nextBtn)
		self.controlArea.addWidget(self.seekSliderLabel1)
		self.controlArea.addWidget(self.seekSlider)
		self.controlArea.addWidget(self.seekSliderLabel2)
		self.controlArea.addWidget(self.infoBtn)
		self.controlArea.addWidget(self.volumeDescBtn)
		self.controlArea.addWidget(self.volumeIncBtn)

		# link buttons to media
		self.seekSlider.valueChanged.connect(self.qmq_setposition)
		self.seekSlider.sliderMoved.connect(self.qmq_setposition)
		self.playBtn.clicked.connect(self.playHandler)
		self.stopBtn.clicked.connect(self.stopHandler)
		self.volumeDescBtn.clicked.connect(self.decreaseVolume)
		self.volumeIncBtn.clicked.connect(self.increaseVolume)
		self.prevBtn.clicked.connect(self.prevItemPlaylist)
		self.nextBtn.clicked.connect(self.nextItemPlaylist)
		self.infoBtn.clicked.connect(self.displaySongInfo)

		return self.controlArea

	def playHandler(self):
		if self.player.state() == QMediaPlayer.PlayingState:
			self.player.pause()
			message = '[Paused at %s]' % self.seekSliderLabel1.text()
			self.messtitle = message + self.namemedia
			self.signaltxt.emit(self.messtitle)
		else:
			if self.player.state() == QMediaPlayer.StoppedState:
				if self.player.mediaStatus() == QMediaPlayer.NoMedia:
					if self.currentPlaylist.mediaCount() != 0:
						self.player.setPlaylist(self.currentPlaylist)
				elif self.player.mediaStatus() == QMediaPlayer.LoadedMedia:
					self.player.play()
				elif self.player.mediaStatus() == QMediaPlayer.BufferedMedia:
					self.player.play()
			elif self.player.state() == QMediaPlayer.PlayingState:
				pass
			elif self.player.state() == QMediaPlayer.PausedState:
				self.player.play()
			if self.player.volume() is not None and self.player.state() == QMediaPlayer.PlayingState:
				message = '[Vol. %d] ' % self.player.volume()
				self.messtitle = message + self.namemedia
				self.signaltxt.emit(self.messtitle)

	def stopHandler(self):
		if self.player.state() == QMediaPlayer.PlayingState:
			self.stopState = True
			self.player.stop()
		elif self.player.state() == QMediaPlayer.PausedState:
			self.player.stop()
		elif self.player.state() == QMediaPlayer.StoppedState:
			pass
		if self.player.volume()is not None and self.player.state() == QMediaPlayer.PlayingState:
			self.messtitle = '[Stop] ' + self.namemedia
			self.signaltxt.emit(self.messtitle)

	def qmp_stateChanged(self):
		if self.player.state() == QMediaPlayer.StoppedState:
			self.player.stop()
		# buttons icon play/pause change
		if self.player.state() == QMediaPlayer.PlayingState:
			self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
		else:
			self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

	def qmp_positionChanged(self, position):
		# update position slider
		self.seekSlider.blockSignals(True)
		self.seekSlider.setValue(position)
		self.seekSlider.blockSignals(False)
		# update the text label
		self.seekSliderLabel1.setText('%d:%02d' % (int(position/60000), int((position/1000) % 60)))
	
	def qmq_setposition(self, position):
		# imposed position with slider
		self.seekSlider.blockSignals(True)
		self.player.stop()
		self.player.setPosition(position)
		self.player.play()
		self.seekSlider.blockSignals(False)

	def qmp_volumeChanged(self):
		if self.player.volume() is not None:
			message = '[Vol. %d] ' % (self.player.volume())
			if self.namemedia != '':
				self.messtitle = message + self.namemedia
			else:
				self.messtitle = message + "Initialisation player "
			self.signaltxt.emit(self.messtitle)

	def qmp_durationChanged(self, duration):
		self.seekSlider.setRange(0, duration)
		self.seekSliderLabel2.setText('%d:%02d' % (int(duration/60000), int((duration/1000) % 60)))
		nummedia = self.currentPlaylist.mediaCount()
		curmedia = self.currentPlaylist.currentIndex()
		#artist = self.player.metaData(QMediaMetaData.Author)
		#tittle = self.player.metaData(QMediaMetaData.Title)
		self.namemedia = path.basename(self.homMed[curmedia])
		self.namemedia = '[%02d/%02d' % (curmedia+1, nummedia) + '] "' + self.namemedia + '"'
		self.buildPlaylist()
		message = '[Vol. %d]' % (self.player.volume())
		if self.player.volume() is not None and self.player.state() == QMediaPlayer.PlayingState:
			self.messtitle = message + self.namemedia
			self.signaltxt.emit(self.messtitle)
	
	def buildPlaylist(self):
		"""Build play list."""
		nummedia = self.currentPlaylist.mediaCount()
		curmedia = self.currentPlaylist.currentIndex() + 1
		compteur = 1
		self.textplaylist = '<b>' + self.albumname + '</b>'
		self.textplaylist += '<table class="tftable" border="0">'
		for namemedia in self.homMed:
			media = path.basename(namemedia)
			media = '[%02d/%02d' % (compteur, nummedia) + '] "' + media + '"'
			if curmedia == compteur:
				self.textplaylist += '<tr><td><b>' + media + '</b></td></tr>'
			else:	
				self.textplaylist += '<tr><td>' + media + '</td></tr>'
			compteur += 1
		self.textplaylist = self.textplaylist + '</table>'
		self.playBtn.setToolTip(self.textplaylist)
		self.signalnum.emit(curmedia-1)
		
	def increaseVolume(self):
		"""Volume +."""
		vol = self.player.volume()
		vol = min(vol+5, 100)
		self.player.setVolume(vol)

	def decreaseVolume(self):
		"""Volume -."""
		vol = self.player.volume()
		vol = max(vol-5, 0)
		self.player.setVolume(vol)

	def prevItemPlaylist(self):
		self.player.playlist().previous()
		if self.currentPlaylist.currentIndex() == -1:
			self.player.playlist().previous()

	def nextItemPlaylist(self):
		self.player.playlist().next()
		if self.currentPlaylist.currentIndex() == -1:
			self.player.playlist().next()

	def addMediaslist(self, listmedias, position, albumname):
		if self.currentPlaylist.mediaCount() > 0:
			self.currentPlaylist.removeMedia(0, self.currentPlaylist.mediaCount())
			self.player.stop()
			self.stopHandler()
		self.currentPlaylist.removeMedia(0, self.currentPlaylist.mediaCount())
		self.albumname = albumname
		if listmedias:
			self.homMed = listmedias
			for media in self.homMed:
				self.currentPlaylist.addMedia(QMediaContent(QUrl.fromLocalFile(media)))
			self.currentPlaylist.setCurrentIndex(position)
			self.playHandler()

	def displaySongInfo(self):
		# extract datas
		metaDataKeyList = self.player.availableMetaData()
		fullText = '<table class="tftable" border="0">'
		for key in metaDataKeyList:
			value = str(self.player.metaData(key)).replace("'", "").replace("[", "").replace("]", "")
			if key == 'Duration':
				value = '%d:%02d' % (int(int(value)/60000), int((int(value)/1000) % 60))
			fullText = fullText + '<tr><td>' + key + '</td><td>' + value + '</td></tr>'
		fullText = fullText + '</table>'
		# re-init
		if self.infoBox is not None:
			self.infoBox.destroy()
		# infos box
		self.infoBox = QMessageBox(self)
		self.infoBox.setWindowTitle('Detailed Song Information')
		self.infoBox.setTextFormat(Qt.RichText)
		self.infoBox.addButton('OK', QMessageBox.AcceptRole)
		self.infoBox.setText(fullText)
		self.infoBox.show()

class TestAudio(QWidget):
	def __init__(self):
		super().__init__()
		self.player = QMediaPlayer(self)
		self.sound = QMediaContent(QUrl.fromLocalFile("E:\\Work\ZTest\\01 - Redemption.flac"))
		self.player.setMedia(self.sound)
		self.player.setVolume(100)
		self.player.play()
		self.show()

#import vlc
#player = vlc.MediaPlayer("E:\\Work\ZTest\\01 - Redemption.flac")
#player.play()
#player.pause()
#player.stop()

#vlc_instance = vlc.Instance()
#player = vlc_instance.media_player_new()
#media = vlc_instance.media_new("E:\\Work\ZTest\\01 - Redemption.flac")
#player.set_media(media)
#player.play()
#duration = player.get_length() / 1000


#class MainExemple(QMainWindow):
#	def __init__(self, parent=None):
#		super(MainExemple, self).__init__(parent)
#		# Init GUI
#		PlayerAudio = DBPlayer()
#		self.setCentralWidget(PlayerAudio)
#		self.show()
#
#		PlayerAudio.signaltxt.connect(self.txtplayeraudio)
#
#		PlayerAudio.addMediaslist(("E:\\Work\ZTest\\02. Tristan - Reincarnation (GMS Remix).mp3",), 0, "test")
#		PlayerAudio.player.play()
#
#	def txtplayeraudio(self, message):
#		print(message)
#
#
#if __name__ == '__main__':
#	app = QApplication(argv)
#	player = MainExemple()
#	rc = app.exec_()
#	exit(rc)
