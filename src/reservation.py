"""Manejo de reservaciones del sistema."""

import json
import os
from hotel import Hotel

RESERVATIONS_FILE = "reservations.json"


def load_reservations():
    """Lee las reservaciones guardadas en el archivo."""
    if not os.path.exists(RESERVATIONS_FILE):
        return {}
    try:
        with open(RESERVATIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error al cargar el archivo de reservaciones: {e}")
        return {}


def save_reservations(reservations):
    """Escribe las reservaciones en el archivo."""
    try:
        with open(RESERVATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(reservations, f, indent=4)
    except IOError as e:
        print(f"Error al guardar el archivo de reservaciones: {e}")


class Reservation:
    """Une a un cliente con un hotel en fechas específicas."""

    def __init__(  # pylint: disable=too-many-arguments,too-many-positional-arguments
            self, reservation_id, customer_id, hotel_id, check_in, check_out):
        """Datos de la reservación: quién, dónde y cuándo."""
        self.reservation_id = str(reservation_id)
        self.customer_id = str(customer_id)
        self.hotel_id = str(hotel_id)
        self.check_in = check_in
        self.check_out = check_out

    def to_dict(self):
        """Regresa los datos de la reservación como diccionario."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
            "check_in": self.check_in,
            "check_out": self.check_out,
        }

    @staticmethod
    def from_dict(data):
        """Arma una Reservation a partir de un diccionario."""
        return Reservation(
            data["reservation_id"],
            data["customer_id"],
            data["hotel_id"],
            data["check_in"],
            data["check_out"],
        )

    @staticmethod
    def create_reservation(reservation_id, customer_id, hotel_id,
                           check_in, check_out):
        """Registra una reservación nueva y ocupa la habitación en el hotel."""
        reservations = load_reservations()
        reservation_id = str(reservation_id)
        if reservation_id in reservations:
            print(f"La reservación {reservation_id} ya existe.")
            return None
        success = Hotel.reserve_room(hotel_id, reservation_id, customer_id)
        if not success:
            print(
                "No se pudo crear la reservación: "
                "habitación no disponible o hotel no encontrado."
            )
            return None
        reservation = Reservation(
            reservation_id, customer_id, hotel_id, check_in, check_out
        )
        reservations[reservation_id] = reservation.to_dict()
        save_reservations(reservations)
        print(f"Reservación {reservation_id} creada correctamente.")
        return reservation

    @staticmethod
    def cancel_reservation(reservation_id):
        """Cancela la reservación y libera la habitación."""
        reservations = load_reservations()
        reservation_id = str(reservation_id)
        if reservation_id not in reservations:
            print(f"Reservación {reservation_id} no encontrada.")
            return False
        res = Reservation.from_dict(reservations[reservation_id])
        Hotel.cancel_room_reservation(res.hotel_id, reservation_id)
        del reservations[reservation_id]
        save_reservations(reservations)
        print(f"Reservación {reservation_id} cancelada correctamente.")
        return True

    @staticmethod
    def display_reservation(reservation_id):
        """Imprime los datos de la reservación en consola."""
        reservations = load_reservations()
        reservation_id = str(reservation_id)
        if reservation_id not in reservations:
            print(f"Reservación {reservation_id} no encontrada.")
            return None
        res = Reservation.from_dict(reservations[reservation_id])
        print("--- Información de la Reservación ---")
        print(f"ID           : {res.reservation_id}")
        print(f"ID Cliente   : {res.customer_id}")
        print(f"ID Hotel     : {res.hotel_id}")
        print(f"Entrada      : {res.check_in}")
        print(f"Salida       : {res.check_out}")
        return res
