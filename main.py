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

        self.ui_timer.start(51)
        self.chronoBlocked = False

    def initState(self):
        self.state = CubeTimerState()

    def initUI(self):
        self.cuTi_ui = Ui_TabWidget()
        self.cuTi_ui.setupUi(self)
        self.setWindowTitle('CubeTimer v0.00')
        self.show()

    def connectSlots(self):
        self.ui_timer.timeout.connect(self.updateUI)
        self.cuTi_ui.pB_timeDelete.clicked.connect(self.slot_timeDeleteClick)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Space:
            if self.state.chronoIsRunning:
                self.state.stopChrono()
                self.cuTi_ui.lV_times.setModel(self.state.timeListModel)
                self.updateStats()
            else:
                self.cuTi_ui.l_chronoTime.setStyleSheet('color:#00CF36')

    def keyReleaseEvent(self, e):
        if e.key() == QtCore.Qt.Key_Space:
            if not (self.chronoBlocked):
                self.state.startChrono()
                self.cuTi_ui.l_chronoTime.setStyleSheet('color:#FFFFFF')
                self.chronoBlocked = True
            else:
                self.chronoBlocked = False

    def updateUI(self):
        if (self.state.chronoIsRunning):
            self.cuTi_ui.l_chronoTime.setText(self.state.chronoToStr(True))

    def slot_timeDeleteClick(self):
        sel_idx = self.cuTi_ui.lV_times.selectedIndexes()[0].row()
        self.state.timeListModel.removeRows(sel_idx, 1)
        self.state.timeList.pop((len(self.state.timeList)-1) - sel_idx)
        # Debug for delete button
        #for i in range(len(self.state.timeList)):
        #     print("item-" + str(i) + " " + str(self.state.timeList[i]))
        #print("\n")

    def updateStats(self):
        self.cuTi_ui.tW_stats1.setItem(0,0, self.state.statMeanItem)
        self.cuTi_ui.tW_stats1.setItem(1,0, self.state.statAverageItem)
        self.cuTi_ui.tW_stats1.setItem(2,0, self.state.statBestItem)
        self.cuTi_ui.tW_stats1.setItem(3,0, self.state.statWorstItem)



def main():
    app = QtGui.QApplication(sys.argv)
    ct = CubeTimer()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
