#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import path
from re import search, DOTALL
from PyQt5.QtCore import QObject, qDebug, QProcess, pyqtSlot
from mutagen.flac import FLAC
from mutagen.apev2 import APEv2, APEv2File
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


class DBMediasTags(QObject):
	"""Mutagen Class for read tag media audio."""
						
	def __init__(self, parent=None):
		"""Init."""
		super(DBMediasTags, self).__init__(parent)
		self.parent = parent
		#filename = filename.decode(sys.getfilesystemencoding())
	
	def getTagMedia(self, pathfile):
		"""collect TAGs media."""
		filemedia = path.basename(pathfile)
		list_infostrack = {}
		try:
			if filemedia.upper().endswith('.FLAC'):
				list_infostrack = self.getTagMediaFLAC(pathfile)
			elif filemedia.upper().endswith('.MP3'):
				list_infostrack = self.getTagMediaMP3(pathfile)
			elif filemedia.upper().endswith('.APE'):
				list_infostrack = self.getTagMediaAPE(pathfile)
			else:
				ext = path.basename(pathfile).split('.')[-1]
				qDebug('WARNING Format ' + ext + ' non pris en charge')
			return list_infostrack
		except:
			qDebug('ERROR : ' + path.dirname(pathfile))
		return list_infostrack
	
	def getTagMediaFLAC(self, pathfile):
		"""Collect tag FLAC file media."""
		mediafile = FLAC(pathfile)
		list_infostrack = self.getTagFile(pathfile, mediafile.info.length, mediafile.mime[0])
		if mediafile:
			for tag in mediafile.tags:
				list_infostrack.update({tag[0].upper() : tag[1]})
		return list_infostrack
	
	def getTagMediaMP3(self, pathfile):
		"""Collect tag MP3 file media."""
		mediafile = MP3(pathfile, ID3=EasyID3)
		list_infostrack = self.getTagFile(pathfile, mediafile.info.length, mediafile.mime[0])
		if mediafile:
			for tag in mediafile.tags.keys():
				list_infostrack.update({tag.upper() : mediafile.tags[tag][0]})
		return list_infostrack

	def getTagMediaAPE(self, pathfile):
		"""Collect tag MP3 file media."""
		# no Mutagen informations !!
		list_infostrack = self.getTagFile(pathfile, DBMediaDuration(pathfile).totalduration, 'audio/ape')
		#mediafile = APEv2(pathfile)
		#print(mediafile.pprint())
		try:
			mediafile = APEv2File(pathfile)
			if mediafile:
				for tag in mediafile.keys():
					if 'COVER' not in tag.upper():
						list_infostrack.update({tag.upper() : mediafile[tag][0]})
		except:
			pass
		if 'TRACK' in list_infostrack.keys():
			list_infostrack['TRACKNUMBER'] = list_infostrack['TRACK']
		return list_infostrack

	def getTagFile(self, pathfile, lengthseconds, typemedia):
		"""Collect tag file media."""
		# FILENAME / PATHNAME / LENGTHSECONDS / LENGTHDISPLAY / TYPEMEDIA
		list_infostrack = {}
		list_infostrack['FILENAME'] = path.basename(pathfile)
		list_infostrack['PATHNAME'] = path.dirname(pathfile)
		seconds = lengthseconds
		minutes = seconds // 60
		list_infostrack['LENGTHSECONDS'] = seconds
		list_infostrack['LENGTHDISPLAY'] = "%02d:%02d" % (minutes, seconds % 60)
		list_infostrack['TYPEMEDIA'] = typemedia
		return list_infostrack

	def getImageFromTagFLAC(self, pathfile, pathimage=None, nameimage='cover'):
		"""Extract Cover b64 from tag FLAC file media."""
		mediafile = FLAC(pathfile)
		if 'pictures' in dir(mediafile):
			picture = mediafile.pictures[0]
			extensions = {	"image/jpeg": "jpg",
							"image/png": "png",
							"image/gif": "gif"}			
			ext = extensions.get(picture.mime, "jpg")
			if pathimage is None:
				imagefinal = path.join(path.dirname(pathfile), 'cover' +'.'+ ext)
			else:
				imagefinal = path.join(pathimage, nameimage +'.'+ ext)
			with open(imagefinal, "wb") as h:
				h.write(picture.data)
			return True
		return False
	
	def getImageFromTag(self, pathfile, pathimage=None, nameimage='cover'):
		filemedia = path.basename(pathfile)
		result = False
		if filemedia.endswith('.flac'):
			result = self.getImageFromTagFLAC(pathfile, pathimage, nameimage)
		elif filemedia.endswith('.mp3'):
			result = self.getImageFromTagMP3(pathfile, pathimage, nameimage)
		elif filemedia.endswith('.ape'):
			result = self.getImageFromTagAPE(pathfile, pathimage, nameimage)
		return result
		
	def getImageFromTagMP3(self, pathfile, pathimage=None, nameimage='cover'):
		"""Extract Cover b64 from tag MP3 file media."""
		mediafile = MP3(pathfile)
		if 'APIC:' in mediafile.tags.keys():
			picture = mediafile.tags['APIC:']
			extensions = {	"image/jpeg": "jpg",
							"image/png": "png",
							"image/gif": "gif"}			
			ext = extensions.get(picture.mime, "jpg")
			if pathimage is None:
				imagefinal = path.join(path.dirname(pathfile), 'cover' +'.'+ ext)
			else:		
				imagefinal = path.join(pathimage, nameimage +'.'+ ext)
			with open(imagefinal, "wb") as h:
				h.write(picture.data)
			return True
		return False
	
	def getImageFromTagAPE(self, pathfile, pathimage=None, nameimage='cover'):
		"""Extract Cover from tag APE file media."""
		mediafile = APEv2(pathfile)
		for tag in mediafile.keys():
			if 'COVER' in tag.upper():
				tagdatapicture = mediafile[tag]
				text_delimiter_index = tagdatapicture.value.find(b'\x00')
				if text_delimiter_index > 0:
					comment = tagdatapicture.value[0:text_delimiter_index]
					comment = comment.decode('utf-8', 'replace')
					ext = comment.split('.')[1]
				else:
					comment = None
					ext = 'jpg'
				if pathimage is None:
					imagefinal = path.join(path.dirname(pathfile), 'cover.'+ext)
				else:
					imagefinal = path.join(pathimage, nameimage +'.'+ ext)
				image_data = tagdatapicture.value[text_delimiter_index + 1:]
				with open(imagefinal, "wb") as h:
					h.write(image_data)
				return True
		return False


class DBMediaDuration(QObject):
	"""ffmpeg Class for read time duration media audio."""
						
	def __init__(self, filemedia, parent=None):
		"""Init."""
		super(DBMediaDuration, self).__init__(parent)
		qDebug('DBMediaDuration')
		self.parent = parent
		self.filemedia = filemedia
		self.textOut = ''
		self.totalduration = 0
		self.getLengthMedia()
		
	def getLengthMedia(self):
		# run process
		exeprocess = r'ffmpeg.exe'
		params = ['-i', self.filemedia]
		self.process = QProcess()
		self.process.setProcessChannelMode(QProcess.MergedChannels)
		self.process.readyReadStandardOutput.connect(self.WorkReply)
		self.process.finished.connect(self.WorkFinished)
		self.process.start(exeprocess, params)
		self.process.waitForFinished()
		
	@pyqtSlot()
	def WorkReply(self):
		"""Outpout to Gui."""
		data = self.process.readAllStandardOutput().data()
		ch = data.decode('cp850')
		self.textOut += ch

	@pyqtSlot()
	def WorkFinished(self):
		"""End of processus."""
		if self.process is not None:
			self.process.readyReadStandardOutput.disconnect()
			self.process.finished.disconnect()
			matches = search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", self.textOut, DOTALL).groupdict()
			#print(matches['hours'], matches['minutes'], matches['seconds'])
			self.totalduration = (int(matches['hours']) * 60 + int(matches['minutes'])) * 60 + int(matches['seconds'].split('.')[0])


	
	
