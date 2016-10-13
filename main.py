from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
from cubetimer import Ui_TabWidget
from state import CubeTimerState

class CubeTimer(QtGui.QTabWidget):
    def __init__(self):
        super(CubeTimer,self).__init__()
        self.initState()
        self.initUI()

        self.ui_timer = QtCore.QTimer()

        self.connectSlots()
        self.connectModels()

        self.ui_timer.start(51)
        self.chronoBlocked = False

    def initState(self):
        self.state = CubeTimerState()

    def initUI(self):
        self.cuTi_ui = Ui_TabWidget()
        self.cuTi_ui.setupUi(self)
        self.cuTi_ui.l_scramble.setText(self.state.scramble.scramble)
        self.setWindowTitle('CubeTimer v0.00')
        self.show()

    def connectSlots(self):
        self.ui_timer.timeout.connect(self.updateUI)
        self.cuTi_ui.pB_timeDelete.clicked.connect(self.slot_timeDeleteClick)

    def connectModels(self):
        self.cuTi_ui.lV_history.setModel(self.state.history.timeListModel)
        self.cuTi_ui.lV_times.setModel(self.state.timeListModel)

        self.cuTi_ui.tW_stats1.setItem(0,0, self.state.statMeanItem)
        self.cuTi_ui.tW_stats1.setItem(1,0, self.state.statAverageItem)
        self.cuTi_ui.tW_stats1.setItem(2,0, self.state.statBestItem)
        self.cuTi_ui.tW_stats1.setItem(3,0, self.state.statMedianItem)
        self.cuTi_ui.tW_stats1.setItem(4,0, self.state.statWorstItem)
        self.cuTi_ui.tW_stats1.setItem(5,0, self.state.statStdDevItem)

        self.cuTi_ui.tW_stats2.setItem(0,0, self.state.statMo3Item)
        self.cuTi_ui.tW_stats2.setItem(1,0, self.state.statBestMo3Item)
        self.cuTi_ui.tW_stats2.setItem(2,0, self.state.statAo5Item)
        self.cuTi_ui.tW_stats2.setItem(3,0, self.state.statBestAo5Item)
        self.cuTi_ui.tW_stats2.setItem(4,0, self.state.statAo12Item)
        self.cuTi_ui.tW_stats2.setItem(5,0, self.state.statBestAo12Item)

    def keyPressEvent(self, e):
        if e.isAutoRepeat():
            e.ignore()
        elif e.key() == QtCore.Qt.Key_Space:
            if self.state.chronoIsRunning:
                self.state.stopChrono()
                self.updateTime(live=False)
                self.cuTi_ui.l_scramble.setText(self.state.scramble.getNewScramble())
            else:
                self.cuTi_ui.l_chronoTime.setStyleSheet('color:#00CF36')

    def keyReleaseEvent(self, e):
        if e.isAutoRepeat():
            e.ignore()
        elif e.key() == QtCore.Qt.Key_Space:
            if not (self.chronoBlocked):
                self.state.startChrono()
                self.cuTi_ui.l_chronoTime.setStyleSheet('color:#FFFFFF')
                self.chronoBlocked = True
            else:
                self.chronoBlocked = False

    def updateUI(self):
        if (self.state.chronoIsRunning):
            self.updateTime(live=True)

    def updateTime(self, live=False):
        self.cuTi_ui.l_chronoTime.setText(self.state.chronoToStr(live))
        if (self.state.statMean != 0):
            cur_perc = 100*float(self.state.chronoTime)/float(self.state.statMean)
            if (cur_perc > 200):
                self.cuTi_ui.pBar_mean.setValue(100)
                self.cuTi_ui.pBar_overtime.setValue(100)
            elif (cur_perc > 100):
                self.cuTi_ui.pBar_mean.setValue(100)
                self.cuTi_ui.pBar_overtime.setValue(cur_perc-100)
            else:
                self.cuTi_ui.pBar_mean.setValue(cur_perc)
                self.cuTi_ui.pBar_overtime.setValue(0)

    def slot_timeDeleteClick(self):
        sel_idx = self.cuTi_ui.lV_times.selectedIndexes()[0].row()
        self.state.timeListModel.removeRows(sel_idx, 1)
        self.state.timeList.pop((len(self.state.timeList)-1) - sel_idx)
        # Debug for delete button
        #for i in range(len(self.state.timeList)):
        #     print("item-" + str(i) + " " + str(self.state.timeList[i]))
        #print("\n")



def main():
    app = QtGui.QApplication(sys.argv)
    ct = CubeTimer()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
