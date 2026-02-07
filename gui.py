# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QHeaderView, QLayout, QMainWindow, QMenuBar,
    QPushButton, QRadioButton, QSizePolicy, QStatusBar,
    QTableView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(451, 723)
        icon = QIcon()
        icon.addFile(u"icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_9 = QGridLayout(self.centralwidget)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.groupBoxOrigin = QGroupBox(self.centralwidget)
        self.groupBoxOrigin.setObjectName(u"groupBoxOrigin")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxOrigin.sizePolicy().hasHeightForWidth())
        self.groupBoxOrigin.setSizePolicy(sizePolicy)
        self.groupBoxOrigin.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.gridLayout = QGridLayout(self.groupBoxOrigin)
        self.gridLayout.setObjectName(u"gridLayout")
        self.radioDrillOrigin = QRadioButton(self.groupBoxOrigin)
        self.radioDrillOrigin.setObjectName(u"radioDrillOrigin")

        self.gridLayout.addWidget(self.radioDrillOrigin, 0, 1, 1, 1)

        self.radioGridOrigin = QRadioButton(self.groupBoxOrigin)
        self.radioGridOrigin.setObjectName(u"radioGridOrigin")
        self.radioGridOrigin.setChecked(True)

        self.gridLayout.addWidget(self.radioGridOrigin, 0, 0, 1, 1)

        self.radioPageOrigin = QRadioButton(self.groupBoxOrigin)
        self.radioPageOrigin.setObjectName(u"radioPageOrigin")

        self.gridLayout.addWidget(self.radioPageOrigin, 0, 2, 1, 1)


        self.gridLayout_8.addWidget(self.groupBoxOrigin, 0, 0, 1, 1)

        self.groupBoxXAxis = QGroupBox(self.centralwidget)
        self.groupBoxXAxis.setObjectName(u"groupBoxXAxis")
        self.gridLayout_2 = QGridLayout(self.groupBoxXAxis)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.radioIncreasesRight = QRadioButton(self.groupBoxXAxis)
        self.radioIncreasesRight.setObjectName(u"radioIncreasesRight")
        self.radioIncreasesRight.setChecked(True)

        self.gridLayout_2.addWidget(self.radioIncreasesRight, 0, 0, 1, 1)

        self.radioIncreasesLeft = QRadioButton(self.groupBoxXAxis)
        self.radioIncreasesLeft.setObjectName(u"radioIncreasesLeft")

        self.gridLayout_2.addWidget(self.radioIncreasesLeft, 0, 1, 1, 1)


        self.gridLayout_8.addWidget(self.groupBoxXAxis, 1, 0, 1, 1)

        self.groupBoxYAxis = QGroupBox(self.centralwidget)
        self.groupBoxYAxis.setObjectName(u"groupBoxYAxis")
        self.gridLayout_3 = QGridLayout(self.groupBoxYAxis)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.radioIncreasesUp = QRadioButton(self.groupBoxYAxis)
        self.radioIncreasesUp.setObjectName(u"radioIncreasesUp")
        self.radioIncreasesUp.setChecked(True)

        self.gridLayout_3.addWidget(self.radioIncreasesUp, 0, 0, 1, 1)

        self.radioIncreasesDown = QRadioButton(self.groupBoxYAxis)
        self.radioIncreasesDown.setObjectName(u"radioIncreasesDown")

        self.gridLayout_3.addWidget(self.radioIncreasesDown, 0, 1, 1, 1)


        self.gridLayout_8.addWidget(self.groupBoxYAxis, 2, 0, 1, 1)

        self.groupBoxDNP = QGroupBox(self.centralwidget)
        self.groupBoxDNP.setObjectName(u"groupBoxDNP")
        self.gridLayout_4 = QGridLayout(self.groupBoxDNP)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.checkDNP = QCheckBox(self.groupBoxDNP)
        self.checkDNP.setObjectName(u"checkDNP")

        self.gridLayout_4.addWidget(self.checkDNP, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.groupBoxDNP, 3, 0, 1, 1)

        self.groupBoxCustom = QGroupBox(self.centralwidget)
        self.groupBoxCustom.setObjectName(u"groupBoxCustom")
        self.gridLayout_5 = QGridLayout(self.groupBoxCustom)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.tableView = QTableView(self.groupBoxCustom)
        self.tableView.setObjectName(u"tableView")

        self.gridLayout_5.addWidget(self.tableView, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.groupBoxCustom, 4, 0, 1, 1)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.btnExport = QPushButton(self.centralwidget)
        self.btnExport.setObjectName(u"btnExport")

        self.gridLayout_6.addWidget(self.btnExport, 0, 0, 1, 1)

        self.btnClose = QPushButton(self.centralwidget)
        self.btnClose.setObjectName(u"btnClose")

        self.gridLayout_6.addWidget(self.btnClose, 0, 1, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_6, 5, 0, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_8, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 451, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Component Position", None))
        self.groupBoxOrigin.setTitle(QCoreApplication.translate("MainWindow", u"Origin:", None))
        self.radioDrillOrigin.setText(QCoreApplication.translate("MainWindow", u"Drill Origin", None))
        self.radioGridOrigin.setText(QCoreApplication.translate("MainWindow", u"Grid Origin", None))
        self.radioPageOrigin.setText(QCoreApplication.translate("MainWindow", u"Page Origin", None))
        self.groupBoxXAxis.setTitle(QCoreApplication.translate("MainWindow", u"X Axis:", None))
        self.radioIncreasesRight.setText(QCoreApplication.translate("MainWindow", u"Increases right", None))
        self.radioIncreasesLeft.setText(QCoreApplication.translate("MainWindow", u"Increases left", None))
        self.groupBoxYAxis.setTitle(QCoreApplication.translate("MainWindow", u"Y Axis:", None))
        self.radioIncreasesUp.setText(QCoreApplication.translate("MainWindow", u"Increases up", None))
        self.radioIncreasesDown.setText(QCoreApplication.translate("MainWindow", u"Increases down", None))
        self.groupBoxDNP.setTitle(QCoreApplication.translate("MainWindow", u"Remove Components with DNP:", None))
        self.checkDNP.setText(QCoreApplication.translate("MainWindow", u"Components with this field not empty will be ignored", None))
        self.groupBoxCustom.setTitle(QCoreApplication.translate("MainWindow", u"Add custom fields:", None))
        self.btnExport.setText(QCoreApplication.translate("MainWindow", u"Export to CSV", None))
        self.btnClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
    # retranslateUi

