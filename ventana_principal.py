'''
Sistema de Gestión de Pescaderías
CREADO EN MAYOR PARTE CON IA DE TECNOLOGÍA VERSEL V0
24/10/2024 11:35 añado este comentario para comprobar los commit en GitHub
'''
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time
import datetime

# Import CRUD modules
from crud_artes import CrudArtes
from crud_especies import CrudEspecies
from crud_expedidores import CrudExpedidores
from crud_metodos import CrudMetodos
from crud_producciones import CrudProducciones
from crud_proveedores import CrudProveedores
from crud_zonas import CrudZonas
from crud_barcos import CrudBarcos
from crud_usuarios import CrudUsuarios
from conexion_db import get_db_connection

class VentanaPrincipal:
    def __init__(self, master=None):
        self.master = master or tk.Tk()
        self.master.title("Sistema de Gestión de Pescaderías")
        self.master.geometry("1000x700")

        # Almacenar el usuario actual
        self.usuario_actual = None

        # Crear un frame principal
        self.frame_principal = ttk.Frame(self.master)
        self.frame_principal.pack(expand=True, fill="both", padx=20, pady=20)

        # Cargar y mostrar la imagen
        self.cargar_imagen()

        # Añadir reloj y fecha
        self.label_reloj = tk.Label(self.frame_principal, font=('Arial', 20))
        self.label_reloj.pack(pady=5)
        self.label_fecha = tk.Label(self.frame_principal, font=('Arial', 14))
        self.label_fecha.pack(pady=5)
        self.actualizar_reloj_y_fecha()

        # Añadir texto de bienvenida
        self.label_bienvenida = tk.Label(self.frame_principal, text="Bienvenido al Sistema de Gestión de Pescaderías", font=('Arial', 16, 'bold'))
        self.label_bienvenida.pack(pady=20)

        # Añadir botones rápidos
        self.frame_botones = ttk.Frame(self.frame_principal)
        self.frame_botones.pack(pady=20)

        botones = [
            ("Gestionar Artes", self.abrir_crud_artes),
            ("Gestionar Especies", self.abrir_crud_especies),
            ("Gestionar Expedidores", self.abrir_crud_expedidores),
            ("Gestionar Métodos", self.abrir_crud_metodos),
            ("Gestionar Producciones", self.abrir_crud_producciones),
            ("Gestionar Proveedores", self.abrir_crud_proveedores),
            ("Gestionar Zonas", self.abrir_crud_zonas),
            ("Gestionar Barcos", self.abrir_crud_barcos)
        ]

        for i, (texto, comando) in enumerate(botones):
            ttk.Button(self.frame_botones, text=texto, command=comando).grid(row=i//4, column=i%4, padx=10, pady=5)

        # Añadir botón de salir
        self.btn_salir = ttk.Button(self.frame_principal, text="Salir", command=self.salir)
        self.btn_salir.pack(pady=20)

        # Crear menú
        self.crear_menu()

    def cargar_imagen(self):
        try:
            imagen = Image.open("logo_pes_png.png")
            imagen = imagen.resize((200, 200))  # Ajusta el tamaño según sea necesario
            self.logo = ImageTk.PhotoImage(imagen)
            label_imagen = tk.Label(self.frame_principal, image=self.logo)
            label_imagen.pack(pady=20)
        except FileNotFoundError:
            print("No se pudo encontrar el archivo de imagen 'logo_pes.jpg'")

    def actualizar_reloj_y_fecha(self):
        hora_actual = time.strftime('%H:%M:%S')
        fecha_actual = datetime.date.today().strftime("%d/%m/%Y")
        self.label_reloj.config(text=hora_actual)
        self.label_fecha.config(text=fecha_actual)
        self.master.after(1000, self.actualizar_reloj_y_fecha)  # Actualizar cada segundo

    def crear_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        crud_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="CRUD", menu=crud_menu)

        crud_menu.add_command(label="Artes", command=self.abrir_crud_artes)
        crud_menu.add_command(label="Especies", command=self.abrir_crud_especies)
        crud_menu.add_command(label="Expedidores", command=self.abrir_crud_expedidores)
        crud_menu.add_command(label="Métodos", command=self.abrir_crud_metodos)
        crud_menu.add_command(label="Producciones", command=self.abrir_crud_producciones)
        crud_menu.add_command(label="Proveedores", command=self.abrir_crud_proveedores)
        crud_menu.add_command(label="Zonas", command=self.abrir_crud_zonas)
        crud_menu.add_command(label="Barcos", command=self.abrir_crud_barcos)
        crud_menu.add_command(label="Usuarios", command=self.abrir_crud_usuarios)

    def abrir_crud_artes(self):
        CrudArtes(self.master)

    def abrir_crud_especies(self):
        CrudEspecies(self.master)

    def abrir_crud_expedidores(self):
        CrudExpedidores(self.master)

    def abrir_crud_metodos(self):
        CrudMetodos(self.master)

    def abrir_crud_producciones(self):
        CrudProducciones(self.master)

    def abrir_crud_proveedores(self):
        CrudProveedores(self.master)

    def abrir_crud_zonas(self):
        CrudZonas(self.master)

    def abrir_crud_barcos(self):
        CrudBarcos(self.master)

    def abrir_crud_usuarios(self):
        if self.confirmar_credenciales():
            CrudUsuarios(self.master)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas o insuficientes")

    def confirmar_credenciales(self):
        # Crear una ventana de diálogo para ingresar las credenciales
        dialog = tk.Toplevel(self.master)
        dialog.title("Confirmar Credenciales")
        dialog.geometry("300x200")
        dialog.resizable(False, False)

        tk.Label(dialog, text="Usuario:").pack(pady=5)
        entry_usuario = tk.Entry(dialog)
        entry_usuario.pack(pady=5)

        tk.Label(dialog, text="Contraseña:").pack(pady=5)
        entry_contrasena = tk.Entry(dialog, show="*")
        entry_contrasena.pack(pady=5)

        resultado = [False]  # Usamos una lista para poder modificar el valor desde dentro de la función

        def verificar():
            usuario = entry_usuario.get()
            contrasena = entry_contrasena.get()

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tabla_usuarios WHERE nombre_usuario = ? AND clave_usuario = ? AND rol_usuario = 'admin'", (usuario, contrasena))
            user = cursor.fetchone()
            conn.close()

            if user:
                resultado[0] = True
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas o usuario no es administrador")

        # Añadir botón de verificación
        tk.Button(dialog, text="Verificar", command=verificar).pack(pady=10)

        # Esperar hasta que se cierre la ventana de diálogo
        self.master.wait_window(dialog)

        return resultado[0]

    def salir(self):
        if messagebox.askyesno("Confirmar salida", "¿Está seguro que desea salir de la aplicación?"):
            self.master.quit()

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.master.mainloop()