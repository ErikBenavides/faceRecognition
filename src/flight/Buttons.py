from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class Buttons:
    def buyButton(self):
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buyBtn = QtWidgets.QPushButton()
        self.buyBtn.setObjectName("buyBtn")
        self.buyBtn.setFont(font)
        self.buyBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.buyBtn.setStyleSheet(
            "QPushButton{\n"
            "	background-color: rgb(52, 142, 148);\n"
            "	padding: 4px;\n"
            "   color: #fff;\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "	background-color: rgb(45, 121, 126);\n"
            "	color: rgb(255, 255, 255);\n"
            "	cursor: pointer;\n"
            "}"
        )
        self.buyBtn.setText("Comprar")
        self.buyBtn.setFlat(False)
        self.buyBtn.setDefault(False)

        return self.buyBtn
