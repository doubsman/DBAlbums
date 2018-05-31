#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sys import argv
from os import path
from base64 import b64decode
from PyQt5.QtCore import QObject, QByteArray, QIODevice, QBuffer, qDebug, qInstallMessageHandler
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtSql import QSqlQuery
from mutagen.flac import FLAC
from mutagen.apev2 import APEv2, APEv2File
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from DBFunction import qtmymessagehandler
from DBDatabase import DBFuncBase, connectDatabase


def migrationB64():
	request = 'SELECT ID_CD, Cover, MD5 FROM DBALBUMS ORDER BY ID_CD'
	listid = DBFuncBase().sqlToArray(request)
	for id in listid:
		idcd = id[0]
		pathimage = id[1]
		print('migration : ', idcd)
			
		request = "SELECT Cover64, MiniCover64 FROM DBCOVERS WHERE MD5='{md5}';".format(md5=id[2])
		query = QSqlQuery(request)
		query.exec_()
		query.first()
		if query.value(0) is not None:
			cover = b64decode(query.value(0))
			coverpixmap = QPixmap()
			coverpixmap.loadFromData(cover)
			inByteArray = QByteArray()
			inBuffer = QBuffer(inByteArray)
			inBuffer.open(QIODevice.WriteOnly);
			coverpixmap.save(inBuffer,"JPG");

			covermini = b64decode(query.value(1))
			coverminipixmap = QPixmap()
			coverminipixmap.loadFromData(covermini)
			inByteArraymini = QByteArray()
			inBuffer = QBuffer(inByteArraymini)
			inBuffer.open(QIODevice.WriteOnly);
			coverminipixmap.save(inBuffer,"JPG");
		
			queryinsert = QSqlQuery()
			queryinsert.prepare( "REPLACE INTO DBPIXMAPS(ID_CD, NamePix, Cover, Thunbnail) VALUES (?, ?, ?, ?)")
			queryinsert.bindValue(0, idcd)
			queryinsert.bindValue(1, pathimage)
			queryinsert.bindValue(2, inByteArray)
			queryinsert.bindValue(3, inByteArraymini)
			if not queryinsert.exec_():
				qDebug(10*' '+":index "+queryinsert.lastError().text())
			queryinsert.clear
		query.clear
	print('end')

class DBMediasTags(QObject):
	"""Mutagen Class for read tag media audio."""
	CardTagTrack = {	'TITLE': None, 
						'ARTIST': None,
						'ALBUM': None,
						'DATE': None,
						'GENRE': None,
						'TRACKNUMBER': None,
						'ALBUMARTIST': None,
						'COMPOSER': None,
						'DISCNUMBER': None,
						'ISRC': None,
						'ORGANIZATION': None,
						'COUNTRY': None}

	def __init__(self, parent=None):
		"""Init."""
		super(DBMediasTags, self).__init__(parent)
		self.parent = parent
		#filename = filename.decode(sys.getfilesystemencoding())
	
	def fileTypeMedia(self, pathfile):
		mediafinaltag = self.CardTagTrack
		for key in mediafinaltag.keys():
			print(key, '=', mediafinaltag[key])
		
	def getTagMediaFLAC(self, pathfile):
		"""Collect tag FLAC file media."""
		mediafile = FLAC(pathfile)
		list_infostrack = self.getTagFile(pathfile, mediafile.info.length, mediafile.mime[0])
		for tag in mediafile.tags:
			list_infostrack.update({tag[0] : tag[1]})
		return list_infostrack
	
	def getTagMediaMP3(self, pathfile):
		"""Collect tag MP3 file media."""
		mediafile = MP3(pathfile, ID3=EasyID3)
		list_infostrack = self.getTagFile(pathfile, mediafile.info.length, mediafile.mime[0])
		for tag in mediafile.tags.keys():
			list_infostrack.update({tag.upper() : mediafile.tags[tag][0]})
		return list_infostrack

	def getTagMediaAPE(self, pathfile):
		"""Collect tag MP3 file media."""
		mediafile = APEv2File(pathfile)
		list_infostrack = self.getTagFile(pathfile, mediafile.info.length, mediafile.mime)
		#mediafile = APEv2(pathfile)
		for tag in mediafile.keys():
			if 'COVER' not in tag.upper():
				list_infostrack.update({tag.upper() : mediafile[tag][0]})
		return list_infostrack

	def getTagFile(self, pathfile, lengthseconds, typemedia):
		"""Collect tag file media."""
		# FILENAME / PATHNAME / LENGHTSECONDS / LENGHTDISPLAY / TYPEMEDIA
		list_infostrack = {}
		list_infostrack.update({'FILENAME' : path.basename(pathfile)})
		list_infostrack.update({'PATHNAME' : path.dirname(pathfile)})
		seconds = lengthseconds
		minutes = seconds // 60
		list_infostrack.update({'LENGHTSECONDS' : seconds})
		list_infostrack.update({'LENGHTDISPLAY' : "%02d:%02d" % (minutes, seconds % 60)})
		list_infostrack.update({'TYPEMEDIA' : typemedia})
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

if __name__ == '__main__':
	app = QApplication(argv)
	# debug
	qInstallMessageHandler(qtmymessagehandler)
	envt = 'LOSSLESS_TEST'
	boolconnect, dbbase, modsql, rootDk, listcategory = connectDatabase(envt)
	
	#print(list_infostrack['FILENAME'])
	
	# FLAC OK
	#list_infostrack = DBMediasTags().getTagMediaFLAC('E:\\Work\\ZTest\\01- Love Action.flac')
	#coveral = DBMediasTags().getImageFromTagFLAC('E:\\Work\\ZTest\\01- Love Action.flac', 'E:\\Work\\ZTest\\', 'FLACtest')
	
	# MP3 OK
	#list_infostrack = DBMediasTags().getTagMediaMP3('E:\\Work\\ZTest\\test.mp3')
	#coveral = DBMediasTags().getImageFromTagMP3('E:\\Work\\ZTest\\test.mp3', 'E:\\Work\\ZTest\\', 'MP3TEST')

	# APE OK  -- NO LENGHT
	#list_infostrack = DBMediasTags().getTagMediaAPE('E:\\Work\\ZTest\\01 - Orb - Valley.ape')
	#for tagname in list_infostrack.keys():print(tagname, '=', list_infostrack[tagname])
	#coveral = DBMediasTags().getImageFromTagAPE('E:\\Work\\ZTest\\01 - Orb - Valley.ape', 'E:\\Work\\ZTest\\', 'APEkkxxyy')
	#print(coveral, True)	
	
#	listeTags = ('TITLE', 'ARTIST', 'ALBUM', 'DATE', 'GENRE', 'TRACKNUMBER', 'ALBUMARTIST', 'DISCNUMBER', 'COMPOSER', 'ISRC', 'COUNTRY', 'ORGANIZATION')
	cuefile = r'E:\Work\ZTest\TAG_bluid\TRANCE\Download\2017\[OVNICD089] Ovnimoon & Rigel - Omnipresent Technology (2014)\Ovnimoon & Rigel - Omnipresent Technology.cue'
	
	
	rc = app.exec_()
	exit(rc)
