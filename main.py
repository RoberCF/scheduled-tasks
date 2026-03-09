import datetime as dt
import pandas as pd
import smtplib
from email.message import EmailMessage
from random import choice
import os

# Comprobamos la fecha actual y la guardamos
fecha = dt.datetime.now()
fecha_hoy = (fecha.month, fecha.day)

# Comprobamos si la fecha actual coincide con el cumpleaños de alguna persona en el listado csv
listado_personas = pd.read_csv("lista_cumpleaños.csv")

diccionario = {(datos_fila.mes, datos_fila.dia): datos_fila for (index, datos_fila) in listado_personas.iterrows()}

if fecha_hoy in diccionario:
    datos_cumpleañero = diccionario[fecha_hoy]

    # Abrimos una carta al azar, y generamos otra nueva temporal con el nombre del cumpleañero
    cartas = ["./plantillas_correo/carta_1.txt", "./plantillas_correo/carta_2.txt", "./plantillas_correo/carta_3.txt"]
    carta_al_azar = choice(cartas)
    with open(carta_al_azar, mode="r") as carta:
        carta_original = carta.read()

    # Guardamos una copia modificaca de la original con el nombre asignado
    carta_personal = carta_original.replace("[NOMBRE]", datos_cumpleañero["nombre"])

    # Enviamos el correo de felicitación a la persona indicada
    mi_correo = os.environ.get("mi_correo")
    mi_contraseña = os.environ.get("mi_contraseña")

    # Datos contenido del correo
    mensaje = EmailMessage()
    mensaje["Subject"] = "¡Feliz Cumpleaños!"
    mensaje["From"] = mi_correo
    mensaje["To"] = datos_cumpleañero["email"]
    mensaje.set_content(carta_personal)

    # Abrimos, como si fuera un archivo, la conexión con nuestro servidor de correo
    with smtplib.SMTP("smtp.gmail.com", port=587) as conexion:
        conexion.starttls() # Protejemos encriptando nuestro correo
        conexion.login(user=mi_correo, password=mi_contraseña)
        conexion.send_message(mensaje)







