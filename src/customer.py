"""Módulo de gestión de clientes para el sistema de reservaciones."""

import json
import os

CUSTOMERS_FILE = "customers.json"


def load_customers():
    """Cargar clientes desde archivo JSON."""
    if not os.path.exists(CUSTOMERS_FILE):
        return {}
    try:
        with open(CUSTOMERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error al cargar el archivo de clientes: {e}")
        return {}


def save_customers(customers):
    """Guardar clientes en archivo JSON."""
    try:
        with open(CUSTOMERS_FILE, "w", encoding="utf-8") as f:
            json.dump(customers, f, indent=4)
    except IOError as e:
        print(f"Error al guardar el archivo de clientes: {e}")


class Customer:
    """Representa a un cliente."""

    def __init__(self, customer_id, name, email, phone):
        """Inicializa una instancia de Cliente."""
        self.customer_id = str(customer_id)
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self):
        """Convierte el cliente a diccionario."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
        }

    @staticmethod
    def from_dict(data):
        """Crear un Cliente desde un diccionario."""
        return Customer(
            data["customer_id"],
            data["name"],
            data["email"],
            data["phone"],
        )

    @staticmethod
    def create_customer(customer_id, name, email, phone):
        """Crear y guardar un nuevo cliente."""
        customers = load_customers()
        customer_id = str(customer_id)
        if customer_id in customers:
            print(f"El cliente con ID {customer_id} ya existe.")
            return None
        customer = Customer(customer_id, name, email, phone)
        customers[customer_id] = customer.to_dict()
        save_customers(customers)
        print(f"Cliente '{name}' creado correctamente.")
        return customer

    @staticmethod
    def delete_customer(customer_id):
        """Eliminar un cliente por ID."""
        customers = load_customers()
        customer_id = str(customer_id)
        if customer_id not in customers:
            print(f"Cliente con ID {customer_id} no encontrado.")
            return False
        del customers[customer_id]
        save_customers(customers)
        print(f"Cliente {customer_id} eliminado correctamente.")
        return True

    @staticmethod
    def display_customer(customer_id):
        """Mostrar información del cliente."""
        customers = load_customers()
        customer_id = str(customer_id)
        if customer_id not in customers:
            print(f"Cliente con ID {customer_id} no encontrado.")
            return None
        customer = Customer.from_dict(customers[customer_id])
        print(f"--- Información del Cliente ---")
        print(f"ID     : {customer.customer_id}")
        print(f"Nombre : {customer.name}")
        print(f"Correo : {customer.email}")
        print(f"Teléfono: {customer.phone}")
        return customer

    @staticmethod
    def modify_customer(customer_id, name=None, email=None, phone=None):
        """Modificar información del cliente."""
        customers = load_customers()
        customer_id = str(customer_id)
        if customer_id not in customers:
            print(f"Cliente con ID {customer_id} no encontrado.")
            return False
        if name:
            customers[customer_id]["name"] = name
        if email:
            customers[customer_id]["email"] = email
        if phone:
            customers[customer_id]["phone"] = phone
        save_customers(customers)
        print(f"Cliente {customer_id} modificado correctamente.")
        return True