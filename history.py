from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyKDE4.kdeui import KPlotWidget, KPlotObject
import sys
import math

class CubeTimerHistory():
    def __init__(self):
        self.histFileName = "history.evt"
        self.timeList = []
        self.timeListModel = QtGui.QStandardItemModel();
        self.plot_obj = KPlotObject(QtGui.QColor(255,0,255))

        self.statNumOfSol = 0
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
        self.statNumOfSolItem = QtGui.QTableWidgetItem()
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

    def initHistory(self):
        with open(self.histFileName, 'r') as file:
            for i,record in enumerate(file):
                split = record.split(";")
                self.timeList.append([self.strToTime(split[1]),split[0], split[1], split[2], split[3][:-1]])
                item = QtGui.QStandardItem(str(i+1) + "\t" + split[0] + "\t\t" + split[1] + \
                                           "\t" + split[2] + "\t" + split[3][:-1])
                self.timeListModel.insertRow(0, item)
        self.calcStats()
        self.makePlot()

    # returns the int form of a provided str-time
    def strToTime(self, time):
        chronoTime_split = str(time).replace(".",":").split(":")
        chronoTime = 60000*int(chronoTime_split[0]) + 1000*int(chronoTime_split[1]) + int(chronoTime_split[2])
        return chronoTime

    # returns the string form of a provided ms-integer
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

    def addTime(self, time):
        # append to list
        self.timeList.append(time)
        # append to display model
        item = QtGui.QStandardItem(str(len(self.timeList)) + "\t" + str(time[1]) + "\t\t" + \
                                   time[2] + "\t" + str(time[3]) + "\t" + \
                                   time[4])
        self.timeListModel.insertRow(0, item)
        # append to plot
        self.plot_obj.addPoint(float(len(self.timeList)), float(time[0])/1000)
        # write to file
        with open(self.histFileName, 'a') as file:
            file.write(time[1]+";"+time[2]+";"+str(time[3])+";"+time[4]+"\n")
        # update stats
        self.calcStats()


    def deleteTime(self, sel_idx):
        self.timeListModel.clear()
        self.timeList.pop((len(self.timeList)-1) - sel_idx)
        with open(self.histFileName, 'w') as file:
            for time in self.timeList:
                file.write(time[1]+";"+time[2]+";"+str(time[3])+";"+time[4]+"\n")
        self.plot_obj.clearPoints()
        self.makePlot()
        with open(self.histFileName, 'r') as file:
            for i,record in enumerate(file):
                split = record.split(";")
                item = QtGui.QStandardItem(str(i+1) + "\t" + split[0] + "\t\t" + split[1] + \
                                           "\t" + split[2] + "\t" + split[3][:-1])
                self.timeListModel.insertRow(0, item)
        self.calcStats()

    def calcStats(self):
        raw_timeList = [time[0] for time in self.timeList]
        if (len(raw_timeList) == 0):
            return
        bestTime = raw_timeList[0]
        worstTime = raw_timeList[0]
        for i, time in enumerate(raw_timeList):
            if (bestTime > time):
                bestTime = time
            if (worstTime < time):
                worstTime = time
        # Num of sol
        self.statNumOfSol = len(raw_timeList)
        self.statNumOfSolItem.setText(str(self.statNumOfSol))
        # Mean
        self.statMean = sum(raw_timeList)/len(raw_timeList)
        self.statMeanItem.setText(self.timeToStr(self.statMean))
        # Average
        if (len(raw_timeList) > 2):
            self.statAverage = (sum(raw_timeList) - bestTime - worstTime)/(len(raw_timeList)-2)
            self.statAverageItem.setText(self.timeToStr(self.statAverage))
        # Best
        self.statBest = bestTime
        self.statBestItem.setText(self.timeToStr(self.statBest))
        # Median
        self.statMedian = sorted(raw_timeList)[len(raw_timeList)/2]
        self.statMedianItem.setText(self.timeToStr(self.statMedian))
        # Worst
        self.statWorst = worstTime
        self.statWorstItem.setText(self.timeToStr(self.statWorst))
        # Standard Deviation
        if (len(self.timeList) > 1):
            self.statStdDev = math.sqrt(sum([(time - self.statMean)**2 for time in raw_timeList])/(len(self.timeList)-1))
            self.statStdDevItem.setText(self.timeToStr(self.statStdDev))

    def makePlot(self):
        self.plot_obj.setShowPoints(False)
        self.plot_obj.setShowLines(True)
        self.plot_obj.setShowBars(False)
        for i, time in enumerate(self.timeList):
            self.plot_obj.addPoint(float(i), float(time[0])/1000)
