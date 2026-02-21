"""Las reservaciones para el sistema."""

import json
import os
from hotel import Hotel

RESERVATIONS_FILE = "reservations.json"


def load_reservations():
    """Cargar reservaciones desde archivo JSON."""
    if not os.path.exists(RESERVATIONS_FILE):
        return {}
    try:
        with open(RESERVATIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error al cargar el archivo de reservaciones: {e}")
        return {}


def save_reservations(reservations):
    """Guardar reservaciones en archivo JSON."""
    try:
        with open(RESERVATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(reservations, f, indent=4)
    except IOError as e:
        print(f"Error al guardar el archivo de reservaciones: {e}")


class Reservation:
    """Reservación que vincula un cliente a un hotel."""

    def __init__(self, reservation_id, customer_id, hotel_id,
                 check_in, check_out):
        self.reservation_id = str(reservation_id)
        self.customer_id = str(customer_id)
        self.hotel_id = str(hotel_id)
        self.check_in = check_in
        self.check_out = check_out

    def to_dict(self):
        """Conviertimos la reservación a diccionario."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
            "check_in": self.check_in,
            "check_out": self.check_out,
        }

    @staticmethod
    def from_dict(data):
        """CreamosS una Reservación desde un diccionario."""
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
        """Crear y guardar una nueva reservación."""
        reservations = load_reservations()
        reservation_id = str(reservation_id)
        if reservation_id in reservations:
            print(f"La reservación {reservation_id} ya existe.")
            return None
        success = Hotel.reserve_room(hotel_id, reservation_id, customer_id)
        if not success:
            print("No se pudo crear la reservación: habitación no disponible o hotel no encontrado.")
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
        """Cancelar una reservación."""
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
        """Mostrar información de la reservación."""
        reservations = load_reservations()
        reservation_id = str(reservation_id)
        if reservation_id not in reservations:
            print(f"Reservación {reservation_id} no encontrada.")
            return None
        res = Reservation.from_dict(reservations[reservation_id])
        print(f"--- Información de la Reservación ---")
        print(f"ID           : {res.reservation_id}")
        print(f"ID Cliente   : {res.customer_id}")
        print(f"ID Hotel     : {res.hotel_id}")
        print(f"Entrada      : {res.check_in}")
        print(f"Salida       : {res.check_out}")
        return res