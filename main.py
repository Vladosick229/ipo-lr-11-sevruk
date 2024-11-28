from transport import functions
from functions import Client,Vehicle, Airplane, Van,TransportCompany

def menu():
    company = TransportCompany("TransCo")

    while True:
      print("\nЧто вы хотите сделать?")
      print("1. Добавить клиента")
      print("2. Добавить транспортное средство")
      print("3. Показать все транспортные средства")
      print("4. Распределить грузы")
      print("5. Показать результат распределения")
      print("6. Выйти из программы")

      res = input("\nВыберите пункт из предложенного списка: ")

      if res=="1":
         name=input("Введите имя клиента:")
         weight=float(input("Введите вес груза:"))
         is_vip=input("Клиент VIP?(Да/Нет):").strip().lower()=='да'
         company.add_client(Client(name, weight, is_vip))
         