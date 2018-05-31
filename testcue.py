#!/usr/bin/env python
"""
deflacue is a Cue Sheet parser and a wrapper for mighty SoX utility - http://sox.sourceforge.net/.

SoX with appropriate plugins should be installed for deflacue to function.
Ubuntu users may install the following SoX packages: `sox`, `libsox-fmt-all`.


deflacue can function both as a Python module and in command line mode.
"""

# https://pypi.python.org/pypi/deflacue

import logging
from io import open  # Py2 support
from copy import deepcopy

COMMENTS_VORBIS = (
    'TITLE',
    'VERSION',
    'ALBUM',
    'TRACKNUMBER',
    'ARTIST',
    'PERFORMER',
    'COPYRIGHT',
    'LICENSE',
    'ORGANIZATION',
    'DESCRIPTION',
    'GENRE',
    'DATE',
    'LOCATION',
    'CONTACT',
    'ISRC'
)

COMMENTS_CUE_TO_VORBIS = {
    'TRACK_NUM': 'TRACKNUMBER',
    'TITLE': 'TITLE',
    'PERFORMER': 'ARTIST',
    'ALBUM': 'ALBUM',
    'GENRE': 'GENRE',
    'DATE': 'DATE',
}

class CueParser(object):
    """Simple Cue Sheet file parser."""

    def __init__(self, cue_file, encoding=None):
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

        self._current_context = self._context_global
        try:
            with open(cue_file, encoding=encoding) as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            print('Unable to read data from .cue file. Please use -encoding command line argument to set correct encoding.')

        for line in lines:
            if line.strip():
                command, args = line.strip().split(' ', 1)
                logging.debug('Command `%s`. Args: %s' % (command, args))
                method = getattr(self, 'cmd_%s' % command.lower(), None)
                if method is not None:
                    method(args)
                else:
                    logging.warning('Unknown command `%s`. Skipping ...' % command)

        for idx, track_data in enumerate(self._context_tracks):
            track_end_pos = None
            try:
                track_end_pos = self._context_tracks[idx + 1]['POS_START_SAMPLES']
            except IndexError:
                pass
            track_data['POS_END_SAMPLES'] = track_end_pos

    def get_data_global(self):
        """Returns a dictionary with global CD data."""
        return self._context_global

    def get_data_tracks(self):
        """Returns a list of dictionaries with individual
        tracks data. Note that some of the data is borrowed from global data.

        """
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
        self._current_context['TRACK_NUM'] = int(num)

    def cmd_flags(self, args):
        pass


cuefile = r'E:\Work\ZTest\TAG_bluid\TRANCE\Download\2017\[OVNICD089] Ovnimoon & Rigel - Omnipresent Technology (2014)\Ovnimoon & Rigel - Omnipresent Technology.cue'
parser = CueParser(cuefile)
header = parser.get_data_global()
for key in header.keys():
	print(key, '=', header[key])
print("---------")	
tracks = parser.get_data_tracks()
print(len(tracks))
print(tracks[0])
print(tracks[8])
#for key in tracks.keys():	print(key, '=', header[key])
print("---------")	


