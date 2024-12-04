
from transport import Client,Vehicle,TransportCompany,Van,Airplane 
import dearpygui.dearpygui as dpg
import json

# Глобальные переменные для хранения данных
company = TransportCompany("Моя Транспортная Компания")

# Функции для обновления таблиц
def update_clients_table():
    dpg.delete_item("clients_table", children_only=True)
    for client in company.clients:
        dpg.add_table_row(parent="clients_table", contents=[client.name, str(client.cargo_weight), "Да" if client.is_vip else "Нет"])

def update_vehicles_table():
    dpg.delete_item("vehicles_table", children_only=True)
    for vehicle in company.vehicles:
        dpg.add_table_row(parent="vehicles_table", contents=[vehicle.vehicle_id, str(vehicle.capacity), str(vehicle.current_load)])

def show_client_form():
    with dpg.handler_registry():
        dpg.add_window(label="Добавить клиента", width=400, height=250, modal=True)
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
    with dpg.handler_registry():
        dpg.add_window(label="Добавить транспорт", width=400, height=250, modal=True)
        dpg.add_text("Тип транспорта:")
        dpg.add_combo(["Грузовик", "Поезд", "Самолет", "Фургон"], tag="vehicle_type", width=250)
        dpg.add_text("Грузоподъемность (тонны):")
        dpg.add_input_text(tag="vehicle_capacity", width=250)
        dpg.add_button(label="Сохранить", callback=save_vehicle)
        dpg.add_button(label="Отмена", callback=lambda: dpg.delete_item("vehicle_form"))

def save_vehicle():
    vehicle_type = dpg.get_value("vehicle_type")
    capacity = dpg.get_value("vehicle_capacity")
    
    if capacity.isdigit() and int(capacity) > 0:
        if vehicle_type == "Самолет":
            vehicle = Airplane(int(capacity), 10000)  # Пример максимальной высоты
        elif vehicle_type == "Фургон":
            vehicle = Van(int(capacity), True)  # Пример с холодильником
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
    with open("export_results.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    dpg.set_value("status", "Результаты экспортированы в файл export_results.json")

# Главная функция для интерфейса
def main_window():
    with dpg.handler_registry():
        dpg.add_window(label="Основное окно", width=800, height=600)

        with dpg.group(horizontal=True):
            with dpg.group():
                dpg.add_text("Клиенты")
                dpg.add_table(tag="clients_table", header_row=True, columns=["Имя клиента", "Вес груза", "VIP статус"])
                update_clients_table()
                dpg.add_button(label="Добавить клиента", callback=show_client_form)
                
            with dpg.group():
                dpg.add_text("Транспортные средства")
                dpg.add_table(tag="vehicles_table", header_row=True, columns=["ID", "Грузоподъемность", "Текущая загрузка"])
                update_vehicles_table()
                dpg.add_button(label="Добавить транспорт", callback=show_vehicle_form)
                dpg.add_button(label="Распределить грузы", callback=distribute_cargo)
                dpg.add_button(label="Экспортировать результат", callback=export_results)

            dpg.add_text("", tag="status")

# Запуск приложения
dpg.create_context()
main_window()
dpg.create_viewport(title="Транспортная компания", width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
