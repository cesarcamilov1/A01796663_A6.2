"""Tests para las clases Hotel, Cliente y Reservación."""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src')
)

import customer as customer_module  # noqa: E402
import hotel as hotel_module  # noqa: E402
import reservation as reservation_module  # noqa: E402
from customer import Customer  # noqa: E402
from hotel import Hotel  # noqa: E402
from reservation import Reservation  # noqa: E402


def cleanup_files():
    """Borra los archivos JSON que quedan de las pruebas."""
    for f in ["hotels.json", "customers.json", "reservations.json"]:
        if os.path.exists(f):
            os.remove(f)


class TestHotel(unittest.TestCase):
    """Pruebas de la clase Hotel."""
    # pylint: disable=too-many-public-methods

    def setUp(self):
        """Limpia el estado antes de cada prueba."""
        cleanup_files()

    def tearDown(self):
        """Limpia los archivos al terminar cada prueba."""
        cleanup_files()

    # --- Pruebas positivas ---

    def test_create_hotel_success(self):
        """Verifica que se puede crear un hotel sin problemas."""
        h = Hotel.create_hotel("H1", "Hotel las pesadillas", "Morelos", 10)
        self.assertIsNotNone(h)
        self.assertEqual(h.name, "Hotel las pesadillas")

    def test_delete_hotel_success(self):
        """Verifica que se puede borrar un hotel existente."""
        Hotel.create_hotel("H2", "Vista Hermosa", "Cuernavaca", 5)
        result = Hotel.delete_hotel("H2")
        self.assertTrue(result)

    def test_display_hotel_success(self):
        """Verifica que se muestran los datos de un hotel correctamente."""
        Hotel.create_hotel("H3", "Montaña Mágica", "Jiutepec", 8)
        h = Hotel.display_hotel("H3")
        self.assertIsNotNone(h)
        self.assertEqual(h.location, "Jiutepec")

    def test_modify_hotel_name(self):
        """Verifica que se puede cambiar el nombre del hotel."""
        Hotel.create_hotel("H4", "Barra Vieja", "Los Arcos", 6)
        result = Hotel.modify_hotel("H4", name="New Name")
        self.assertTrue(result)

    def test_modify_hotel_location(self):
        """Verifica que se puede cambiar la ubicación del hotel."""
        Hotel.create_hotel("H5", "Test Hotel", "OldCity", 4)
        result = Hotel.modify_hotel("H5", location="NewCity")
        self.assertTrue(result)

    def test_modify_hotel_rooms(self):
        """Verifica que se puede cambiar el número de habitaciones."""
        Hotel.create_hotel("H6", "Rooms Hotel", "Valencia", 3)
        result = Hotel.modify_hotel("H6", total_rooms=10)
        self.assertTrue(result)

    def test_reserve_room_success(self):
        """Verifica que se puede reservar una habitación disponible."""
        Hotel.create_hotel("H7", "Reserve Hotel", "Bilbao", 5)
        result = Hotel.reserve_room("H7", "R001", "C1")
        self.assertTrue(result)

    def test_cancel_room_reservation_success(self):
        """Verifica que se puede cancelar una reservación existente."""
        Hotel.create_hotel("H8", "Cancel Hotel", "Malaga", 5)
        Hotel.reserve_room("H8", "R002", "C2")
        result = Hotel.cancel_room_reservation("H8", "R002")
        self.assertTrue(result)

    def test_available_rooms(self):
        """Verifica que el conteo de habitaciones libres es correcto."""
        Hotel.create_hotel("H9", "Count Hotel", "Toledo", 3)
        Hotel.reserve_room("H9", "R003", "C3")
        h = Hotel.display_hotel("H9")
        self.assertEqual(h.available_rooms(), 2)

    def test_hotel_to_dict(self):
        """Verifica que el hotel se serializa bien como dict."""
        h = Hotel("H10", "Dict Hotel", "Zaragoza", 7)
        d = h.to_dict()
        self.assertEqual(d["name"], "Dict Hotel")
        self.assertIn("reservations", d)

    def test_hotel_from_dict(self):
        """Verifica que se puede reconstruir un hotel desde un dict."""
        data = {
            "hotel_id": "H11",
            "name": "From Dict",
            "location": "Cordoba",
            "total_rooms": 4,
            "reservations": {},
        }
        h = Hotel.from_dict(data)
        self.assertEqual(h.hotel_id, "H11")

    # --- Pruebas negativas ---

    def test_create_hotel_invalid_rooms(self):
        """Verifica que habitaciones negativas lanzan ValueError."""
        with self.assertRaises(ValueError):
            Hotel("H_bad", "Bad Hotel", "Nowhere", -1)

    def test_create_hotel_duplicate(self):
        """Verifica que no se puede crear dos hoteles con el mismo ID."""
        Hotel.create_hotel("HD1", "Dup Hotel", "City", 5)
        result = Hotel.create_hotel("HD1", "Dup Hotel", "City", 5)
        self.assertIsNone(result)

    def test_delete_hotel_not_found(self):
        """Verifica que borrar un hotel inexistente regresa False."""
        result = Hotel.delete_hotel("NONEXISTENT")
        self.assertFalse(result)

    def test_display_hotel_not_found(self):
        """Verifica que consultar un hotel inexistente regresa None."""
        result = Hotel.display_hotel("NONEXISTENT")
        self.assertIsNone(result)

    def test_modify_hotel_not_found(self):
        """Verifica que modificar un hotel inexistente regresa False."""
        result = Hotel.modify_hotel("NONEXISTENT", name="X")
        self.assertFalse(result)

    def test_modify_hotel_invalid_rooms(self):
        """Verifica que poner habitaciones negativas regresa False."""
        Hotel.create_hotel("HM1", "Mod Hotel", "City", 5)
        result = Hotel.modify_hotel("HM1", total_rooms=-5)
        self.assertFalse(result)

    def test_reserve_room_no_availability(self):
        """Verifica que no se pueden hacer más reservas que habitaciones."""
        Hotel.create_hotel("HF1", "Full Hotel", "City", 1)
        Hotel.reserve_room("HF1", "R_A", "C1")
        result = Hotel.reserve_room("HF1", "R_B", "C2")
        self.assertFalse(result)

    def test_reserve_room_hotel_not_found(self):
        """Verifica que reservar en un hotel inexistente regresa False."""
        result = Hotel.reserve_room("NOTEXIST", "R_X", "C1")
        self.assertFalse(result)

    def test_reserve_room_duplicate_reservation(self):
        """Verifica que no se puede usar el mismo ID dos veces."""
        Hotel.create_hotel("HDR", "Dup Res Hotel", "City", 5)
        Hotel.reserve_room("HDR", "RDUP", "C1")
        result = Hotel.reserve_room("HDR", "RDUP", "C2")
        self.assertFalse(result)

    def test_cancel_room_reservation_not_found(self):
        """Verifica que cancelar una reservación inexistente regresa False."""
        Hotel.create_hotel("HC1", "Cancel Hotel", "City", 5)
        result = Hotel.cancel_room_reservation("HC1", "NOTEXIST")
        self.assertFalse(result)

    def test_cancel_room_reservation_hotel_not_found(self):
        """Verifica que cancelar en un hotel inexistente regresa False."""
        result = Hotel.cancel_room_reservation("NOTEXIST", "R1")
        self.assertFalse(result)

    def test_load_hotels_invalid_json(self):
        """Verifica que un JSON corrupto no rompe la carga de hoteles."""
        with open("hotels.json", "w", encoding="utf-8") as f:
            f.write("INVALID JSON{{{")
        result = hotel_module.load_hotels()
        self.assertEqual(result, {})

    def test_hotel_rooms_zero_invalid(self):
        """Verifica que cero habitaciones también lanza ValueError."""
        with self.assertRaises(ValueError):
            Hotel("H_zero", "Zero Hotel", "City", 0)


class TestCustomer(unittest.TestCase):
    """Pruebas de la clase Customer."""

    def setUp(self):
        """Preparar estado limpio antes de cada prueba."""
        cleanup_files()

    def tearDown(self):
        """Limpiar archivos después de cada prueba."""
        cleanup_files()

    # --- Pruebas positivas ---

    def test_create_customer_success(self):
        """Verifica que se puede crear un cliente sin problemas."""
        c = Customer.create_customer("C1", "Alice", "alice@x.com", "555-0001")
        self.assertIsNotNone(c)
        self.assertEqual(c.name, "Alice")

    def test_delete_customer_success(self):
        """Verifica que se puede borrar un cliente existente."""
        Customer.create_customer("C2", "Bob", "bob@x.com", "555-0002")
        result = Customer.delete_customer("C2")
        self.assertTrue(result)

    def test_display_customer_success(self):
        """Verifica que se muestran los datos de un cliente correctamente."""
        Customer.create_customer("C3", "Carol", "carol@x.com", "555-0003")
        c = Customer.display_customer("C3")
        self.assertIsNotNone(c)
        self.assertEqual(c.email, "carol@x.com")

    def test_modify_customer_name(self):
        """Verifica que se puede cambiar el nombre del cliente."""
        Customer.create_customer("C4", "Dave", "dave@x.com", "555-0004")
        result = Customer.modify_customer("C4", name="David")
        self.assertTrue(result)

    def test_modify_customer_email(self):
        """Verifica que se puede cambiar el correo del cliente."""
        Customer.create_customer("C5", "Eve", "eve@x.com", "555-0005")
        result = Customer.modify_customer("C5", email="neweye@x.com")
        self.assertTrue(result)

    def test_modify_customer_phone(self):
        """Verifica que se puede cambiar el teléfono del cliente."""
        Customer.create_customer("C6", "Frank", "frank@x.com", "555-0006")
        result = Customer.modify_customer("C6", phone="999-9999")
        self.assertTrue(result)

    def test_customer_to_dict(self):
        """Verifica que el cliente se serializa bien como dict."""
        c = Customer("C7", "Grace", "grace@x.com", "555-0007")
        d = c.to_dict()
        self.assertEqual(d["name"], "Grace")

    def test_customer_from_dict(self):
        """Verifica que se puede reconstruir un cliente desde un dict."""
        data = {
            "customer_id": "C8",
            "name": "Hank",
            "email": "hank@x.com",
            "phone": "555-0008",
        }
        c = Customer.from_dict(data)
        self.assertEqual(c.customer_id, "C8")

    # --- Pruebas negativas ---

    def test_create_customer_duplicate(self):
        """Verifica que no se puede crear dos clientes con el mismo ID."""
        Customer.create_customer("CD1", "Dup", "d@x.com", "000")
        result = Customer.create_customer("CD1", "Dup", "d@x.com", "000")
        self.assertIsNone(result)

    def test_delete_customer_not_found(self):
        """Verifica que borrar un cliente inexistente regresa False."""
        result = Customer.delete_customer("NOTEXIST")
        self.assertFalse(result)

    def test_display_customer_not_found(self):
        """Verifica que consultar un cliente inexistente regresa None."""
        result = Customer.display_customer("NOTEXIST")
        self.assertIsNone(result)

    def test_modify_customer_not_found(self):
        """Verifica que modificar un cliente inexistente regresa False."""
        result = Customer.modify_customer("NOTEXIST", name="X")
        self.assertFalse(result)

    def test_load_customers_invalid_json(self):
        """Verifica que un JSON corrupto no rompe la carga de clientes."""
        with open("customers.json", "w", encoding="utf-8") as f:
            f.write("NOT JSON ][")
        result = customer_module.load_customers()
        self.assertEqual(result, {})


class TestReservation(unittest.TestCase):
    """Pruebas de la clase Reservation."""

    def setUp(self):
        """Crea un hotel y un cliente de prueba antes de cada caso."""
        cleanup_files()
        Hotel.create_hotel("H1", "Test Hotel", "TestCity", 5)
        Customer.create_customer("C1", "Alice", "a@x.com", "555-1111")

    def tearDown(self):
        """Limpia los archivos al terminar cada prueba."""
        cleanup_files()

    # --- Pruebas positivas ---

    def test_create_reservation_success(self):
        """Verifica que se puede crear una reservación sin problemas."""
        r = Reservation.create_reservation(
            "R1", "C1", "H1", "2025-01-01", "2025-01-05"
        )
        self.assertIsNotNone(r)
        self.assertEqual(r.customer_id, "C1")

    def test_cancel_reservation_success(self):
        """Verifica que se puede cancelar una reservación existente."""
        Reservation.create_reservation(
            "R2", "C1", "H1", "2025-02-01", "2025-02-05"
        )
        result = Reservation.cancel_reservation("R2")
        self.assertTrue(result)

    def test_display_reservation_success(self):
        """Verifica que se muestran los datos de una reservación."""
        Reservation.create_reservation(
            "R3", "C1", "H1", "2025-03-01", "2025-03-05"
        )
        r = Reservation.display_reservation("R3")
        self.assertIsNotNone(r)
        self.assertEqual(r.hotel_id, "H1")

    def test_reservation_to_dict(self):
        """Verifica que la reservación se serializa bien como dict."""
        r = Reservation("R_T", "C1", "H1", "2025-04-01", "2025-04-05")
        d = r.to_dict()
        self.assertIn("check_in", d)

    def test_reservation_from_dict(self):
        """Verifica que se puede reconstruir una reservación desde un dict."""
        data = {
            "reservation_id": "R_FD",
            "customer_id": "C1",
            "hotel_id": "H1",
            "check_in": "2025-05-01",
            "check_out": "2025-05-05",
        }
        r = Reservation.from_dict(data)
        self.assertEqual(r.reservation_id, "R_FD")

    def test_cancel_reservation_restores_room(self):
        """Verifica que al cancelar se libera la habitación del hotel."""
        Hotel.create_hotel("H_SM", "Small Hotel", "City", 1)
        Reservation.create_reservation(
            "R_SM", "C1", "H_SM", "2025-06-01", "2025-06-03"
        )
        Reservation.cancel_reservation("R_SM")
        h = Hotel.display_hotel("H_SM")
        self.assertEqual(h.available_rooms(), 1)

    # --- Pruebas negativas ---

    def test_create_reservation_duplicate(self):
        """Verifica que no se puede usar el mismo ID dos veces."""
        Reservation.create_reservation(
            "R_DUP", "C1", "H1", "2025-07-01", "2025-07-05"
        )
        result = Reservation.create_reservation(
            "R_DUP", "C1", "H1", "2025-07-01", "2025-07-05"
        )
        self.assertIsNone(result)

    def test_create_reservation_hotel_not_found(self):
        """Verifica que no se puede reservar en un hotel que no existe."""
        result = Reservation.create_reservation(
            "R_NF", "C1", "NOTEXIST", "2025-08-01", "2025-08-05"
        )
        self.assertIsNone(result)

    def test_cancel_reservation_not_found(self):
        """Verifica que cancelar una reservación inexistente regresa False."""
        result = Reservation.cancel_reservation("NOTEXIST")
        self.assertFalse(result)

    def test_display_reservation_not_found(self):
        """Verifica que consultar una reservación inexistente regresa None."""
        result = Reservation.display_reservation("NOTEXIST")
        self.assertIsNone(result)

    def test_create_reservation_full_hotel(self):
        """Verifica que no se puede reservar cuando el hotel ya está lleno."""
        Hotel.create_hotel("H_FULL", "Full Hotel", "City", 1)
        Reservation.create_reservation(
            "R_F1", "C1", "H_FULL", "2025-09-01", "2025-09-03"
        )
        result = Reservation.create_reservation(
            "R_F2", "C1", "H_FULL", "2025-09-01", "2025-09-03"
        )
        self.assertIsNone(result)

    def test_load_reservations_invalid_json(self):
        """Verifica que un JSON corrupto no rompe la carga de reservaciones."""
        with open("reservations.json", "w", encoding="utf-8") as f:
            f.write("{{INVALID")
        result = reservation_module.load_reservations()
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
