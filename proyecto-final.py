import tkinter as tk
from tkinter import messagebox
import requests
import datetime
import os

# URL del servidor PHP que maneja la lógica del chatbot.
URL_PHP = "https://leoviquez.com/IproyectoIntro/"

ventana_conversaciones = None
listbox = None
Chat_ids = []
conversacion = [
    {"role": "system", "content": "Eres un asistente útil y conversacional."}
]


usuarios = [
    {"id": 1, "user": "user1"},
]

data = [
    {
        "user_id": 1,
        "chats": [
            {
                "chat_id": 1,
                "chat_date": "2023-06-12",
                "chat_string": [
                    {"role": "user", "content": "Hola, ¿me podrías contar quién ganó el último partido de la Champions League?"}, 
                    {"role": "bot", "content": "¡Claro! El último partido de la Champions League se jugó el 10 de junio de 2023 entre el Manchester City y el Inter de Milán en Estambul."},
                    {"role": "user", "content": "¿Y cómo fue el partido? ¿Hubo alguna jugada interesante?"}, 
                    {"role": "bot", "content": "Fue un partido muy reñido. Manchester City ganó 2-1, pero el Inter estuvo cerca de empatar. El gol de la victoria lo marcó Rodri en el minuto 68. Hubo una gran jugada de Kevin De Bruyne, que dio la asistencia para el primer gol."},
                    {"role": "user", "content": "Suena emocionante. ¿De qué equipo se espera más para la próxima temporada?"}, 
                    {"role": "bot", "content": "El Manchester City sigue siendo uno de los favoritos, pero el Real Madrid y el Bayern Munich también son muy fuertes. El mercado de fichajes siempre cambia mucho, así que será interesante ver cómo se refuerzan los equipos."},
                    {"role": "user", "content": "Entonces, ¿crees que City repetirá el título?"}, 
                    {"role": "bot", "content": "Es difícil decirlo, pero si mantienen su plantilla y siguen con el rendimiento que tuvieron en 2023, es probable que sigan siendo contendientes fuertes. Aunque la competencia siempre es feroz."}
                ]
            },
            {
                "chat_id": 2,
                "chat_date": "2025-04-11",
                "chat_string": [
                    {"role": "user", "content": "¿Qué es la teoría de la relatividad? Siempre he oído hablar de ella, pero nunca entendí bien de qué trata."}, 
                    {"role": "bot", "content": "La teoría de la relatividad es una teoría física propuesta por Albert Einstein a principios del siglo XX. En términos simples, explica cómo el espacio y el tiempo están interrelacionados y cómo son afectados por la velocidad y la gravedad."},
                    {"role": "user", "content": "¿Cómo afecta la velocidad y la gravedad al espacio-tiempo? ¿De qué manera se puede ver eso en la vida cotidiana?"}, 
                    {"role": "bot", "content": "La relatividad especial, que es una parte de la teoría, dice que a medida que un objeto se mueve más rápido, el tiempo para ese objeto pasa más lentamente en comparación con un observador que está en reposo. Esto se conoce como dilatación del tiempo."},
                    {"role": "user", "content": "¡Eso suena raro! ¿Un reloj que se mueve a gran velocidad podría atrasarse?"}, 
                    {"role": "bot", "content": "Exactamente. Si pudieras viajar a una velocidad cercana a la de la luz, tu reloj avanzaría más lentamente en comparación con un reloj que permanece en reposo. Este efecto ha sido comprobado en experimentos con partículas subatómicas."},
                    {"role": "user", "content": "Y, ¿qué pasa con la gravedad? ¿Cómo afecta la relatividad general?"}, 
                    {"role": "bot", "content": "La relatividad general es la parte de la teoría que trata sobre cómo la gravedad afecta al espacio-tiempo. Según Einstein, la gravedad no es simplemente una fuerza, sino una curvatura del espacio-tiempo causada por la presencia de masa o energía. Por ejemplo, la Tierra curva el espacio-tiempo, y por eso los objetos caen hacia ella."},
                    {"role": "user", "content": "Eso explica mucho. ¿Hay alguna evidencia de esto en el mundo real?"}, 
                    {"role": "bot", "content": "Sí, hay varias pruebas experimentales que respaldan la teoría. Un ejemplo famoso es la observación de cómo la luz de las estrellas se curva al pasar cerca del Sol, un fenómeno conocido como 'lentes gravitacionales'. Además, los satélites GPS deben tener en cuenta la relatividad para dar la hora exacta."},
                    {"role": "user", "content": "Es fascinante cómo algo tan abstracto como el espacio-tiempo puede tener tantas aplicaciones en la vida real."}, 
                    {"role": "bot", "content": "¡Definitivamente! La relatividad ha cambiado nuestra comprensión del universo y sigue siendo fundamental para muchas tecnologías modernas."}
                ]
            }
        ]
    },
]


def chat_con_php(mensaje:str)->str:
    """
    Envía el historial de la conversación a un servidor PHP y recibe la respuesta del asistente.
    
    Args:
        mensaje (str): Entrada del user que será enviada al servidor.

    Returns:
        str: Respuesta generada por el asistente en el servidor PHP o mensaje de error.
    """
    # Se añade el mensaje del user al historial de la conversación.
    conversacion.append({"role": "user", "content": mensaje + ', se conciso con tu respuesta.'})

    try:
        # Se envía una solicitud POST al servidor PHP con el historial de conversación en formato JSON.
        respuesta = requests.post(URL_PHP, json={"messages": conversacion})
        
        # Se intenta convertir la respuesta en formato JSON.
        respuesta_json = respuesta.json()
        
        # Extrae el contenido de la respuesta generada por el asistente.
        mensaje_respuesta = respuesta_json["choices"][0]["message"]["content"]
        
        # Se añade la respuesta del asistente al historial de la conversación.
        conversacion.append({"role": "assistant", "content": mensaje_respuesta})
        
        return mensaje_respuesta  # Se retorna el mensaje de respuesta del asistente.
    
    except Exception as e:
        # En caso de error (por ejemplo, problemas de conexión), se devuelve un mensaje de error.
        return f"Error al conectar con el servidor: {e}"
    
def cerrar_sesion():
    """cierra la ventana en la que se esta trabajando
    """
    
    global usuario_actual, ventana_conversaciones
    usuario_actual = None
    ventana_conversaciones.withdraw()
    salvar_chats()
    main()



def obtener_conversaciones(usuario_id):
    """obtiene las conversacion del usuario que a tenido

    Args:
        usuario_id (type): usuario a esta utilizando el programa en el momento

    Returns:
        type: retorna los chats del usuario o retorna un vacio
    """
    for i in data:
        if i["user_id"] == usuario_id:
            return i["chats"]
    return []

def string_conversaciones(lista):
    """obtiene los chats y los convierte a un solo str

    Args:
        lista (type): la lista donde se alamacena las preguntas y respuestas

    Returns:
        type: description
    """
    mensajes = []
    for msg in lista:
        if msg["role"] == "user":
            mensajes.append("Tú: " + msg["content"])
        else:
            mensajes.append("Bot: " + msg["content"])
    return " ".join(mensajes)

def generar_resumen():
    """genera un resumen de la conversacion que se le pide 
    """
    global VentanaResumen, usuario_actual

    VentanaResumen = tk.Toplevel()
    VentanaResumen.title("Resumen conversacion")
    Chat_Area = tk.Text(VentanaResumen, height=15, width=50, state=tk.NORMAL)
    Chat_Area.pack()
    seleccion = listbox.curselection()
    if seleccion:
        chat_id = Chat_ids[seleccion[0]]
        for user in data:
            if user["user_id"] == usuario_actual:
                for chat in user["chats"]:
                    if chat["chat_id"] == chat_id:
                        lista = chat["chat_string"]
                        full_string = string_conversaciones(lista)
                        respuesta = chat_con_php('Chat, generame un resumen de un maximo de 50 palabras de la siguiente conversacion: ' + full_string)
                        Chat_Area.insert(tk.END, respuesta)
                        print(f"Generando resumen para el chat ID: {lista}")
    def cerrar():
        """cierra la ventana que se estaba usando al usar tkinter
        """
        VentanaResumen.destroy()

    BotonCerrar = tk.Button(VentanaResumen, text="Cerrar", command=cerrar)
    BotonCerrar.pack()

def actualizar_lista_conversaciones(buscar_termino=None):
    """Actualiza la lista de conversaciones, opcionalmente filtrando por un término de búsqueda."""
    global Chat_ids
    listbox.delete(0, tk.END)
    Chat_ids = []
    conversaciones = obtener_conversaciones(usuario_actual)
    conversaciones.sort(key=lambda chat: datetime.datetime.strptime(chat['chat_date'], "%Y-%m-%d"), reverse=True)
    
    for chat in conversaciones:
        chat_string = string_conversaciones(chat["chat_string"])
        if buscar_termino is None or buscar_termino.lower() in chat_string.lower():
            listbox.insert(tk.END, f"Conversación {chat['chat_id']} - {chat['chat_date']}")
            Chat_ids.append(chat['chat_id'])
    print(Chat_ids)

def obtener_usuario_actual():
    """se busca en la lista de usuarios el usuario que esta ejecutando el programa ene se momento

    Returns:
        type: el usuario que lo esta ejecutando
    """
    global usuario_actual
    for user in usuarios:
        if user["id"] == usuario_actual:
            return user["user"]
def buscar_conversaciones():
    """Filtra las conversaciones según el término de búsqueda ingresado."""
    buscar_termino = entrada_busqueda.get()
    actualizar_lista_conversaciones(buscar_termino)
def mostrar_conversaciones():
    """Muestra la ventana de conversaciones previas."""
    global ventana_conversaciones, listbox, entrada_busqueda
    if ventana_conversaciones:
        ventana_conversaciones.deiconify()
        actualizar_lista_conversaciones()
        return
    
    ventana_conversaciones = tk.Tk()
    ventana_conversaciones.title("Conversaciones Previas")
    nombre_usuario = obtener_usuario_actual()
    tk.Label(ventana_conversaciones, text=f"Conversaciones de Usuario {nombre_usuario}").pack()
    
    buscar_frame = tk.Frame(ventana_conversaciones)
    buscar_frame.pack()
    entrada_busqueda = tk.Entry(buscar_frame)
    entrada_busqueda.pack(side=tk.LEFT)
    buscar_boton = tk.Button(buscar_frame, text="Buscar", command=buscar_conversaciones)
    buscar_boton.pack(side=tk.LEFT)
    
    listbox = tk.Listbox(ventana_conversaciones)
    listbox.pack()
    
    actualizar_lista_conversaciones()
    
    BotonResumen = tk.Button(ventana_conversaciones, text="Generar Resumen", command=generar_resumen)
    BotonResumen.pack()
    
    BotonNuevaConversacion = tk.Button(ventana_conversaciones, text="Nueva Conversación", command=abrir_chat)
    BotonNuevaConversacion.pack()

    BotonVerMas = tk.Button(ventana_conversaciones, text="Ver Más", command=ver_conversacion_completa)
    BotonVerMas.pack()

    BotonCerrar_cesion = tk.Button(ventana_conversaciones, text="Cerrar Sesión", command=cerrar_sesion, bg="red")
    BotonCerrar_cesion.pack()
    
    ventana_conversaciones.mainloop()

def ver_conversacion_completa():
    """funcion que hace que el usuario pueda volver a ver toda la conversacion que tuvo con el asistente
    """
    global Chat_ids, usuario_actual
    seleccion = listbox.curselection()
    if seleccion:
        chat_id = Chat_ids[seleccion[0]]
        for user in data:
            print("Usuario actual:", usuario_actual)
            print("Usuario en data:", user["user_id"])
            if user["user_id"] == usuario_actual:
                for chat in user["chats"]:
                    if chat["chat_id"] == chat_id:
                        mostrar_chat_completo(chat["chat_string"])


def mostrar_chat_completo(chat_string):
    """se muestra la conversacion que haya tenido el usuario con el asistente

    Args:
        chat_string (_type_): los chats de este usuario
    """
    ventana_completa = tk.Toplevel()
    ventana_completa.title("Conversación Completa")
    
    Chat_Area = tk.Text(ventana_completa, height=15, width=50, state=tk.NORMAL, padx=20, pady=40)
    Chat_Area.pack()
    
    for mensaje in chat_string:
        if mensaje["role"] == "user":
            Chat_Area.insert(tk.END, f"Tú: {mensaje['content']}\n")
        else:
            Chat_Area.insert(tk.END, f"Bot: {mensaje['content']}\n")

    Chat_Area.config(state=tk.DISABLED)
    
def enviar_mensaje(mensaje):
    """funcion que envia los mensajes a la funcion php

    Args:
        mensaje (type): el mensaje que se escribio

    Returns:
        type: retorna la respuesta a esa misma pregunta
    """
    result = chat_con_php(mensaje)
    return result

def salvar_chats():
    """funcion que guarda los chats de las personas que estan usando el programa y las guarda en archivo de texto
    """
    if not os.path.exists("chats"):
        os.mkdir("chats")

    lista_usuarios = {}
    for usuario in usuarios:
        lista_usuarios[usuario["id"]] = usuario["user"]

    for usuario in data:
        id_usuario = usuario["user_id"]

        if id_usuario in lista_usuarios:
            nombre_usuario = lista_usuarios[id_usuario]
        else:
            nombre_usuario = "user_" + str(id_usuario)

        ruta_usuario = "chats/" + nombre_usuario
        if not os.path.exists(ruta_usuario):
            os.mkdir(ruta_usuario)

        for chat in usuario["chats"]:
            id_chat = chat["chat_id"]
            mensajes = chat["chat_string"]

            ruta_chat = ruta_usuario + "/chat_" + str(id_chat) + ".txt"

            with open(ruta_chat, "w", encoding="utf-8") as archivo:
                for mensaje in mensajes:
                    if mensaje["role"] == "user":
                        archivo.write("Tú: " + mensaje["content"] + "\n")
                    else:
                        archivo.write("Bot: " + mensaje["content"] + "\n")

    print("Todos los chats se han guardado.")

def abrir_chat():
    """funcion que abre el chat del programa con tkinter
    """
    print("Abriendo chat...")
    print(usuarios)
    print(data)
    global usuario_actual, ventana_chat
    ventana_conversaciones.withdraw()
    ventana_chat = tk.Toplevel()
    ventana_chat.title("Chat")
    
    Chat_Area = tk.Text(ventana_chat, height=15, width=50, state=tk.DISABLED, padx=40)
    Chat_Area.pack()
    
    MensajeEntrada = tk.Entry(ventana_chat)
    MensajeEntrada.pack()
    
    date = datetime.datetime.now()
    format_date = date.strftime("%Y-%m-%d")

    Nuevo_Chat = {"chat_id": len(obtener_conversaciones(usuario_actual)) + 1, "chat_date": format_date,  "chat_string": []}
    
    def enviar():
        """muestra las  preguntas y las respuestas en la interfaz grafica con las especificaciones que se le pide
        """
        mensaje = MensajeEntrada.get()
        if mensaje:
            Chat_Area.config(state=tk.NORMAL)
            Chat_Area.insert(tk.END, f"Tú:{mensaje}\n","derecha"              )
            Nuevo_Chat["chat_string"].append({"role": "user", "content": mensaje})
            
            respuesta = enviar_mensaje(mensaje)
            Chat_Area.insert(tk.END, f"Bot:   {respuesta}\n","izquierda")
            Nuevo_Chat["chat_string"].append({"role": "bot", "content": respuesta})
            
            Chat_Area.config(state=tk.DISABLED)
            MensajeEntrada.delete(0, tk.END)
    
    def guardar_chat():
        """esta funcion guarda los chats que el usuario en cuestion quiera guardar en un archivo
        """
        print("Nuevo Chat guardado")
        print(Nuevo_Chat)
        global usuario_actual
        print("Guardando chat...")
        print(usuarios)
        
        for user in data:
            print("Usuario actual:", usuario_actual)
            print("Usuario en data:", user["user_id"])
            if user["user_id"] == usuario_actual:
                user["chats"].append(Nuevo_Chat)
                print("Chat guardado:", Nuevo_Chat)
                print("Datos actualizados:", data)
                break
            else:
                print("Usuario no encontrado en los datos.")
            print(usuarios)

        ventana_chat.destroy()
        mostrar_conversaciones()    

    Chat_Area.tag_configure("izquierda", justify="left")
    Chat_Area.tag_configure("derecha", justify="right")
    
    botonEnviar = tk.Button(ventana_chat, text="Enviar", command=enviar)
    botonEnviar.pack()
    
    botonGuardar = tk.Button(ventana_chat, text="Guardar", command=guardar_chat, bg="lightblue")
    botonGuardar.pack(side=tk.RIGHT, padx=10)
    
    ventana_chat.mainloop()

def login():
    """inicia sesion con un usario que ya esta registrado
    """
    global usuario_actual
    NombreUsuario = entry_usuario.get()
    for user in usuarios:
        if user["user"] == NombreUsuario:
            usuario_actual = user["id"]
            print(f"Usuario actual: {NombreUsuario} (ID: {usuario_actual})")
            ventana_login.destroy()
            mostrar_conversaciones()
            return
    
    messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def signup():
    """esto registra nuevos usuarios que quieran usar el programa
    """
    ventana_signup = tk.Toplevel()
    ventana_signup.title("Registro")

    tk.Label(ventana_signup, text="Nuevo Usuario:").pack()
    entry_nuevo = tk.Entry(ventana_signup)
    entry_nuevo.pack()

    def registrar():
        NombreUsuario = entry_nuevo.get() 

        if not NombreUsuario:
            messagebox.showerror("Error", "El nombre de user no puede estar vacío")
            return
        
        for user in usuarios:
            if user["user"] == NombreUsuario:
                messagebox.showerror("Error", "El user ya existe")
                return

        Nuevoid = len(usuarios) + 1
        usuarios.append({"id": Nuevoid, "user": NombreUsuario})
        data.append({"user_id": Nuevoid, "chats": []})
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        ventana_signup.destroy()

    BotonCrear = tk.Button(ventana_signup, text="Registrar", command=registrar)
    BotonCrear.pack()

def main():
    """la primera ventana que ve el usuario a la hora de ejecutar el programa
    """
    global ventana_login, entry_usuario
    ventana_login = tk.Tk()
    ventana_login.title("Login")
    
    tk.Label(ventana_login, text="Usuario:").pack()
    entry_usuario = tk.Entry(ventana_login)
    entry_usuario.pack()
    
    tk.Button(ventana_login, text="Login", command=login).pack()
    tk.Button(ventana_login, text="Signup", command=signup).pack()
    
    ventana_login.mainloop()


if __name__ == "__main__":
    main()