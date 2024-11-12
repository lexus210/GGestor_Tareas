import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk  # Asegúrate de tener instalada la librería usando: pip install ttkbootstrap

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

class GestorTareasApp:
    def __init__(self, root, gestor):
        self.gestor = gestor
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

        # Listbox de tareas con scrollbar
        self.tareas_frame = ttk.Frame(root)
        self.tareas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tareas_listbox = tk.Listbox(self.tareas_frame, height=8, font=("Helvetica", 10))
        self.tareas_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tareas_listbox.bind("<<ListboxSelect>>", self.mostrar_descripcion)

        scrollbar = ttk.Scrollbar(self.tareas_frame, orient="vertical", command=self.tareas_listbox.yview)
        self.tareas_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Área de texto para la descripción de la tarea seleccionada
        ttk.Label(root, text="Descripción de la Tarea Seleccionada:", font=("Helvetica", 12)).pack(pady=5)
        self.descripcion_text = tk.Text(root, height=4, font=("Helvetica", 10), wrap="word", state="disabled")
        self.descripcion_text.pack(fill=tk.X, padx=10, pady=5)

        # Botón para marcar como completada
        ttk.Button(root, text="Marcar como Completada", command=self.marcar_completada, bootstyle="success-outline").pack(pady=5)

        # Configurar cierre de ventana con confirmación
        self.root.protocol("WM_DELETE_WINDOW", self.confirmar_salida)

    def confirmar_salida(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas salir de la aplicación?"):
            self.root.destroy()

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
    app = GestorTareasApp(root, gestor)
    root.mainloop()


if __name__ == "__main__":
    run()