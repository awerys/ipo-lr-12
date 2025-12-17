import uuid
class Client:
    def __init__(self, name, cargo_weight, is_vip=False):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip
    def __str__(self):
        return f"Клиент {self.name}: {self.cargo_weight} кг"
class Vehicle:
    def __init__(self, capacity):
        self.vehicle_id = str(uuid.uuid4())[:8]
        self.capacity = capacity
        self.current_load = 0
        self.clients_list = []
    def load_cargo(self, client):
        new_load = self.current_load + client.cargo_weight
        capacity_kg = self.capacity * 1000  
        self.current_load = new_load
        self.clients_list.append(client)
        return True
    def unload_cargo(self, client=None):
        if client is None:
            self.current_load = 0
            unloaded = self.clients_list
            self.clients_list = []
            return unloaded
            client in self.clients_list:
            self.current_load -= client.cargo_weight
            self.clients_list.remove(client)
            return [client]
    def get_available_capacity(self):
        return self.capacity * 1000 - self.current_load
    def __str__(self):
        load_percent = (self.current_load / (self.capacity * 1000)) * 100
        clients_count = len(self.clients_list)
        return f"Транспорт {self.vehicle_id} ({self.capacity} т): {self.current_load} кг ({load_percent:.1f}%), Клиентов: {clients_count}"
if __name__ == "__main__":
    client1 = Client("Иван", 500) 
    client2 = Client("Мария", 300)  
    client3 = Client("Алексей", 800)  
    truck = Vehicle(2)  
    print(truck)
    try:
        truck.load_cargo(client1)
        truck.load_cargo(client2)
        print(truck)
        truck.load_cargo(client3)  
    except ValueError as e:
        print(f"Ошибка: {e}")
    print(f"Доступная грузоподъемность: {truck.get_available_capacity()} кг")
    print("\nКлиенты в транспорте:")
    for client in truck.clients_list:
        print(f"  - {client}")
