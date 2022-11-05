import sqlite3
import logging
from datetime import datetime
import uuid


class TicketStg:
    def __init__(self):
        self.connection = sqlite3.connect("./faceRecognition.db")
        self.cursor = self.connection.cursor()

    def findAll(self):
        query = """select * from ticket"""
        try:
            data = self.cursor.execute(query).fetchall()
            return data, None
        except Exception as error:
            logging.error(error)

            return None, error
        finally:
            self.connection.close()

    def findByName(self, passengerName):
        query = """select * from ticket where passengerName = '{}'""".format(
            passengerName
        )
        try:
            data = self.cursor.execute(query).fetchall()
            return data[0]
        except Exception as error:
            logging.error(error)

    def insert(self, passengerName, ticket):
        now = datetime.now()
        createdAt = now.strftime("%Y-%m-%d")

        query = """insert into ticket (idTicket, passengerName, createdAt, idFlight)
								values('{}', '{}', '{}', '{}')""".format(
            str(uuid.uuid4()), passengerName, createdAt, ticket[0]
        )
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as error:
            return error
        finally:
            self.connection.close()
