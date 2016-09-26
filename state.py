from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import *

import sys

class CubeTimerState():
    def __init__(self):
        self.puzzleType = "3x3x3"
        self.chronoTimer = QTime()
        self.chronoIsRunning = False
        self.chronoStr = QString('00 : 00 . 000')
        self.timeList = [];
        self.timeListModel = QtGui.QStandardItemModel();

        self.statMean = 0;
        self.statAverage = 0;
        self.statBest = 0;
        self.statWorst = 0;
        self.statMeanItem = QtGui.QTableWidgetItem()
        self.statAverageItem = QtGui.QTableWidgetItem()
        self.statBestItem = QtGui.QTableWidgetItem()
        self.statWorstItem = QtGui.QTableWidgetItem()


    def chronoToStr(self, live):
        if live:
            chronoTime = self.chronoTimer.elapsed()
        else:
            chronoTime = self.timeList[-1]
        ms = chronoTime % 1000
        chronoTime /= 1000
        s = chronoTime % 60
        chronoTime /= 60
        m = chronoTime % 60
        chronoTime /= 60
        self.chronoStr = QString("%1 : ").arg(m, 2, 10, QChar('0'))
        self.chronoStr += QString("%1 . ").arg(s, 2, 10, QChar('0'))
        self.chronoStr += QString("%1").arg(ms, 3, 10, QChar('0'))
        return self.chronoStr

    def timeToStr(self, time):
        chronoTime = time
        ms = chronoTime % 1000
        chronoTime /= 1000
        s = chronoTime % 60
        chronoTime /= 60
        m = chronoTime % 60
        chronoTime /= 60
        ret_chronoStr = QString("%1 : ").arg(m, 2, 10, QChar('0'))
        ret_chronoStr += QString("%1 . ").arg(s, 2, 10, QChar('0'))
        ret_chronoStr += QString("%1").arg(ms, 3, 10, QChar('0'))
        return ret_chronoStr

    def startChrono(self):
        self.chronoIsRunning = True
        self.chronoTimer.restart()

    def stopChrono(self):
        self.timeList.append(self.chronoTimer.elapsed())
        self.chronoIsRunning = False
        item = QtGui.QStandardItem(str(len(self.timeList)) + ".\t" +self.chronoToStr(False))
        self.timeListModel.insertRow(0, item)
        self.calcStats()

    def calcStats(self):
        bestTime = self.timeList[0]
        worstTime = 0
        for i, time in enumerate(self.timeList):
            if (bestTime > time):
                bestTime = time
            if (worstTime < time):
                worstTime = time
        self.statMean = sum(self.timeList)/len(self.timeList)
        self.statMeanItem.setText(self.timeToStr(self.statMean))
        if (len(self.timeList) > 2):
            self.statAverage = (sum(self.timeList) - bestTime - worstTime)/(len(self.timeList)-2)
            self.statAverageItem.setText(self.timeToStr(self.statAverage))
        self.statBest = bestTime
        self.statBestItem.setText(self.timeToStr(self.statBest))
        self.statWorst = worstTime
        self.statWorstItem.setText(self.timeToStr(self.statWorst))

        #Debug for mean
        print("Mean: " + str(self.statMean))
