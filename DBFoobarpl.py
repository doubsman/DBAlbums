#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from PyQt5.QtCore import qDebug, QObject, pyqtSignal
from PyQt5.QtSql import QSqlQuery
from DBFunction import getListFiles
# dev ext https://github.com/rr-/fpl_reader
from fpl_reader import read_playlist


class playlistFoobar2000(QObject):
	signalchgt = pyqtSignal(int, str)		# signal browse
	
	def __init__(self, folder, parent=None):
		"""Init."""
		super(playlistFoobar2000, self).__init__(parent)
		self.parent = parent
		self.folder = folder
		self.trackslist = []
		self.numtracks = 0
		self.dirPlaylist()

	def dirPlaylist(self):
		"""build list of playlists foobar 2000."""
		playfiles = list(getListFiles(self.folder, (".fpl",)))
		for playfile in playfiles:
			self.readPlaylist(playfile)
	
	def importPlaylist(self):
		"""Insert playlist track in database dans update score."""
		self.numtracks = len(self.trackslist)
		counter = 0
		request = self.parent.CnxConnect.getrequest('playlistfoobar')		
		self.signalchgt.emit(0, "Crowse playlists fooBar 2000")
		for footrack in self.trackslist:
			query = QSqlQuery()
			query.prepare(request)
			pos = 0
			for colval in footrack:
				query.bindValue(pos, colval)
				pos += 1
			if not query.exec_():
				qDebug(request + ' ' + query.lastError().text())
				qDebug(','.join(list(str(query.boundValues().values()))))
				break
			query.clear
			counter += 1
			self.signalchgt.emit((counter/self.numtracks)*100, 'Import playlists FooBar2000 in progess...')

	def updateScore(self, filerequests):
		self.parent.CnxConnect.signalchgt.connect(self.loadingProgress)
		update.execSqlFile(filerequests)

	def readPlaylist(self, file_path):
		"""Buil list track from playlists."""
		folder = path.dirname(file_path)
		file_name = path.basename(file_path)
		listfiles = []
		try:
			playlistcontent = read_playlist(self.getFile(folder, file_name))
			for lfile in playlistcontent.tracks:
				playlist = file_path
				audiofil = str(lfile.file_name[7:], 'utf-8')
				albumnam = audiofil.split('\\')[-2]
				#albummd5 = QCryptographicHash.hash(albumnam.encode('utf-8'), QCryptographicHash.Md5).toHex()
				#albummd5 = (albummd5.data()).decode('utf-8').upper()
				TAG_Album = ''
				TAG_Artists = ''
				TAG_Title = ''
				try:
					TAG_Album = lfile.primary_keys[b"album"].decode()
					TAG_Artists = lfile.primary_keys[b"artist"].decode()
					TAG_Title = lfile.primary_keys[b"title"].decode()
				except:
					pass
				# add list Playlist, Path, FIL_Track, Name , TABalbum, TAGartist, TAGtitle
				listfiles.append((path.basename(playlist), path.dirname(audiofil), path.basename(audiofil), albumnam, TAG_Album, TAG_Artists, TAG_Title))
		except BaseException as e:
			pass
			#logger.error('Failed' + str(e))
			qDebug('#problem : '+file_path)
			qDebug('Failed' + str(e))
		self.trackslist += listfiles
		
	def getFile(self, folder, file_name):
		"""open file playlist foobar 2000."""
		with open(path.join(folder, file_name), 'rb') as handle:
			return handle.read()

	def loadingProgress(self, int, text):
		"""Traced back progress."""
		self.signalchgt.emit(int, text)


	
