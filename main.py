import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

DATA_FILE = 'weather_data.json'

def load_weather_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_weather_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def validate_input():
    date = entry_date.get()
    temperature = entry_temperature.get()
    description = entry_description.get()

    # Проверка даты
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД.")
        return False

    # Проверка температуры
    if not temperature.replace('-', '', 1).replace('.', '', 1).isdigit():
        messagebox.showerror("Ошибка", "Температура должна быть числом.")
        return False

    # Проверка описания
    if not description.strip():
        messagebox.showerror("Ошибка", "Описание погоды не может быть пустым.")
        return False

    return True

def add_record():
    if validate_input():
        record = {
            "date": entry_date.get(),
            "temperature": float(entry_temperature.get()),
            "description": entry_description.get(),
            "precipitation": var_precipitation.get()
        }
        weather_data.append(record)
        save_weather_data(weather_data)
        update_table()
        clear_inputs()

def update_table(filter_date=None, filter_temp=None):
    for i in tree.get_children():
        tree.delete(i)
    for record in weather_data:
        if filter_date and record["date"] != filter_date:
            continue
        if filter_temp is not None and record["temperature"] < filter_temp:
            continue
        precipitation_text = "Да" if record["precipitation"] else "Нет"
        tree.insert("", "end", values=(
            record["date"],
            record["temperature"],
            record["description"],
            precipitation_text
        ))

def filter_records():
    filter_date = entry_filter_date.get() if entry_filter_date.get() else None
    filter_temp_text = entry_filter_temp.get()
    filter_temp = float(filter_temp_text) if filter_temp_text else None
    update_table(filter_date, filter_temp)

def clear_inputs():
    entry_date.delete(0, tk.END)
    entry_temperature.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    var_precipitation.set(False)

# Загрузка данных
weather_data = load_weather_data()

# Создание GUI
root = tk.Tk()
root.title("Weather Diary")
root.geometry("900x500")

tab_control = ttk.Notebook(root)
tab_main = ttk.Frame(tab_control)
tab_filter = ttk.Frame(tab_control)

tab_control.add(tab_main, text="Добавить запись")
tab_control.add(tab_filter, text="Фильтр")
tab_control.pack(expand=1, fill="both")

# Вкладка "Добавить запись"
tk.Label(tab_main, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_date = tk.Entry(tab_main)
entry_date.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_main, text="Температура (°C):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_temperature = tk.Entry(tab_main)
entry_temperature.grid(row=1, column=1, padx=5, pady=5)

tk.Label(tab_main, text="Описание погоды:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_description = tk.Entry(tab_main, width=40)
entry_description.grid(row=2, column=1, padx=5, pady=5)

var_precipitation = tk.BooleanVar()
tk.Checkbutton(tab_main, text="Осадки", variable=var_precipitation).grid(row=3, column=0, columnspan=2, pady=10)

btn_add = tk.Button(tab_main, text="Добавить запись", command=add_record)
btn_add.grid(row=4, column=0, columnspan=2, pady=10)

# Таблица
tree = ttk.Treeview(tab_main, columns=("date", "temp", "desc", "precip"), show="headings")
tree.heading("date", text="Дата")
tree.heading("temp", text="Температура (°C)")
tree.heading("desc", text="Описание")
tree.heading("precip", text="Осадки")
tree.column("date", width=120)
tree.column("temp", width=100)
tree.column("desc", width=300)
tree.column("precip", width=80)
tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Вкладка "Фильтр"
tk.Label(tab_filter, text="Дата:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_filter_date = tk.Entry(tab_filter)
entry_filter_date.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_filter, text="Температура выше (°C):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_filter_temp = tk.Entry(tab_filter)
entry_filter_temp.grid(row=1, column=1, padx=5, pady=5)

btn_filter = tk.Button(tab_filter, text="Применить фильтр", command=filter_records)
btn_filter.grid(row=2, column=0, columnspan=2, pady=10)

update_table()
root.mainloop()
