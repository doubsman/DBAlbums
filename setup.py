#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""c:\Python36\python.exe setup.py build."""
from cx_Freeze import setup, Executable
import sys
import os

os.environ['TCL_LIBRARY'] = r'C:\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Python36\tcl\tk8.6'

if sys.platform=='win32':
	base = 'Win32GUI'

includefiles = [r'DBAlbums-cd-blank.png',r'DBAlbums-cd-blank3d.png',r'DBAlbums-cd-blank-mini.jpg',r'DBAlbums-cd-blank-mini3d.jpg',
				r'DBAlbums-icone.ico',r'DBAlbums-icone.xbm',r'DBAlbums.ini',
				r'C:\Python36\DLLs\tcl86t.dll',r'C:\Python36\DLLs\tk86t.dll',r'C:\Python36\DLLs\sqlite3.dll']
buildOptions = dict(packages = [], excludes = [], include_files = includefiles)

setup(name='DbAlbums',
	version = '1.45',
	description = 'Invent Albums',
	author = 'doubsman',
	options = {"build_exe": buildOptions},
	executables = [Executable(script="DBAlbums.pyw", base=base, icon=r"DBAlbums-icone.ico")])
