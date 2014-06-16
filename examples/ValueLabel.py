# -*- coding: utf-8 -*-
"""
Demonstrates use of ValueLabel, which provides text display for monitoring
a value that changes over time.
"""
import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

pg.mkQApp()

win = QtGui.QWidget()
win.setWindowTitle('pyqtgraph example: ValueLabel')

hlayout = QtGui.QHBoxLayout()
win.setLayout(hlayout)

plot = pg.PlotWidget()
hlayout.addWidget(plot)

vwidget = QtGui.QWidget()
hlayout.addWidget(vwidget)
vlayout = QtGui.QVBoxLayout()
vwidget.setLayout(vlayout)

# Make several ValueLabels with a variety of configurations
labels = [
    pg.ValueLabel(),
    pg.ValueLabel(suffix='V', siPrefix=False),
    pg.ValueLabel(suffix='V', siPrefix=True),
    pg.ValueLabel(suffix='V', siPrefix=True, averageTime=1),
    pg.ValueLabel(suffix='V', siPrefix=True, averageTime=5),
    pg.ValueLabel(formatStr="{value:.2} (avg: {avgValue:.2})", averageTime=-1),
    pg.ValueLabel(error=True, errorType='stdDev', suffix='V', siPrefix=True, averageTime=3),
    pg.ValueLabel(error=True, errorType='stdDev', suffix='V', siPrefix=False, averageTime=3),
    ]
for label in labels:
    label.setMinimumWidth(200)
    vlayout.addWidget(label)
vlayout.addItem(QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))


win.resize(800, 400)
win.show()

data = [.01]

def update():
    global data, plot, labels
    x = 1.01**np.random.normal() * data[-1]
    data = data[-500:] + [x]
    plot.plot(data, clear=True)
    for l in labels:
        l.setValue(x)
    
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(20)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
