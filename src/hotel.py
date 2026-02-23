"""Manejo de hoteles para el sistema de reservaciones."""

import json
import os

HOTELS_FILE = "hotels.json"


def load_hotels():
    """Lee los hoteles guardados en el archivo."""
    if not os.path.exists(HOTELS_FILE):
        return {}
    try:
        with open(HOTELS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error al cargar el archivo de hoteles: {e}")
        return {}


def save_hotels(hotels):
    """Escribe los hoteles en el archivo."""
    try:
        with open(HOTELS_FILE, "w", encoding="utf-8") as f:
            json.dump(hotels, f, indent=4)
    except IOError as e:
        print(f"Error al guardar el archivo de hoteles: {e}")


class Hotel:
    """Un hotel con sus habitaciones y reservaciones."""

    def __init__(self, hotel_id, name, location, total_rooms):
        """Datos básicos del hotel. Requiere al menos una habitación."""
        if not isinstance(total_rooms, int) or total_rooms <= 0:
            raise ValueError("total_rooms must be a positive integer.")
        self.hotel_id = str(hotel_id)
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.reservations = {}

    def to_dict(self):
        """Regresa los datos del hotel como diccionario."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
            "reservations": self.reservations,
        }

    @staticmethod
    def from_dict(data):
        """Arma un Hotel a partir de un diccionario."""
        hotel = Hotel(
            data["hotel_id"],
            data["name"],
            data["location"],
            data["total_rooms"],
        )
        hotel.reservations = data.get("reservations", {})
        return hotel

    def available_rooms(self):
        """Cuántas habitaciones quedan libres."""
        return self.total_rooms - len(self.reservations)

    @staticmethod
    def create_hotel(hotel_id, name, location, total_rooms):
        """Agrega un hotel nuevo al sistema."""
        hotels = load_hotels()
        hotel_id = str(hotel_id)
        if hotel_id in hotels:
            print(f"El hotel con ID {hotel_id} ya existe.")
            return None
        hotel = Hotel(hotel_id, name, location, total_rooms)
        hotels[hotel_id] = hotel.to_dict()
        save_hotels(hotels)
        print(f"Hotel '{name}' creado correctamente.")
        return hotel

    @staticmethod
    def delete_hotel(hotel_id):
        """Borra un hotel del sistema."""
        hotels = load_hotels()
        hotel_id = str(hotel_id)
        if hotel_id not in hotels:
            print(f"Hotel con ID {hotel_id} no encontrado.")
            return False
        del hotels[hotel_id]
        save_hotels(hotels)
        print(f"Hotel {hotel_id} eliminado correctamente.")
        return True

    @staticmethod
    def display_hotel(hotel_id):
        """Imprime los datos del hotel en consola."""
        hotels = load_hotels()
        hotel_id = str(hotel_id)
        if hotel_id not in hotels:
            print(f"Hotel con ID {hotel_id} no encontrado.")
            return None
        hotel = Hotel.from_dict(hotels[hotel_id])
        print("--- Información del Hotel ---")
        print(f"ID        : {hotel.hotel_id}")
        print(f"Nombre    : {hotel.name}")
        print(f"Ubicación : {hotel.location}")
        print(
            f"Habitaciones: {hotel.total_rooms} total, "
            f"{hotel.available_rooms()} disponibles"
        )
        return hotel

    @staticmethod
    def modify_hotel(hotel_id, name=None, location=None, total_rooms=None):
        """Actualiza los campos del hotel que se quieran cambiar."""
        hotels = load_hotels()
        hotel_id = str(hotel_id)
        if hotel_id not in hotels:
            print(f"Hotel con ID {hotel_id} no encontrado.")
            return False
        if name:
            hotels[hotel_id]["name"] = name
        if location:
            hotels[hotel_id]["location"] = location
        if total_rooms is not None:
            if not isinstance(total_rooms, int) or total_rooms <= 0:
                print("Valor de habitaciones inválido.")
                return False
            hotels[hotel_id]["total_rooms"] = total_rooms
        save_hotels(hotels)
        print(f"Hotel {hotel_id} modificado correctamente.")
        return True

    @staticmethod
    def reserve_room(hotel_id, reservation_id, customer_id):
        """Ocupa una habitación del hotel con la reservación dada."""
        hotels = load_hotels()
        hotel_id = str(hotel_id)
        if hotel_id not in hotels:
            print(f"Hotel con ID {hotel_id} no encontrado.")
            return False
        hotel = Hotel.from_dict(hotels[hotel_id])
        if hotel.available_rooms() <= 0:
            print(f"No hay habitaciones disponibles en el hotel {hotel_id}.")
            return False
        reservation_id = str(reservation_id)
        if reservation_id in hotel.reservations:
            print(f"La reservación {reservation_id} ya existe.")
            return False
        hotel.reservations[reservation_id] = str(customer_id)
        hotels[hotel_id] = hotel.to_dict()
        save_hotels(hotels)
        print(f"Habitación reservada. ID de reservación: {reservation_id}")
        return True

    @staticmethod
    def cancel_room_reservation(hotel_id, reservation_id):
        """Libera la habitación asociada a la reservación."""
        hotels = load_hotels()
        hotel_id = str(hotel_id)
        if hotel_id not in hotels:
            print(f"Hotel con ID {hotel_id} no encontrado.")
            return False
        reservation_id = str(reservation_id)
        if reservation_id not in hotels[hotel_id]["reservations"]:
            print(
                f"Reservación {reservation_id} no encontrada "
                f"en el hotel {hotel_id}."
            )
            return False
        del hotels[hotel_id]["reservations"][reservation_id]
        save_hotels(hotels)
        print(
            f"Reservación {reservation_id} cancelada "
            f"en el hotel {hotel_id}."
        )
        return True
