import dearpygui.dearpygui as dpg
import json

# Заглушки для классов
class Client:
    def __init__(self, name, cargo_weight, is_vip):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip

class Vehicle:
    def __init__(self, capacity):
        self.vehicle_id = id(self)
        self.capacity = capacity
        self.current_load = 0

class Van(Vehicle):
    def __init__(self, capacity, has_refrigeration):
        super().__init__(capacity)
        self.has_refrigeration = has_refrigeration

class Airplane(Vehicle):
    def __init__(self, capacity, max_altitude):
        super().__init__(capacity)
        self.max_altitude = max_altitude

class TransportCompany:
    def __init__(self, name):
        self.name = name
        self.clients = []
        self.vehicles = []

    def add_client(self, client):
        self.clients.append(client)

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def optimize_cargo_distribution(self):
        # Простая логика распределения грузов
        for client in self.clients:
            for vehicle in self.vehicles:
                if vehicle.current_load + client.cargo_weight <= vehicle.capacity:
                    vehicle.current_load += client.cargo_weight
                    break

# Глобальные переменные для хранения данных
company = TransportCompany("Моя Транспортная Компания")

# Функции для обновления таблиц
def update_clients_table():
    dpg.delete_item("clients_table", children_only=True)
    for client in company.clients:
        dpg.add_table_row(parent="clients_table", label=client.name, 
                          contents=[client.name, str(client.cargo_weight), "Да" if client.is_vip else "Нет"])

def update_vehicles_table():
    dpg.delete_item("vehicles_table", children_only=True)
    for vehicle in company.vehicles:
        dpg.add_table_row(parent="vehicles_table", label=f"vehicle_{vehicle.vehicle_id}", 
                          contents=[str(vehicle.vehicle_id), str(vehicle.capacity), str(vehicle.current_load)])

def show_client_form():
    if dpg.does_item_exist("client_form"):
        return
    with dpg.window(label="Добавить клиента", width=400, height=250, modal=True, tag="client_form"):
        dpg.add_text("Имя клиента:")
        dpg.add_input_text(tag="client_name", width=250)
        dpg.add_text("Вес груза:")
        dpg.add_input_text(tag="client_weight", width=250)
        dpg.add_text("VIP статус:")
        dpg.add_checkbox(tag="client_vip")
        dpg.add_button(label="Сохранить", callback=save_client)
        dpg.add_button(label="Отмена", callback=lambda: dpg.delete_item("client_form"))

def save_client():
    name = dpg.get_value("client_name")
    weight = dpg.get_value("client_weight")
    vip = dpg.get_value("client_vip")
    
    if name and weight.isdigit() and int(weight) > 0:
        client = Client(name, int(weight), vip)
        company.add_client(client)
        update_clients_table()
        dpg.delete_item("client_form")

def show_vehicle_form():
    if dpg.does_item_exist("vehicle_form"):
        return
    with dpg.window(label="Добавить транспорт", width=400, height=250, modal=True, tag="vehicle_form"):
        dpg.add_text("Тип транспорта:")
        dpg.add_combo(["Грузовик", "Самолет", "Фургон"], tag="vehicle_type", width=250)
        dpg.add_text("Грузоподъемность (тонны):")
        dpg.add_input_text(tag="vehicle_capacity", width=250)
        dpg.add_button(label="Сохранить", callback=save_vehicle)
        dpg.add_button(label="Отмена", callback=lambda: dpg.delete_item("vehicle_form"))

def save_vehicle():
    vehicle_type = dpg.get_value("vehicle_type")
    capacity = dpg.get_value("vehicle_capacity")
    
    if capacity.isdigit() and int(capacity) > 0:
        if vehicle_type == "Самолет":
            vehicle = Airplane(int(capacity), 10000)
        elif vehicle_type == "Фургон":
            vehicle = Van(int(capacity), True)
        else:
            vehicle = Vehicle(int(capacity))
        
        company.add_vehicle(vehicle)
        update_vehicles_table()
        dpg.delete_item("vehicle_form")

def distribute_cargo():
    company.optimize_cargo_distribution()
    update_vehicles_table()

def export_results():
    data = {
        "clients": [{"name": c.name, "cargo_weight": c.cargo_weight, "is_vip": c.is_vip} for c in company.clients],
        "vehicles": [{"vehicle_id": v.vehicle_id, "capacity": v.capacity, "current_load": v.current_load} for v in company.vehicles]
    }
    with open("export_results.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    dpg.set_value("status", "Результаты экспортированы в файл export_results.json")

# Функция для настройки шрифта
def setup_fonts():
    with dpg.font_registry():
        # Укажите путь к файлу шрифта
        default_font = dpg.add_font("C:/Windows/Fonts/Arial.ttf", 20)
  # Убедитесь, что файл arial.ttf существует
        dpg.bind_font(default_font)

# Главная функция интерфейса
def main_window():
    with dpg.window(label="Основное окно", width=800, height=600):
        with dpg.group(horizontal=True):
            with dpg.group():
                dpg.add_text("Клиенты")
                with dpg.table(tag="clients_table", header_row=True):
                    dpg.add_table_column(label="Имя клиента")
                    dpg.add_table_column(label="Вес груза")
                    dpg.add_table_column(label="VIP статус")
                dpg.add_button(label="Добавить клиента", callback=show_client_form)
                
            with dpg.group():
                dpg.add_text("Транспортные средства")
                with dpg.table(tag="vehicles_table", header_row=True):
                    dpg.add_table_column(label="ID")
                    dpg.add_table_column(label="Грузоподъемность")
                    dpg.add_table_column(label="Текущая загрузка")
                dpg.add_button(label="Добавить транспорт", callback=show_vehicle_form)
                dpg.add_button(label="Распределить грузы", callback=distribute_cargo)
                dpg.add_button(label="Экспортировать результат", callback=export_results)

            dpg.add_text("", tag="status")

# Запуск приложения
dpg.create_context()
setup_fonts()  # Устанавливаем шрифт для кириллицы
main_window()
dpg.create_viewport(title="Транспортная компания", width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
