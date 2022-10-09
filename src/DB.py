import sqlite3
import logging


class DB:
    def __init__(self):
        self.connection = sqlite3.connect("./faceRecognition.db")
        self.cursor = self.connection.cursor()

    def create(self):
        self.cursor.execute("pragma foreign_keys = on")

        self.cursor.execute(
            """create table if not exists flight (
                                                idFlight text primary key,
                                                destination text not null,
                                                dateDeparture text not null,
                                                hourDeparture text not null,
                                                price real not null,
                                                createdAt text not null
                                    ) """
        )

        self.cursor.execute(
            """create table if not exists ticket (
                                                idTicket text primary key,
                                                passengerName text not null,
                                                createdAt text not null,
                                                idFlight text not null,
                                                
                                                foreign key(idFlight) references flight(idFlight)
                                    )"""
        )

    def fillFlightTable(self):
        query = """insert into flight (
                                    idFlight,
                                    destination,
                                    dateDeparture,
                                    hourDeparture,
                                    price,
                                    createdAt
                                )  
            values ("3d60ce39-2863-4b4e-9584-526abfa6926e", "Cancún - México", "2022-11-25", "13:50",  10500.0, "2022-10-05"),
                    ("8f480c2e-6e39-44f3-887e-da3cb0eac85e", "Tijuana - México", "2022-11-20", "15:30",  8500.0, "2022-10-05" ),
                    ("182d84ea-38e2-4987-b7af-39f20d1ef992", "Londres - Inglaterra", "2022-12-03", "08:30",  28000.0, "2022-10-05" ),
                    ("ac80192c-b195-48da-b9a3-6e585a2ffb0b", "Tokio - Japón", "2022-11-20", "15:30",  8500.0, "2022-10-05" ),
                    ("0f762590-1b53-4111-8ab7-7e1940f3346d", "Guadalajara - México", "2022-12-08", "18:00",  3500.0, "2022-10-05" ),
                    ("c5fc43f3-0052-4234-864e-eaa8eb0c0cf1", "Monterrey - México", "2022-12-10", "12:00",  5500.0, "2022-10-05" ),
                    ("2e131c0f-31db-45e8-9ccc-684530be938b", "Roma - Italia", "2022-12-18", "09:00",  30000.0, "2022-10-05" )
        """

        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as error:
            logging.error(error)
            return error
        finally:
            self.connection.close()
