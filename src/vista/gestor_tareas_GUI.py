import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk  # Asegúrate de tener instalada la librería

class GestorTareasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("500x400")
        self.root.style = ttk.Style("darkly")  # Cambia el tema aquí

        # Título y descripción de tarea
        ttk.Label(root, text="Título de la Tarea", font=("Helvetica", 12)).pack(pady=5)
        self.titulo_entry = ttk.Entry(root, font=("Helvetica", 10))
        self.titulo_entry.pack(fill=tk.X, padx=10)

        ttk.Label(root, text="Descripción", font=("Helvetica", 12)).pack(pady=5)
        self.descripcion_entry = ttk.Entry(root, font=("Helvetica", 10))
        self.descripcion_entry.pack(fill=tk.X, padx=10)

        # Botones con estilo
        frame_buttons = ttk.Frame(root)
        frame_buttons.pack(pady=10)
        ttk.Button(frame_buttons, text="Agregar Tarea", command=self.agregar_tarea, bootstyle="success-outline").pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Eliminar Tarea", command=self.eliminar_tarea, bootstyle="danger-outline").pack(side=tk.LEFT, padx=5)

        # Listbox de tareas
        self.tareas_listbox = tk.Listbox(root, height=10, font=("Helvetica", 10))
        self.tareas_listbox.pack(fill=tk.BOTH, padx=10, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.confirmar_salida)

    def agregar_tarea(self):
        titulo = self.titulo_entry.get()
        descripcion = self.descripcion_entry.get()
        if titulo:
            self.tareas_listbox.insert(tk.END, f"{titulo} - {descripcion}")
            self.titulo_entry.delete(0, tk.END)
            self.descripcion_entry.delete(0, tk.END)

    def eliminar_tarea(self):
        seleccion = self.tareas_listbox.curselection()
        if seleccion:
            self.tareas_listbox.delete(seleccion[0])

    def confirmar_salida(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas salir de la aplicación?"):
            self.root.destroy()

root = tk.Tk()
app = GestorTareasApp(root)
root.mainloop()
