from dataclasses import dataclass


@dataclass
class Flight:
    idFlight: str
    destination: str
    dateDeparture: str
    hourDeparture: str
    price: str
    createdAt: str
