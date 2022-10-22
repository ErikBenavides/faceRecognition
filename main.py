import sys
from src.DB import *
from src.flight.ui_main_window import *
from src.flight.repository import *
from src.flight.Buttons import *

from src.ticket.ui_buy_ticket_window import *


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

    def updateFlightTable(self):
        flightStg = FlightStg()
        data, error = flightStg.findAll()
        print(data)
        if error is not None:
            # QMessageBox.critical(self, Lang.appName, str(error))

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
        self.window = QtWidgets.QMainWindow()
        self.uiBuyTicket = Ui_buyTicketWindow()
        self.uiBuyTicket.setupUi(self.window)
        self.window.show()

        self.uiBuyTicket.finishBuyBtn.clicked.connect(self.finishBooked)

    def finishBooked(self):
        name = self.uiBuyTicket.nameTxt.text()
        print(name)


if __name__ == "__main__":
    print("face recognition")
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
