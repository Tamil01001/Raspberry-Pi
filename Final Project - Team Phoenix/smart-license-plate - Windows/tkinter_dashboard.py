# --- tkinter_dashboard.py ---
import tkinter as tk
from tkinter import ttk
import sqlite3
from PIL import ImageTk, Image
import os

DB_PATH = "logs/plates.db"
IMG_DIR = "logs/snaps"

root = tk.Tk()
root.title("License Plate Dashboard")
root.geometry("900x600")

cols = ("Plate", "Timestamp", "Confidence", "Image")
tree = ttk.Treeview(root, columns=cols, show='headings')
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor='center')
tree.pack(fill='both', expand=True)

img_label = tk.Label(root)
img_label.pack(side=tk.BOTTOM, pady=10)

def load_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT plate, timestamp, confidence, image_path FROM plate_logs ORDER BY id DESC")
    rows = cur.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', values=row)
    conn.close()

def on_select(event):
    for selected_item in tree.selection():
        item = tree.item(selected_item)['values']
        img_path = item[3]
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img.thumbnail((500, 300))
            img_tk = ImageTk.PhotoImage(img)
            img_label.configure(image=img_tk)
            img_label.image = img_tk

btn = tk.Button(root, text="Refresh", command=load_data)
btn.pack()
tree.bind("<<TreeviewSelect>>", on_select)

load_data()
root.mainloop()