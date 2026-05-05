import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

HIST_FILE = 'history.json'

def load_history():
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(hist):
    with open(HIST_FILE, 'w') as f:
        json.dump(hist, f)

def generate_password():
    try:
        length = int(length_var.get())
        if length < 6 or length > 32:
            messagebox.showwarning('Ошибка', 'Длина пароля от 6 до 32')
            return
    except:
        messagebox.showwarning('Ошибка', 'Некорректная длина')
        return

    chars = ''
    if var_digit.get():
        chars += string.digits
    if var_lower.get():
        chars += string.ascii_lowercase
    if var_upper.get():
        chars += string.ascii_uppercase
    if var_special.get():
        chars += string.punctuation

    if not chars:
        messagebox.showwarning('Ошибка', 'Выберите хотя бы один тип символов')
        return

    password = ''.join(random.choices(chars, k=length))
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)

    history.append(password)
    save_history(history)
    update_history()

def update_history():
    for i in tree.get_children():
        tree.delete(i)
    for p in history[-10:]:
        tree.insert('', tk.END, values=(p,))

def on_copy():
    password = entry_password.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)

root = tk.Tk()
root.title('Random Password Generator')
root.geometry('500x400')

length_var = tk.StringVar(value='12')

tk.Label(root, text='Длина пароля:').pack(pady=5)
tk.Scale(root, from_=6, to=32, orient=tk.HORIZONTAL, variable=length_var).pack(pady=5)

var_digit = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_upper = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=True)

tk.Checkbutton(root, text='Цифры', variable=var_digit).pack()
tk.Checkbutton(root, text='Строчные', variable=var_lower).pack()
tk.Checkbutton(root, text='Прописные', variable=var_upper).pack()
tk.Checkbutton(root, text='Спецсимволы', variable=var_special).pack()

tk.Button(root, text='Сгенерировать', command=generate_password).pack(pady=10)

entry_password = tk.Entry(root, width=40)
entry_password.pack(pady=5)
tk.Button(root, text='Копировать', command=on_copy).pack(pady=5)

history = load_history()

tree = ttk.Treeview(root, columns=('password',), show='headings', height=10)
tree.heading('password', text='История паролей')
tree.column('password', width=450)
tree.pack(pady=10)

update_history()

root.mainloop()