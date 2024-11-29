import uuid
from .client import Client
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