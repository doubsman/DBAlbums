#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import QObject, QDateTime, pyqtSignal, QTimer


class DBChrono(QObject):
	# signals	
	signalnow = pyqtSignal(str)		# emit chrono str 00:00:00
	signalsto = pyqtSignal(int)		# emit chrono = stopsec

	def __init__(self, startsec = 0, stopsec = None, parent = None):
		"""Init."""
		super(DBChrono, self).__init__(parent)
		self.now = startsec
		self.sto = stopsec
		# Initialize timer
		self.timer = QTimer()
		self.timer.timeout.connect(self.tick_timer)

	def reinit_timer(self):
		self.now = 0

	def start_timer(self):
		"""Start Chrono."""
		# Start timer and update display
		self.timer.start(1000)
		self.update_timer()

	def update_timer(self):
		"""Update chrono display."""
		hours, seconds =  self.now // 3600, self.now % 3600
		minutes, seconds = seconds // 60, seconds % 60
		runtime = "%02d:%02d:%02d" % (hours, minutes, seconds)
		self.signalnow.emit(runtime)
		if self.sto is not None:
			#print(self.sto, self.now)
			if self.now >= self.sto:
				self.signalsto.emit(1)
				self.stop_timer()

	def tick_timer(self):
		"""Tic tac."""
		self.now += 1
		self.update_timer()

	def stop_timer(self):
		self.timer.stop()