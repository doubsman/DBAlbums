#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore

def start_timer(slot, count=1, interval=1000):
    counter = 0
    def handler():
        nonlocal counter
        counter += 1
        slot(counter)
        if counter >= count:
            timer.stop()
            timer.deleteLater()
    timer = QtCore.QTimer()
    timer.timeout.connect(handler)
    timer.start(interval)

def timer_func(count):
    print('Timer:', count)
    if count >= 5:
        QtCore.QCoreApplication.quit()

app = QtCore.QCoreApplication([])
start_timer(timer_func, 5)
app.exec_()

