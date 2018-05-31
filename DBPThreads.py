#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread

class DBPThreads(QThread):
	def __init__(self, parent):
		super(DBPThreads, self).__init__(parent)

	def __del__(self):
		self.wait()

	def run(self):
		# your logic here
		pass
