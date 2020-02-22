#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import platform, stdout
from os import path, walk, listdir
from PyQt5.QtCore import (QProcess, QTime, QtInfoMsg, qDebug, 
						QtWarningMsg, QtCriticalMsg, QtFatalMsg)


# Logging
def qtmymessagehandler(mode, context, message):
	curdate = QTime.currentTime().toString('hh:mm:ss')
	if mode == QtInfoMsg:
		mode = 'INFO'
	elif mode == QtWarningMsg:
		mode = 'WARNING'
	elif mode == QtCriticalMsg:
		mode = 'CRITICAL'
	elif mode == QtFatalMsg:
		mode = 'FATAL'
	else:
		mode = 'DEBUG'
	print('qt_message_handler: line: {li}, func: {fu}(), file: {fi}, time: {ti}'.format(li=context.line,
																		 fu=context.function,
																		 fi=context.file, 
																		 ti=curdate))
	print('  {m}: {e}\n'.format(m=mode, e=message))


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    stdout.flush()


def displayCounters(num=0, text=''):
	"""format 0 000 + plural."""
	strtxt = " %s%s" % (text, "s"[num == 1:])
	if num > 9999:
		strnum = '{0:,}'.format(num).replace(",", " ")
	else:
		strnum = str(num)
	return (strnum + strtxt)


def getListFiles(folder, masks=None, exact=None):
	"""Build files list."""
	blacklist = ['desktop.ini', 'Thumbs.db']
	for folderName, subfolders, filenames in walk(folder):
		if subfolders:
			for subfolder in subfolders:
				getListFiles(subfolder, masks, exact)
		for filename in filenames:
			if masks is None:
				# no mask
				if filename not in blacklist:
					yield path.join(folderName, filename)
			else:
				# same
				if exact:
					if filename.lower() in masks:
						if filename not in blacklist:
								yield path.join(folderName, filename)
				else:
					# mask joker
					for xmask in masks:
						if filename[-len(xmask):].lower() in xmask:
							if filename not in blacklist:
								yield path.join(folderName, filename)


def getListFilesNoSubFolders(folder, masks=None, exact=None):
	"""Build files list."""
	blacklist = ['desktop.ini', 'Thumbs.db']
	for filename in listdir(folder):
		# file
		if not path.isdir(path.join(folder, filename)):
			if masks is None:
				yield path.join(folder, filename)
			else:
				# same
				if exact:
					if filename.lower() in masks:
						if filename not in blacklist:
								yield path.join(folder, filename)
				else:
					# mask joker
					for xmask in masks:
						if filename[-len(xmask):].lower() in xmask:
							if filename not in blacklist:
								yield path.join(folder, filename)


def getListFolders(folder):
	"""Build folders list."""
	return [d for d in listdir(folder) if path.isdir(path.join(folder, d))]


def getFolderSize(folder):
	"""Calcul folder size."""
	total_size = path.getsize(folder)
	for item in listdir(folder):
		itempath = path.join(folder, item)
		if path.isfile(itempath):
			total_size += path.getsize(itempath)
		elif path.isdir(itempath):
			total_size += getFolderSize(itempath)
	return total_size


def runCommand(prog, *argv):
	"""Execut a program no wait, no link."""
	argums = []
	for arg in argv:
		argums += (arg,)
	p = QProcess()
	# print(prog, argums)
	p.startDetached(prog, argums)


def openFolder(path):
	"""Open File Explorer."""
	if platform == "win32":
		runCommand('explorer', path)
	elif platform == "darwin":
		runCommand('open', path)
	elif platform == 'linux':
		runCommand('xdg-open', path)


def buildalbumnamehtml(name, label, isrc, country, year, nbcd, nbtracks, nbmin, nbcovers, albumPath, RESS_LABS, RESS_ICOS, RESS_FLAGS):
	"""buil label name & album name."""
	# name + label
	stylehtml = "text-decoration:none;color: black;"
	infoslabel = ''
	infonameal = ''
	infosayear = ''
	inffolder = ''
	infotags = ''
	infopowe = ''
	imageflag = ''
	imglabel = None
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
	snbcd = str(nbcd)
	sctxt = infonameal.split(' - ')[0].rstrip().replace(' ', '_')
	infonameal = infonameal.replace('('+snbcd+'CD)', '').replace(snbcd+'CD', '')
	infonameal = infonameal.replace(snbcd+'CD', '').replace(snbcd+'CD', '')
	infonameal = '<a style="' + stylehtml + '" href="dbfunction://s' + sctxt + '"><b><big>' + infonameal + '</big></b></a>'
	# label
	if label != "":
		if label.find('(')>0:
			label = label[0:label.find('(')].rstrip()
		label = label.replace(' - ', ' ').title()
		imglabel = path.join(RESS_LABS, label.replace(' ','_') +'.jpg')
		if not path.isfile(imglabel):
			qDebug('no image label : ' + imglabel)
			imglabel = None
		# isrc
		if isrc != "":
			infoslabel = '<a style="' + stylehtml + '" href="dbfunction://l'+label.replace(' ', '_')+'">' + label + '[' + isrc + ']' + '</a>'
		else:
			infoslabel = '<a style="' + stylehtml + '" href="dbfunction://l'+label.replace(' ', '_')+'">' + label + '</a>'
	elif infoslabel != "":
		if infoslabel.find('-') > 0:
			label = infoslabel.split('-')[0].replace('[', '').rstrip()
			infoslabel = '<big>' + label + '</big>'
			isrc = infoslabel.split('-')[1].replace(']', '').lstrip()
	# year
	if year != "":
		infosayear = '<a style="' + stylehtml + '" href="dbfunction://y'+year+'">' + year + '</a>'
	# flags
	if country != "":
		flagfile = path.join(RESS_FLAGS, country.replace(' ', '-') + '.png')
		if path.isfile(flagfile):
			imageflag = '<img style="vertical-align:Bottom;" src="' + flagfile + '" height="17">'
			imageflag = '<a style="' + stylehtml + '" href="dbfunction://c' + country + '">' + imageflag + '</a>'
	# nb cd
	if nbcd<6:
		infosnbcd = '<img style="vertical-align:Bottom;" src="' + path.join(RESS_ICOS, 'cdrom.png') + '" height="17">'
		infosnbcd = nbcd*infosnbcd
	else:
		infosnbcd = displayCounters(nbcd, 'CD')
	infosnbcd = ''
	if path.exists(albumPath):
		# folder
		inffolder =  '<img style="vertical-align:Bottom;" src="' + path.join(RESS_ICOS, 'folder.png') + '" height="17">'
		inffolder = '<a style=' + stylehtml + ' href="dbfunction://f">' + inffolder + '</a>'
		# tagscan / powershell
		if platform == "win32":
			infotags = '<img style="vertical-align:Bottom;" src="' + path.join(RESS_ICOS, 'tag.png') + '" height="17">'
			infotags = '<a style="' + stylehtml + '" href="dbfunction://t">' + infotags + '</a>'
			infopowe = '<img style="vertical-align:Bottom;" src="' + path.join(RESS_ICOS, 'update.png') + '" height="17">'
			infopowe = '<a style="' + stylehtml + '" href="dbfunction://p">' + infopowe + '</a>'
		else:
			infotags = infopowe = ''
	# others
	infotrack = displayCounters(nbtracks, 'Track')
	infoduree = displayCounters(nbmin, 'min')
	infoartco = displayCounters(nbcovers, 'art')
	infopics = ''
	# artwork
	if nbcovers>0:
		infoartco = '<a style="' + stylehtml + '" href="dbfunction://a">' + infoartco + '</a>'
		infopics = '<img style="vertical-align:Bottom;" src="' + path.join(RESS_ICOS, 'art.png') + '" height="17">'
		infopics = '<a style="' + stylehtml + '" href="dbfunction://a">' + infopics + '</a>'
	infoshtml = '<span>' + infonameal + '</span>' + imageflag + ' ' + infosnbcd + ' ' + infopics + ' ' + inffolder + ' ' + infotags + ' ' + infopowe + '<br/>'
	if infoslabel != "":
		#if infosaisrc != "":
		#	infoshtml += infoslabel + ' • ' + infosaisrc + ' • '
		#else:
		infoshtml += infoslabel + ' • '
	infoshtml += infotrack + ' • ' + infoartco + ' • ' + infoduree + ' • ' + infosayear
	return infoshtml, imglabel


