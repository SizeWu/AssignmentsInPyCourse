#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QDesktopWidget,  QAction, qApp, QMenu,\
    QLabel, QWidget, QLineEdit, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from API import request1


class Interface(QMainWindow):

    def __init__(self):

        super().__init__()
        self.central_widget = QWidget()             # 建一个 central widget
        self.setCentralWidget(self.central_widget)  # 设置 QMainWindow.centralWidget
        self.infor = {'city': '', 'date': 'today'}  # 建一个字典，储存查询信息
        self.datadict = {'today':                   # 见字典，接收从request1返回的天气信息
                             {'date': '', 'week': '', 'lunar': '', 'pm25': '',
                              'dawn': {'weather': '', 'temp': '', 'wind': ''},
                              'day': {'weather': '', 'temp': '', 'wind': ''},
                              'night': {'weather': '', 'temp': '', 'wind': ''}
                              },
                         'tomorrow':
                             {'date': '', 'week': '', 'lunar': '', 'pm25': '',
                              'dawn': {'weather': '', 'temp': '', 'wind': ''},
                              'day': {'weather': '', 'temp': '', 'wind': ''},
                              'night': {'weather': '', 'temp': '', 'wind': ''}
                              }
                         }
        self.appkey = "1be2cc9793f64ff4321dbb71c0a29380"     # 聚合数据申请的key
        # 创建 QLabel 和 QLineEdit的实例，在后面的display里显示
        self.city = QLabel('城市')          # 下面是要显示的内容
        self.date = QLabel('日期')
        self.week = QLabel('星期')
        self.lunar = QLabel('农历')
        self.dawn = QLabel('黎明')
        self.day = QLabel('白天')
        self.night = QLabel('夜间')
        self.weather = QLabel('天气')
        self.temp = QLabel('气温')
        self.wind = QLabel('刮风')
        self.pm25 = QLabel('PM2.5')

        self.line11 = QLineEdit()       # 数据显示在Line里面
        self.line12 = QLineEdit()
        self.line13 = QLineEdit()
        self.line14 = QLineEdit()

        self.line31 = QLineEdit()
        self.line32 = QLineEdit()
        self.line33 = QLineEdit()

        self.line41 = QLineEdit()
        self.line42 = QLineEdit()
        self.line43 = QLineEdit()
        self.line51 = QLineEdit()
        self.line52 = QLineEdit()
        self.line53 = QLineEdit()

        self.line61 = QLineEdit()
        self.line62 = QLineEdit()
        self.line63 = QLineEdit()

        self.initUI()

    def initUI(self):

        # 下面的注释是学的时候写的，都是英文，后面为了说清楚，就写中文了
        # Initialize the status bar with 'Ready'
        self.statusBar().showMessage('Ready')

        # Create a menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&选项')    # Name it as 'Selection'

        # Set an action in the menu bar that can exit the window
        exitAct = QAction(QIcon('exit.jpg'), '&退出', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('退出界面')
        exitAct.triggered.connect(qApp.quit)  # Represent tips on the status bar
        fileMenu.addAction(exitAct)   # Add the action

        eAct = QAction('展示', self)
        eAct.triggered.connect(self.display)  # Represent tips on the status bar
        fileMenu.addAction(eAct)   # Add the action

        # Set an submenu in the menu bar that provides choice of areas in China
        areaMenu = QMenu('城市', self)
        areaAct1 = QAction('重庆', self)
        areaAct1.setStatusTip('重庆的天气')
        areaAct1.triggered.connect(self.setChongqing)

        areaAct2= QAction('合肥', self)
        areaAct2.setStatusTip('合肥的天气')
        areaAct2.triggered.connect(self.setHefei)

        areaAct3= QAction('北京', self)
        areaAct3.setStatusTip('北京的天气')   # Tips are also represented
        areaAct3.triggered.connect(self.setBeijing)

        areaAct4= QAction('更新城市', self)
        areaAct4.setStatusTip('输入后，点击更新城市')   # Tips are also represented
        areaAct4.triggered.connect(self.updateCity)

        # Add the actions
        areaMenu.addAction(areaAct1)
        areaMenu.addAction(areaAct2)
        areaMenu.addAction(areaAct3)
        # Add the submenu to menu bar
        fileMenu.addMenu(areaMenu)

        # Set an submenu that provides choice of today or tomorrow
        dateMenu = QMenu('日期', self)
        dateAct1 = QAction('今天', self)
        dateAct1.triggered.connect(self.settoday)
        dateAct1.setStatusTip('今天的天气')
        dateAct2 = QAction('明天', self)
        dateAct2.triggered.connect(self.settomorrow)
        dateAct2.setStatusTip('明天的天气')  # Tips are also represented

        # Add the actions
        dateMenu.addAction(dateAct1)
        dateMenu.addAction(dateAct2)
        # Add the submenu to menu bar
        fileMenu.addMenu(dateMenu)

        # Set a toolbar
        self.toolbar = self.addToolBar('退出')
        self.toolbar.addAction(exitAct)
        self.toolbar = self.addToolBar('今天')
        self.toolbar.addAction(dateAct1)
        self.toolbar = self.addToolBar('明天')
        self.toolbar.addAction(dateAct2)
        self.toolbar = self.addToolBar('重庆')
        self.toolbar.addAction(areaAct1)
        self.toolbar = self.addToolBar('合肥')
        self.toolbar.addAction(areaAct2)
        self.toolbar = self.addToolBar('北京')
        self.toolbar.addAction(areaAct3)
        self.toolbar = self.addToolBar('更新城市')
        self.toolbar.addAction(areaAct4)

        self.display()

        # Initialize the window
        self.resize(600, 300)     # Size
        self.setWindowTitle('国内天气')
        self.show()
        self.center()      # Center the window on the screen

    # Define the exit function
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # Define the center function
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Set a context menu event
    def contextMenuEvent(self, event):
        cmenu = QMenu(self)
        updateAct = cmenu.addAction("Update")
        quitAct = cmenu.addAction("Quit")
        showAct = cmenu.addAction('data')
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAct:
            qApp.quit()
        if action == updateAct:
            self.update()
        if action == showAct:
            self.display()

    # 按Ese可退出
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    # 更新天气数据
    def updatedata(self):
        self.datadict = request1(self.appkey, 'GET', self.infor['city'])
        print(self.datadict[self.infor['date']])
        print(self.datadict[self.infor['date']]['dawn']['weather'])

    # 今天 or 明天
    def settoday(self):
        self.infor['date'] = 'today'
        self.display()

    def settomorrow(self):
        self.infor['date'] = 'tomorrow'
        self.display()

    # 选择城市
    def setChongqing(self):
        self.infor['city'] = '重庆'
        self.updatedata()
        self.display()

    def setHefei(self):
        self.infor['city'] = '合肥'
        self.updatedata()
        self.display()

    def setBeijing(self):
        self.infor['city'] = '北京'
        self.updatedata()
        self.display()

    def updateCity(self):
        self.infor['city'] = self.line11.displayText()
        self.updatedata()
        self.display()

    # 显示内容
    def display(self):
        # Labels and lines
        # 设置 line 里的文字内容
        self.line11.setText(self.infor['city'])
        self.line12.setText(self.datadict[self.infor['date']]['date'])
        if self.infor['date'] == 'today':
            self.line13.setText(self.datadict[self.infor['date']]['week']+' 今天')
        else:
            self.line13.setText(self.datadict[self.infor['date']]['week']+' 明天')
        self.line14.setText(self.datadict[self.infor['date']]['lunar'])
        self.line31.setText(self.datadict[self.infor['date']]['dawn']['weather'])
        self.line32.setText(self.datadict[self.infor['date']]['day']['weather'])
        self.line33.setText(self.datadict[self.infor['date']]['night']['weather'])

        self.line41.setText(self.datadict[self.infor['date']]['dawn']['temp'])
        self.line42.setText(self.datadict[self.infor['date']]['day']['temp'])
        self.line43.setText(self.datadict[self.infor['date']]['night']['temp'])

        self.line51.setText(self.datadict[self.infor['date']]['dawn']['wind'])
        self.line52.setText(self.datadict[self.infor['date']]['day']['wind'])
        self.line53.setText(self.datadict[self.infor['date']]['night']['wind'])
        print(self.line53.displayText())

        self.line61.setText(self.datadict[self.infor['date']]['pm25'])
        self.line62.setText(self.datadict[self.infor['date']]['pm25'])
        self.line63.setText(self.datadict[self.infor['date']]['pm25'])

        grid = QGridLayout()
        self.centralWidget().setLayout(grid)
        grid.setSpacing(15)

        # 设置位置
        grid.addWidget(self.city, 1, 1)
        grid.addWidget(self.date, 1, 3)
        grid.addWidget(self.week, 1, 5)
        grid.addWidget(self.lunar, 1, 7)

        grid.addWidget(self.dawn, 2, 2)
        grid.addWidget(self.day, 2, 4)
        grid.addWidget(self.night, 2, 6)

        grid.addWidget(self.weather, 3, 1)
        grid.addWidget(self.temp, 4, 1)
        grid.addWidget(self.wind, 5, 1)
        grid.addWidget(self.pm25, 6, 1)

        grid.addWidget(self.line11, 1, 2)
        grid.addWidget(self.line12, 1, 4)
        grid.addWidget(self.line13, 1, 6)
        grid.addWidget(self.line14, 1, 8)
        grid.addWidget(self.line31, 3, 2)
        grid.addWidget(self.line32, 3, 4)
        grid.addWidget(self.line33, 3, 6)
        grid.addWidget(self.line41, 4, 2)
        grid.addWidget(self.line42, 4, 4)
        grid.addWidget(self.line43, 4, 6)
        grid.addWidget(self.line51, 5, 2)
        grid.addWidget(self.line52, 5, 4)
        grid.addWidget(self.line53, 5, 6)
        grid.addWidget(self.line61, 6, 2)
        grid.addWidget(self.line62, 6, 4)
        grid.addWidget(self.line63, 6, 6)

        self.setLayout(grid)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Interface()
    sys.exit(app.exec_())
