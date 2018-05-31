#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import platform
from os import path, walk
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QDesktopWidget


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


def getListFiles(folder, masks):
	"""Build files list."""
	for folderName, subfolders, filenames in walk(folder):
		if subfolders:
			for subfolder in subfolders:
				getListFiles(subfolder, masks)
		for filename in filenames:
			for xmask in masks:
				if filename[-4:].lower() in xmask:
					yield path.join(folderName, filename)


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



