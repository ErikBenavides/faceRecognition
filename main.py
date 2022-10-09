import sys
from src.DB import *
from src.flight.ui_main_window import *
from src.flight.repository import *


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

            tableRow += 1


if __name__ == "__main__":
    print("face recognition")
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
