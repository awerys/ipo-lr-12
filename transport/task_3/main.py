import random
class Client:
    def __init__(self, name, weight, is_vip=False):
        self.name = name
        self.weight = weight
        self.is_vip = is_vip
class Vehicle:
    def __init__(self, capacity):
        self.id = random.randint(1000, 9999)
        self.capacity = capacity  # тонны
        self.load = 0  # кг
        self.clients = []
    def can_load(self, weight):
        return self.load + weight <= self.capacity * 1000
    def add_load(self, client):
        if self.can_load(client.weight):
            self.load += client.weight
            self.clients.append(client)
            return True
        return False
    def __str__(self):
        return f"ID:{self.id} ({self.capacity}т): {self.load}кг"
class Truck(Vehicle):
    def __init__(self, capacity, color):
        super().__init__(capacity)
        self.color = color
class Train(Vehicle):
    def __init__(self, capacity, cars):
        super().__init__(capacity)
        self.cars = cars
class TransportCompany:
    def __init__(self, name):
        self.name = name
        self.vehicles = []
        self.clients = []
    def add_vehicle(self, v):
        self.vehicles.append(v)
    def add_client(self, c):
        self.clients.append(c)
    def optimize(self):
        print("Распределяем грузы...")
        vip = [c for c in self.clients if c.is_vip]
        others = [c for c in self.clients if not c.is_vip]
        all_clients = vip + others
        vehicles_sorted = sorted(self.vehicles, key=lambda x: -x.capacity)
        
        for client in all_clients:
            loaded = False
            for vehicle in vehicles_sorted:
                if vehicle.add_load(client):
                    loaded = True
                    break
            if not loaded:
                print(f"Не смогли загрузить {client.name}")
        used = [v for v in vehicles_sorted if v.load > 0]
        print(f"\nИспользовано транспорта: {len(used)}")
        for v in used:
            print(f"  {v} - {len(v.clients)} клиентов")
company = TransportCompany("Тест")
company.add_vehicle(Truck(5, "красный"))
company.add_vehicle(Train(15, 3))
company.add_client(Client("VIP1", 2000, True))
company.add_client(Client("Обычный1", 1000))
company.optimize()
