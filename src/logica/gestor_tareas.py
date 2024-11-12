import tkinter as tk
from tkinter import ttk, messagebox

class Tarea:
    def __init__(self, titulo, descripcion):
        self.titulo = titulo
        self.descripcion = descripcion
        self.completada = False

class GestorTareas:
    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, titulo, descripcion):
        if not titulo:
            raise ValueError("El título no puede estar vacío")
        tarea = Tarea(titulo, descripcion)
        self.tareas.append(tarea)

    def obtener_tareas(self):
        return self.tareas

    def marcar_completada(self, indice):
        if 0 <= indice < len(self.tareas):
            self.tareas[indice].completada = True
        else:
            raise IndexError("Índice fuera de rango")

    def eliminar_tarea(self, indice):
        if 0 <= indice < len(self.tareas):
            del self.tareas[indice]
        else:
            raise IndexError("Índice fuera de rango")

class GestorTareasGUI:
    def __init__(self, root, gestor):
        self.gestor = gestor
        self.root = root
        self.root.title("Gestor de Tareas")

        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.titulo_entry = ttk.Entry(self.frame, width=20)
        self.titulo_entry.grid(row=0, column=1, sticky=tk.W)

        self.descripcion_entry = ttk.Entry(self.frame, width=50)
        self.descripcion_entry.grid(row=1, column=1, sticky=tk.W)

        self.agregar_btn = ttk.Button(self.frame, text="Agregar Tarea", command=self.agregar_tarea)
        self.agregar_btn.grid(row=2, column=1, sticky=tk.W)

        self.tareas_listbox = tk.Listbox(self.frame, height=10, width=50)
        self.tareas_listbox.grid(row=3, column=1, sticky=tk.W)

        self.completar_btn = ttk.Button(self.frame, text="Marcar como Completada", command=self.marcar_completada)
        self.completar_btn.grid(row=4, column=1, sticky=tk.W)

        self.eliminar_btn = ttk.Button(self.frame, text="Eliminar Tarea", command=self.eliminar_tarea)
        self.eliminar_btn.grid(row=5, column=1, sticky=tk.W)

        self.actualizar_lista()

    def agregar_tarea(self):
        titulo = self.titulo_entry.get()
        descripcion = self.descripcion_entry.get()
        try:
            self.gestor.agregar_tarea(titulo, descripcion)
            self.actualizar_lista()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def actualizar_lista(self):
        self.tareas_listbox.delete(0, tk.END)
        for indice, tarea in enumerate(self.gestor.obtener_tareas()):
            estado = "Completada" if tarea.completada else "Pendiente"
            self.tareas_listbox.insert(tk.END, f"{indice + 1}. {tarea.titulo} - {estado}")

    def marcar_completada(self):
        seleccion = self.tareas_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            self.gestor.marcar_completada(indice)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para marcar como completada")

    def eliminar_tarea(self):
        seleccion = self.tareas_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            self.gestor.eliminar_tarea(indice)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para eliminar")

def run():
    root = tk.Tk()
    gestor = GestorTareas()
    app = GestorTareasGUI(root, gestor)
    root.mainloop()

if __name__ == "__main__":
    run()
