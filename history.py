from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import *
import math

import sys

class CubeTimerHistory():
    def __init__(self):
        self.histFileName = "history.evt"
        self.timeList = []
        self.timeListModel = QtGui.QStandardItemModel();


    def initHistory(self):
        with open(self.histFileName) as file:
            for record in file:
                split = record.split(";")
                self.timeList.append([split[0], split[1], split[2], split[3], split[4]])
                item = QtGui.QStandardItem(split[0] + "\t" + split[1] + "\t\t\t" + split[2] + \
                                           "\t\t" + split[3] + "\t" + split[4][:-1])
                self.timeListModel.insertRow(0, item)
