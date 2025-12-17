class Client:
    def __init__(self, name, cargo_weight, is_vip=False):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip
class Vehicle:
    def __init__(self, capacity):
        self.capacity = capacity
        self.current_load = 0
        self.clients = []
clients = [
    Client("Иван", 1500, False),
    Client("Мария", 800, True),
    Client("Алексей", 2000, False),
    Client("Ольга", 1200, True)
]
vehicles = [
    Vehicle(5),  
    Vehicle(3),  
    Vehicle(10)  
]
def show_all_clients():
    print("\n" + "="*50)
    print("Все клиенты")
    print(" "*10)
    print(f"Всего клиентов: {len(clients)}\n")
    for i, client in enumerate(clients, 1):
        vip = " (VIP)" if client.is_vip else ""
        print(f"{i}. Имя: {client.name}{vip}")
        print(f"   Вес груза: {client.cargo_weight} кг")
        print()
def show_client_by_id():
    print("\nПоиск клиента")
    try:
        client_id = int(input("Введите номер клиента: "))
        if 1 <= client_id <= len(clients):
            client = clients[client_id-1]
            vip = "Да" if client.is_vip else "Нет"
            print(f"\nКлиент #{client_id}:")
            print(f"  Имя: {client.name}")
            print(f"  Вес груза: {client.cargo_weight} кг")
            print(f"  VIP статус: {vip}")
def add_client():
    print("\nДобавление клиента")
    name = input("Имя клиента: ")
        weight = float(input("Вес груза (кг): "))
        return
    vip = input("VIP клиент? (да/нет): ").lower()
    is_vip = vip in ['да', 'yes', 'y', 'д']
    clients.append(Client(name, weight, is_vip))
    print(f"Клиент '{name}' добавлен")
def delete_client():
    print("\nУдаление клиента")
    show_all_clients()
    try:
        client_id = int(input("Введите номер клиента для удаления: "))
        if 1 <= client_id <= len(clients):
            deleted = clients.pop(client_id-1)
            print(f"Клиент '{deleted.name}' удален")
def show_vehicles():
    print("\n" + " "*50)
    print("Весь транспорт")
    print(" "*20)
    print(f"Всего единиц транспорта: {len(vehicles)}\n")
    for i, vehicle in enumerate(vehicles, 1):
        used = vehicle.current_load / (vehicle.capacity * 1000) * 100
        print(f"{i}. Грузоподъемность: {vehicle.capacity} т")
        print(f"   Загружено: {vehicle.current_load} кг ({used:.1f}%)")
        print(f"   Клиентов: {len(vehicle.clients)}")
        if vehicle.clients:
            print("   Загружены:")
            for client in vehicle.clients:
                vip = " (VIP)" if client.is_vip else ""
                print(f"     - {client.name}{vip}: {client.cargo_weight} кг")
        print()
def distribute_cargo():
    print("\nРаспределенение грузов")
    for vehicle in vehicles:
        vehicle.current_load = 0
        vehicle.clients = []
    clients_to_load = sorted(clients, key=lambda x: (not x.is_vip, -x.cargo_weight))
    loaded_count = 0
    for client in clients_to_load:
        loaded = False
        for vehicle in vehicles:
            if vehicle.current_load + client.cargo_weight <= vehicle.capacity * 1000:
                vehicle.current_load += client.cargo_weight
                vehicle.clients.append(client)
                loaded = True
                loaded_count += 1
                break
    print(f"\nРаспределение завершено")
    print(f"Загружено {loaded_count} из {len(clients)} клиентов")
    show_distribution_results()
def show_distribution_results():
    print("\n" + " "*50)
    print("Результаты")
    print(" "*50)
    for i, vehicle in enumerate(vehicles, 1):
        if vehicle.current_load > 0:
            used = vehicle.current_load / (vehicle.capacity * 1000) * 100
            print(f"\nТранспорт #{i} ({vehicle.capacity} т):")
            print(f"  Загружено: {vehicle.current_load} кг ({used:.1f}%)")
            print(f"  Клиентов: {len(vehicle.clients)}")
            if vehicle.clients:
                print("  Список клиентов:")
                for client in vehicle.clients:
                    vip = " (VIP)" if client.is_vip else ""
                    print(f"    • {client.name}{vip}: {client.cargo_weight} кг")
def main():
    while True:
        print("\n" + "="*40)
        print("Управление грузоперевозками")
        print(" "*40)
        print("1. Вывести всех клиентов")
        print("2. Вывести клиента по номеру")
        print("3. Добавить клиента")
        print("4. Удалить клиента по номеру")
        print("5. Вывести весь транспорт")
        print("6. Распределить грузы")
        print("7. Вывести результаты распределения")
        print("8. Выйти из программы")
        print(" "*40)
        choice = input("Выберите пункт меню (1-8): ")
        if choice == "1":
            show_all_clients()
        elif choice == "2":
            show_client_by_id()
        elif choice == "3":
            add_client()
        elif choice == "4":
            delete_client()
        elif choice == "5":
            show_vehicles()
        elif choice == "6":
            distribute_cargo()
        elif choice == "7":
            show_distribution_results()
        elif choice == "8":
            print("Всего доброго")
            break
if __name__ == "__main__":
    print(" "*50)
    print("Система управления")
    print(" "*50)
    main()
