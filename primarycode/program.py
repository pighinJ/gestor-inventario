import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Inventario")

        #usuario y registro


        # Estilo
        self.style = ttk.Style()
        self.style.configure('Custom.TLabel', 
                             foreground='black',  # Color del texto negro
                             font=('Helvetica', 12),
                             padding=10)
        self.style.map('Custom.TLabel',
                       background=[('active', '#FF5733')])  # Color de fondo cuando se activa

        
# Conexión a la base de datos SQLite
        self.connection = sqlite3.connect("inventory.db")
        self.cursor = self.connection.cursor()

        # Crear tabla de productos si no existe
        self.create_product_table()

        # Resto del código de inicialización

    def create_product_table(self):
        # Eliminar la tabla existente si existe
        self.cursor.execute("DROP TABLE IF EXISTS products")

        # Crear la nueva tabla con todas las columnas necesarias
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                brand TEXT,
                                size TEXT,
                                color TEXT,
                                price REAL,
                                quantity INTEGER
                            )''')
        self.connection.commit()

        messagebox.showinfo("Éxito", "Tabla de productos creada correctamente")

        # Interfaz gráfica
        self.label_name = ttk.Label(root, text="Indumentaria:", style='Custom.TLabel')
        self.label_name.grid(row=0, column=0)
        self.entry_name = ttk.Entry(root)
        self.entry_name.grid(row=0, column=1)

        self.label_brand = ttk.Label(root, text="Marca:", style='Custom.TLabel')
        self.label_brand.grid(row=0, column=2)
        self.entry_brand = ttk.Entry(root)
        self.entry_brand.grid(row=0, column=3)

        self.label_size = ttk.Label(root, text="Talle:", style='Custom.TLabel')
        self.label_size.grid(row=1, column=0)
        self.entry_size = ttk.Entry(root)
        self.entry_size.grid(row=1, column=1)

        self.label_color = ttk.Label(root, text="Color:", style='Custom.TLabel')
        self.label_color.grid(row=1, column=2)
        self.entry_color = ttk.Entry(root)
        self.entry_color.grid(row=1, column=3)

        self.label_price = ttk.Label(root, text="Precio:", style='Custom.TLabel')
        self.label_price.grid(row=2, column=0)
        self.entry_price = ttk.Entry(root)
        self.entry_price.grid(row=2, column=1)

        self.label_quantity = ttk.Label(root, text="Cantidad:", style='Custom.TLabel')
        self.label_quantity.grid(row=2, column=2)
        self.entry_quantity = ttk.Entry(root)
        self.entry_quantity.grid(row=2, column=3)

        # Espacio en blanco
        self.empty_label = ttk.Label(root, text="")
        self.empty_label.grid(row=3, column=0, columnspan=4)

        # Botones con estilo personalizado
        self.btn_add = ttk.Button(root, text="Agregar Producto", style='Horizontal.TButton', command=self.add_product)
        self.btn_add.grid(row=4, column=0)

        self.btn_update = ttk.Button(root, text="Actualizar Producto", style='Horizontal.TButton', command=self.update_product)
        self.btn_update.grid(row=4, column=1)

        self.btn_delete = ttk.Button(root, text="Eliminar Producto", style='Horizontal.TButton', command=self.delete_product)
        self.btn_delete.grid(row=4, column=2)

        self.btn_search = ttk.Button(root, text="Buscar Producto", style='Horizontal.TButton', command=self.search_product)
        self.btn_search.grid(row=4, column=3)

        # Espacio en blanco
        self.empty_label = ttk.Label(root, text="")
        self.empty_label.grid(row=5, column=0, columnspan=4)

        self.btn_show = ttk.Button(root, text="Mostrar Productos", style='Horizontal.TButton', command=self.show_products)
        self.btn_show.grid(row=6, column=0, columnspan=4)

    def add_product(self):
        name = self.entry_name.get()
        brand = self.entry_brand.get()
        size = self.entry_size.get()
        color = self.entry_color.get()
        price = self.entry_price.get()
        quantity = self.entry_quantity.get()

        # Validación de datos
        if not name or not brand or not size or not color or not price or not quantity:
            messagebox.showerror("Error", "Por favor completa todos los campos")
            return

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Precio y cantidad deben ser números")
            return

        # Insertar producto en la base de datos
        self.cursor.execute("INSERT INTO products (name, brand, size, color, price, quantity) VALUES (?, ?, ?, ?, ?, ?)",
                            (name, brand, size, color, price, quantity))
        self.connection.commit()

        messagebox.showinfo("Éxito", "Producto agregado correctamente")

    def update_product(self):
        # Obtener datos del producto a actualizar
        name = self.entry_name.get()
        brand = self.entry_brand.get()
        size = self.entry_size.get()
        color = self.entry_color.get()
        price = self.entry_price.get()
        quantity = self.entry_quantity.get()

        # Validación de datos
        if not name:
            messagebox.showerror("Error", "Ingrese un nombre de producto para buscar")
            return

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Precio y cantidad deben ser números")
            return

        # Actualizar producto en la base de datos
        self.cursor.execute("UPDATE products SET brand=?, size=?, color=?, price=?, quantity=? WHERE name=?",
                            (brand, size, color, price, quantity, name))
        self.connection.commit()

        messagebox.showinfo("Éxito", "Producto actualizado correctamente")

    def delete_product(self):
        # Obtener el nombre del producto a eliminar
        name = self.entry_name.get()

        # Validación de datos
        if not name:
            messagebox.showerror("Error", "Ingrese un nombre de producto para eliminar")
            return

        # Eliminar producto de la base de datos
        self.cursor.execute("DELETE FROM products WHERE name=?", (name,))
        self.connection.commit()

        messagebox.showinfo("Éxito", "Producto eliminado correctamente")

    def search_product(self):
        # Obtener el nombre del producto a buscar
        name = self.entry_name.get()

        # Validación de datos
        if not name:
            messagebox.showerror("Error", "Ingrese un nombre de producto para buscar")
            return

        # Buscar producto en la base de datos
        self.cursor.execute("SELECT * FROM products WHERE name=?", (name,))
        product = self.cursor.fetchone()

        if product:
            messagebox.showinfo("Producto Encontrado", f"Nombre: {product[1]}\nMarca: {product[2]}\nTalle: {product[3]}\nColor: {product[4]}\nPrecio: {product[5]}\nCantidad: {product[6]}")
        else:
            messagebox.showerror("Error", "Producto no encontrado")

    def show_products(self):
        self.products_window = tk.Toplevel(self.root)
        self.products_window.title("Lista de Productos")

        self.listbox_frame = ttk.Frame(self.products_window)
        self.listbox_frame.pack(padx=10, pady=10)

        self.listbox_scrollbar = ttk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.listbox_frame, width=80, height=15, yscrollcommand=self.listbox_scrollbar.set)
        self.listbox_scrollbar.config(command=self.listbox.yview)
        self.listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Obtener productos de la base de datos y mostrarlos en la lista
        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()
        for product in products:
            self.listbox.insert(tk.END, f"{product[1]} - {product[2]} - {product[3]} - {product[4]} - {product[5]} - {product[6]}")


def add_product(self):
    name = self.entry_name.get()
    brand = self.entry_brand.get()
    size = self.entry_size.get()
    color = self.entry_color.get()
    price = self.entry_price.get()
    quantity = self.entry_quantity.get()

    # Imprimir los datos para diagnóstico
    print("Name:", name)
    print("Brand:", brand)
    print("Size:", size)
    print("Color:", color)
    print("Price:", price)
    print("Quantity:", quantity)

    # Validación de datos
    if not name or not brand or not size or not color or not price or not quantity:
        messagebox.showerror("Error", "Por favor completa todos los campos")
        return

    try:
        price = float(price)
        quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Error", "Precio y cantidad deben ser números")
        return

    # Insertar producto en la base de datos
    self.cursor.execute("INSERT INTO products (name, brand, size, color, price, quantity) VALUES (?, ?, ?, ?, ?, ?)",
                        (name, brand, size, color, price, quantity))
    self.connection.commit()

    messagebox.showinfo("Éxito", "Producto agregado correctamente")
# Crear y correr la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
   

