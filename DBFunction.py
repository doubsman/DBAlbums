#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import platform, stdout
from os import path, walk, listdir
from PyQt5.QtCore import (QProcess, QObject, QTime, QtInfoMsg,
						QtWarningMsg, QtCriticalMsg, QtFatalMsg)
from PyQt5.QtWidgets import QDesktopWidget


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


class ThemeColors(QObject):
	def __init__(self, nametheme):
		"""init theme list"""
		super(ThemeColors, self).__init__()
		self.themes = ['blue', 'green', 'brown', 'grey', 'pink']
		self.curthe = self.themes.index(nametheme)
		self.selectTheme(nametheme)
	
	def selectTheme(self, nametheme):
		"""Select theme "http://www.rapidtables.com/web/color/html-color-codes.htm"."""
		if nametheme == self.themes[0]:
			self.listcolors = ['lightsteelblue', 'lavender', 'lightgray', 'silver', 'dodgerblue']
		elif nametheme == self.themes[1]:
			self.listcolors = ['darkseagreen', 'honeydew', 'lightgray', 'silver', 'mediumseagreen']
		elif nametheme == self.themes[2]:
			self.listcolors = ['tan', 'papayawhip', 'lightgray', 'silver', 'peru']
		elif nametheme == self.themes[3]:
			self.listcolors = ['darkgray', 'azure', 'lightgray', 'silver', 'dimgray']
		elif nametheme == self.themes[4]:
			self.listcolors = ['rosybrown', 'lavenderblush', 'lightgray', 'silver', 'sienna']
	
	def nextTheme(self):
		"""Next color theme."""
		self.curthe += 1 
		self.curthe = self.curthe % len(self.themes)
		nametheme = self.themes[self.curthe]
		self.selectTheme(nametheme)


def buildlistcategory(configini, category, racine,  mode):
	"""Build list category from read ini file."""
	list_category = []
	configini.beginGroup(category)
	for cate in configini.allKeys():
		listracate = configini.value(cate)
		family = None
		if isinstance(listracate, list):
			for racate in listracate:
				if racate.find('|') > 0:
					family = racate.split('|')[1]
					racate = racate.split('|')[0]
				racate = path.join(racine, racate)
				list_category.append([cate, mode, racate, family])
		else:
			racate = listracate
			if racate.find('|') > 0:
				family = racate.split('|')[1]
				racate = racate.split('|')[0]
			racate = path.join(racine, racate)
			list_category.append([cate, mode, racate, family])
	configini.endGroup()
	return list_category


def displayCounters(num=0, text=''):
	"""format 0 000 + plural."""
	strtxt = " %s%s" % (text, "s"[num == 1:])
	if num > 9999:
		strnum = '{0:,}'.format(num).replace(",", " ")
	else:
		strnum = str(num)
	return (strnum + strtxt)


def displayStars(star, scorelist):
	"""scoring."""
	maxstar = len(scorelist)-1
	txt_score = scorelist[star]
	txt_color = "<font color=yellow><big>" + star*'★' + "</p></big></font>" 
	txt_color += "<font color=\"black\"><big>" +(maxstar-star)*'☆' + "</big></font>"
	txt_color += "<br/><font color=\"black\"><small>" + txt_score + " </small></font>" 
	#return (txt_score+'  '+star*'★'+(maxstar-star)*'☆')
	return txt_color


def centerWidget(widget):
	"""Center Widget."""
	qtrectangle = widget.frameGeometry()
	centerPoint = QDesktopWidget().availableGeometry().center()
	qtrectangle.moveCenter(centerPoint)
	widget.move(qtrectangle.topLeft())


def getListFiles(folder, masks=None):
	"""Build files list."""
	blacklist = ['desktop.ini', 'Thumbs.db']
	for folderName, subfolders, filenames in walk(folder):
		if subfolders:
			for subfolder in subfolders:
				getListFiles(subfolder, masks)
		for filename in filenames:
			if masks is None:
				if filename not in blacklist:
					yield path.join(folderName, filename)
			else:
				for xmask in masks:
					if filename[-len(xmask):].lower() in xmask:
						if filename not in blacklist:
							yield path.join(folderName, filename)


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


def logit(dat, filename):
	"""Send message to log file."""
	rt = open(filename, "a")
	rt.write(dat+"\n")
	rt.close()


def buildCommandPowershell(script, *argv):
	"""Build command PowerShell."""
	command = [r'-ExecutionPolicy', 'Unrestricted',
				'-WindowStyle', 'Hidden',
				'-File',
				script]
	for arg in argv:
		command += (arg,)
	return 'powershell.exe', command


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


def convertUNC(path):
	""" convert path UNC to linux."""
	# open file unc from Linux (mount \HOMERSTATION\_lossLess)
	if (platform == "darwin" or platform == 'linux') and path.startswith(r'\\'):
		path = r""+path.replace('\\\\', '/').replace('\\', '/')
	return(path)


def buildalbumnamehtml(name, label, isrc, year, nbcd, nbtracks, nbmin, nbcovers, albumPath, RESS_LABS, RESS_ICOS):
	"""buil label name & album name."""
	# name + label
	stylehtml = "text-decoration:none;color: black;"
	infoslabel = ""
	infonameal = ""
	infosayear = ""
	inffolder = ""
	infotags = ""
	infopowe = ""
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
		label = label.replace(' - ', ' ')
		imglabel = RESS_LABS +'/'+ label.replace(' ','_') +'.jpg'
		if not path.isfile(imglabel):
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
	# nb cd
	if nbcd<6:
		infosnbcd = '<img style="vertical-align:Bottom;" src="' + path.join(RESS_ICOS, 'cdrom.png') + '" height="17">'
		infosnbcd = nbcd*infosnbcd
	else:
		infosnbcd = displayCounters(nbcd, 'CD')
	if path.exists(albumPath):
		# folder
		inffolder =  '<img style="vertical-align:Bottom;" src="' + path.join(RESS_ICOS, 'folder.png') + '" height="17">'
		inffolder = '<a style=' + stylehtml + ' href="dbfunction://f">' + inffolder + '</a>'
		# tagscan / powershell
		if platform == "win32":
			infotags = '<img style="vertical-align:Bottom;" src="' + path.join(RESS_ICOS, 'tag.png') + '" height="17">'
			infotags = '<a style="' + stylehtml + '" href="dbfunction://t">' + infotags + '</a>'
			infopowe = '<img style="vertical-align:Bottom;" src="' + path.join(RESS_ICOS, 'pwr.png') + '" height="17">'
			infopowe = '<a style="' + stylehtml + '" href="dbfunction://p">' + infopowe + '</a>'
		else:
			infotags = infopowe = ''
	# others
	infotrack = displayCounters(nbtracks, 'Track')
	infoduree = displayCounters(nbmin, 'min')
	infoartco = displayCounters(nbcovers, 'art')
	if nbcovers>0:
		infoartco = '<a style="' + stylehtml + '" href="dbfunction://a">' + infoartco + '</a>'
	infoshtml = '<span>' + infonameal + '</span>' + infosnbcd + ' ' + inffolder + infotags + infopowe + '<br/>'
	if infoslabel != "":
		#if infosaisrc != "":
		#	infoshtml += infoslabel + ' • ' + infosaisrc + ' • '
		#else:
		infoshtml += infoslabel + ' • '
	infoshtml += infotrack + ' • ' + infoartco + ' • ' + infoduree + ' • ' + infosayear
	return infoshtml, imglabel


