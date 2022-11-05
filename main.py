import sys
import logging

from PyQt5.QtWidgets import QMessageBox
from src.DB import *
from src.Lang import Lang
from src.flight.ui_main_window import *
from src.flight.repository import *
from src.flight.Buttons import *

from src.ticket.ui_buy_ticket_window import *
from src.ticket.repository import *

from detection.main import *
import faceRecognition
from pydispatch import dispatcher

logging.basicConfig(level=logging.INFO)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.uiMain = Ui_mainWindow()
        self.uiMain.setupUi(self)

        # crea la base de datos y los muestra en la tabla
        db = DB()
        db.create()
        db.fillFlightTable()
        self.updateFlightTable()
        self.clearPassengerData()
        dispatcher.connect(
            self.listenFaceRecognition,
            sender=faceRecognition.MyNode,
            signal=faceRecognition.metaKey,
        )
        self.uiMain.identifyYourselfBtn.clicked.connect(self.openFaceRecognition)

    def updateFlightTable(self):
        flightStg = FlightStg()
        data, error = flightStg.findAll()
        if error is not None:
            QMessageBox.critical(self, Lang.appName, str(error))
            return

        self.uiMain.flightTable.setRowCount(len(data))
        self.uiMain.flightTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        tableRow = 0
        for row in data:
            # agrega los valores de la base de datos en la tabla
            self.uiMain.flightTable.setItem(
                tableRow, 0, QtWidgets.QTableWidgetItem(row[1])
            )
            self.uiMain.flightTable.setItem(
                tableRow, 1, QtWidgets.QTableWidgetItem(row[2])
            )
            self.uiMain.flightTable.setItem(
                tableRow, 2, QtWidgets.QTableWidgetItem(row[3])
            )
            self.uiMain.flightTable.setItem(
                tableRow, 3, QtWidgets.QTableWidgetItem(str(row[4]))
            )

            # agrega los botones a la tabla
            buttons = Buttons()
            buyButton = buttons.buyButton()
            self.uiMain.flightTable.setCellWidget(tableRow, 4, buyButton)

            buyButton.clicked.connect(self.opeBuyTicketWindow)

            tableRow += 1

    def opeBuyTicketWindow(self):
        button = QtWidgets.QApplication.focusWidget()
        index = self.uiMain.flightTable.indexAt(button.pos())
        if index.isValid():
            flightStg = FlightStg()
            flights, error = flightStg.findAll()

            if error:
                logging.critical(str(error))
                return

            self.window = QtWidgets.QMainWindow()
            self.uiBuyTicket = Ui_buyTicketWindow()
            self.uiBuyTicket.setupUi(self.window)
            self.window.show()

            self.uiBuyTicket.bookFlightBtn.clicked.connect(self.openFaceDetectionWindow)
            self.uiBuyTicket.finishBuyBtn.clicked.connect(
                lambda: self.finishBooked(flights[index.row()])
            )

    def openFaceDetectionWindow(
        self,
    ):
        name = self.uiBuyTicket.nameTxt.text()
        if name == "":
            QMessageBox.critical(self, Lang.appName, Lang.nameRequired)
            return
        runFaceDetection(name)

    def finishBooked(self, flight):
        name = self.uiBuyTicket.nameTxt.text()
        ticketStg = TicketStg()
        error = ticketStg.insert(name, flight)

        if error:
            logging.critical(str(error))
            QMessageBox.critical(self, Lang.appName, Lang.failSave)
            return
        QMessageBox.information(self, Lang.appName, Lang.successfulSave)
        self.window.close()

    def openFaceRecognition(
        self,
    ):
        print("abriendo reconocimiento")
        faceRecognition.detectFace()

    def clearPassengerData(
        self,
    ):
        self.uiMain.destinationLbl.setText("")
        self.uiMain.dateDepartureLbl.setText("")
        self.uiMain.hourDepartureLbl.setText("")
        self.uiMain.nameLbl.setText("")
        self.uiMain.priceLbl.setText("")

    def listenFaceRecognition(self, event=None):
        print("evento recibido")

        if event != None:
            ticket = event["ticket"]
            flight = event["flight"]
            self.uiMain.nameLbl.setText(ticket[1])
            self.uiMain.destinationLbl.setText(flight[1])
            self.uiMain.dateDepartureLbl.setText(flight[2])
            self.uiMain.hourDepartureLbl.setText(flight[3])
            self.uiMain.priceLbl.setText(str(flight[4]))
        else:
            self.clearPassengerData()


if __name__ == "__main__":
    logging.info(Lang.runningApp + Lang.appName)
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

# self.flightTable.horizontalHeader().setSectionResizeMode(1)
