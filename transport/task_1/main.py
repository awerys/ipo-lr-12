class Client:
    def __init__(self, name, cargo_weight, is_vip=False):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip
    def update_weight(self, new_weight):
        self.cargo_weight = new_weight
    def update_vip(self, status):
        self.is_vip = status 
    def show(self):
        print(f"Клиент: {self.name}")
        print(f"Вес: {self.cargo_weight} кг")
        print(f"VIP: {'Да' if self.is_vip else 'Нет'}")
client = Client("Алексей", 100)
client.show()
client.update_weight(150)
client.update_vip(True)
client.show()
