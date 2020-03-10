#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from sys import platform
from PyQt5.QtCore import QObject, qDebug
from zipfile import ZipFile

class StringFormatAlbum(QObject):
	"""format name albums to present."""
	
	def __init__(self, parent):
		"""Init."""
		super(StringFormatAlbum, self).__init__(parent)
		self.parent = parent
		self.infoshtml = ''
		self.imglabel = None
		self.heighticon = '22'

	def formatCounters(self, num, text = ''):
		"""format 0 000 + plural."""
		strtxt = " %s%s" % (text, "s"[num == 1:])
		if num > 9999:
			strnum = '{0:,}'.format(num).replace(",", " ")
		else:
			strnum = str(num)
		return (strnum + strtxt)

	def formatAlbums(self):
		# infos albums
		name      = self.parent.tableMdlAlb.getData(self.parent.currow, 'NAME')
		label     = str(self.parent.tableMdlAlb.getData(self.parent.currow, 'LABEL'))
		if label == '':
			label = str(self.parent.tableMdlAlb.getData(self.parent.currow, 'TAGLABEL'))
		isrc      = str(self.parent.tableMdlAlb.getData(self.parent.currow, 'ISRC'))
		if isrc == '':
			isrc  = str(self.parent.tableMdlAlb.getData(self.parent.currow, 'TAGISRC'))
		country   = str(self.parent.tableMdlAlb.getData(self.parent.currow, 'COUNTRY'))
		year      = str(self.parent.tableMdlAlb.getData(self.parent.currow, 'YEAR'))
		nbcd      = int(self.parent.tableMdlAlb.getData(self.parent.currow, 'CD'))
		nbtracks  = int(self.parent.tableMdlAlb.getData(self.parent.currow, 'TRACKS'))
		nbmin     = int(self.parent.tableMdlAlb.getData(self.parent.currow, 'LENGTHDISPLAY').split(':')[0])
		nbcovers  = int(self.parent.tableMdlAlb.getData(self.parent.currow, 'PIC'))
		albumPath = self.parent.tableMdlAlb.getData(self.parent.currow, 'PATHNAME')
		stylehtml = "text-decoration:none;color: black;"
		
		# nb cds
		snbcd = str(nbcd)

		# name + label
		infonameal = ''
		infoslabel = ''
		if '[' in name:
			textsalbum = name[name.find('[')+1:name.find(']')]
			infonameal = name.replace('['+textsalbum+']', '')
			infoslabel += textsalbum.replace('-', ' • ')
		else:
			infonameal = name
		infonameal = infonameal.replace('(2CD)', '')
		infonameal = infonameal.replace('2CD', '')
		infonameal = infonameal.replace(' EP ', ' ')
		infonameal = infonameal.replace('VA - ', '')
		infonameal = infonameal.replace('(single)', '')
		infonameal = infonameal.replace('(Single)', '')
		sctxt = infonameal.split(' - ')[0].rstrip().replace(' ', '_') + ' '
		infonameal = infonameal.replace('('+snbcd+'CD)', '').replace(snbcd+'CD', '')
		infonameal = infonameal.replace(snbcd+'CD', '').replace(snbcd+'CD', '')
		infonameal = '<a style="' + stylehtml + '" href="dbfunction://s' + sctxt + '"><b><big>' + infonameal + '</big></b></a>'

		# label	+ isrc
		self.imglabel = None
		if label != "":
			if label.find('(') > 0:
				label = label[0:label.find('(')].rstrip()
			label = label.replace(' - ', ' ').title()
			# only family label
			if str(self.parent.tableMdlAlb.getData(self.parent.currow, 'LABEL')) != '':
				self.Extract_FileToPath(self.parent.LABEL_ZIP, label.replace(' ','_') +'.jpg', self.parent.RESS_TEMP)
				self.imglabel = path.join(self.parent.RESS_TEMP, label.replace(' ','_') +'.jpg')
				if not path.isfile(self.imglabel):
					qDebug('no image label : ' + self.imglabel)
					self.imglabel = None
			# isrc
			if isrc != "":
				infoslabel = '<a style="' + stylehtml + '" href="dbfunction://l'+label.replace(' ', '_')+'">' + label + ' [' + isrc + '] ' + '</a>'
			else:
				infoslabel = '<a style="' + stylehtml + '" href="dbfunction://l'+label.replace(' ', '_')+'">' + label + '</a>'
		elif infoslabel != "":
			if infoslabel.find('-') > 0:
				label = infoslabel.split('-')[0].replace('[', '').rstrip()
				infoslabel = '<big>' + label + '</big>'
				isrc = infoslabel.split('-')[1].replace(']', '').lstrip()

		# year
		infosayear = ''
		if year != "":
			infosayear = '<a style="' + stylehtml + '" href="dbfunction://y'+year+'">' + year + '</a>'

		# flags
		imageflag = ''
		if country != "":
			self.Extract_FileToPath(self.parent.FLAGS_ZIP, country.replace(' ', '-') + '.png', self.parent.RESS_TEMP)
			flagfile = path.join(self.parent.RESS_TEMP, country.replace(' ', '-') + '.png')
			if path.isfile(flagfile):
				imageflag = '<img style="vertical-align:Bottom;" src="' + flagfile + '" height="' + self.heighticon + '">'
				imageflag = '<a style="' + stylehtml + '" href="dbfunction://c' + country + '">' + imageflag + '</a>'
			else:
				qDebug('no image country : ' + country)
		# nb cd
		if nbcd > 1:
			infosnbcd = ' • ' + snbcd + "x"
			infosnbcd += '<img style="vertical-align:Bottom;" src="' + path.join(self.parent.RESS_ICOS, 'cdrom.png') + '" height="' + self.heighticon + '">'
		else:
			infosnbcd = ''

		inffolder = ''
		infotags = ''
		infopowe = ''
		if path.exists(albumPath):
			# folder
			inffolder =  '<img style="vertical-align:Bottom;" src="' + path.join(self.parent.RESS_ICOS, 'folder.png') + '" height="' + self.heighticon + '">'
			inffolder = '<a style=' + stylehtml + ' href="dbfunction://f">' + inffolder + '</a>'
			# update
			infopowe = '<img style="vertical-align:Bottom;" src="' + path.join(self.parent.RESS_ICOS, 'update.png') + '" height="' + self.heighticon + '">'
			infopowe = '<a style="' + stylehtml + '" href="dbfunction://p">' + infopowe + '</a>'
			# tagscan
			if platform == "win32":
				infotags = '<img style="vertical-align:Bottom;" src="' + path.join(self.parent.RESS_ICOS, 'tag.png') + '" height="' + self.heighticon + '">'
				infotags = '<a style="' + stylehtml + '" href="dbfunction://t">' + infotags + '</a>'
		
		# others
		infotrack = self.formatCounters(nbtracks, 'Track')
		infoduree = self.formatCounters(nbmin, 'min')
		infoartco = self.formatCounters(nbcovers, 'pic')
		infopics = ''
		
		# artwork
		if nbcovers > 1:
			infoartco = '<a style="' + stylehtml + '" href="dbfunction://a">' + infoartco + '</a>'
			infopics = '<img style="vertical-align:Bottom;" src="' + path.join(self.parent.RESS_ICOS, 'art.png') + '" height="' + self.heighticon + '">'
			infopics = '<a style="' + stylehtml + '" href="dbfunction://a">' + infopics + '</a>'
		
		# build final
		self.infoshtml = '<span>' + infonameal + '</span>' + infopics + ' ' + inffolder + ' ' + infotags + ' ' + infopowe + '<br/>'
		if infoslabel != "":
			self.infoshtml += infoslabel + '   ' + imageflag + country + '<br/>'
		elif country != "":
			self.infoshtml += imageflag + country + '<br/>'
		self.infoshtml += infosayear + ' • ' + infotrack + ' • ' + infoduree + ' • ' + infoartco + infosnbcd

	def Extract_FileToPath(self, my_zip, my_file, extractpath = None):
		if not path.isfile(path.join(extractpath, my_file)):
			with ZipFile(my_zip) as zip:
				for zip_info in zip.infolist():
					if my_file in zip_info.filename:
						zip_info.filename = path.basename(zip_info.filename)
						qDebug('extract (' + my_zip + ') : ' + my_file)
						zip.extract(zip_info, extractpath)