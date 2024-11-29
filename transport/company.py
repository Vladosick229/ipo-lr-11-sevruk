from .client import Client
from .vehicle import Vehicle
class TransportCompany():
     def __init__(self,name,vehicles,clients):
           self.name = name
           self.vehicles = []
           self.clients =[]

     def add_vehicle(self,vehicle):
          if not isinstance(vehicle, Vehicle):
               raise ValueError("Неверный тип грузовика")
          self.clients.append(vehicle)

     def list_vehicles(self):
          return [str(vehicle) for vehicle in self.vehicles]
     
     def add_client(self,client):
          if not isinstance(client,Client):
               raise ValueError("Неверный тип грузовика")
          self.clients.append(client)

     def optimize_cargo_distribution(self):
          vip_clients=sorted([client for client in self.clients if client.is_vip], key=lambda c: c.cargo_weight, reverse=True)
          regular_clients = sorted([client for client in self.clients if not client.is_vip], key=lambda c: c.cargo_weight, reverse=True)

          all_clients=vip_clients+regular_clients

          for client in all_clients:
               for vehicle in sorted(self.vehicles, key=lambda v: v.current_load):
                    if vehicle.load_cargo(client):
                         break
                   