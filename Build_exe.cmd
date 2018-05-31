rem remove build
RMDIR "N:\_INVENT\DBAlbums\Build" /S /Q

rem create EXE
N:
CD N:\_INVENT\DBAlbums
c:\Python36\python.exe setup.py build

rem copy files
XCOPY N:\_INVENT\DBAlbums\LIB\* N:\_INVENT\DBAlbums\build\exe.win32-3.6\LIB /E /F /I
XCOPY N:\_INVENT\DBAlbums\LOC\* N:\_INVENT\DBAlbums\build\exe.win32-3.6\LOC /E /F /I
XCOPY N:\_INVENT\DBAlbums\LOG\* N:\_INVENT\DBAlbums\build\exe.win32-3.6\LOG /E /F /I
XCOPY N:\_INVENT\DBAlbums\PS1\* N:\_INVENT\DBAlbums\build\exe.win32-3.6\PS1 /E /F /I
XCOPY N:\_INVENT\DBAlbums\SQL\* N:\_INVENT\DBAlbums\build\exe.win32-3.6\SQL /E /F /I