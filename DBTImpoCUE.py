#!/usr/bin/env python
# coding: utf-8

from PyQt5.QtCore import qDebug, qInstallMessageHandler
from copy import deepcopy
from DBFunction import qtmymessagehandler


class CueParser(object):
	"""Simple Cue Sheet file parser, The last tracks have no duration."""
	# https://pypi.python.org/pypi/deflacue
	# 'PERFORMER', 'SONGWRITER', 'ALBUM', 'GENRE', 'DATE', 'FILE', 'COMMENT', 'DISCID', 'TRACKNUMBER', 'TITLE', 'INDEX', 'POS_START_SAMPLES', 'POS_END_SAMPLES', 'LENGTHSECONDS', 'LENGTHDISPLAY'

	def __init__(self, cue_file, totalseconds=None, encoding=None):
		self._context_global = {
			'PERFORMER': 'Unknown',
			'SONGWRITER': None,
			'ALBUM': 'Unknown',
			'GENRE': 'Unknown',
			'DATE': None,
			'FILE': None,
			'COMMENT': None,
			}
		self._context_tracks = []
		self.lastfiletrack = None

		self._current_context = self._context_global
		try:
			with open(cue_file, encoding=encoding) as f:
				lines = f.readlines()
		except UnicodeDecodeError:
			qDebug('Unable to read data from .cue file. Please use -encoding command line argument to set correct encoding. '+cue_file)

		for line in lines:
			if line.strip():
				command, args = line.strip().split(' ', 1)
				#qDebug('Command `%s`. Args: %s' % (command, args))
				method = getattr(self, 'cmd_%s' % command.lower(), None)
				if method is not None:
					method(args)
				else:
					pass
					#qDebug('Unknown command `%s`. Skipping ...' % command)

		for idx, track_data in enumerate(self._context_tracks):
			track_end_pos = None
			trackduration = None
			try:
				cumulduration = self._timestr_to_sec(self._context_tracks[idx + 1]['INDEX'])
				trackduration = cumulduration  - self._timestr_to_sec(self._context_tracks[idx]['INDEX'])
				track_end_pos = self._context_tracks[idx + 1]['POS_START_SAMPLES']
			except IndexError:
				pass
			track_data['POS_END_SAMPLES'] = track_end_pos
			track_data['LENGTHSECONDS'] = trackduration
			track_data['LENGTHDISPLAY'] = self._seconds_to_string(trackduration)
		# last track
		lasttrack = len(self._context_tracks)-1
		self.lastfiletrack  = self._context_tracks[lasttrack]['FILE']
		if totalseconds is not None:
			# Each minute contains 60 seconds (obviously); each second contains 75 frames; and each frame contains 588 samples.
			# offset = ((((minutes * 60) + seconds) * 75) + frames) * 588
			self._context_tracks[lasttrack]['POS_END_SAMPLES'] = totalseconds * 75 * 588
			self._context_tracks[lasttrack]['LENGTHSECONDS'] = totalseconds - self._timestr_to_sec(self._context_tracks[lasttrack]['INDEX'])
			self._context_tracks[lasttrack]['LENGTHDISPLAY'] = self._seconds_to_string(self._context_tracks[lasttrack]['LENGTHSECONDS'])
			

	def get_data_global(self):
		"""Returns a dictionary with global CD data."""
		return self._context_global

	def get_data_tracks(self):
		"""Returns a list of dictionaries with individual
		tracks data. Note that some of the data is borrowed from global data."""
		return self._context_tracks

	def _unquote(self, in_str):
		return in_str.strip(' "')

	def _timestr_to_sec(self, timestr):
		"""Converts `mm:ss:` time string into seconds integer."""
		splitted = timestr.split(':')[:-1]
		splitted.reverse()
		seconds = 0
		for i, chunk in enumerate(splitted, 0):
			factor = pow(60, i)
			if i == 0:
				factor = 1
			seconds += int(chunk) * factor
		return seconds

	def _timestr_to_samples(self, timestr):
		"""Converts `mm:ss:ff` time string into samples integer, assuming the
		CD sampling rate of 44100Hz."""
		seconds_factor = 44100
		# 75 frames per second of audio
		frames_factor = seconds_factor // 75
		full_seconds = self._timestr_to_sec(timestr)
		frames = int(timestr.split(':')[-1])
		return full_seconds * seconds_factor + frames * frames_factor
	
	def _seconds_to_string(self, seconds):
		"""Convert duration seconds int to string mm:ss"""
		if seconds is not None:
			minutes = seconds // 60
			return "%02d:%02d" % (minutes, seconds % 60)
		return None
		
	def _in_global_context(self):
		return self._current_context == self._context_global

	def cmd_rem(self, args):
		subcommand, subargs = args.split(' ', 1)
		if subargs.startswith('"'):
			subargs = self._unquote(subargs)
		self._current_context[subcommand.upper()] = subargs

	def cmd_performer(self, args):
		unquoted = self._unquote(args)
		self._current_context['PERFORMER'] = unquoted

	def cmd_title(self, args):
		unquoted = self._unquote(args)
		if self._in_global_context():
			self._current_context['ALBUM'] = unquoted
		else:
			self._current_context['TITLE'] = unquoted

	def cmd_file(self, args):
		filename = self._unquote(args.rsplit(' ', 1)[0])
		self._current_context['FILE'] = filename

	def cmd_index(self, args):
		timestr = args.split()[1]
		self._current_context['INDEX'] = timestr
		self._current_context['POS_START_SAMPLES'] = self._timestr_to_samples(timestr)

	def cmd_track(self, args):
		num, ttype = args.split()
		new_track_context = deepcopy(self._context_global)
		self._context_tracks.append(new_track_context)
		self._current_context = new_track_context
		self._current_context['TRACKNUMBER'] = int(num)

	def cmd_flags(self, args):
		pass


if __name__ == '__main__':
	qInstallMessageHandler(qtmymessagehandler)
	cuefile = r'E:\Work\ZTest\TAG_bluid\TRANCE\Download\2017\[OVNICD089] Ovnimoon & Rigel - Omnipresent Technology (2014)\Ovnimoon & Rigel - Omnipresent Technology.cue'
	parser = CueParser(cuefile, 4560)
	header = parser.get_data_global()
	for key in header.keys():
		print(key, '=', header[key])
	print("---------")	
	listtracks = parser.get_data_tracks()
	print(len(listtracks), 'Tracks')
	print("---------")	
	for track in listtracks:
		for key in track.keys():
			print(key, '=', track[key])
		print("---------")		





