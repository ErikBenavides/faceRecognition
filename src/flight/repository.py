import sqlite3
import logging


class FlightStg:
    def __init__(self):
        self.connection = sqlite3.connect("./faceRecognition.db")
        self.cursor = self.connection.cursor()

    def findAll(self):
        query = """select * from flight"""
        try:
            data = self.cursor.execute(query).fetchall()
            return data, None
        except Exception as error:
            logging.error(error)

            return None, error
        finally:
            self.connection.close()

    def findById(self, id):
        query = """select * from flight where idFlight = '{}'""".format(id)
        try:
            data = self.cursor.execute(query).fetchall()
            return data[0]
        except Exception as error:
            logging.error(error)
