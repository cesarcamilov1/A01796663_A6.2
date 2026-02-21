"""Módulo de gestión de hoteles para el sistema de reservaciones."""

import json
import os

HOTELS_FILE = "hotels.json"


def load_hotels():
    """Cargar hoteles desde archivo JSON."""
    if not os.path.exists(HOTELS_FILE):
        return {}
    try:
        with open(HOTELS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error al cargar el archivo de hoteles: {e}")
        return {}


def save_hotels(hotels):
    """Guardar hoteles en archivo JSON."""
    try:
        with open(HOTELS_FILE, "w", encoding="utf-8") as f:
            json.dump(hotels, f, indent=4)
    except IOError as e:
        print(f"Error al guardar el archivo de hoteles: {e}")


class Hotel:
    """Representa un hotel con habitaciones y reservaciones."""

    def __init__(self, hotel_id, name, location, total_rooms):
        """Inicializa una instancia de Hotel."""
        if not isinstance(total_rooms, int) or total_rooms <= 0:
            raise ValueError("total_rooms must be a positive integer.")
        self.hotel_id = str(hotel_id)
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.reservations = {}

    def to_dict(self):
        """Convierte el hotel a diccionario."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
            "reservations": self.reservations,
        }

    @staticmethod
    def from_dict(data):
        """Crear un Hotel desde un diccionario."""
        hotel = Hotel(
            data["hotel_id"],
            data["name"],
            data["location"],
            data["total_rooms"],
        )
        hotel.reservations = data.get("reservations", {})
        return hotel

    def available_rooms(self):
        """Regresa el número de habitaciones disponibles."""
        return self.total_rooms - len(self.reservations)

    @staticmethod
    def create_hotel(hotel_id, name, location, total_rooms):
        """Crear y guardar un nuevo hotel."""
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
        """Eliminar un hotel por ID."""
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
        """Mostrar información del hotel."""
        hotels = load_hotels()
        hotel_id = str(hotel_id)
        if hotel_id not in hotels:
            print(f"Hotel con ID {hotel_id} no encontrado.")
            return None
        hotel = Hotel.from_dict(hotels[hotel_id])
        print(f"--- Información del Hotel ---")
        print(f"ID        : {hotel.hotel_id}")
        print(f"Nombre    : {hotel.name}")
        print(f"Ubicación : {hotel.location}")
        print(f"Habitaciones: {hotel.total_rooms} total, {hotel.available_rooms()} disponibles")
        return hotel

    @staticmethod
    def modify_hotel(hotel_id, name=None, location=None, total_rooms=None):
        """Modificar información del hotel."""
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
        """Reservar una habitación en un hotel."""
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
        """Cancelar una reservación de habitación en un hotel."""
        hotels = load_hotels()
        hotel_id = str(hotel_id)
        if hotel_id not in hotels:
            print(f"Hotel con ID {hotel_id} no encontrado.")
            return False
        reservation_id = str(reservation_id)
        if reservation_id not in hotels[hotel_id]["reservations"]:
            print(f"Reservación {reservation_id} no encontrada en el hotel {hotel_id}.")
            return False
        del hotels[hotel_id]["reservations"][reservation_id]
        save_hotels(hotels)
        print(f"Reservación {reservation_id} cancelada en el hotel {hotel_id}.")
        return True