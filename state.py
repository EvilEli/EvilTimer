from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import *
from history import CubeTimerHistory

import math
import sys
import datetime

class CubeTimerState():
    def __init__(self):
        self.initHist()
        self.puzzleType = "3x3x3"
        self.chronoTimer = QTime()
        self.chronoIsRunning = False
        self.chronoStr = QString('00 : 00 . 000')
        self.timeList = [];
        self.timeListModel = QtGui.QStandardItemModel();

        self.statMean = 0
        self.statAverage = 0
        self.statBest = 0
        self.statMedian = 0
        self.statWorst = 0
        self.statStdDev = 0
        self.statMo3 = 0
        self.statBestMo3 = 0
        self.statAo5 = 0
        self.statBestAo5 = 0
        self.statAo12 = 0
        self.statBestAo12 = 0
        self.statMeanItem = QtGui.QTableWidgetItem()
        self.statAverageItem = QtGui.QTableWidgetItem()
        self.statBestItem = QtGui.QTableWidgetItem()
        self.statMedianItem = QtGui.QTableWidgetItem()
        self.statWorstItem = QtGui.QTableWidgetItem()
        self.statStdDevItem = QtGui.QTableWidgetItem()

        self.statMo3Item = QtGui.QTableWidgetItem()
        self.statBestMo3Item = QtGui.QTableWidgetItem()
        self.statAo5Item = QtGui.QTableWidgetItem()
        self.statBestAo5Item = QtGui.QTableWidgetItem()
        self.statAo12Item = QtGui.QTableWidgetItem()
        self.statBestAo12Item = QtGui.QTableWidgetItem()

    def initHist(self):
        self.history = CubeTimerHistory()
        self.history.initHistory()

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
        self.updateHistory()

    def calcStats(self):
        bestTime = self.timeList[0]
        worstTime = self.timeList[0]
        for i, time in enumerate(self.timeList):
            if (bestTime > time):
                bestTime = time
            if (worstTime < time):
                worstTime = time
        # Mean
        self.statMean = sum(self.timeList)/len(self.timeList)
        self.statMeanItem.setText(self.timeToStr(self.statMean))
        # Average
        if (len(self.timeList) > 2):
            self.statAverage = (sum(self.timeList) - bestTime - worstTime)/(len(self.timeList)-2)
            self.statAverageItem.setText(self.timeToStr(self.statAverage))
        # Best
        self.statBest = bestTime
        self.statBestItem.setText(self.timeToStr(self.statBest))
        # Median
        self.statMedian = sorted(self.timeList)[len(self.timeList)/2]
        self.statMedianItem.setText(self.timeToStr(self.statMedian))
        # Worst
        self.statWorst = worstTime
        self.statWorstItem.setText(self.timeToStr(self.statWorst))
        # Standard Deviation
        if (len(self.timeList) > 1):
            self.statStdDev = math.sqrt(sum([(time - self.statMean)**2 for time in self.timeList])/(len(self.timeList)-1))
            self.statStdDevItem.setText(self.timeToStr(self.statStdDev))
        # Mean of 3
        if (len(self.timeList) > 2):
            self.statMo3 = (self.timeList[-1]+self.timeList[-2]+self.timeList[-3])/3
            self.statMo3Item.setText(self.timeToStr(self.statMo3))
        # Best Mean of 3
            self.statBestMo3 = self.statMo3
            for i in range(len(self.timeList)-3):
                cur_Mo3 = self.statMo3 = (self.timeList[i]+self.timeList[i+1]+self.timeList[i+2])/3
                if (cur_Mo3 < self.statBestMo3):
                    self.statBestMo3 = cur_Mo3
            self.statBestMo3Item.setText(self.timeToStr(self.statBestMo3))
        # Average of 5
        if (len(self.timeList) > 4):
            bestTime = self.timeList[-1]
            worstTime = self.timeList[-1]
            for i in range(5):
                if (self.timeList[len(self.timeList)-1 -i] < bestTime):
                    bestTime = self.timeList[len(self.timeList)-1 -i]
                if (self.timeList[len(self.timeList)-1 -i] > worstTime):
                    worstTime = self.timeList[len(self.timeList)-1 -i]
            self.statAo5 = (sum(self.timeList[-5:])- bestTime - worstTime)/3
            self.statAo5Item.setText(self.timeToStr(self.statAo5))
        # Best Average of 5
            self.statBestAo5 = self.statAo5
            for k in range(len(self.timeList)-5):
                bestTime = self.timeList[k]
                worstTime = self.timeList[k]
                for i in range(5):
                    if (self.timeList[k+i] < bestTime):
                        bestTime = self.timeList[k+i]
                    if (self.timeList[k+i] > worstTime):
                        worstTime = self.timeList[k+i]
                cur_Ao5 = (sum(self.timeList[k:k+5])- bestTime - worstTime)/3
                if (cur_Ao5 < self.statBestAo5):
                    self.statBestAo5 = cur_Ao5
            self.statBestAo5Item.setText(self.timeToStr(self.statBestAo5))
        # Average of 12
        if (len(self.timeList) > 11):
            bestTime = self.timeList[-1]
            worstTime = self.timeList[-1]
            for i in range(12):
                if (self.timeList[len(self.timeList)-1 -i] < bestTime):
                    bestTime = self.timeList[len(self.timeList)-1 -i]
                if (self.timeList[len(self.timeList)-1 -i] > worstTime):
                    worstTime = self.timeList[len(self.timeList)-1 -i]
            self.statAo12 = (sum(self.timeList[-12:])- bestTime - worstTime)/10
            self.statAo12Item.setText(self.timeToStr(self.statAo12))
        # Best Average of 12
            self.statBestAo12 = self.statAo12
            for k in range(len(self.timeList)-12):
                bestTime = self.timeList[k]
                worstTime = self.timeList[k]
                for i in range(12):
                    if (self.timeList[k+i] < bestTime):
                        bestTime = self.timeList[k+i]
                    if (self.timeList[k+i] > worstTime):
                        worstTime = self.timeList[k+i]
                cur_Ao12 = (sum(self.timeList[k:k+12])- bestTime - worstTime)/10
                if (cur_Ao12 < self.statBestAo12):
                    self.statBestAo12 = cur_Ao12
            self.statBestAo12Item.setText(self.timeToStr(self.statBestAo12))

    def updateHistory(self):
        self.history.timeList.append([len(self.history.timeList), str(datetime.datetime.utcnow())[:-7], self.chronoToStr(False), 0, "scramble"])
        item = QtGui.QStandardItem(str(self.history.timeList[-1][0]) + "\t" + self.history.timeList[-1][1] + "\t\t" + \
                                   self.history.timeList[-1][2] + "\t" + str(self.history.timeList[-1][3]) + "\t" + \
                                   self.history.timeList[-1][4])
        #item = QtGui.QStandardItem("test")
        self.history.timeListModel.insertRow(1, item)
