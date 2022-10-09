from dataclasses import dataclass


@dataclass
class Ticket:
    idTicket: str
    passengerName: str
    createdAt: str
    idFlight: str
