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

        # Configuración de estilo
        self.root.geometry("500x400")
        style = ttk.Style()
        style.configure("TFrame", background="#f5f5f5")
        style.configure("TLabel", background="#f5f5f5", font=("Arial", 10))
        style.configure("TButton", background="#5DADE2", foreground="black", font=("Arial", 10, "bold"))
        style.map("TButton", background=[("active", "#3498DB")])

        # Marco principal
        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Campo de título
        ttk.Label(self.frame, text="Título de la Tarea:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.titulo_entry = ttk.Entry(self.frame, width=40)
        self.titulo_entry.grid(row=0, column=1, sticky=tk.W)

        # Campo de descripción
        ttk.Label(self.frame, text="Descripción:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.descripcion_entry = ttk.Entry(self.frame, width=40)
        self.descripcion_entry.grid(row=1, column=1, sticky=tk.W)

        # Botón Agregar Tarea
        self.agregar_btn = ttk.Button(self.frame, text="Agregar Tarea", command=self.agregar_tarea)
        self.agregar_btn.grid(row=2, column=1, sticky=tk.W, pady=10)

        # Listbox de tareas con scrollbar
        self.tareas_frame = ttk.Frame(self.frame)
        self.tareas_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        self.tareas_listbox = tk.Listbox(self.tareas_frame, height=8, width=40, font=("Arial", 10))
        self.tareas_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.tareas_listbox.bind("<<ListboxSelect>>", self.mostrar_descripcion)

        scrollbar = ttk.Scrollbar(self.tareas_frame, orient="vertical", command=self.tareas_listbox.yview)
        self.tareas_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Área de texto para la descripción de la tarea seleccionada
        ttk.Label(self.frame, text="Descripción de la Tarea Seleccionada:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.descripcion_text = tk.Text(self.frame, height=4, width=50, font=("Arial", 10), wrap="word", state="disabled")
        self.descripcion_text.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # Botones de acciones
        self.completar_btn = ttk.Button(self.frame, text="Marcar como Completada", command=self.marcar_completada)
        self.completar_btn.grid(row=6, column=0, pady=5, sticky=tk.W)

        self.eliminar_btn = ttk.Button(self.frame, text="Eliminar Tarea", command=self.eliminar_tarea)
        self.eliminar_btn.grid(row=6, column=1, pady=5, sticky=tk.E)

        # Actualizar lista inicial
        self.actualizar_lista()

    def agregar_tarea(self):
        titulo = self.titulo_entry.get()
        descripcion = self.descripcion_entry.get()
        try:
            self.gestor.agregar_tarea(titulo, descripcion)
            self.actualizar_lista()
            self.titulo_entry.delete(0, tk.END)
            self.descripcion_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def actualizar_lista(self):
        self.tareas_listbox.delete(0, tk.END)
        for indice, tarea in enumerate(self.gestor.obtener_tareas()):
            estado = "Completada" if tarea.completada else "Pendiente"
            self.tareas_listbox.insert(tk.END, f"{indice + 1}. {tarea.titulo} - {estado}")

    def mostrar_descripcion(self, event):
        seleccion = self.tareas_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            tarea = self.gestor.obtener_tareas()[indice]
            self.descripcion_text.config(state="normal")
            self.descripcion_text.delete("1.0", tk.END)
            self.descripcion_text.insert(tk.END, tarea.descripcion)
            self.descripcion_text.config(state="disabled")

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
            self.descripcion_text.config(state="normal")
            self.descripcion_text.delete("1.0", tk.END)
            self.descripcion_text.config(state="disabled")
        else:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para eliminar")

def run():
    root = tk.Tk()
    gestor = GestorTareas()
    app = GestorTareasGUI(root, gestor)
    root.mainloop()

if __name__ == "__main__":
    run()
