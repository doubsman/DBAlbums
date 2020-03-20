#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import call
from sys import argv, executable
from os import path
try:
	import mutagen
except ImportError:
	call([executable, "-m", "pip", "install", 'mutagen'])

try:
	import PyQt5.QtCore
except ImportError:
	call([executable, "-m", "pip", "install", 'PyQt5'])
	call([executable, "-m", "pip", "install", 'libqt5sql5-mysql'])
	call([executable, "-m", "pip", "install", 'python-pyqt5.qtmultimedia'])

try:
	import fpl_reader
except ImportError:
	#pip install git+https://github.com/rr-/fpl_reader/
	call([executable, "-m", "pip", "install", 'git+https://github.com/rr-/fpl_reader/'])
	call([executable, "-m", "pip", "install", 'git+https://github.com/rr-/fpl_reader/'])


# pip install -r requirements.txt
PATH_PROG = path.dirname(path.abspath(__file__))
call([executable, "-m", "pip", "install", '-r', path.join(PATH_PROG, 'requirements.txt')])
# dev
# pip install pyqt5-tools
from PyQt5.QtCore import (QTime, QtInfoMsg, qDebug, QtWarningMsg, QtCriticalMsg, QtFatalMsg,  qInstallMessageHandler)
from PyQt5.QtWidgets import QApplication
from DBAlbumsQT5 import DBAlbumsMainGui





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




if __name__ == '__main__':
	# debug
	qInstallMessageHandler(qtmymessagehandler)
	qDebug('start')
	app = QApplication(argv)
	DB = DBAlbumsMainGui()
	DB.show()
	rc = app.exec_()
	exit(rc)
