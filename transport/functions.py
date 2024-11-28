import uuid

class Client():
    def __init__(self, name,cargo_weight,is_vip=False):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip

class Vehicle():
        def __init__(self,vehicle_id,capacity,clients_list,current_load=0):
            self.vehicle_id=str(uuid.uuid4())
            self.capacity=capacity
            self.current_load=current_load
            self.clients_list=[]

        def load_cargo(self,client):
            if not isinstance(client,Client):#проверка, является ли объект экземпляром указанного класса
                raise ValueError("Неверный тип клиента")
            if self.current_load + client.cargo_weight <= self.capacity:
                self.current_load += client.cargo_weight
                self.clients_list.append(client)
            else:
                raise ValueError("Невозможно загрузить груз: превышена грузоподъемность")
        
        def __str__(self):
             return f"ID транспорта:{self.vehicle_id},грузоподъёмность:{self.capacity},текущая загрузка:{self.current_load}"
        
class Airplane(Vehicle):
     def __init__(self,capacity,max_altitude):
          super().__init__(capacity)
          self.max_altitude=max_altitude

class Van(Vehicle):
     def __init__(self,capacity,is_refrigerated):
          super().__init__(capacity)
          self.is_refrigerated=is_refrigerated

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
                        
