#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
from os import path
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
	# working directory
	PATH_PROG = path.dirname(path.abspath(__file__))
	# debug
	qInstallMessageHandler(qtmymessagehandler)
	qDebug('start')
	app = QApplication(argv)
	DB = DBAlbumsMainGui()
	DB.show()
	rc = app.exec_()
	exit(rc)
