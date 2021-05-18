import cv2
import sys
from json import loads
from common import device
from client import sendImg
from plateDraw import drawRectBox
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        self.CAM_NUM = 0
        self.__initCamera()
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.flagTimer = False

    def initSlot(self):
        self.timer_camera.timeout.connect(self.show_camera)
        self.pushButton.clicked.connect(self.toggle_timer)

    def __initCamera(self):
        # init camera
        self.cap = cv2.VideoCapture(self.CAM_NUM) #打开内置摄像头

        frameWidth, frameHeight = 640, 480

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)

    def toggle_timer(self):
        if not self.flagTimer:
            flag = self.cap.open(self.CAM_NUM)
            if not flag:
                raise Exception("No Camera!")
            else:
                self.flagTimer = True
                self.timer_camera.start(40)
                self.pushButton.setText("停止识别")
        else:
            self.flagTimer = False
            self.timer_camera.stop()
            self.pushButton.setText("开始识别")

    def show_camera(self):
        _, frame = self.cap.read()
        res = loads(sendImg(device['win-forward'], frame))

        if any(res['res']):
            frame = drawRectBox(frame, res['rect'], res['con'], res['res'])

        show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.camera.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(920, 520)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.camera = QtWidgets.QLabel(self.centralwidget)
        self.camera.setEnabled(True)
        self.camera.setGeometry(QtCore.QRect(20, 20, 640, 480))
        self.camera.setMouseTracking(False)
        self.camera.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.camera.setFrameShape(QtWidgets.QFrame.Box)
        self.camera.setFrameShadow(QtWidgets.QFrame.Plain)
        self.camera.setLineWidth(1)
        self.camera.setScaledContents(True)
        self.camera.setAlignment(QtCore.Qt.AlignCenter)
        self.camera.setIndent(0)
        self.camera.setObjectName("camera")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(670, 80, 240, 421))
        self.tableWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.NoPen)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(115)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(115)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setDefaultSectionSize(19)
        self.tableWidget.verticalHeader().setMinimumSectionSize(19)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(670, 20, 240, 45))
        self.pushButton.setStyleSheet("font: 12pt \"等线\";")
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "车牌识别"))
        self.camera.setText(_translate("MainWindow", "camera"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "时间"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "车牌号"))
        self.pushButton.setText(_translate("MainWindow", "获取车牌"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.initSlot()

    MainWindow.show()
    sys.exit(app.exec_())
