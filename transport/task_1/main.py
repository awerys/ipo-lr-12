import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import re
class TransportApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Система распределения грузов")
        self.window.geometry("1000x600")
        self.clients = []
        self.vehicles = []
        self.results = []
        self.next_client_id = 1
        self.next_vehicle_id = 1
        self.make_menu()
        self.make_interface()
        self.load_test_data()
    def make_menu(self):
        menu_bar = tk.Menu(self.window)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить данные", command=self.save_data)
        file_menu.add_command(label="Загрузить данные", command=self.load_data)
        file_menu.add_separator()
        self.export_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Экспорт результатов", menu=self.export_menu, state='disabled')
        self.export_menu.add_command(label="В JSON", command=self.export_json)
        self.export_menu.add_command(label="В TXT", command=self.export_txt)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.window.quit)
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.about)
        self.window.config(menu=menu_bar)
    def make_interface(self):
        top_frame = tk.Frame(self.window, bd=2, relief=tk.RAISED)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        self.add_client_btn = tk.Button(top_frame, text="Добавить клиента", 
                                       command=self.open_add_client, width=20)
        self.add_client_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.add_vehicle_btn = tk.Button(top_frame, text="Добавить транспорт", 
                                       command=self.open_add_vehicle, width=20)
        self.add_vehicle_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.distribute_btn = tk.Button(top_frame, text="Распределить грузы", 
                                       command=self.distribute_cargo, width=20, 
                                       state='disabled')
        self.distribute_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.delete_btn = tk.Button(top_frame, text="Удалить выбранное", 
                                   command=self.delete_selected, width=20, 
                                   state='disabled')
        self.delete_btn.pack(side=tk.LEFT, padx=5, pady=5)
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        client_frame = tk.Frame(notebook)
        notebook.add(client_frame, text="Клиенты")
        self.make_client_table(client_frame)
        vehicle_frame = tk.Frame(notebook)
        notebook.add(vehicle_frame, text="Транспорт")
        self.make_vehicle_table(vehicle_frame)
        result_frame = tk.Frame(notebook)
        notebook.add(result_frame, text="Результаты")
        self.make_result_table(result_frame)
        self.status_bar = tk.Label(self.window, text="Готово", 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.window.bind('<Return>', lambda e: self.distribute_cargo())
        self.window.bind('<Delete>', lambda e: self.delete_selected())
    def make_client_table(self, parent):
        columns = ("ID", "Имя", "Вес груза", "Тип груза", "VIP", "Адрес")
        self.client_table = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        for col in columns:
            self.client_table.heading(col, text=col)
            self.client_table.column(col, width=120)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.client_table.yview)
        self.client_table.configure(yscrollcommand=scrollbar.set)
        self.client_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.client_table.bind('<Double-1>', lambda e: self.edit_client())
        self.client_table.bind('<<TreeviewSelect>>', 
                              lambda e: self.delete_btn.config(state='normal'))
    def make_vehicle_table(self, parent):
        columns = ("ID", "Тип", "Грузоподъемность", "Цена/км", "Местоположение", "Доступен")
        self.vehicle_table = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        for col in columns:
            self.vehicle_table.heading(col, text=col)
            self.vehicle_table.column(col, width=120)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.vehicle_table.yview)
        self.vehicle_table.configure(yscrollcommand=scrollbar.set)
        self.vehicle_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.vehicle_table.bind('<Double-1>', lambda e: self.edit_vehicle())
        self.vehicle_table.bind('<<TreeviewSelect>>', 
                               lambda e: self.delete_btn.config(state='normal'))
    def make_result_table(self, parent):
        columns = ("Клиент", "Транспорт", "Вес", "Стоимость", "Статус")
        self.result_table = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        for col in columns:
            self.result_table.heading(col, text=col)
            self.result_table.column(col, width=150)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.result_table.yview)
        self.result_table.configure(yscrollcommand=scrollbar.set)
        self.result_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    def load_test_data(self):
        self.clients = [
            {'id': 1, 'name': 'Иванов Иван', 'weight': 500, 'cargo_type': 'Хрупкий', 
             'vip': True, 'address': 'ул. Ленина, 10'},
            {'id': 2, 'name': 'Петров Петр', 'weight': 1500, 'cargo_type': 'Обычный', 
             'vip': False, 'address': 'ул. Мира, 25'},
            {'id': 3, 'name': 'Сидорова Анна', 'weight': 800, 'cargo_type': 'Скоропортящийся', 
             'vip': True, 'address': 'пр. Победы, 15'}
        ]
        self.vehicles = [
            {'id': 1, 'type': 'Грузовик', 'capacity': 2000, 'cost': 50, 
             'location': 'Склад №1', 'available': True},
            {'id': 2, 'type': 'Фургон', 'capacity': 1000, 'cost': 35, 
             'location': 'Склад №2', 'available': True},
            {'id': 3, 'type': 'Рефрижератор', 'capacity': 1200, 'cost': 60, 
             'location': 'Склад №3', 'available': True}
        ]
        self.next_client_id = 4
        self.next_vehicle_id = 4
        self.update_client_table()
        self.update_vehicle_table()
        if self.clients and self.vehicles:
            self.distribute_btn.config(state='normal')
    def open_add_client(self, client=None):
        win = tk.Toplevel(self.window)
        win.title("Редактировать клиента" if client else "Добавить клиента")
        win.geometry("400x350")
        name_var = tk.StringVar(value=client['name'] if client else "")
        weight_var = tk.StringVar(value=str(client['weight']) if client else "")
        cargo_var = tk.StringVar(value=client['cargo_type'] if client else "Обычный")
        vip_var = tk.BooleanVar(value=client.get('vip', False) if client else False)
        address_var = tk.StringVar(value=client['address'] if client else "")
        tk.Label(win, text="Имя клиента *:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        name_entry = tk.Entry(win, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(win, text="Вес груза (кг) *:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        weight_entry = tk.Entry(win, textvariable=weight_var, width=30)
        weight_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(win, text="Тип груза:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        cargo_combo = ttk.Combobox(win, textvariable=cargo_var, 
                                  values=["Хрупкий", "Скоропортящийся", "Опасный", "Обычный"], 
                                  state="readonly", width=28)
        cargo_combo.grid(row=2, column=1, padx=10, pady=5)
        tk.Checkbutton(win, text="VIP клиент", variable=vip_var).grid(row=3, column=0, columnspan=2, sticky='w', padx=10, pady=5)
        tk.Label(win, text="Адрес:").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        address_entry = tk.Entry(win, textvariable=address_var, width=30)
        address_entry.grid(row=4, column=1, padx=10, pady=5)
        def save():
            name_valid, name_error = self.validate_name(name_var.get())
            weight_valid, weight_result = self.validate_weight(weight_var.get())
                return
            if client:
                client['name'] = name_var.get().strip()
                client['weight'] = weight_result
                client['cargo_type'] = cargo_var.get()
                client['vip'] = vip_var.get()
                client['address'] = address_var.get().strip()
                self.status_bar.config(text="Клиент обновлен")
            else:
                new_client = {
                    'id': self.next_client_id,
                    'name': name_var.get().strip(),
                    'weight': weight_result,
                    'cargo_type': cargo_var.get(),
                    'vip': vip_var.get(),
                    'address': address_var.get().strip()
                }
                self.clients.append(new_client)
                self.next_client_id += 1
                self.status_bar.config(text="Новый клиент добавлен")
            self.update_client_table()
            if self.clients and self.vehicles:
                self.distribute_btn.config(state='normal')
            win.destroy()
        btn_frame = tk.Frame(win)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        tk.Button(btn_frame, text="Сохранить", command=save, width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Отмена", command=win.destroy, width=15).pack(side=tk.LEFT, padx=10)
        name_entry.focus_set()
        win.bind('<Return>', lambda e: save())
    def open_add_vehicle(self, vehicle=None):
        win = tk.Toplevel(self.window)
        win.title("Редактировать транспорт" if vehicle else "Добавить транспорт")
        win.geometry("400x300")
        type_var = tk.StringVar(value=vehicle['type'] if vehicle else "Грузовик")
        capacity_var = tk.StringVar(value=str(vehicle['capacity']) if vehicle else "")
        cost_var = tk.StringVar(value=str(vehicle['cost']) if vehicle else "")
        location_var = tk.StringVar(value=vehicle['location'] if vehicle else "")
        available_var = tk.BooleanVar(value=vehicle.get('available', True) if vehicle else True)
        tk.Label(win, text="Тип транспорта *:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        type_combo = ttk.Combobox(win, textvariable=type_var, 
                                 values=["Грузовик", "Фургон", "Рефрижератор", "Поезд"], 
                                 state="readonly", width=28)
        type_combo.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(win, text="Грузоподъемность *:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        capacity_entry = tk.Entry(win, textvariable=capacity_var, width=30)
        capacity_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(win, text="Цена за км *:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        cost_entry = tk.Entry(win, textvariable=cost_var, width=30)
        cost_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Label(win, text="Местоположение:").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        location_entry = tk.Entry(win, textvariable=location_var, width=30)
        location_entry.grid(row=3, column=1, padx=10, pady=5)
        tk.Checkbutton(win, text="Доступен", variable=available_var).grid(row=4, column=0, columnspan=2, sticky='w', padx=10, pady=5)
        def save():
            try:
                cost = float(cost_var.get())
                return
            if vehicle:
                vehicle['type'] = type_var.get()
                vehicle['capacity'] = capacity
                vehicle['cost'] = cost
                vehicle['location'] = location_var.get().strip()
                vehicle['available'] = available_var.get()
                self.status_bar.config(text="Транспорт обновлен")
            else:
                new_vehicle = {
                    'id': self.next_vehicle_id,
                    'type': type_var.get(),
                    'capacity': capacity,
                    'cost': cost,
                    'location': location_var.get().strip(),
                    'available': available_var.get()
                }
                self.vehicles.append(new_vehicle)
                self.next_vehicle_id += 1
                self.status_bar.config(text="Новый транспорт добавлен")
            self.update_vehicle_table()
            if self.clients and self.vehicles:
                self.distribute_btn.config(state='normal')
            win.destroy()
        btn_frame = tk.Frame(win)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        tk.Button(btn_frame, text="Сохранить", command=save, width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Отмена", command=win.destroy, width=15).pack(side=tk.LEFT, padx=10)
        type_combo.focus_set()
        win.bind('<Return>', lambda e: save())
    def edit_client(self):
        selection = self.client_table.selection()
        if not selection:
            return
        item = self.client_table.item(selection[0])
        client_id = int(item['values'][0])
        for client in self.clients:
            if client['id'] == client_id:
                self.open_add_client(client)
                break
    def edit_vehicle(self):
        selection = self.vehicle_table.selection()
        if not selection:
            return
        item = self.vehicle_table.item(selection[0])
        vehicle_id = int(item['values'][0])
        for vehicle in self.vehicles:
            if vehicle['id'] == vehicle_id:
                self.open_add_vehicle(vehicle)
                break
    def delete_selected(self):
        notebook = self.window.winfo_children()[1]
        current_tab = notebook.index(notebook.select())
        if current_tab == 0:  
            selection = self.client_table.selection()
            if not selection:
                return
            item = self.client_table.item(selection[0])
            client_id = int(item['values'][0])
            client_name = item['values'][1]
            if messagebox.askyesno("Подтверждение", f"Удалить клиента '{client_name}'?"):
                self.clients = [c for c in self.clients if c['id'] != client_id]
                self.update_client_table()
                self.status_bar.config(text=f"Клиент '{client_name}' удален")
                if not self.clients:
                    self.distribute_btn.config(state='disabled')
        elif current_tab == 1: 
            selection = self.vehicle_table.selection()
            if not selection:
                return
            item = self.vehicle_table.item(selection[0])
            vehicle_id = int(item['values'][0])
            vehicle_type = item['values'][1]
            if messagebox.askyesno("Подтверждение", f"Удалить транспорт '{vehicle_type}'?"):
                self.vehicles = [v for v in self.vehicles if v['id'] != vehicle_id]
                self.update_vehicle_table()
                self.status_bar.config(text=f"Транспорт '{vehicle_type}' удален")
                if not self.vehicles:
                    self.distribute_btn.config(state='disabled')
        self.delete_btn.config(state='disabled')
    def distribute_cargo(self):
        self.results = []
        sorted_clients = sorted(self.clients, key=lambda x: x['weight'], reverse=True)
        available_vehicles = [v for v in self.vehicles if v['available']]
        for client in sorted_clients:
            suitable = []
            for vehicle in available_vehicles:
                if vehicle['capacity'] >= client['weight']:
                    base_cost = vehicle['cost'] * 10  
                    if client['vip']:
                        base_cost *= 0.9
                    if client['cargo_type'] == "Опасный":
                        base_cost *= 1.2
                    elif client['cargo_type'] == "Хрупкий":
                        base_cost *= 1.1
                    suitable.append({
                        'vehicle': vehicle,
                        'cost': base_cost
                    })
            if suitable:
                best_option = min(suitable, key=lambda x: x['cost'])
                
                self.results.append({
                    'client_name': client['name'],
                    'client_weight': client['weight'],
                    'vehicle_type': best_option['vehicle']['type'],
                    'cost': round(best_option['cost'], 2),
                    'status': 'Назначен'
                })
                available_vehicles.remove(best_option['vehicle'])
            else:
                self.results.append({
                    'client_name': client['name'],
                    'client_weight': client['weight'],
                    'vehicle_type': 'Не найден',
                    'cost': 0,
                    'status': 'Не распределен'
                })
        self.update_result_table()
        self.export_menu.entryconfig(0, state='normal')
        self.export_menu.entryconfig(1, state='normal')
        notebook = self.window.winfo_children()[1]
        notebook.select(2)
        distributed = len([r for r in self.results if r['status'] == 'Назначен'])
        self.status_bar.config(text=f"Распределено {distributed} из {len(self.clients)} грузов")
    def update_client_table(self):
        for row in self.client_table.get_children():
            self.client_table.delete(row)
        
        for client in self.clients:
            vip_text = "good" if client.get('vip', False) else ""
            self.client_table.insert("", tk.END, values=(
                client['id'],
                client['name'],
                f"{client['weight']} кг",
                client['cargo_type'],
                vip_text,
                client['address']
            ))
    def update_vehicle_table(self):
        for row in self.vehicle_table.get_children():
            self.vehicle_table.delete(row)
        for vehicle in self.vehicles:
            available_text = "✓" if vehicle.get('available', True) else "✗"
            self.vehicle_table.insert("", tk.END, values=(
                vehicle['id'],
                vehicle['type'],
                f"{vehicle['capacity']} кг",
                f"{vehicle['cost']} руб",
                vehicle['location'],
                available_text
            ))
    def update_result_table(self):
        for row in self.result_table.get_children():
            self.result_table.delete(row)
        for result in self.results:
            self.result_table.insert("", tk.END, values=(
                result['client_name'],
                result['vehicle_type'],
                f"{result['client_weight']} кг",
                f"{result['cost']} руб",
                result['status']
            ))
    def save_data(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON файлы", "*.json")],
            initialfile="transport_data.json"
        )
        if filename:
            data = {
                'clients': self.clients,
                'vehicles': self.vehicles,
                'next_client_id': self.next_client_id,
                'next_vehicle_id': self.next_vehicle_id
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.status_bar.config(text=f"Данные сохранены")
    def load_data(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON файлы", "*.json")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.clients = data.get('clients', [])
                self.vehicles = data.get('vehicles', [])
                self.next_client_id = data.get('next_client_id', 1)
                self.next_vehicle_id = data.get('next_vehicle_id', 1)
                self.update_client_table()
                self.update_vehicle_table()
                if self.clients and self.vehicles:
                    self.distribute_btn.config(state='normal')
                self.status_bar.config(text=f"Данные загружены")
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON файлы", "*.json")],
            initialfile="results.json"
        )
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            self.status_bar.config(text="Результаты экспортированы")
    def export_txt(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt")],
            initialfile="results.txt"
        )
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Результаты распределения грузов\n")
                f.write(" "*50 + "\n\n")
                for result in self.results:
                    f.write(f"Клиент: {result['client_name']}\n")
                    f.write(f"  Вес: {result['client_weight']} кг\n")
                    f.write(f"  Транспорт: {result['vehicle_type']}\n")
                    f.write(f"  Стоимость: {result['cost']} руб\n")
                    f.write(f"  Статус: {result['status']}\n")
                    f.write(" "*30 + "\n")
            self.status_bar.config(text="Результаты экспортированы в TXT")
    def about(self):
        about_text = """Лабораторная работа 13
Вариант: 1
Разработчик: Калюжная Е.С.
Функции:
- Управление клиентами
- Управление транспортом
- Распределение грузов
- Экспорт результатов
"""
        messagebox.showinfo("О программе", about_text)
    def run(self):
        self.window.mainloop()
if __name__ == "__main__":
    app = TransportApp()
    app.run()
