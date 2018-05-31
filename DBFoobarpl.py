#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from PyQt5.QtCore import QCryptographicHash, qDebug
from PyQt5.QtSql import QSqlQuery
from DBFunction import getListFiles
from DBDatabase import getrequest
# dev ext https://github.com/rr-/fpl_reader
from fpl_reader import read_playlist


def getFile(folder, file_name):
	"""open file playlist foobar 2000."""
	with open(path.join(folder, file_name), 'rb') as handle:
		return handle.read()


def foobarBuildTracksList(folder):
	"""build list of playlists foobar 2000."""
	trackslist = []
	playfiles = list(getListFiles(folder, (".fpl",)))
	for playfile in playfiles:
		trackslist += foobargetListFilesFromPlaylist(playfile)
	return(trackslist)


def foobargetListFilesFromPlaylist(file_path):
	"""Buil list track from playlists."""
	folder = path.dirname(file_path)
	file_name = path.basename(file_path)
	listfiles = []
	try:
		playlistcontent = read_playlist(getFile(folder, file_name))
		for lfile in playlistcontent.tracks:
			playlist = file_path
			audiofil = str(lfile.file_name[7:], 'utf-8')
			albumnam = audiofil.split('\\')[-2]
			albummd5 = QCryptographicHash.hash(albumnam.encode('utf-8'), QCryptographicHash.Md5).toHex()
			albummd5 = (albummd5.data()).decode('utf-8').upper()
			TAG_Album = ''
			TAG_Artists = ''
			TAG_Title = ''
			try:
				TAG_Album = lfile.primary_keys[b"album"]
				TAG_Artists = lfile.primary_keys[b"artist"]
				TAG_Title = lfile.primary_keys[b"title"]
			except:
				pass
		# add list Playlist, Path, FIL_Track, Name , MD5, TAGartist, TABalbum, TAGtitle
		listfiles.append((path.basename(playlist), path.dirname(audiofil), path.basename(audiofil), albumnam, albummd5, TAG_Album, TAG_Artists, TAG_Title))
	except BaseException as e:
		pass
		#logger.error('Failed' + str(e))
		qDebug('#problem : '+file_path)
		qDebug('Failed' + str(e))
	return(listfiles)


def DBFOOBAR(parent, folder):
	"""Insert track in database dans update score."""
	# fill DBFOOBAR
	footracks = foobarBuildTracksList(folder)
	numtracks = len(footracks)
	counter = 0
	parent.updateGaugeBar(0, "Crowse playlists fooBar 2000")
	request = getrequest('playlistfoobar')
	for footrack in footracks:
		query = QSqlQuery()
		query.prepare(request)
		pos = 0
		for colval in footrack:
			query.bindValue(pos, colval)
			pos += 1
		if not query.exec_():
			errorText = query.lastError().text()
			qDebug(request, errorText)
			numtracks = 0
			break
		query.clear
		counter += 1
		parent.updateGaugeBar((counter/numtracks)*100)
	parent.updateGaugeBar(100)
	return(numtracks)
