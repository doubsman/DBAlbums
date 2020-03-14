#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import QObject, QDateTime, pyqtSignal, QTimer


class DBChrono(QObject):
	# signals	
	signalnow = pyqtSignal(str)
	signalsto = pyqtSignal(int)

	def __init__(self, startsec = 0, stopsec = None, parent = None):
		"""Init."""
		super(DBChrono, self).__init__(parent)
		self.now = 0 #float(startsec)
		self.sto = stopsec

	def start_timer(self):
		"""Start Chrono."""
		# Initialize timer
		self.timer = QTimer()
		self.timer.timeout.connect(self.tick_timer)
		# Start timer and update display
		self.timer.start(1000)
		self.update_timer()

	def update_timer(self):
		"""Update chrono display."""
		hours, seconds =  self.now // 3600, self.now % 3600
		minutes, seconds = seconds // 60, seconds % 60
		runtime = "%02d:%02d:%02d" % (hours, minutes, seconds)
		self.signalnow.emit(runtime)
		if self.sto:
			if self.sto >= (self.now % 3600):
				self.signalsto.emit(1)
				self.stop_timer()

	def tick_timer(self):
		"""Tic tac."""
		self.now += 1
		self.update_timer()

	def stop_timer(self):
		self.timer.stop()