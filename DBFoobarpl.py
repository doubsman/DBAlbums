#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from PyQt5.QtCore import qDebug, QObject, pyqtSignal
# dev ext https://github.com/rr-/fpl_reader
from fpl_reader import read_playlist


class playlistFoobar2000(QObject):
	signalchgt = pyqtSignal(int, str)		# signal browse
	
	def __init__(self, parent, folder):
		"""Init."""
		super(playlistFoobar2000, self).__init__(parent)
		self.parent = parent
		self.folder = folder
		self.trackslist = []
		self.numtracks = 0
		self.dirPlaylist()

	def dirPlaylist(self):
		"""build list of playlists foobar 2000."""
		playfiles = self.parent.folder_list_files(self.folder, True, (".fpl",))
		for playfile in playfiles:
			# update self.trackslist
			self.readPlaylist(playfile)
	
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

	
