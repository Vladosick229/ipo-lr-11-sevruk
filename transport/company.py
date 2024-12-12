from .vehicle import Vehicle, Airplane, Van
from .client import Client

class TransportCompany:
    def __init__(self, name):
        self.name = name
        self.vehicles = []
        self.clients = []

    def add_vehicle(self, vehicle):
        if isinstance(vehicle, Vehicle):
            self.vehicles.append(vehicle)

    def list_vehicles(self):
        return [str(vehicle) for vehicle in self.vehicles]

    def add_client(self, client):
        if isinstance(client, Client):
            self.clients.append(client)

    def optimize_cargo_distribution(self):
        # Сортируем транспортные средства по грузоподъемности (по убыванию)
        sorted_vehicles = sorted(self.vehicles, key=lambda v: v.capacity, reverse=True)

        for client in self.clients:
            for vehicle in sorted_vehicles:
                if vehicle.current_load + client.cargo_weight <= vehicle.capacity:
                    vehicle.current_load += client.cargo_weight  # Добавляем груз
                    print(f"Груз клиента {client.name} (вес: {client.cargo_weight}) распределен на транспортное средство {vehicle.vehicle_id}")
                    break
