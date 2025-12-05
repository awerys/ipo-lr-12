class Client:
    def __init__(self, name, cargo_weight, is_vip=False):
        if not name or not isinstance(name, str):
            raise ValueError("Некорректное имя")
        if not isinstance(cargo_weight, (int, float)) or cargo_weight <= 0:
            raise ValueError("Вес должен быть положительным числом")

        if not isinstance(is_vip, bool):
            raise ValueError("VIP-статус должен быть True или False")
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip
    def update_weight(self, new_weight):
        if new_weight <= 0:
            print("Ошибка: Вес должен быть положительным")
            return
        self.cargo_weight = new_weight
    def update_vip(self, status):
        if status not in [True, False]:
            print("Ошибка: Укажите True или False для VIP-статуса")
            return
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
