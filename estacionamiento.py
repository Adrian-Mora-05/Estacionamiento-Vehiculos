"""Proyecto 3: Estacionamiento de Vehículos - Adrián Mora Rivera"""

# MÓDULOS
import os

import subprocess

from tkinter import *
import tkinter as tk

from tkinter import ttk

from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext

from dateutil.relativedelta import relativedelta #Para calcular el tiempo cobrado

import datetime

from datetime import datetime, timedelta #Para los registro de la hora y la fecha 

import math #Para redondear flotantes

from PIL import Image, ImageTk
import fitz
import copy #Para restaurar dicc_cajero si se Cancela cargarlo 
import io
import re # para usarlo para validar que los minutos de los goles estén bien escritos

import pickle # para ir guardando los datos ingresados por el usuario al usar el programa en archivos


#########################################################################



# DEFINICIÓN DE FUNCIONES SECUNDARIAS

"""1. CONFIGURACIÓN"""

#1.A. Función validate_cant_espacios para aceptar solo enteros >= 1
def validate_cant_espacios(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
    if action != '1':  # Si no es una acción de inserción, permitirla
        return True
    if value_if_allowed.isdigit() and int(value_if_allowed) >= 1:  # Permitir solo números mayores o iguales a 1
        return True
    else:
        return False

#1.B. Función validate_precio_hora para aceptar solo flotantes de máx. 2 decimales
def validate_precio_hora(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
    if action != '1':  # Si no es una acción de inserción, permitirla
        return True
    try:
        # Intentar convertir a float
        float_value = float(value_if_allowed)
        # Comprobar si hay más de 2 decimales
        if '.' in value_if_allowed:
            decimal_part = value_if_allowed.split('.')[1]
            if len(decimal_part) > 2:
                return False
        return True
    except ValueError:
        return False

#1.C. Función validate_pago_minimo para aceptar solo enteros >= 0
def validate_pago_minimo(action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
    if action != '1':  # Si no es una acción de inserción, permitirla
        return True
    if text.isdigit() and int(text) >= 0:  # Permitir solo dígitos mayores o iguales a 0
        return True
    else:
        return False


#1.D. Función validate_redondeo para aceptar solo enteros entre 0 y 60
def validate_redondeo(text):
    if text == "":
        return True
    if text.isdigit():
        value = int(text)
        if 0 <= value <= 60:
            return True
    return False


#1.E. Función validate_minutos_max para aceptar solo enteros >= 0
def validate_minutos_max(action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
    if action != '1':  # Si no es una acción de inserción, permitirla
        return True
    if text.isdigit() and int(text) >= 0:  # Permitir solo dígitos mayores o iguales a 0
        return True
    else:
        return False


#1.F. Función validate_moneda1 para permitir solo enteros >= 1
def validate_moneda1(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
    if action != '1':  # Permitir acciones que no sean de inserción
        return True
    if text.isdigit() and int(text) >= 0:  # Permitir solo dígitos mayores o iguales a 0
        return True
    return False

#1.G. Función validate_moneda2 para permitir solo 0 o enteros mayores a moneda1
def validate_moneda2(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
    if action != '1':  # Permitir acciones que no sean de inserción
        return True
    if text.isdigit() and int(text) >= 0:  # Permitir solo dígitos mayores o iguales a 0
        return True
    return False

#1.H. Función validate_moneda3 para permitir solo 0 o enteros mayores a moneda2
def validate_moneda3(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
    if action != '1':  # Permitir acciones que no sean de inserción
        return True
    if text.isdigit() and int(text) >= 0:  # Permitir solo dígitos mayores o iguales a 0
        return True
    return False

#1.I. Función check_moneda2 para detener los entry de monedas en caso de que se ponga 0 en moneda1
def check_moneda2(event=None):
    if input_moneda1.get().isdigit() and int(input_moneda1.get()) > 0:
        entry_moneda2.config(state='normal')
    else:
        input_moneda2.set("0")
        entry_moneda2.config(state='readonly')
        input_moneda3.set("0")
        entry_moneda3.config(state='readonly')

#1.J. Función check_moneda3 para detener los entry de monedas en caso de que se ponga 0 en moneda2
def check_moneda3(event=None):
    if input_moneda2.get().isdigit() and int(input_moneda2.get()) > 0:
        entry_moneda3.config(state='normal')
    else:
        input_moneda3.set("0")
        entry_moneda3.config(state='readonly')


#1.K. Función validate_billete1 para permitir solo enteros >= 0
def validate_billete1(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
    if action != '1':  # Permitir acciones que no sean de inserción
        return True
    if text.isdigit() and int(text) >= 0:  # Permitir solo dígitos mayores o iguales a 0
        return True
    return False

#1.L. Función validate_billete2 para permitir solo enteros >= 0
def validate_billete2(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
    if action != '1':  # Permitir acciones que no sean de inserción
        return True
    if text.isdigit() and int(text) >= 0:  # Permitir solo dígitos mayores o iguales a 0
        return True
    return False

#1.M. Función validate_billete3 para permitir solo enteros >= 0
def validate_billete3(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
    if action != '1':  # Permitir acciones que no sean de inserción
        return True
    if text.isdigit() and int(text) >= 0:  # Permitir solo dígitos mayores o iguales a 0
        return True
    return False

#1.N. Función validate_billete4 para permitir solo enteros >= 0
def validate_billete4(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
    if action != '1':  # Permitir acciones que no sean de inserción
        return True
    if text.isdigit() and int(text) >= 0:  # Permitir solo dígitos mayores o iguales a 0
        return True
    return False

#1.Ñ. Función validate_billete5 para permitir solo enteros >= 0
def validate_billete5(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
    if action != '1':  # Permitir acciones que no sean de inserción
        return True
    if text.isdigit() and int(text) >= 0:  # Permitir solo dígitos mayores o iguales a 0
        return True
    return False

#1.O. Función check_billete2 para detener los entry de billetes siguientes en caso de que se ponga 0 en billete1
def check_billete2(event=None):
    if input_billete1.get().isdigit() and int(input_billete1.get()) > 0:
        entry_billete2.config(state='normal')
    else:
        input_billete2.set("0")
        entry_billete2.config(state='readonly')
        input_billete3.set("0")
        entry_billete3.config(state='readonly')
        input_billete4.set("0")
        entry_billete4.config(state='readonly')
        input_billete5.set("0")
        entry_billete5.config(state='readonly')

#1.P. Función check_billete3 para detener los entry de billetes siguientes en caso de que se ponga 0 en billete1
def check_billete3(event=None):
    if input_billete2.get().isdigit() and int(input_billete2.get()) > 0:
        entry_billete3.config(state='normal')
    else:
        input_billete3.set("0")
        entry_billete3.config(state='readonly')
        input_billete4.set("0")
        entry_billete4.config(state='readonly')
        input_billete5.set("0")
        entry_billete5.config(state='readonly')

#1.Q. Función check_billete4 para detener los entry de billetes siguientes en caso de que se ponga 0 en billete1
def check_billete4(event=None):
    if input_billete3.get().isdigit() and int(input_billete3.get()) > 0:
        entry_billete4.config(state='normal')
    else:
        input_billete4.set("0")
        entry_billete4.config(state='readonly')
        input_billete5.set("0")
        entry_billete5.config(state='readonly')
        

#1.R. Función check_billete4 para detener los entry de billetes siguientes en caso de que se ponga 0 en billete1
def check_billete5(event=None):
    if input_billete4.get().isdigit() and int(input_billete4.get()) > 0:
        entry_billete5.config(state='normal')
    else:
        input_billete5.set("0")
        entry_billete5.config(state='readonly')

#.......................................

#Guardar
def guardar_datos_configuracion(input_cant_espacios, input_precio_hora, input_pago_minimo, input_redondeo, input_minutos_max, input_moneda1, input_moneda2, input_moneda3, input_billete1, input_billete2, input_billete3, input_billete4, input_billete5):

    global cant_espacios, precio_por_hora, pago_minimo, redondeo, minutos_maximos, moneda1, moneda2, moneda3, billete1, billete2, billete3, billete4, billete5, parqueo, dicc_cajero

    cant_espacios = int(input_cant_espacios.get())
    precio_por_hora = float(input_precio_hora.get())
    pago_minimo = int(input_pago_minimo.get())
    redondeo = int(input_redondeo.get())
    minutos_maximos = int(input_minutos_max.get())
    moneda1 = int(input_moneda1.get())
    moneda2 = int(input_moneda2.get())
    moneda3 = int(input_moneda3.get())
    billete1 = int(input_billete1.get())
    billete2 = int(input_billete2.get())
    billete3 = int(input_billete3.get())
    billete4 = int(input_billete4.get())
    billete5 = int(input_billete5.get())

    #Inicializando el diccionario de monedas 
    dicc_monedas = {}
    total_monedas = "Total de monedas"
    denominaciones = [moneda1, moneda2, moneda3, total_monedas]
    for denominacion in denominaciones:
        if denominacion != 0:  #Solo agregamos denominaciones válidas
            dicc_monedas[denominacion] = [[0, 0], [0, 0], [0, 0]] #Se pone en cada llave (que es cada denominación) una lista de listas: entradas, salidas, saldo y cada sublista tiene 2 valores: cantidad y total. 

    #Inicializando el diccionario de billetes 
    dicc_billetes = {}
    total_billetes = "Total de billetes"
    denominaciones = [billete1, billete2, billete3, billete4, billete5, total_billetes]
    for denominacion in denominaciones:
        if denominacion != 0:  #Solo agregamos denominaciones válidas
            dicc_billetes[denominacion] = [[0, 0], [0, 0], [0, 0]] #Se pone en cada llave (que es cada denominación) una lista de listas: entradas, salidas, saldo y cada sublista tiene 2 valores: cantidad y total. 

    #Inicializando el diccionario cajero, que contiene tanto dicc_monedas como dicc_billetes
    dicc_cajero = {}
    dicc_cajero = {'dicc_monedas': dicc_monedas, 'dicc_billetes': dicc_billetes}
            
    # Inicializar la lista parqueo solo si no está inicializada
    if 'parqueo' not in globals() or parqueo is None:
        parqueo = [[] for _ in range(cant_espacios)]
    else:
        # Si ya está inicializada, ajustar la longitud según la nueva cantidad de espacios
        if len(parqueo) < cant_espacios:
            parqueo.extend([[] for _ in range(cant_espacios - len(parqueo))])
        elif len(parqueo) > cant_espacios:
            parqueo = parqueo[:cant_espacios]

    mostrar_frame(inicio_frame)


#Cancelar
def cancelar_datos_configuracion():
    mostrar_frame(inicio_frame)

#.....................................
    
#1.1. Función validar_orden_monedas

def validar_orden_monedas():
    monedas = [int(input_moneda1.get()),
               int(input_moneda2.get()),
               int(input_moneda3.get())]

    for indice in range(1, len(monedas)):
        if monedas[indice] != 0 and monedas[indice] <= monedas[indice - 1]:
            messagebox.showerror("Error", f"La denominación de moneda {indice + 1} debe ser mayor que la de moneda {indice}")
            # Borra los datos incorrectos
            input_moneda2.set("0")
            input_moneda3.set("0")
            # Actualiza los entry
            entry_moneda2.delete(0, tk.END)
            entry_moneda3.delete(0, tk.END)
            return False
    return True


#1.2. Función validar_orden_billetes
def validar_orden_billetes():
    billetes = [int(input_billete1.get()),
                int(input_billete2.get()),
                int(input_billete3.get()),
                int(input_billete4.get()),
                int(input_billete5.get())]

    for indice in range(1, len(billetes)):
        if billetes[indice] != 0 and billetes[indice] <= billetes[indice - 1]:
            messagebox.showerror("Error", f"La denominación de billete {indice + 1} debe ser mayor que la de billete {indice}")
            # Borra los datos incorrectos
            input_billete2.set("0")
            input_billete3.set("0")
            input_billete4.set("0")
            input_billete5.set("0")
            # Actualiza los entry
            entry_billete2.delete(0, tk.END)
            entry_billete3.delete(0, tk.END)
            entry_billete4.delete(0, tk.END)
            entry_billete5.delete(0, tk.END)
            return False
    return True


#1.3. Función validar_vueltos

# Función auxiliar para comprobar si se puede formar un monto con las denominaciones
def se_puede_formar_monto(monto, denominaciones):
    dp = [False] * (monto + 1)
    dp[0] = True

    for denominacion in denominaciones:
        for indice in range(denominacion, monto + 1):
            if dp[indice - denominacion]:
                dp[indice] = True

    return dp[monto]


def validar_vueltos(precio_hora, pago_minimo, monedas, billetes):
    denominaciones = monedas + billetes

    # Validar el pago mínimo
    if pago_minimo > 0:
        denominaciones_menores = [d for d in denominaciones if d < pago_minimo]
        if not denominaciones_menores:
            messagebox.showerror("Error", f"No es posible dar vueltos para el pago mínimo de {pago_minimo} con las denominaciones registradas")
            return False
        if not se_puede_formar_monto(pago_minimo, denominaciones_menores):
            messagebox.showerror("Error", f"No es posible dar vueltos para el pago mínimo de {pago_minimo} con las denominaciones ingresadas")
            return False

    # Validar los pagos desde el precio por hora hasta varios múltiplos del precio por hora
    for horas in range(1, 24): 
        monto = int(precio_hora * horas)
        denominaciones_menores = [d for d in denominaciones if d < monto]
        if not denominaciones_menores:
            messagebox.showerror("Error", f"No es posible dar vueltos al monto de {monto} con las denominaciones ingresadas")
            return False
        if not se_puede_formar_monto(monto, denominaciones_menores):
            messagebox.showerror("Error", f"No es posible dar vueltos para el monto de {monto} con las denominaciones ingresadas")
            return False

    return True


#1.4. Función validar_y_guardar_configuracion
def validar_y_guardar_configuracion():
    if (not input_cant_espacios.get() or  #Validar que todos los campos estén llenos
            not input_precio_hora.get() or
            not input_pago_minimo.get() or
            not input_redondeo.get() or
            not input_minutos_max.get() or
            not input_moneda1.get() or
            not input_moneda2.get() or
            not input_moneda3.get() or
            not input_billete1.get() or
            not input_billete2.get() or
            not input_billete3.get() or
            not input_billete4.get() or
            not input_billete5.get()):
        messagebox.showerror("Error", "Hace falta completar algunos datos de configuración \nDe omitir un dato, póngalo como 0")
        return

    if not validar_orden_monedas():  #Validando monedas
        return

    if not validar_orden_billetes(): #Validando billetes
        return

    # Validar si es posible dar vuelto con los datos de configuración
    monedas = [int(input_moneda1.get()), int(input_moneda2.get()), int(input_moneda3.get())]
    billetes = [int(input_billete1.get()), int(input_billete2.get()), int(input_billete3.get()), int(input_billete4.get()), int(input_billete5.get())]
    precio_hora = float(input_precio_hora.get())
    pago_minimo = int(input_pago_minimo.get())

    if not validar_vueltos(precio_hora, pago_minimo, monedas, billetes):
        return

    #Si todo bien, guardar los datos
    guardar_datos_configuracion(input_cant_espacios, input_precio_hora, input_pago_minimo, input_redondeo, input_minutos_max, input_moneda1, input_moneda2, input_moneda3, input_billete1, input_billete2, input_billete3, input_billete4, input_billete5)


#1.5. Función cargar_configuracion para desplegar los datos existentes en las cajas de texto una vez que se completaron los datos
def cargar_configuracion():
    configuracion = {}
    if os.path.exists('configuración.dat'):
        with open('configuración.dat', 'r') as file:
            lines = file.readlines()
            if len(lines) >= 10:  
                configuracion['cant_espacios'] = lines[0].strip()
                configuracion['precio_hora'] = lines[1].strip()
                configuracion['pago_minimo'] = lines[2].strip()
                configuracion['redondeo'] = lines[3].strip()
                configuracion['minutos_maximos'] = lines[4].strip()
                configuracion['moneda1'] = lines[5].strip()
                configuracion['moneda2'] = lines[6].strip()
                configuracion['moneda3'] = lines[7].strip()
                configuracion['billete1'] = lines[8].strip()
                configuracion['billete2'] = lines[9].strip()
                configuracion['billete3'] = lines[10].strip()
                configuracion['billete4'] = lines[11].strip()
                configuracion['billete5'] = lines[12].strip()
    return configuracion



"""2. DINERO DEL CAJERO"""

"""2.A. SALDO DEL CAJERO"""

#Para el botón de Ok
def ok_saldo(dicc_cajero, vaciar_cajero_var):
    if vaciar_cajero_var.get():
        vaciar_cajero(dicc_cajero)
    mostrar_frame(inicio_frame)
    
#Para el botón de Cancelar
def cancelar_saldo():
    mostrar_frame(inicio_frame)

#Para el botón de Vaciar cajero
def vaciar_cajero(dicc_cajero):
    for cada_llave in dicc_cajero['dicc_monedas']:
        dicc_cajero['dicc_monedas'][cada_llave] = [[0, 0], [0, 0], [0, 0]]
    for cada_llave in dicc_cajero['dicc_billetes']:
        dicc_cajero['dicc_billetes'][cada_llave] = [[0, 0], [0, 0], [0, 0]]


"""2.B. CARGAR CAJERO"""

def actualizar_dicc_cajero(dicc_cajero, es_monedas, denominacion, cantidad):
    if es_monedas:
        dicc_cajero['dicc_monedas'][denominacion][0][0] += cantidad
        dicc_cajero['dicc_monedas'][denominacion][0][1] += denominacion * cantidad
        dicc_cajero['dicc_monedas'][denominacion][2][0] = (dicc_cajero['dicc_monedas'][denominacion][0][0]) - (dicc_cajero['dicc_monedas'][denominacion][1][0])
        dicc_cajero['dicc_monedas'][denominacion][2][1] = (dicc_cajero['dicc_monedas'][denominacion][0][1]) - (dicc_cajero['dicc_monedas'][denominacion][1][1])
        dicc_cajero['dicc_monedas']['Total de monedas'][0][0] += cantidad
        dicc_cajero['dicc_monedas']['Total de monedas'][0][1] += denominacion * cantidad
        dicc_cajero['dicc_monedas']['Total de monedas'][2][0] = (dicc_cajero['dicc_monedas']['Total de monedas'][0][0]) - (dicc_cajero['dicc_monedas']['Total de monedas'][1][0])
        dicc_cajero['dicc_monedas']['Total de monedas'][2][1] = (dicc_cajero['dicc_monedas']['Total de monedas'][0][1]) - (dicc_cajero['dicc_monedas']['Total de monedas'][1][1])
    else:
        dicc_cajero['dicc_billetes'][denominacion][0][0] += cantidad
        dicc_cajero['dicc_billetes'][denominacion][0][1] += denominacion * cantidad
        dicc_cajero['dicc_billetes'][denominacion][2][0] = (dicc_cajero['dicc_billetes'][denominacion][0][0]) - (dicc_cajero['dicc_billetes'][denominacion][1][0])
        dicc_cajero['dicc_billetes'][denominacion][2][1] = (dicc_cajero['dicc_billetes'][denominacion][0][1]) - (dicc_cajero['dicc_billetes'][denominacion][1][1])
        dicc_cajero['dicc_billetes']['Total de billetes'][0][0] += cantidad
        dicc_cajero['dicc_billetes']['Total de billetes'][0][1] += denominacion * cantidad
        dicc_cajero['dicc_billetes']['Total de billetes'][2][0] = (dicc_cajero['dicc_billetes']['Total de billetes'][0][0]) - (dicc_cajero['dicc_billetes']['Total de billetes'][1][0])
        dicc_cajero['dicc_billetes']['Total de billetes'][2][1] = (dicc_cajero['dicc_billetes']['Total de billetes'][0][1]) - (dicc_cajero['dicc_billetes']['Total de billetes'][1][1])

    


def actualizar_saldo(saldo_cantidad_label, saldo_total_label, denominacion, dicc_cajero, row):
    dicc_monedas = dicc_cajero['dicc_monedas']
    dicc_billetes = dicc_cajero['dicc_billetes']
    
    if denominacion in dicc_monedas:
        denm = dicc_monedas[denominacion]
        nuevo_saldo_cantidad = denm[2][0]
        nuevo_saldo_total = denm[2][1]
    elif denominacion in dicc_billetes:
        denm = dicc_billetes[denominacion]
        nuevo_saldo_cantidad = denm[2][0]
        nuevo_saldo_total = denm[2][1]
        
    saldo_cantidad_label[row].config(text=str(nuevo_saldo_cantidad))
    saldo_total_label[row].config(text=str(nuevo_saldo_total))


# Función para actualizar el total
def actualizar_total(entry, total_label, denominacion, update_totals_func, dicc_cajero, es_monedas, saldo_cantidad_label, saldo_total_label,
                     saldo_inicial_cantidad, saldo_inicial_total, row):
    cantidad = entry.get()
    if cantidad.isdigit():
        cantidad = int(cantidad)
        total = denominacion * cantidad
        total_label.config(text=str(total))
        update_totals_func()  # Llamar a la función para actualizar los totales
        actualizar_dicc_cajero(dicc_cajero, es_monedas, denominacion, cantidad)  # Actualizar el diccionario dicc_cajero
        actualizar_saldo(saldo_cantidad_label, saldo_total_label, denominacion, dicc_cajero, row)  # Actualizar los saldos en las columnas 5 y 6


def validate_integer(P):
    # Verificar que la cadena P contiene solo dígitos y no está vacía
    return P.isdigit() or P == ""

def calcular_totales_columnas_cinco_y_seis_monedas(diccionario, total_monedas_cantidad_label, total_monedas_total_label):
    global cantidad_monedas_en_columna_1, total_monedas_en_columna1, total_monedas_total
    total_monedas_cantidad = cantidad_monedas_en_columna_1
    total_monedas_total = total_monedas_en_columna1
    
    # Calcular totales para monedas
    for denominacion, datos in diccionario.items():
        if len(datos) >= 4:  # Verificar si la lista tiene al menos 4 elementos
            cantidad_entry, _ = datos[3]
            cantidad = cantidad_entry.get()
            if cantidad.isdigit():
                cantidad = int(cantidad)
                total_monedas_cantidad += cantidad
                total_monedas_total += cantidad * denominacion
        
    # Actualizar etiquetas de totales
    total_monedas_cantidad_label.config(text=str(total_monedas_cantidad))
    total_monedas_total_label.config(text=str(total_monedas_total))


def calcular_totales_columnas_cinco_y_seis_billetes(diccionario, total_billetes_cantidad_label, total_billetes_total_label):
    global cantidad_billetes_en_columna_1, total_billetes_en_columna1, total_billetes_total
    total_billetes_cantidad = cantidad_billetes_en_columna_1
    total_billetes_total = total_billetes_en_columna1
        
    # Calcular totales para billetes
    for denominacion, datos in diccionario.items():
        if len(datos) >= 4:  # Verificar si la lista tiene al menos 4 elementos
            cantidad_entry, _ = datos[3]
            cantidad = cantidad_entry.get()
            if cantidad.isdigit():
                cantidad = int(cantidad)
                total_billetes_cantidad += cantidad
                total_billetes_total += cantidad * denominacion
    
    # Actualizar etiquetas de totales
    total_billetes_cantidad_label.config(text=str(total_billetes_cantidad))
    total_billetes_total_label.config(text=str(total_billetes_total))

def cambiar_total_cajero(label_cajero_final, total_monedas_total, total_billetes_total):
    
    suma_cajero_final = str(total_monedas_total + total_billetes_total)
    label_cajero_final.config(text=f"Total del cajero:                                                                         {suma_cajero_final}")


# Mostrar los datos en las columnas correspondientes, incluyendo la lógica para la actualización de saldos
def mostrar_datos_siguientes_dos_columnas(tipo, diccionario, cargar_cajero_frame, start_row, update_totals_func):
    row = start_row  # Start_row para indicar desde qué fila comenzar
    
    vcmd = cargar_cajero_frame.register(validate_integer)  # Validar entry
    
    # Crear listas para las etiquetas de saldo, de manera que se puedan actualizar más tarde
    saldo_cantidad_labels = {}
    saldo_total_labels = {}

    # Crear diccionarios para almacenar los valores anteriores de los Entries
    previous_entries = {}

    for denominacion, datos in diccionario.items():
        if denominacion == "Total de monedas" or denominacion == "Total de billetes":
            continue        
        # Obtener saldo inicial de cantidad y total
        saldo_inicial_cantidad = datos[2][0]
        saldo_inicial_total = datos[2][1]
        
        total_label = tk.Label(cargar_cajero_frame, text="", bg="beige")  # Columna de total
        total_label.grid(row=row, column=4, padx=5, pady=5)
        
        cantidad_entry = tk.Entry(cargar_cajero_frame, validate="key", validatecommand=(vcmd, "%P"))  # Columna de cantidad
        cantidad_entry.grid(row=row, column=3, padx=5, pady=5)

        # Labels para las columnas de saldo
        saldo_cantidad_label = tk.Label(cargar_cajero_frame, text=saldo_inicial_cantidad, bg="beige")
        saldo_total_label = tk.Label(cargar_cajero_frame, text=saldo_inicial_total, bg="beige")
        saldo_cantidad_label.grid(row=row, column=5, padx=5, pady=5)
        saldo_total_label.grid(row=row, column=6, padx=5, pady=5)

        # Almacenar las etiquetas en diccionarios usando la fila como clave
        saldo_cantidad_labels[row] = saldo_cantidad_label
        saldo_total_labels[row] = saldo_total_label

        # Guardar el valor inicial del Entry en el diccionario de valores anteriores
        previous_entries[cantidad_entry] = cantidad_entry.get()

        # Definir la función de actualización para el evento <FocusOut>
        def actualizar(event, entry=cantidad_entry, label=total_label, denom=denominacion, es_monedas=tipo == "monedas", r=row):
            current_value = entry.get()
            previous_value = previous_entries[entry]
            if current_value != previous_value:  # Solo actualizar si el valor ha cambiado
                previous_entries[entry] = current_value
                
                actualizar_total(entry, label, denom, update_totals_func, dicc_cajero, es_monedas, saldo_cantidad_labels, saldo_total_labels,
                                 saldo_inicial_cantidad, saldo_inicial_total, r)


        cantidad_entry.bind("<FocusOut>", actualizar)
        diccionario[denominacion].append((cantidad_entry, total_label))  # Guardar los widgets para calcular los totales

        row += 1

def calcular_totales(diccionario, cantidad_labels, total_labels):
    total_cantidad = 0
    total_suma = 0
    for denominacion, datos in diccionario.items():
        if denominacion == "Total de monedas" or denominacion == "Total de billetes":
            continue
        cantidad_entry, total_label = datos[3]  # Obtener los widgets
        cantidad = cantidad_entry.get()
        if cantidad.isdigit():
            cantidad = int(cantidad)
            total_cantidad += cantidad
            total_suma += int(total_label.cget("text"))
    cantidad_labels.config(text=str(total_cantidad))
    total_labels.config(text=str(total_suma))

#Para ir viendo el total general del cajero
def calcular_total_cajero(total_monedas_total_label_5_6, total_billetes_total_label_5_6): 
    if total_monedas_total_label_5_6.cget("text") != "" and total_billetes_total_label_5_6.cget("text") != "":
        total_monedas = int(total_monedas_total_label_5_6.cget("text"))  # Total de monedas en la columna 6
        total_billetes = int(total_billetes_total_label_5_6.cget("text"))  # Total de billetes en la columna 6
        total_cajero = total_monedas + total_billetes
        return total_cajero


#Para el botón de Ok
def ok_cargar(dicc_cajero):
    dicc_monedas = dicc_cajero['dicc_monedas']
    dicc_billetes = dicc_cajero['dicc_billetes']

    for valores in dicc_monedas.values():
        if len(valores) >=4:
            valores.pop(3)
        

    for valores in dicc_billetes.values():
        if len(valores) >=4:
            valores.pop(3)
        

    
    mostrar_frame(inicio_frame)  # Como dicc_cajero es global y lo estuvimos actualizando conforme vamos cargando el cajero, simplemente regresamos a la pantalla principal





"""3. ENTRADA DE VEHÍCULO"""
def ok_entrar_vehiculo(parqueo):
    
    mostrar_frame(inicio_frame)


def cancelar_entrar_vehiculo():
    mostrar_frame(inicio_frame)



"""4. CAJERO"""
def calcular_tiempo_cobrado(entrada, salida):
    # Convertir las fechas a minutos totales desde una fecha base (por ejemplo, 1/1/0001 00:00)
    def minutos_totales(fecha):
        dia, mes, año, hora, minuto = fecha
        # Días transcurridos hasta la fecha dada
        dias = dia + 30 * (mes - 1) + 365 * (año - 1)
        # Minutos transcurridos en ese día
        minutos_dia = hora * 60 + minuto
        # Minutos totales
        return dias * 24 * 60 + minutos_dia
    
    minutos_entrada = minutos_totales(entrada)
    minutos_salida = minutos_totales(salida)
    
    # Diferencia en minutos
    diferencia_minutos = minutos_salida - minutos_entrada
    
    # Convertir la diferencia en días, horas y minutos
    dias = diferencia_minutos // (24 * 60)
    diferencia_minutos %= (24 * 60)
    horas = diferencia_minutos // 60
    minutos = diferencia_minutos % 60
    
    return horas, minutos, dias


def extraer_denominaciones(dicc_cajero):
    denominaciones = []
    for dicc in dicc_cajero.values():
        for denom in dicc.keys():
            if isinstance(denom, int):
                denominaciones.append(denom)
    return denominaciones

def redondear_a_denominacion(monto, denominaciones):
    denominaciones.sort()
    if monto % denominaciones[1] != 0:
        monto = math.ceil(monto / denominaciones[1]) * denominaciones[1]
    return monto

def calcular_monto_a_pagar(horas, minutos, dias):
    # Calcular el total de minutos
    total_minutos = dias * 24 * 60 + horas * 60 + minutos
    
    # Aplicar redondeo de minutos si es necesario
    if redondeo != 0:
        total_minutos = math.ceil(total_minutos / redondeo) * redondeo
    
    # Convertir minutos a horas y calcular el monto base
    total_horas = total_minutos / 60
    monto = total_horas * precio_por_hora
    
    # Aplicar pago mínimo si el monto calculado es menor
    if pago_minimo != 0:
        monto = max(monto, pago_minimo)
    
    # Extraer denominaciones de dicc_cajero
    denominaciones = extraer_denominaciones(dicc_cajero)
    
    # Redondear el monto para que se pueda formar con las denominaciones
    monto = redondear_a_denominacion(monto, denominaciones)
    
    return round(monto)


"""6. REPORTE DE INGRESOS DE DINERO"""

def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%d/%m/%Y")
        return True
    except:
        return False

def validar_hora(hora, minutos):
    try:
        hora_int = int(hora)
        minutos_int = int(minutos)
        return 0 <= hora_int <= 23 and 0 <= minutos_int <= 59
    except:
        return False

########################################################################





# DEFINICIÓN DE FUNCIONES PARA CADA OPCIÓN DEL MENÚ 
                   
"""1. CONFIGURACIÓN DEL TORNEO"""

def configuracion():
    for espacio in parqueo:
        if espacio != []:
            messagebox.showerror("Hay vehículos en el parqueo", "Para modificar los datos de configuración, el parqueo debe estar vacío.")
            return 

    configuracion_frame = tk.Frame(raiz, bg="beige")
    configuracion_frame.grid(row=0, column=0, sticky='nsew')

    # Poner el título
    titulo_label = tk.Label(configuracion_frame, text="Estacionamiento | Configuración", font=("Consolas", 20), bg="beige")
    titulo_label.pack(pady=20)

    # Creando un frame interno para ir poniendo los entry y sus descripciones
    frame_entry = tk.Frame(configuracion_frame, bg="beige")
    frame_entry.pack(pady=20)

    # Cargar configuración previa si existe
    configuracion_guardada = cargar_configuracion()

    # Cantidad de espacios
    label_cant_espacios = tk.Label(frame_entry, text="Cantidad de espacios en el parqueo:", bg="beige")
    label_cant_espacios.grid(row=0, column=0, padx=5, pady=5, sticky='e')
    global input_cant_espacios
    input_cant_espacios = tk.StringVar()
    if configuracion_guardada:
        input_cant_espacios.set(configuracion_guardada.get('cant_espacios', ''))
    vcmd = (frame_entry.register(validate_cant_espacios), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    entry_cant_espacios = ttk.Entry(frame_entry, textvariable=input_cant_espacios, validate='key', validatecommand=vcmd)
    entry_cant_espacios.grid(row=0, column=1, padx=10, pady=5, sticky='w')

    # Precio por hora
    label_precio_hora = tk.Label(frame_entry, text="Precio por hora:", bg="beige")
    label_precio_hora.grid(row=1, column=0, padx=5, pady=5, sticky='e')
    global input_precio_hora
    input_precio_hora = tk.StringVar()
    if configuracion_guardada:
        input_precio_hora.set(configuracion_guardada.get('precio_hora', ''))
    vcmd_precio_hora = (frame_entry.register(validate_precio_hora), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    entry_precio_hora = ttk.Entry(frame_entry, textvariable=input_precio_hora, validate='key', validatecommand=vcmd_precio_hora)
    entry_precio_hora.grid(row=1, column=1, padx=10, pady=5, sticky='w')

    # Pago mínimo
    label_pago_minimo = tk.Label(frame_entry, text="Pago mínimo (si no desea aplicar este pago, ponga 0):", bg="beige")
    label_pago_minimo.grid(row=2, column=0, padx=5, pady=5, sticky='e')
    global input_pago_minimo
    input_pago_minimo = tk.StringVar()
    if configuracion_guardada:
        input_pago_minimo.set(configuracion_guardada.get('pago_minimo', ''))
    vcmd_pago_minimo = (frame_entry.register(validate_pago_minimo), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    entry_pago_minimo = ttk.Entry(frame_entry, textvariable=input_pago_minimo, validate='key', validatecommand=vcmd_pago_minimo)
    entry_pago_minimo.grid(row=2, column=1, padx=10, pady=5, sticky='w')

    # Redondeo
    label_redondeo = tk.Label(frame_entry, text="Redondear el tiempo cobrado al próximo minuto (0-60) :", bg="beige")
    label_redondeo.grid(row=3, column=0, padx=5, pady=5, sticky='e')
    global input_redondeo
    input_redondeo = tk.StringVar()
    if configuracion_guardada:
        input_redondeo.set(configuracion_guardada.get('redondeo', ''))
    validate_command = (frame_entry.register(validate_redondeo), '%P')
    entry_redondeo = ttk.Entry(frame_entry, textvariable=input_redondeo, validate="key", validatecommand=validate_command)
    entry_redondeo.grid(row=3, column=1, padx=10, pady=5, sticky='w')

    # Minutos máximos
    label_minutos_max = tk.Label(frame_entry, text="Minutos máximos para salir después del pago:", bg="beige")
    label_minutos_max.grid(row=4, column=0, padx=5, pady=5, sticky='e')
    global input_minutos_max
    input_minutos_max = tk.StringVar()
    if configuracion_guardada:
        input_minutos_max.set(configuracion_guardada.get('minutos_maximos', ''))
    vcmd_minutos_max = (frame_entry.register(validate_minutos_max), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    entry_minutos_max = ttk.Entry(frame_entry, textvariable=input_minutos_max, validate='key', validatecommand=vcmd_minutos_max)
    entry_minutos_max.grid(row=4, column=1, padx=10, pady=5, sticky='w')

    # Tipos de moneda
    label_tipo_moneda = tk.Label(frame_entry, text="Tipos de moneda (máximo 3 tipos):", bg="beige")
    label_tipo_moneda.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='w')

    # Moneda 1
    label_moneda1 = tk.Label(frame_entry, text="Moneda 1, la de menor denominación:", bg="beige")
    label_moneda1.grid(row=6, column=0, padx=5, pady=5, sticky='e')
    global input_moneda1
    input_moneda1 = tk.StringVar()
    if configuracion_guardada:
        input_moneda1.set(configuracion_guardada.get('moneda1', ''))
    vcmd_moneda1 = (frame_entry.register(validate_moneda1), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    global entry_moneda1
    entry_moneda1 = ttk.Entry(frame_entry, textvariable=input_moneda1, validate='key', validatecommand=vcmd_moneda1)
    entry_moneda1.grid(row=6, column=1, padx=10, pady=5, sticky='w')
    entry_moneda1.bind('<FocusOut>', check_moneda2)

    # Moneda 2
    label_moneda2 = tk.Label(frame_entry, text="Moneda 2, denominación siguiente a la anterior:", bg="beige")
    label_moneda2.grid(row=7, column=0, padx=5, pady=5, sticky='e')
    global input_moneda2
    input_moneda2 = tk.StringVar()
    if configuracion_guardada:
        input_moneda2.set(configuracion_guardada.get('moneda2', ''))
    vcmd_moneda2 = (frame_entry.register(validate_moneda2), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    global entry_moneda2
    entry_moneda2 = ttk.Entry(frame_entry, textvariable=input_moneda2, validate='key', validatecommand=vcmd_moneda2)
    entry_moneda2.grid(row=7, column=1, padx=10, pady=5, sticky='w')
    entry_moneda2.bind('<FocusOut>', check_moneda3)

    # Moneda 3
    label_moneda3 = tk.Label(frame_entry, text="Moneda 3, denominación siguiente a la anterior:", bg="beige")
    label_moneda3.grid(row=8, column=0, padx=5, pady=5, sticky='e')
    global input_moneda3
    input_moneda3 = tk.StringVar()
    if configuracion_guardada:
        input_moneda3.set(configuracion_guardada.get('moneda3', ''))
    vcmd_moneda3 = (frame_entry.register(validate_moneda3), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    global entry_moneda3
    entry_moneda3 = ttk.Entry(frame_entry, textvariable=input_moneda3, validate='key', validatecommand=vcmd_moneda3)
    entry_moneda3.grid(row=8, column=1, padx=10, pady=5, sticky='w')
    entry_moneda3.bind('<FocusOut>', check_moneda3)  

    # Tipos de billetes
    label_tipo_billete = tk.Label(frame_entry, text="Tipos de billetes (máximo 5 tipos):", bg="beige")
    label_tipo_billete.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky='w')

    # Billete 1
    label_billete1 = tk.Label(frame_entry, text="Billete 1, el de menor denominación:", bg="beige")
    label_billete1.grid(row=10, column=0, padx=5, pady=5, sticky='e')
    global input_billete1
    input_billete1 = tk.StringVar()
    if configuracion_guardada:
        input_billete1.set(configuracion_guardada.get('billete1', ''))
    vcmd_billete1 = (frame_entry.register(validate_billete1), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    global entry_billete1
    entry_billete1 = ttk.Entry(frame_entry, textvariable=input_billete1, validate='key', validatecommand=vcmd_billete1)
    entry_billete1.grid(row=10, column=1, padx=10, pady=5, sticky='w')
    entry_billete1.bind('<FocusOut>', check_billete2)

    # Billete 2
    label_billete2 = tk.Label(frame_entry, text="Billete 2, denominación siguiente a la anterior:", bg="beige")
    label_billete2.grid(row=11, column=0, padx=5, pady=5, sticky='e')
    global input_billete2
    input_billete2 = tk.StringVar()
    if configuracion_guardada:
        input_billete2.set(configuracion_guardada.get('billete2', ''))
    vcmd_billete2 = (frame_entry.register(validate_billete2), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    global entry_billete2
    entry_billete2 = ttk.Entry(frame_entry, textvariable=input_billete2, validate='key', validatecommand=vcmd_billete2)
    entry_billete2.grid(row=11, column=1, padx=10, pady=5, sticky='w')
    entry_billete2.bind('<FocusOut>', check_billete3)

    # Billete 3
    label_billete3 = tk.Label(frame_entry, text="Billete 3, denominación siguiente a la anterior:", bg="beige")
    label_billete3.grid(row=12, column=0, padx=5, pady=5, sticky='e')
    global input_billete3
    input_billete3 = tk.StringVar()
    if configuracion_guardada:
        input_billete3.set(configuracion_guardada.get('billete3', ''))
    vcmd_billete3 = (frame_entry.register(validate_billete3), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    global entry_billete3
    entry_billete3 = ttk.Entry(frame_entry, textvariable=input_billete3, validate='key', validatecommand=vcmd_billete3)
    entry_billete3.grid(row=12, column=1, padx=10, pady=5, sticky='w')
    entry_billete3.bind('<FocusOut>', check_billete4)

    # Billete 4
    label_billete4 = tk.Label(frame_entry, text="Billete 4, denominación siguiente a la anterior:", bg="beige")
    label_billete4.grid(row=13, column=0, padx=5, pady=5, sticky='e')
    global input_billete4
    input_billete4 = tk.StringVar()
    if configuracion_guardada:
        input_billete4.set(configuracion_guardada.get('billete4', ''))
    vcmd_billete4 = (frame_entry.register(validate_billete4), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    global entry_billete4
    entry_billete4 = ttk.Entry(frame_entry, textvariable=input_billete4, validate='key', validatecommand=vcmd_billete4)
    entry_billete4.grid(row=13, column=1, padx=10, pady=5, sticky='w')
    entry_billete4.bind('<FocusOut>', check_billete5)

    # Billete 5
    label_billete5 = tk.Label(frame_entry, text="Billete 5, denominación siguiente a la anterior:", bg="beige")
    label_billete5.grid(row=14, column=0, padx=5, pady=5, sticky='e')
    global input_billete5
    input_billete5 = tk.StringVar()
    if configuracion_guardada:
        input_billete5.set(configuracion_guardada.get('billete5', ''))
    vcmd_billete5 = (frame_entry.register(validate_billete5), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    global entry_billete5
    entry_billete5 = ttk.Entry(frame_entry, textvariable=input_billete5, validate='key', validatecommand=vcmd_billete5)
    entry_billete5.grid(row=14, column=1, padx=10, pady=5, sticky='w')
    entry_billete5.bind('<FocusOut>', check_billete5)

    # Botones
    frame_buttons = tk.Frame(configuracion_frame, bg="beige")
    frame_buttons.pack(pady=15)

    # Botón Ok
    boton_ok = tk.Button(frame_buttons, text="Ok", width=10, command=validar_y_guardar_configuracion)
    boton_ok.grid(row=15, column=0, padx=25)

    # Botón Cancelar
    boton_cancelar = tk.Button(frame_buttons, text="Cancelar", width=10, command=cancelar_datos_configuracion)
    boton_cancelar.grid(row=15, column=1, padx=25)

    mostrar_frame(configuracion_frame)






"""2. DINERO DEL CAJERO"""

"""2.A. SALDO DEL CAJERO"""
def saldo_cajero(dicc_cajero):
    
    if cant_espacios == 0 or precio_por_hora == 0 or moneda1 == 0 or billete1 == 0:
        messagebox.showerror("Error", "Hace falta completar algunos datos de configuración para acceder al saldo del cajero")
        return

    if dicc_cajero == {}:
        messagebox.showerror("Error", "Hace falta completar la configuración inicial para poder mostrar el saldo del cajero")
        return
   
    saldo_cajero_frame = tk.Frame(raiz, bg="beige")
    saldo_cajero_frame.grid(row=0, column=0, sticky='nsew')

    # Poner el título
    titulo_label = tk.Label(saldo_cajero_frame, text="Estacionamiento | Saldo del Cajero", font=("Consolas", 20), bg="beige")
    titulo_label.grid(row=0, column=1, columnspan=7, pady=20)

    # Creando las secciones y las columnas
    tk.Label(saldo_cajero_frame, text="DENOMINACIÓN", font=("Consolas", 12, "bold"), bg="beige").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(saldo_cajero_frame, text="ENTRADAS", font=("Consolas", 12, "bold"), bg="beige").grid(row=1, column=1, columnspan=2, padx=5, pady=5)
    tk.Label(saldo_cajero_frame, text="SALIDAS", font=("Consolas", 12, "bold"), bg="beige").grid(row=1, column=3, columnspan=2, padx=5, pady=5)
    tk.Label(saldo_cajero_frame, text="SALDO", font=("Consolas", 12, "bold"), bg="beige").grid(row=1, column=5, columnspan=2, padx=5, pady=5)

    tk.Label(saldo_cajero_frame, text="CANTIDAD", font=("Consolas", 10, "bold"), bg="beige").grid(row=2, column=1, padx=5, pady=5)
    tk.Label(saldo_cajero_frame, text="TOTAL", font=("Consolas", 10, "bold"), bg="beige").grid(row=2, column=2, padx=5, pady=5)
    tk.Label(saldo_cajero_frame, text="CANTIDAD", font=("Consolas", 10, "bold"), bg="beige").grid(row=2, column=3, padx=5, pady=5)
    tk.Label(saldo_cajero_frame, text="TOTAL", font=("Consolas", 10, "bold"), bg="beige").grid(row=2, column=4, padx=5, pady=5)
    tk.Label(saldo_cajero_frame, text="CANTIDAD", font=("Consolas", 10, "bold"), bg="beige").grid(row=2, column=5, padx=5, pady=5)
    tk.Label(saldo_cajero_frame, text="TOTAL", font=("Consolas", 10, "bold"), bg="beige").grid(row=2, column=6, padx=5, pady=5)


    #Desplegar los datos en dicc_cajero
    row = 3

    def mostrar_datos(tipo, diccionario):
        nonlocal row
        for denominacion, datos in diccionario.items():
            if denominacion == "Total de monedas" or denominacion == "Total de billetes":
                continue
            texto_denominacion = f"Monedas de {denominacion}" if tipo == "monedas" else f"Billetes de {denominacion}"
            tk.Label(saldo_cajero_frame, text=texto_denominacion, bg="beige").grid(row=row, column=0, padx=5, pady=5)
            tk.Label(saldo_cajero_frame, text=datos[0][0], bg="beige").grid(row=row, column=1, padx=5, pady=5)  # Entradas - Cantidad
            tk.Label(saldo_cajero_frame, text=datos[0][1], bg="beige").grid(row=row, column=2, padx=5, pady=5)  # Entradas - Total
            tk.Label(saldo_cajero_frame, text=datos[1][0], bg="beige").grid(row=row, column=3, padx=5, pady=5)  # Salidas - Cantidad
            tk.Label(saldo_cajero_frame, text=datos[1][1], bg="beige").grid(row=row, column=4, padx=5, pady=5)  # Salidas - Total
            tk.Label(saldo_cajero_frame, text=datos[2][0], bg="beige").grid(row=row, column=5, padx=5, pady=5)  # Saldo - Cantidad
            tk.Label(saldo_cajero_frame, text=datos[2][1], bg="beige").grid(row=row, column=6, padx=5, pady=5)  # Saldo - Total
            row += 1
        # Mostrar el total
        total_key = "Total de monedas" if tipo == "monedas" else "Total de billetes"
        total_datos = diccionario[total_key]
        tk.Label(saldo_cajero_frame, text=total_key, font=("Consolas", 10, "bold"), bg="beige").grid(row=row, column=0, padx=5, pady=5)
        tk.Label(saldo_cajero_frame, text=total_datos[0][0], bg="beige").grid(row=row, column=1, padx=5, pady=5)  # Entradas - Cantidad
        tk.Label(saldo_cajero_frame, text=total_datos[0][1], bg="beige").grid(row=row, column=2, padx=5, pady=5)  # Entradas - Total
        tk.Label(saldo_cajero_frame, text=total_datos[1][0], bg="beige").grid(row=row, column=3, padx=5, pady=5)  # Salidas - Cantidad
        tk.Label(saldo_cajero_frame, text=total_datos[1][1], bg="beige").grid(row=row, column=4, padx=5, pady=5)  # Salidas - Total
        tk.Label(saldo_cajero_frame, text=total_datos[2][0], bg="beige").grid(row=row, column=5, padx=5, pady=5)  # Saldo - Cantidad
        tk.Label(saldo_cajero_frame, text=total_datos[2][1], bg="beige").grid(row=row, column=6, padx=5, pady=5)  # Saldo - Total
        row += 2  # Añadir un espacio después de la fila de total

    # Mostrar datos de monedas
    mostrar_datos("monedas", dicc_cajero['dicc_monedas'])
    
    # Mostrar datos de billetes
    mostrar_datos("billetes", dicc_cajero['dicc_billetes'])

    #Botón de check para la opción de "Vaciar cajero"
    vaciar_cajero_var = tk.BooleanVar(value=False)
    vaciar_cajero_check = tk.Checkbutton(saldo_cajero_frame, text="Vaciar cajero", variable=vaciar_cajero_var, bg="beige")
    vaciar_cajero_check.grid(row=row, column=0, columnspan=7, pady=5)
    row += 1

    # Botones "Ok" y "Cancelar"
    ok_button = tk.Button(saldo_cajero_frame, text="Ok", command=lambda: ok_saldo(dicc_cajero, vaciar_cajero_var), width=10)
    ok_button.grid(row=row, column=2, pady=5, padx=10)

    cancel_button = tk.Button(saldo_cajero_frame, text="Cancelar", command=cancelar_saldo, width=10)
    cancel_button.grid(row=row, column=4, pady=5, padx=10)

    
    mostrar_frame(saldo_cajero_frame)
    


"""2.B. CARGAR CAJERO"""

def cargar_cajero(dicc_cajero):
    #Se hace una copia de dicc_cajero tal y como lo llevamos hasta el momento, para regresar a esta versión en caso de dar "Cancelar"
    global dicc_cajero_si_se_cancela
    dicc_cajero_si_se_cancela = copy.deepcopy(dicc_cajero)

    if cant_espacios == 0 or precio_por_hora == 0 or moneda1 == 0 or billete1 == 0:
        messagebox.showerror("Error", "Hace falta completar algunos datos de configuración para poder cargar dinero al cajero")
        return

    if dicc_cajero == {}:
        messagebox.showerror("Error", "Hace falta completar la configuración inicial para poder cargar dinero al cajero")
        return
    
    cargar_cajero_frame = tk.Frame(raiz, bg="beige")
    cargar_cajero_frame.grid(row=0, column=0, sticky='nsew')

    # Poner el título
    titulo_label = tk.Label(cargar_cajero_frame, text="Estacionamiento | Cargar cajero", font=("Consolas", 20), bg="beige")
    titulo_label.grid(row=0, column=1, columnspan=7, pady=20)

    # Creando las secciones y las columnas
    tk.Label(cargar_cajero_frame, text="DENOMINACIÓN", font=("Consolas", 12, "bold"), bg="beige").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(cargar_cajero_frame, text="SALDO ANTES DE LA CARGA", font=("Consolas", 11, "bold"), bg="beige").grid(row=1, column=1, columnspan=2, padx=5, pady=5)
    tk.Label(cargar_cajero_frame, text="CARGA", font=("Consolas", 12, "bold"), bg="beige").grid(row=1, column=3, columnspan=2, padx=5, pady=5)
    tk.Label(cargar_cajero_frame, text="SALDO", font=("Consolas", 12, "bold"), bg="beige").grid(row=1, column=5, columnspan=2, padx=5, pady=5)

    tk.Label(cargar_cajero_frame, text="CANTIDAD", font=("Consolas", 10, "bold"), bg="beige").grid(row=2, column=1, padx=5, pady=5)
    tk.Label(cargar_cajero_frame, text="TOTAL", font=("Consolas", 10, "bold"), bg="beige").grid(row=2, column=2, padx=5, pady=5)
    tk.Label(cargar_cajero_frame, text="CANTIDAD", font=("Consolas", 10, "bold"), bg="beige").grid(row=2, column=3, padx=5, pady=5)
    tk.Label(cargar_cajero_frame, text="TOTAL", font=("Consolas", 10, "bold"), bg="beige").grid(row=2, column=4, padx=5, pady=5)
    tk.Label(cargar_cajero_frame, text="CANTIDAD", font=("Consolas", 10, "bold"), bg="beige").grid(row=2, column=5, padx=5, pady=5)
    tk.Label(cargar_cajero_frame, text="TOTAL", font=("Consolas", 10, "bold"), bg="beige").grid(row=2, column=6, padx=5, pady=5)

    diccionario_monedas = dicc_cajero['dicc_monedas']
    diccionario_billetes = dicc_cajero['dicc_billetes']
    global cantidad_monedas_en_columna_1, total_monedas_en_columna1, cantidad_billetes_en_columna_1, total_billetes_en_columna1 
    
    for denominacion, datos in diccionario_monedas.items():
        if denominacion == "Total de monedas":
            cantidad_monedas_en_columna_1 = datos[2][0]
            total_monedas_en_columna1 = datos[2][1] 

    for denominacion, datos in diccionario_billetes.items():
        if denominacion == "Total de billetes":
            cantidad_billetes_en_columna_1 = datos[2][0]
            total_billetes_en_columna1 = datos[2][1] 


    # Desplegar los datos en dicc_cajero
    row = 3

    def mostrar_datos_primeras_tres_columnas(tipo, diccionario, cargar_cajero_frame):
        nonlocal row
        
        for denominacion, datos in diccionario.items():
            if denominacion == "Total de monedas" or denominacion == "Total de billetes":
                continue            
            texto_denominacion = f"Monedas de {denominacion}" if tipo == "monedas" else f"Billetes de {denominacion}"
            tk.Label(cargar_cajero_frame, text=texto_denominacion, bg="beige").grid(row=row, column=0, padx=5, pady=5)
            
            saldo_cantidad = datos[2][0] 
            saldo_total = datos[2][1] 
            
            tk.Label(cargar_cajero_frame, text=saldo_cantidad, bg="beige").grid(row=row, column=1, padx=5, pady=5)  # Saldo - Cantidad
            tk.Label(cargar_cajero_frame, text=saldo_total, bg="beige").grid(row=row, column=2, padx=5, pady=5)  # Saldo - Total

            #Inicializando columnas 5 y 6 para los saldos actualizados
            tk.Label(cargar_cajero_frame, text=saldo_cantidad, bg="beige").grid(row=row, column=5, padx=5, pady=5)  # Nuevo Saldo - Cantidad
            tk.Label(cargar_cajero_frame, text=saldo_total, bg="beige").grid(row=row, column=6, padx=5, pady=5)  # Nuevo Saldo - Total
            
            row += 1
        
        # Mostrar el total
        total_key = "Total de monedas" if tipo == "monedas" else "Total de billetes"
        total_datos = diccionario[total_key]
        tk.Label(cargar_cajero_frame, text=total_key, font=("Consolas", 10, "bold"), bg="beige").grid(row=row, column=0, padx=5, pady=5)
        tk.Label(cargar_cajero_frame, text=total_datos[2][0], bg="beige").grid(row=row, column=1, padx=5, pady=5)  # Saldo - Cantidad
        tk.Label(cargar_cajero_frame, text=total_datos[2][1], bg="beige").grid(row=row, column=2, padx=5, pady=5)  # Saldo - Total
                
        if tipo == "monedas":
            global total_monedas_row
            total_monedas_row = row
        else:
            global total_billetes_row
            total_billetes_row = row
        
        row += 2  # Añadir un espacio después de la fila de total
    
    # Llamar a la función para mostrar los datos de las monedas
    mostrar_datos_primeras_tres_columnas("monedas", dicc_cajero['dicc_monedas'], cargar_cajero_frame)
    
    # Llamar a la función para mostrar los datos de los billetes
    mostrar_datos_primeras_tres_columnas("billetes", dicc_cajero['dicc_billetes'], cargar_cajero_frame)
    
    # Obtener la fila para colocar los botones
    row_botones = row
    
    # Labels para los totales
    total_monedas_cantidad_label_3_4 = tk.Label(cargar_cajero_frame, text="", bg="beige")
    total_monedas_total_label_3_4 = tk.Label(cargar_cajero_frame, text="", bg="beige")
    total_billetes_cantidad_label_3_4 = tk.Label(cargar_cajero_frame, text="", bg="beige")
    total_billetes_total_label_3_4 = tk.Label(cargar_cajero_frame, text="", bg="beige")

    total_monedas_cantidad_label_5_6 = tk.Label(cargar_cajero_frame, text="", bg="beige")
    total_monedas_total_label_5_6 = tk.Label(cargar_cajero_frame, text="", bg="beige")
    total_billetes_cantidad_label_5_6 = tk.Label(cargar_cajero_frame, text="", bg="beige")
    total_billetes_total_label_5_6 = tk.Label(cargar_cajero_frame, text="", bg="beige")

    global total_monedas_total, total_billetes_total
    total_monedas_total = 0
    total_billetes_total = 0
    # Funciones para actualizar los totales
    def actualizar_totales_monedas():
        calcular_totales(dicc_cajero['dicc_monedas'], total_monedas_cantidad_label_3_4, total_monedas_total_label_3_4)
        calcular_totales_columnas_cinco_y_seis_monedas(dicc_cajero['dicc_monedas'], total_monedas_cantidad_label_5_6, total_monedas_total_label_5_6)
        cambiar_total_cajero(label_total_cajero, total_monedas_total, total_billetes_total)
        
    def actualizar_totales_billetes():
        calcular_totales(dicc_cajero['dicc_billetes'], total_billetes_cantidad_label_3_4, total_billetes_total_label_3_4)
        calcular_totales_columnas_cinco_y_seis_billetes(dicc_cajero['dicc_billetes'], total_billetes_cantidad_label_5_6, total_billetes_total_label_5_6)
        cambiar_total_cajero(label_total_cajero, total_monedas_total, total_billetes_total)

    # Mostrar datos de monedas
    mostrar_datos_siguientes_dos_columnas("monedas", dicc_cajero['dicc_monedas'], cargar_cajero_frame, 3, actualizar_totales_monedas)
    
    # Calcular la fila de inicio para billetes
    start_row = 3 + len(dicc_cajero['dicc_monedas']) + 1  # Ajustar fila de inicio para billetes a una fila más arriba

    # Mostrar datos de billetes
    mostrar_datos_siguientes_dos_columnas("billetes", dicc_cajero['dicc_billetes'], cargar_cajero_frame, start_row, actualizar_totales_billetes)

    # Mostrar totales en las columnas 3 y 4
    tk.Label(cargar_cajero_frame, text="Total de monedas", font=("Consolas", 10, "bold"), bg="beige").grid(row=total_monedas_row, column=0, padx=5, pady=5)
    total_monedas_cantidad_label_3_4.grid(row=total_monedas_row, column=3, padx=5, pady=5)
    total_monedas_total_label_3_4.grid(row=total_monedas_row, column=4, padx=5, pady=5)

    tk.Label(cargar_cajero_frame, text="Total de billetes", font=("Consolas", 10, "bold"), bg="beige").grid(row=total_billetes_row, column=0, padx=5, pady=5)
    total_billetes_cantidad_label_3_4.grid(row=total_billetes_row, column=3, padx=5, pady=5)
    total_billetes_total_label_3_4.grid(row=total_billetes_row, column=4, padx=5, pady=5)

    # Mostrar totales en las columnas 5 y 6
    tk.Label(cargar_cajero_frame, text="Total de monedas", font=("Consolas", 10, "bold"), bg="beige").grid(row=total_monedas_row, column=0, padx=5, pady=5)
    total_monedas_cantidad_label_5_6.grid(row=total_monedas_row, column=5, padx=5, pady=5)
    total_monedas_total_label_5_6.grid(row=total_monedas_row, column=6, padx=5, pady=5)

    tk.Label(cargar_cajero_frame, text="Total de billetes", font=("Consolas", 10, "bold"), bg="beige").grid(row=total_billetes_row, column=0, padx=5, pady=5)
    total_billetes_cantidad_label_5_6.grid(row=total_billetes_row, column=5, padx=5, pady=5)
    total_billetes_total_label_5_6.grid(row=total_billetes_row, column=6, padx=5, pady=5)

    # Mostrar el total del cajero
    label_total_cajero = tk.Label(cargar_cajero_frame, text="Total del cajero:                                                                                   xx", font=("Consolas", 10, "bold"), bg="beige")
    label_total_cajero.grid(row=15, column=0, columnspan=6, padx=5, pady=5, sticky='w')

    # Botones "Ok" y "Cancelar"
    ok_button = tk.Button(cargar_cajero_frame, text="Ok", command = lambda : ok_cargar(dicc_cajero), width=10)
    ok_button.grid(row=17, column=2, pady=5, padx=10)

    def cancelar_cargar(): #Hay que hacer que esta versión sea la que se mantiene de ahora en adelante
        global dicc_cajero

        dicc_cajero = dicc_cajero_si_se_cancela  #Se restaura dicc_cajero como estaba antes de ingresar a "Cargar cajero"
        
        mostrar_frame(inicio_frame)


    cancel_button = tk.Button(cargar_cajero_frame, text="Cancelar", command=cancelar_cargar, width=10)
    cancel_button.grid(row=17, column=4, pady=5, padx=10)

    mostrar_frame(cargar_cajero_frame)

    




"""3. ENTRADA DE VEHÍCULO"""

def entrada_vehiculo():

    if cant_espacios == 0 or precio_por_hora == 0 or moneda1 == 0 or billete1 == 0:
        messagebox.showerror("Error", "Hace falta completar algunos datos de configuración para acceder a esta opción")
        return

    entrada_vehiculo_frame = tk.Frame(raiz, bg="beige")
    entrada_vehiculo_frame.grid(row=0, column=0, sticky='nsew')

    # Configurar el grid para centrado
    entrada_vehiculo_frame.grid_columnconfigure(0, weight=1)
    entrada_vehiculo_frame.grid_columnconfigure(1, weight=1)

    # Mostrar el frame
    mostrar_frame(entrada_vehiculo_frame)

    # Calcular espacios disponibles
    espacios_disponibles = len([espacio for espacio in parqueo if not espacio])

    if espacios_disponibles == 0:
        # Mostrar mensaje de no hay espacio
        no_espacio_label = tk.Label(entrada_vehiculo_frame, text="NO HAY ESPACIO", font=("Consolas", 35, "bold"), fg="red", bg="beige")
        no_espacio_label.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')
        #return --por si acaso, acá podríamos poner esto si es necesario, pero antes no poníamos ese return
    else:
        # Título del frame
        titulo_label = tk.Label(entrada_vehiculo_frame, text="Estacionamiento | Entrada de Vehículo", font=("Consolas", 20), bg="beige")
        titulo_label.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')

        # Etiqueta de espacios disponibles
        espacios_disponibles_label = tk.Label(entrada_vehiculo_frame, text="Espacios disponibles:", font=("Consolas", 14), bg="beige")
        espacios_disponibles_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        # Mostrar espacios disponibles
        espacios_disponibles_valor = tk.Label(entrada_vehiculo_frame, text=str(espacios_disponibles), font=("Consolas", 14), bg="beige")
        espacios_disponibles_valor.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # Etiqueta para la placa
        placa_label = tk.Label(entrada_vehiculo_frame, text="SU PLACA:", font=("Consolas", 14), bg="beige")
        placa_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        # Entry para la placa
        placa_var = tk.StringVar()
        placa_entry = tk.Entry(entrada_vehiculo_frame, textvariable=placa_var, font=("Consolas", 14), width=10)
        placa_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        # Validar longitud de placa
        def validar_placa(*args):
            placa = placa_var.get()
            if len(placa) > 8:
                placa_var.set(placa[:8])
        placa_var.trace('w', validar_placa)

        # Etiquetas y valores iniciales
        campo_asignado_label = tk.Label(entrada_vehiculo_frame, text="Campo asignado:", font=("Consolas", 14), bg="beige")
        campo_asignado_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        campo_asignado_valor = tk.Label(entrada_vehiculo_frame, text="x", font=("Consolas", 14), bg="beige")
        campo_asignado_valor.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        hora_entrada_label = tk.Label(entrada_vehiculo_frame, text="Hora de entrada:", font=("Consolas", 14), bg="beige")
        hora_entrada_label.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        hora_entrada_valor = tk.Label(entrada_vehiculo_frame, text="x", font=("Consolas", 14), bg="beige")
        hora_entrada_valor.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        precio_por_hora_label = tk.Label(entrada_vehiculo_frame, text="Precio por hora:", font=("Consolas", 14), bg="beige")
        precio_por_hora_label.grid(row=5, column=0, padx=10, pady=10, sticky='e')
        precio_por_hora_valor = tk.Label(entrada_vehiculo_frame, text=str(precio_por_hora), font=("Consolas", 14), bg="beige")
        precio_por_hora_valor.grid(row=5, column=1, padx=10, pady=10, sticky='w')

        pago_minimo_label = tk.Label(entrada_vehiculo_frame, text="Pago mínimo:", font=("Consolas", 14), bg="beige")
        pago_minimo_label.grid(row=6, column=0, padx=10, pady=10, sticky='e')
        pago_minimo_valor = tk.Label(entrada_vehiculo_frame, text=str(pago_minimo), font=("Consolas", 14), bg="beige")
        pago_minimo_valor.grid(row=6, column=1, padx=10, pady=10, sticky='w')

        # Función para validar la placa y actualizar la información
        def validar_y_actualizar(*args):
            placa = placa_var.get()
            if len(placa) > 0:
                # Verificar si la placa ya está en el estacionamiento
                for espacio in parqueo:
                    if espacio and espacio[0] == placa:
                        messagebox.showerror("Error", "Vehículo ya está dentro del estacionamiento")
                        placa_var.set("")
                        return

                # Encontrar el primer espacio disponible
                for idx, espacio in enumerate(parqueo):
                    if not espacio:
                        fecha_hora_entrada = datetime.now()
                        fecha_hora_entrada_str = fecha_hora_entrada.strftime("%H:%M %d/%m/%Y")

                        # Actualizar la información en los labels
                        campo_asignado_valor.config(text=str(idx + 1))
                        hora_entrada_valor.config(text=fecha_hora_entrada_str)
                        break

        placa_var.trace('w', validar_y_actualizar)

        # Botón Ok
        def ok_entrar():
            placa = placa_var.get()
            if len(placa) == 0:
                messagebox.showerror("Error", "La placa no puede estar vacía")
                return

            for idx, espacio in enumerate(parqueo):
                if not espacio:
                    fecha_hora_entrada = datetime.now()
                    parqueo[idx] = [
                        placa,
                        [fecha_hora_entrada.day, fecha_hora_entrada.month, fecha_hora_entrada.year, fecha_hora_entrada.hour, fecha_hora_entrada.minute],
                        [0, 0, 0, 0, 0],
                        0, None
                    ]
                    
                    entrada_vehiculo()
                    break

        boton_ok = tk.Button(entrada_vehiculo_frame, text="Ok", width=10, command=ok_entrar)
        boton_ok.grid(row=7, column=0, padx=25, pady=20)

        # Función para cancelar
        def cancelar_entrar():
           
            entrada_vehiculo()

        # Botón Cancelar
        boton_cancelar = tk.Button(entrada_vehiculo_frame, text="Cancelar", width=10, command=cancelar_entrar)
        boton_cancelar.grid(row=7, column=1, padx=25, pady=20)



"""4. CAJERO"""
def cajero():

    if cant_espacios == 0 or precio_por_hora == 0 or moneda1 == 0 or billete1 == 0:
        messagebox.showerror("Error", "Hace falta completar algunos datos de configuración para acceder al cajero")
        return

    # Guardar los estados iniciales de las variables para poder restaurarlas
    estado_inicial_parqueo = copy.deepcopy(parqueo)
    estado_inicial_dicc_cajero = copy.deepcopy(dicc_cajero)

    cajero_frame = tk.Frame(raiz, bg="beige")
    cajero_frame.grid(row=0, column=0, sticky='nsew')

    # Crear canvas y scrollbar
    canvas = tk.Canvas(cajero_frame, bg="beige")
    scrollbar = tk.Scrollbar(cajero_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="beige")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Configurar el grid para centrado
    scrollable_frame.grid_columnconfigure(0, weight=1)
    scrollable_frame.grid_columnconfigure(1, weight=1)
    scrollable_frame.grid_columnconfigure(2, weight=1)
    scrollable_frame.grid_columnconfigure(3, weight=1)

    # Mostrar el frame
    mostrar_frame(cajero_frame)

    # Título del frame
    titulo_label = tk.Label(scrollable_frame, text="Estacionamiento | CAJERO", font=("Consolas", 20, "bold"), bg="beige")
    titulo_label.grid(row=0, column=0, columnspan=3, pady=10, sticky='ew')

    # Precio por hora
    precio_label = tk.Label(scrollable_frame, text=f"{precio_por_hora} POR HORA", font=("Consolas", 12), bg="beige")
    precio_label.grid(row=1, column=2, pady=10, sticky='e')

    # Caja de entry para la placa
    placa_label = tk.Label(scrollable_frame, text="Paso 1. SU PLACA: ", font=("Consolas", 13), bg="beige")
    placa_label.grid(row=2, column=0, pady=10, sticky='w')

    placa_entry = tk.Entry(scrollable_frame, font=("Consolas", 14), width=10, validate="key")
    placa_entry.grid(row=2, column=1, pady=10, sticky='w')

    placa_entry_var = tk.StringVar()
    placa_entry.config(textvariable=placa_entry_var)

    # Hora de entrada
    hora_entrada_label = tk.Label(scrollable_frame, text="Hora de entrada: HH:MM dd/mm/aaaa", font=("Consolas", 13), bg="beige")
    hora_entrada_label.grid(row=3, column=0, columnspan=3, pady=10, sticky='w')

    # Hora de salida
    hora_salida_label = tk.Label(scrollable_frame, text="Hora de salida: HH:MM dd/mm/aaaa", font=("Consolas", 13), bg="beige")
    hora_salida_label.grid(row=4, column=0, columnspan=3, pady=10, sticky='w')

    # Tiempo cobrado
    tiempo_cobrado_label = tk.Label(scrollable_frame, text="Tiempo cobrado: XXh YYm zzzd", font=("Consolas", 13), bg="beige")
    tiempo_cobrado_label.grid(row=5, column=0, columnspan=3, pady=10, sticky='w')

    # A Pagar label
    a_pagar_label = tk.Label(scrollable_frame, text="A PAGAR", font=("Consolas", 14), bg="beige")
    a_pagar_label.grid(row=3, column=2, rowspan=3, pady=10, sticky='n')

    # Rectángulo de monto a pagar
    monto_a_pagar_canvas = tk.Canvas(scrollable_frame, width=150, height=60, bg="red")
    monto_a_pagar_canvas.grid(row=3, column=2, rowspan=3, pady=10, sticky='w')
    monto_a_pagar_canvas.create_rectangle(10, 10, 140, 50, fill="red", outline="red", width=2)
    monto_a_pagar_text = monto_a_pagar_canvas.create_text(75, 30, text="XXXXX", fill="white", font=("Consolas", 14, "bold"))

    # Pago label
    pago_label = tk.Label(scrollable_frame, text="Pago", font=("Consolas", 14), bg="beige")
    pago_label.grid(row=3, column=3, pady=10, sticky='w')

    # Rectángulo de pago
    pago_canvas = tk.Canvas(scrollable_frame, width=150, height=30, bg="lightgreen")
    pago_canvas.grid(row=3, column=4, pady=10, sticky='w')
    pago_canvas.create_rectangle(10, 10, 140, 20, fill="lightgreen", outline="lightgreen", width=2)
    pago_text = pago_canvas.create_text(75, 15, text="XXXXX", fill="black", font=("Consolas", 14, "bold"))

    # Cambio label
    cambio_label = tk.Label(scrollable_frame, text="Cambio", font=("Consolas", 14), bg="beige")
    cambio_label.grid(row=4, column=3, pady=10, sticky='w')

    # Rectángulo de cambio
    cambio_canvas = tk.Canvas(scrollable_frame, width=150, height=30, bg="lightgreen")
    cambio_canvas.grid(row=4, column=4, pady=10, sticky='w')
    cambio_canvas.create_rectangle(10, 10, 140, 20, fill="lightgreen", outline="lightgreen", width=2)
    cambio_text = cambio_canvas.create_text(75, 15, text="XXXXX", fill="black", font=("Consolas", 14, "bold"))



    def validar_longitud_placa(*args):
        texto_actual = placa_entry.get()
        if len(texto_actual) > 8:
            placa_entry_var.set(texto_actual[:8])
        elif len(texto_actual) == 8:
            validar_placa_existe()


    placa_entry_var.trace("w", validar_longitud_placa)

    def validar_placa_existe():
        global placa
        placa = placa_entry.get().strip()
        if len(placa) != 8:
            return

        placa_encontrada = False
        placa_pagada = False

        # Buscar la placa en el estacionamiento
        for espacio in parqueo:
            if espacio and espacio[0] == placa:
                placa_encontrada = True
                if espacio[3] == 0:
                    now = datetime.now()
                    espacio[2] = [now.day, now.month, now.year, now.hour, now.minute]
                    hora_entrada_label.config(text=f"Hora de entrada: {espacio[1][3]:02}:{espacio[1][4]:02} {espacio[1][0]:02}/{espacio[1][1]:02}/{espacio[1][2]}")
                    hora_salida_label.config(text=f"Hora de salida: {now.hour:02}:{now.minute:02} {now.day:02}/{now.month:02}/{now.year}")
                    
                    horas, minutos, dias = calcular_tiempo_cobrado(espacio[1], espacio[2])
                    tiempo_cobrado_label.config(text=f"Tiempo cobrado: {horas}h {minutos}m {dias}d")
                    global monto_a_pagar
                    monto_a_pagar = calcular_monto_a_pagar(horas, minutos, dias)
                    monto_a_pagar_canvas.itemconfig(monto_a_pagar_text, text=f"{monto_a_pagar:.2f}")
                    return
                else:
                    placa_pagada = True
                    break

        if placa_pagada:
            messagebox.showerror("Error", "Vehículo ya fue pagado")
        elif not placa_encontrada:
            messagebox.showerror("Error", "Vehículo no registrado en el estacionamiento")

        # Restablecer los campos
        placa_entry_var.set("")
        hora_entrada_label.config(text="Hora de entrada: HH:MM dd/mm/aaaa")
        hora_salida_label.config(text="Hora de salida: HH:MM dd/mm/aaaa")
        tiempo_cobrado_label.config(text="Tiempo cobrado: XXh YYm zzzd")
        monto_a_pagar_canvas.itemconfig(monto_a_pagar_text, text="XXXXX")

    # Paso 2: Su pago en
    paso2_label = tk.Label(scrollable_frame, text="Paso 2: SU PAGO EN", font=("Consolas", 14), bg="beige")
    paso2_label.grid(row=6, column=0, pady=10, sticky='w')

    # Columnas de métodos de pago
    monedas_label = tk.Label(scrollable_frame, text="MONEDAS", font=("Consolas", 14), bg="beige")
    monedas_label.grid(row=6, column=1, pady=10, sticky='w')

    billetes_label = tk.Label(scrollable_frame, text="BILLETES", font=("Consolas", 14), bg="beige")
    billetes_label.grid(row=6, column=2, pady=10, sticky='w')

    tarjeta_label = tk.Label(scrollable_frame, text="TARJETA DE CRÉDITO", font=("Consolas", 14), bg="beige")
    tarjeta_label.grid(row=6, column=3, pady=10, sticky='w')

    global dinero_acumulado, formando_pago, botones
    dinero_acumulado = 0
    formando_pago = {}

    botones = []

    def distribuir_monto(monto):
        denominaciones_billetes = [denom for denom in dicc_cajero['dicc_billetes'].keys() if isinstance(denom, int)]
        denominaciones_monedas = [denom for denom in dicc_cajero['dicc_monedas'].keys() if isinstance(denom, int)]
        denominaciones_disponibles = sorted(denominaciones_billetes + denominaciones_monedas, reverse=True)
        
        distribucion = {}
        for denominacion in denominaciones_disponibles:
            if monto == 0:
                break
            cantidad = monto // denominacion
            if cantidad > 0:
                distribucion[denominacion] = cantidad
                monto -= denominacion * cantidad
        
        return distribucion

    def actualizando_a_dicc_cajero(formando_pago, vuelto_formado):
        global parqueo, placa, dinero_acumulado
        # Actualizar dicc_cajero con las denominaciones utilizadas en formando_pago
        for denominacion, cantidad in formando_pago.items():
            if denominacion in dicc_cajero['dicc_billetes']:
                dicc_cajero['dicc_billetes'][denominacion][0][0] += cantidad
                dicc_cajero['dicc_billetes'][denominacion][0][1] = dicc_cajero['dicc_billetes'][denominacion][0][0] * denominacion
                dicc_cajero['dicc_billetes'][denominacion][2][0] = (dicc_cajero['dicc_billetes'][denominacion][0][0]) - (dicc_cajero['dicc_billetes'][denominacion][1][0])
                dicc_cajero['dicc_billetes'][denominacion][2][1] = (dicc_cajero['dicc_billetes'][denominacion][0][1]) - (dicc_cajero['dicc_billetes'][denominacion][1][1])

                dicc_cajero['dicc_billetes']['Total de billetes'][0][0] += cantidad
                dicc_cajero['dicc_billetes']['Total de billetes'][0][1] += denominacion * cantidad
                dicc_cajero['dicc_billetes']['Total de billetes'][2][0] = (dicc_cajero['dicc_billetes']['Total de billetes'][0][0]) - (dicc_cajero['dicc_billetes']['Total de billetes'][1][0])
                dicc_cajero['dicc_billetes']['Total de billetes'][2][1] = (dicc_cajero['dicc_billetes']['Total de billetes'][0][1]) - (dicc_cajero['dicc_billetes']['Total de billetes'][1][1])


            elif denominacion in dicc_cajero['dicc_monedas']:
                dicc_cajero['dicc_monedas'][denominacion][0][0] += cantidad
                dicc_cajero['dicc_monedas'][denominacion][0][1] = dicc_cajero['dicc_monedas'][denominacion][0][0] * denominacion
                dicc_cajero['dicc_monedas'][denominacion][2][0] = (dicc_cajero['dicc_monedas'][denominacion][0][0]) - (dicc_cajero['dicc_monedas'][denominacion][1][0])
                dicc_cajero['dicc_monedas'][denominacion][2][1] = (dicc_cajero['dicc_monedas'][denominacion][0][1]) - (dicc_cajero['dicc_monedas'][denominacion][1][1])

                dicc_cajero['dicc_monedas']['Total de monedas'][0][0] += cantidad
                dicc_cajero['dicc_monedas']['Total de monedas'][0][1] += denominacion * cantidad
                dicc_cajero['dicc_monedas']['Total de monedas'][2][0] = (dicc_cajero['dicc_monedas']['Total de monedas'][0][0]) - (dicc_cajero['dicc_monedas']['Total de monedas'][1][0])
                dicc_cajero['dicc_monedas']['Total de monedas'][2][1] = (dicc_cajero['dicc_monedas']['Total de monedas'][0][1]) - (dicc_cajero['dicc_monedas']['Total de monedas'][1][1])

        
        # Actualizar dicc_cajero con las denominaciones utilizadas en vuelto_formado
        if vuelto_formado:
            for denominacion, cantidad in vuelto_formado.items():
                if denominacion in dicc_cajero['dicc_billetes']:
                    dicc_cajero['dicc_billetes'][denominacion][1][0] += cantidad
                    dicc_cajero['dicc_billetes'][denominacion][1][1] = dicc_cajero['dicc_billetes'][denominacion][1][0] * denominacion
                    dicc_cajero['dicc_billetes'][denominacion][2][0] = (dicc_cajero['dicc_billetes'][denominacion][0][0]) - (dicc_cajero['dicc_billetes'][denominacion][1][0])
                    dicc_cajero['dicc_billetes'][denominacion][2][1] = (dicc_cajero['dicc_billetes'][denominacion][0][1]) - (dicc_cajero['dicc_billetes'][denominacion][1][1])

                    dicc_cajero['dicc_billetes']['Total de billetes'][1][0] += cantidad
                    dicc_cajero['dicc_billetes']['Total de billetes'][1][1] += denominacion * cantidad
                    dicc_cajero['dicc_billetes']['Total de billetes'][2][0] = (dicc_cajero['dicc_billetes']['Total de billetes'][0][0]) - (dicc_cajero['dicc_billetes']['Total de billetes'][1][0])
                    dicc_cajero['dicc_billetes']['Total de billetes'][2][1] = (dicc_cajero['dicc_billetes']['Total de billetes'][0][1]) - (dicc_cajero['dicc_billetes']['Total de billetes'][1][1])


                elif denominacion in dicc_cajero['dicc_monedas']:
                    dicc_cajero['dicc_monedas'][denominacion][1][0] += cantidad
                    dicc_cajero['dicc_monedas'][denominacion][1][1] = dicc_cajero['dicc_monedas'][denominacion][1][0] * denominacion
                    dicc_cajero['dicc_monedas'][denominacion][2][0] = (dicc_cajero['dicc_monedas'][denominacion][0][0]) - (dicc_cajero['dicc_monedas'][denominacion][1][0])
                    dicc_cajero['dicc_monedas'][denominacion][2][1] = (dicc_cajero['dicc_monedas'][denominacion][0][1]) - (dicc_cajero['dicc_monedas'][denominacion][1][1])

                    dicc_cajero['dicc_monedas']['Total de monedas'][1][0] += cantidad
                    dicc_cajero['dicc_monedas']['Total de monedas'][1][1] += denominacion * cantidad
                    dicc_cajero['dicc_monedas']['Total de monedas'][2][0] = (dicc_cajero['dicc_monedas']['Total de monedas'][0][0]) - (dicc_cajero['dicc_monedas']['Total de monedas'][1][0])
                    dicc_cajero['dicc_monedas']['Total de monedas'][2][1] = (dicc_cajero['dicc_monedas']['Total de monedas'][0][1]) - (dicc_cajero['dicc_monedas']['Total de monedas'][1][1])

        # Buscar la placa en el estacionamiento
        for espacio in parqueo:
            if espacio and espacio[0] == placa:
                espacio[3] = dinero_acumulado


        


    def bloquear_botones():
        for boton in botones:
            boton.config(state=tk.DISABLED)
        tarjeta_entry.config(state='readonly')
        
    def devolver_vuelto():
        global dinero_acumulado, formando_pago, vuelto_formado
        vuelto = dinero_acumulado - monto_a_pagar
        
        # Obtener denominaciones disponibles sin incluir las llaves no numéricas
        denominaciones_billetes = [denom for denom in dicc_cajero['dicc_billetes'].keys() if isinstance(denom, int)]
        denominaciones_monedas = [denom for denom in dicc_cajero['dicc_monedas'].keys() if isinstance(denom, int)]
        
        # Combinar y ordenar las denominaciones
        denominaciones_disponibles = denominaciones_billetes + denominaciones_monedas
        denominaciones_disponibles.sort(reverse=True)
        
        vuelto_formado = {}
        for denominacion in denominaciones_disponibles:
            if denominacion in dicc_cajero['dicc_billetes']:
                cantidad_disponible = dicc_cajero['dicc_billetes'][denominacion][2][0]
            else:
                cantidad_disponible = dicc_cajero['dicc_monedas'][denominacion][2][0]
            
            if vuelto >= denominacion and cantidad_disponible > 0:
                cantidad = min(vuelto // denominacion, cantidad_disponible)
                vuelto_formado[denominacion] = cantidad
                vuelto -= cantidad * denominacion
                if vuelto == 0:
                    break
        
        if vuelto == 0:
            cambio_canvas.itemconfigure(cambio_text, text=f"{dinero_acumulado - monto_a_pagar}")
            # Actualizar labels de monedas y billetes
            
            for denominacion, cantidad in vuelto_formado.items():
                if denominacion in dicc_cajero['dicc_billetes']:
                    cambio_billetes_labels[denominacion].config(text=f"{cantidad} de {denominacion}")
                else:
                    cambio_monedas_labels[denominacion].config(text=f"{cantidad} de {denominacion}")
            
            # Poner 0 en denominaciones no usadas para vuelto
            for denominacion in cambio_monedas_labels:
                if denominacion not in vuelto_formado:
                    cambio_monedas_labels[denominacion].config(text=f"0 de {denominacion}")
            for denominacion in cambio_billetes_labels:
                if denominacion not in vuelto_formado:
                    cambio_billetes_labels[denominacion].config(text=f"0 de {denominacion}")
            #Bloquear botones
            for boton in botones:
                boton.config(state=tk.DISABLED)
            tarjeta_entry.config(state='readonly')
        else:
            messagebox.showerror("Error", "No hay suficiente cambio disponible. Intente pagar con tarjeta o espere a que recarguen el cajero.")
            dinero_acumulado = 0
            formando_pago = {}
            actualizar_pago()

            # Reiniciar labels de monedas y billetes a XX
            for denominacion in cambio_monedas_labels:
                cambio_monedas_labels[denominacion].config(text=f"XX de {denominacion}")
            for denominacion in cambio_billetes_labels:
                cambio_billetes_labels[denominacion].config(text=f"XX de {denominacion}")


    def actualizar_pago():
        # Actualizar la visualización del monto acumulado
        pago_canvas.itemconfigure(pago_text, text=f"{dinero_acumulado}")

    def boton_moneda_click(denominacion):
        global dinero_acumulado, formando_pago, parqueo, placa
        # Verificar si el monto acumulado aún no alcanza el monto a pagar
        if dinero_acumulado < monto_a_pagar:
            dinero_acumulado += denominacion
            # Actualizar la visualización del monto acumulado
            actualizar_pago()
            # Actualizar la lista formando_pago
            formando_pago[denominacion] = formando_pago.get(denominacion, 0) + 1
            
            # Si se alcanza el monto a pagar, bloquear los botones
            if dinero_acumulado >= monto_a_pagar:
                if dinero_acumulado == monto_a_pagar:
                    bloquear_botones()
                    cambio_canvas.itemconfigure(cambio_text, text=0)
                    actualizando_a_dicc_cajero(formando_pago, {})
                else:
                    devolver_vuelto()
                    actualizando_a_dicc_cajero(formando_pago, vuelto_formado)
                # Actualizar parqueo con el método de pago
                for espacio in parqueo:
                    if espacio and espacio[0] == placa:
                        espacio[4] = "efectivo"  # Registrar que el pago fue con efectivo
                        break

                

    def boton_billete_click(denominacion):
        global dinero_acumulado, formando_pago, parqueo, placa
        # Verificar si el monto acumulado aún no alcanza el monto a pagar
        if dinero_acumulado < monto_a_pagar:
            dinero_acumulado += denominacion
            # Actualizar la visualización del monto acumulado
            actualizar_pago()
            # Actualizar la lista formando_pago
            formando_pago[denominacion] = formando_pago.get(denominacion, 0) + 1
            
            # Si se alcanza el monto a pagar, bloquear los botones
            if dinero_acumulado >= monto_a_pagar:
                if dinero_acumulado == monto_a_pagar:
                    bloquear_botones()
                    cambio_canvas.itemconfigure(cambio_text, text=0)
                    actualizando_a_dicc_cajero(formando_pago, {})
                else:
                    devolver_vuelto()
                    actualizando_a_dicc_cajero(formando_pago, vuelto_formado)
                # Actualizar parqueo con el método de pago
                for espacio in parqueo:
                    if espacio and espacio[0] == placa:
                        espacio[4] = "efectivo"  # Registrar que el pago fue con efectivo
                        break



    def crear_botones_pago():
        fila_inicial = 7   

        # Botones para monedas
        fila_monedas = fila_inicial
        for denominacion in dicc_cajero['dicc_monedas']:
            if isinstance(denominacion, int):
                canvas_moneda = tk.Canvas(scrollable_frame, width=50, height=50, bg="beige", highlightthickness=0)
                canvas_moneda.grid(row=fila_monedas, column=1, pady=5, padx=5, sticky='w')
                canvas_moneda.create_oval(2, 15, 50, 45, fill="lightblue", outline="lightblue")
                canvas_moneda.create_text(25, 30, text=f"{denominacion}", font=("Consolas", 12), fill="black")
                canvas_moneda.bind("<Button-1>", lambda e, denom=denominacion: boton_moneda_click(denom))
                botones.append(canvas_moneda)  # Añadir a la lista de botones
                fila_monedas += 1

        # Botones para billetes
        fila_billetes = fila_inicial
        for denominacion in dicc_cajero['dicc_billetes']:
            if isinstance(denominacion, int):
                boton_billete = tk.Button(scrollable_frame, text=f"{denominacion}", font=("Consolas", 12), bg="lightyellow", relief="raised")
                boton_billete.grid(row=fila_billetes, column=2, pady=5, padx=5, sticky='w')
                boton_billete.config(width=15, height=1)
                boton_billete.config(command=lambda denom=denominacion: boton_billete_click(denom))
                botones.append(boton_billete)  # Añadir a la lista de botones
                fila_billetes += 1

    crear_botones_pago()

    

    # Entry para tarjeta de crédito
    tarjeta_entry = tk.Entry(scrollable_frame, font=("Consolas", 14), width=15, validate="key")
    tarjeta_entry.grid(row=7, column=3, pady=5, sticky='w')

    tarjeta_entry_var = tk.StringVar()
    tarjeta_entry.config(textvariable=tarjeta_entry_var)

    def validar_tarjeta(*args):
        global dinero_acumulado, parqueo, placa
        texto_actual = tarjeta_entry.get()
        if not texto_actual.isdigit() or len(texto_actual) > 10:
            tarjeta_entry_var.set(re.sub(r'\D', '', texto_actual)[:10])

        if len(texto_actual) == 10:
            dinero_acumulado = monto_a_pagar
            formando_pago.clear()
            formando_pago.update(distribuir_monto(monto_a_pagar))
            
            actualizar_pago()
            cambio_canvas.itemconfigure(cambio_text, text=0)
            actualizando_a_dicc_cajero(formando_pago, {})

            # Actualizar parqueo con el método de pago
            for espacio in parqueo:
                if espacio and espacio[0] == placa:
                    espacio[4] = "tarjeta"  # Registrar que el pago fue con tarjeta
                    break
            
            bloquear_botones()

    tarjeta_entry_var.trace("w", validar_tarjeta)


    # Paso 3: Su cambio
    fila_billetes = 12
    paso3_label = tk.Label(scrollable_frame, text="Paso 3: Su cambio en:", font=("Consolas", 14), bg="beige")
    paso3_label.grid(row=fila_billetes, column=0, pady=10, sticky='w')

    monedas_cambio_label = tk.Label(scrollable_frame, text="MONEDAS", font=("Consolas", 14), bg="beige")
    monedas_cambio_label.grid(row=fila_billetes, column=1, pady=10, sticky='w')

    billetes_cambio_label = tk.Label(scrollable_frame, text="BILLETES", font=("Consolas", 14), bg="beige")
    billetes_cambio_label.grid(row=fila_billetes, column=2, pady=10, sticky='w')

    fila_cambio_monedas = fila_billetes + 1
    fila_cambio_billetes = fila_billetes + 1

    # Inicializar frases de cambio para monedas
    cambio_monedas_labels = {}
    for denominacion in dicc_cajero['dicc_monedas']:
        if isinstance(denominacion, int):  # Evitar "Total de monedas"
            cambio_monedas_labels[denominacion] = tk.Label(scrollable_frame, text=f"XX de {denominacion}", font=("Consolas", 14), bg="beige")
            cambio_monedas_labels[denominacion].grid(row=fila_cambio_monedas, column=1, pady=5, sticky='w')
            fila_cambio_monedas += 1

    # Inicializar frases de cambio para billetes
    cambio_billetes_labels = {}
    for denominacion in dicc_cajero['dicc_billetes']:
        if isinstance(denominacion, int):  # Evitar "Total de billetes"
            cambio_billetes_labels[denominacion] = tk.Label(scrollable_frame, text=f"XX de {denominacion}", font=("Consolas", 14), bg="beige")
            cambio_billetes_labels[denominacion].grid(row=fila_cambio_billetes, column=2, pady=5, sticky='w')
            fila_cambio_billetes += 1


    def anular_pago():
        global parqueo, dicc_cajero
        
        parqueo = estado_inicial_parqueo
        
        dicc_cajero = estado_inicial_dicc_cajero
        cajero()

    # Botón Anular el pago
    anular_button = tk.Button(scrollable_frame, text="Anular el pago", width=15, command=anular_pago)
    anular_button.grid(row=18, column=0, columnspan=2, pady=20)


    def ok_pago():
        mostrar_frame(inicio_frame)
        cajero()

    # Botón Ok
    poner_ok_button = tk.Button(scrollable_frame, text="Ok", width=15, command=ok_pago)
    poner_ok_button.grid(row=18, column=1, columnspan=2, pady=20)





"""5. SALIDA DE VEHÍCULO"""

def salida_vehiculo():

    if cant_espacios == 0 or precio_por_hora == 0 or moneda1 == 0 or billete1 == 0:
        messagebox.showerror("Error", "Hace falta completar algunos datos de configuración para acceder a esta opción")
        return

    salida_vehiculo_frame = tk.Frame(raiz, bg="beige")
    salida_vehiculo_frame.grid(row=0, column=0, sticky='nsew')

    # Configurar el grid para centrado
    salida_vehiculo_frame.grid_columnconfigure(0, weight=1)
    salida_vehiculo_frame.grid_columnconfigure(1, weight=1)
    salida_vehiculo_frame.grid_columnconfigure(2, weight=1)

    # Mostrar el frame
    mostrar_frame(salida_vehiculo_frame)

    # Título del frame
    titulo_label = tk.Label(salida_vehiculo_frame, text="Estacionamiento | Salida de Vehículo", font=("Consolas", 20), bg="beige")
    titulo_label.grid(row=0, column=0, columnspan=3, pady=10, sticky='ew')

    # Caja de entry para la placa
    placa_label = tk.Label(salida_vehiculo_frame, text="Su placa: ", font=("Consolas", 13), bg="beige")
    placa_label.grid(row=2, column=0, pady=10, sticky='e')

    placa_entry = tk.Entry(salida_vehiculo_frame, font=("Consolas", 14), width=10, validate="key")
    placa_entry.grid(row=2, column=1, pady=10, sticky='w')

    placa_entry_var = tk.StringVar()
    placa_entry.config(textvariable=placa_entry_var)


    def calcular_minutos_transcurridos(fecha_hora_inicio, fecha_hora_fin):
        # Conversión de listas de fecha y hora a objetos datetime para el cálculo de la diferencia
        dt_inicio = datetime(fecha_hora_inicio[2], fecha_hora_inicio[1], fecha_hora_inicio[0],
                             fecha_hora_inicio[3], fecha_hora_inicio[4])
        dt_fin = datetime(fecha_hora_fin[2], fecha_hora_fin[1], fecha_hora_fin[0],
                          fecha_hora_fin[3], fecha_hora_fin[4])
        delta = dt_fin - dt_inicio
        return delta.total_seconds() // 60

    def ok_salir():
        global parqueo, historial_parqueo
        now = datetime.now()
        fecha_hora_de_salida = [now.day, now.month, now.year, now.hour, now.minute]
        

        # Buscar la placa en el estacionamiento
        for i, espacio in enumerate(parqueo):
            if espacio and espacio[0] == placa:
                fecha_hora_pago = espacio[2]
                tiempo_transcurrido = calcular_minutos_transcurridos(fecha_hora_pago, fecha_hora_de_salida)
                
                
                if tiempo_transcurrido > minutos_maximos:
                    horas_excedidas, minutos_excedidos = divmod(tiempo_transcurrido - minutos_maximos, 60)
                    horas_excedidas = int(horas_excedidas)
                    minutos_excedidos = int(minutos_excedidos)
                    
                    error_label = tk.Label(salida_vehiculo_frame, text=f"No puede salir porque excedió el tiempo permitido para ello.\n"
                                                                      f"Tiempo máximo para salir luego del pago: {minutos_maximos} minutos\n"
                                                                      f"Tiempo que usted ha tardado: {horas_excedidas}h {minutos_excedidos}m\n"
                                                                      f"Debe regresar al cajero a pagar la diferencia",
                                           font=("Consolas", 16, "bold"), bg="beige", fg="red", justify="center")
                    error_label.grid(row=4, column=0, columnspan=3, pady=10, sticky='ew')

                    espacio[1] = espacio[2]
                    espacio[2] = 0
                    espacio[3] = 0
                    espacio[4] = None
                    # Botón Regresar y pagar la diferencia
                    def regresar_a_pagar():
                        mostrar_frame(inicio_frame)
                    poner_regresar_pagar_button = tk.Button(salida_vehiculo_frame, text="Regresar y pagar la diferencia", width=80, command=regresar_a_pagar)
                    poner_regresar_pagar_button.grid(row=5, column=0, columnspan=10, pady=20)
                    
                    
                else:
                    numero_espacio = i + 1
                    historial_parqueo.append([placa, numero_espacio, espacio[1], espacio[2], espacio[3], espacio[4], fecha_hora_de_salida])
                    parqueo[i] = []
                    
                    salida_vehiculo() 

    def cancelar_salir():
        salida_vehiculo()

        
    def validar_placa_existe_func5():
        global placa
        placa = placa_entry.get().strip()
        if len(placa) != 8:
            return

        placa_encontrada = False
        placa_pagada = False

        # Buscar la placa en el estacionamiento
        
        for espacio in parqueo:
            if espacio and espacio[0] == placa:
                placa_encontrada = True
                if espacio[3] != 0:
                    placa_pagada = True
                break

        if not placa_encontrada:
            messagebox.showerror("Error", "Vehículo no registrado en el estacionamiento")
            # Restablecer los campos
            placa_entry_var.set("")
        elif not placa_pagada:
            messagebox.showerror("Error", "Hace falta pagar el vehículo para hacer la salida")
            # Restablecer los campos
            placa_entry_var.set("")
        
        else:
            # Botón Ok
            poner_ok_button = tk.Button(salida_vehiculo_frame, text="Ok", width=15, command=ok_salir)
            poner_ok_button.grid(row=5, column=0, columnspan=2, pady=20)

            # Botón Cancelar
            anular_button = tk.Button(salida_vehiculo_frame, text="Cancelar", width=15, command=cancelar_salir)
            anular_button.grid(row=5, column=1, columnspan=2, pady=20)
       

    def validar_longitud_placa_func5(*args):
        texto_actual = placa_entry.get()
        if len(texto_actual) > 8:
            placa_entry_var.set(texto_actual[:8])
        elif len(texto_actual) == 8:
            validar_placa_existe_func5()

    placa_entry_var.trace("w", validar_longitud_placa_func5)




"""6. REPORTE DE INGRESOS DE DINERO"""

def reporte_ingresos():

    if cant_espacios == 0 or precio_por_hora == 0 or moneda1 == 0 or billete1 == 0:
        messagebox.showerror("Error", "Hace falta completar algunos datos de configuración para acceder a esta opción")
        return

    reporte_ingresos_frame = tk.Frame(raiz, bg="beige")
    reporte_ingresos_frame.grid(row=0, column=0, sticky='nsew')

    # Configurar el grid para centrado
    reporte_ingresos_frame.grid_columnconfigure(0, weight=1)
    reporte_ingresos_frame.grid_columnconfigure(1, weight=1)
    reporte_ingresos_frame.grid_columnconfigure(2, weight=1)

    # Mostrar el frame
    mostrar_frame(reporte_ingresos_frame)

    # Título del frame
    titulo_label = tk.Label(reporte_ingresos_frame, text="Estacionamiento | Reporte de Ingresos de Dinero", font=("Consolas", 20), bg="beige")
    titulo_label.grid(row=0, column=0, columnspan=3, pady=10, sticky='ew')

    def calcular_ingresos():
        fecha_inicio = fecha_inicio_entry.get().strip()
        fecha_fin = fecha_fin_entry.get().strip()
        fecha_estimacion = fecha_estimacion_entry.get().strip()
        hora_estimacion = hora_estimacion_entry.get().strip()
        minutos_estimacion = minutos_estimacion_entry.get().strip()

        if not (validar_fecha(fecha_inicio) and validar_fecha(fecha_fin)):
            messagebox.showerror("Error", "Ingrese fechas válidas en el formato dd/mm/aaaa")
            return

        if fecha_estimacion or hora_estimacion or minutos_estimacion:
            if not (validar_fecha(fecha_estimacion) and validar_hora(hora_estimacion, minutos_estimacion)):
                messagebox.showerror("Error", "Ingrese una fecha y hora de estimación válidas\n Fecha va en el formato dd/mm/aaaa")
                return

        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%d/%m/%Y")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%d/%m/%Y")

        if fecha_inicio_dt > fecha_fin_dt:
            messagebox.showerror("Error", "La fecha de inicio no puede ser posterior a la fecha de fin")
            return

        total_efectivo = 0
        total_tarjeta = 0

        for espacio in parqueo:
            if espacio and espacio[3] != 0:
                fecha_pago_dt = datetime(espacio[2][2], espacio[2][1], espacio[2][0])
                if fecha_inicio_dt <= fecha_pago_dt <= fecha_fin_dt:
                    if espacio[4] == 'efectivo':
                        total_efectivo += espacio[3]
                    elif espacio[4] == 'tarjeta':
                        total_tarjeta += espacio[3]

        for espacio in historial_parqueo:
            if espacio and espacio[4] != 0:
                fecha_pago_dt = datetime(espacio[3][2], espacio[3][1], espacio[3][0])
                if fecha_inicio_dt <= fecha_pago_dt <= fecha_fin_dt:
                    if espacio[5] == 'efectivo':
                        total_efectivo += espacio[4]
                    elif espacio[5] == 'tarjeta':
                        total_tarjeta += espacio[4]


        total_ingresos = total_efectivo + total_tarjeta

        total_efectivo_label.config(text=f"Total de ingresos en efectivo: {total_efectivo:,.2f}")
        total_tarjeta_label.config(text=f"Total de ingresos por tarjeta de crédito: {total_tarjeta:,.2f}")
        total_ingresos_label.config(text=f"Total de ingresos: {total_ingresos:,.2f}")

        if fecha_estimacion and hora_estimacion and minutos_estimacion:
            fecha_estimacion_dt = datetime.strptime(fecha_estimacion, "%d/%m/%Y")
            hora_estimacion_dt = timedelta(hours=int(hora_estimacion), minutes=int(minutos_estimacion))
            fecha_hora_estimacion_dt = fecha_estimacion_dt + hora_estimacion_dt

            estimado_ingresos = 0

            for espacio in parqueo:
                if espacio and espacio[3] == 0:
                    fecha_entrada_dt = datetime(espacio[1][2], espacio[1][1], espacio[1][0], espacio[1][3], espacio[1][4])
                    tiempo_estacionado = fecha_hora_estimacion_dt - fecha_entrada_dt
                    minutos_estacionados = tiempo_estacionado.total_seconds() // 60
                    if minutos_estacionados <= minutos_maximos:
                        estimado_ingresos += precio_por_hora
                    else:
                        horas_a_cobrar = (minutos_estacionados - minutos_maximos) // 60 + 1
                        estimado_ingresos += horas_a_cobrar * precio_por_hora

            estimado_ingresos_label.config(text=f"Estimado de ingresos por recibir: {estimado_ingresos:,.2f}")


    def cancelar():
        mostrar_frame(inicio_frame)


    # Cajas de entry para las fechas
    fecha_inicio_label = tk.Label(reporte_ingresos_frame, text="Ingresos desde el día:", font=("Consolas", 14), bg="beige")
    fecha_inicio_label.grid(row=1, column=0, pady=10, sticky='e')

    fecha_inicio_entry = tk.Entry(reporte_ingresos_frame, font=("Consolas", 14), width=10)
    fecha_inicio_entry.grid(row=1, column=1, pady=10, sticky='w')

    fecha_fin_label = tk.Label(reporte_ingresos_frame, text="Hasta el día:", font=("Consolas", 14), bg="beige")
    fecha_fin_label.grid(row=2, column=0, pady=10, sticky='e')

    fecha_fin_entry = tk.Entry(reporte_ingresos_frame, font=("Consolas", 14), width=10)
    fecha_fin_entry.grid(row=2, column=1, pady=10, sticky='w')

    # Para la estimación de ingresos
    estimacion_label = tk.Label(reporte_ingresos_frame, text="Para hacer una estimación de ingresos digite la fecha y hora\n hasta la cual ocupa la estimación:", font=("Consolas", 14), bg="beige")
    estimacion_label.grid(row=7, column=0, columnspan=3, pady=10, sticky='w')

    fecha_estimacion_label = tk.Label(reporte_ingresos_frame, text="Fecha para la estimación:", font=("Consolas", 14), bg="beige")
    fecha_estimacion_label.grid(row=8, column=0, pady=10, sticky='e')

    fecha_estimacion_entry = tk.Entry(reporte_ingresos_frame, font=("Consolas", 14), width=10)
    fecha_estimacion_entry.grid(row=8, column=1, pady=10, sticky='w')

    hora_estimacion_label = tk.Label(reporte_ingresos_frame, text="Hora para la estimación:", font=("Consolas", 14), bg="beige")
    hora_estimacion_label.grid(row=9, column=0, pady=10, sticky='e')

    hora_estimacion_entry = tk.Entry(reporte_ingresos_frame, font=("Consolas", 14), width=5)
    hora_estimacion_entry.grid(row=9, column=1, pady=10, sticky='w')

    minutos_estimacion_entry = tk.Entry(reporte_ingresos_frame, font=("Consolas", 14), width=5)
    minutos_estimacion_entry.grid(row=9, column=2, pady=10, sticky='w')

    # Espacio para mostrar los resultados
    total_efectivo_label = tk.Label(reporte_ingresos_frame, text="Total de ingresos en efectivo: xxx.xxx.xxx", font=("Consolas", 13, "bold"), bg="beige")
    total_efectivo_label.grid(row=3, column=0, columnspan=3, pady=10, sticky='w')

    total_tarjeta_label = tk.Label(reporte_ingresos_frame, text="Total de ingresos por tarjeta de crédito: xxx.xxx.xxx", font=("Consolas", 13, "bold"), bg="beige")
    total_tarjeta_label.grid(row=4, column=0, columnspan=3, pady=10, sticky='w')

    total_ingresos_label = tk.Label(reporte_ingresos_frame, text="Total de ingresos: xxx.xxx.xxx", font=("Consolas", 13, "bold"), bg="beige")
    total_ingresos_label.grid(row=5, column=0, columnspan=3, pady=10, sticky='w')

    estimado_ingresos_label = tk.Label(reporte_ingresos_frame, text="Estimado de ingresos por recibir: xxx.xxx.xxx", font=("Consolas", 13, "bold"), bg="beige")
    estimado_ingresos_label.grid(row=10, column=0, columnspan=3, pady=10, sticky='w')

    # Botones de Ok y Cancelar
    ok_button = tk.Button(reporte_ingresos_frame, text="Ok", width=15, command=calcular_ingresos)
    ok_button.grid(row=16, column=0, columnspan=1, pady=10)

    cancelar_button = tk.Button(reporte_ingresos_frame, text="Cancelar", width=15, command=cancelar)
    cancelar_button.grid(row=16, column=1, columnspan=1, pady=10)
  








"""7. AYUDA"""
#7.1. Función acerca_de

#Qué hace: abrir el manual
#Entradas: el archivo del manual
#Salidas: abre el manual en un lector de PDF
def ayuda():

    def regresar():
        mostrar_frame(inicio_frame)

    ayuda_frame = tk.Frame(raiz, bg="beige")
    ayuda_frame.grid(row=0, column=0, sticky='nsew')

    # Configurar el grid para centrado
    ayuda_frame.grid_columnconfigure(0, weight=1)
    ayuda_frame.grid_rowconfigure(0, weight=1)

    # Mostrar el frame
    mostrar_frame(ayuda_frame)

    # Título del frame
    titulo_label = tk.Label(ayuda_frame, text="Estacionamiento | Manual de Usuario", font=("Consolas", 20), bg="beige")
    titulo_label.grid(row=0, column=0, pady=10, sticky='ew')

    # Text widget para mostrar el contenido del PDF
    texto_pdf = scrolledtext.ScrolledText(ayuda_frame, wrap=tk.WORD, bg="white", font=("Consolas", 12))
    texto_pdf.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

    # Botón Cancelar
    boton_regresar = tk.Button(ayuda_frame, text="Regresar", command=regresar)
    boton_regresar.grid(row=2, column=0, pady=10)

    # Extraer el texto del PDF
    try:
        pdf_documento = fitz.open("manual_de_usuario_estacionamiento.pdf")
        texto_completo = ""
        for pagina in pdf_documento:
            texto_completo += pagina.get_text()
        texto_pdf.insert(tk.END, texto_completo)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el PDF: {e}")

    mostrar_frame(ayuda_frame)




"""8. ACERCA DE"""
#8.1. Función acerca_de

#Qué hace: desplegar información de interés sobre el proyecto
#Entradas: los datos del Acerca de 
#Salidas: un messagebox con los datos del Acerca de

def acerca_de():
    nombre_programa = "Estacionamiento de Vehículos"
    version = "1.0.0"
    fecha_creacion = "17/06/2024"
    autor = "Adrián Mora Rivera"
    mensaje = f"""
Programa: {nombre_programa} \n
Versión: {version} \n
Fecha de creación: {fecha_creacion} \n
Autor: {autor}
"""
    messagebox.showinfo("Acerca de", mensaje)


"""9. SALIR"""
#9.1. Función cerrar_aplicacion

#Qué hace: cerrar la aplicación y guardar los datos en los archivos
#Entradas: todas las estructuras almacenadas en los archivos
#Salidas: los datos guardados
def cerrar_aplicacion():
    
    grabar_archivos(cant_espacios, precio_por_hora, pago_minimo, redondeo, minutos_maximos, moneda1, moneda2, moneda3, billete1, billete2, billete3, billete4, billete5, parqueo, historial_parqueo, dicc_cajero)
    raiz.destroy()



"""Funciones para hacer frames"""
def mostrar_frame(frame):
    frame.tkraise()
          
#########################################################################

# FUNCIONES PARA LEER Y GRABAR DATOS. POR DEFAULT LOS ARCHIVOS SE CREAN EN EL DIRECTORIO DONDE ESTÁ EL PROGRAMA
#Para el cajero: hacer un diccionario cuyas llaves son cada denominacion y los valores son: cantidad de entrada, cantidad de salida, cantidad total



# Leer los datos de los archivos y asignarlos a las estructuras y variables del programa
def leer_archivos():    
    # leer archivo de configuración
    try:
        archivo_configuracion = open("configuración.dat", "r")
        cant_espacios = eval(archivo_configuracion.readline()[:-1])
        precio_por_hora = eval(archivo_configuracion.readline()[:-1])
        pago_minimo = eval(archivo_configuracion.readline()[:-1])
        redondeo = eval(archivo_configuracion.readline()[:-1])
        minutos_maximos = eval(archivo_configuracion.readline()[:-1])       
        moneda1 = eval(archivo_configuracion.readline()[:-1])       
        moneda2 = eval(archivo_configuracion.readline()[:-1])       
        moneda3 = eval(archivo_configuracion.readline()[:-1])       
        billete1 = eval(archivo_configuracion.readline()[:-1])       
        billete2 = eval(archivo_configuracion.readline()[:-1])       
        billete3 = eval(archivo_configuracion.readline()[:-1])       
        billete4 = eval(archivo_configuracion.readline()[:-1])       
        billete5 = eval(archivo_configuracion.readline()[:-1])       
        archivo_configuracion.close()

    except: # cuando el archivo no existe se inicializan los datos respectivos
        cant_espacios = 0
        precio_por_hora = 0
        pago_minimo = 0
        redondeo = 0
        minutos_maximos = 0      
        moneda1 = 0       
        moneda2 = 0   
        moneda3 = 0      
        billete1 = 0       
        billete2 = 0       
        billete3 = 0       
        billete4 = 0      
        billete5 = 0      

    # leer archivo de parqueo
    try:
        archivo_parqueo = open("parqueo.dat", "rb")
        parqueo = pickle.load(archivo_parqueo)
        archivo_parqueo.close()
    except: # cuando el archivo no existe se inicializan los datos respectivos
        parqueo = []
        

    # leer archivo de historial_parqueo
    try:
        archivo_historial_parqueo = open("historial_parqueo.dat", "rb")
        historial_parqueo = pickle.load(archivo_historial_parqueo)
        archivo_historial_parqueo.close()
    except: # cuando el archivo no existe se inicializan los datos respectivos
        historial_parqueo = []


    # leer archivo de cajero
    try:
        archivo_cajero = open("cajero.dat", "rb")
        dicc_cajero = pickle.load(archivo_cajero)
        archivo_cajero.close()

    except: # cuando el archivo no existe se inicializan los datos respectivos
        dicc_cajero = {}
       
    return cant_espacios, precio_por_hora, pago_minimo, redondeo, minutos_maximos, moneda1, moneda2, moneda3, billete1, billete2, billete3, billete4, billete5, parqueo, historial_parqueo, dicc_cajero


# Grabar datos en los archivos
def grabar_archivos(cant_espacios, precio_por_hora, pago_minimo, redondeo, minutos_maximos, moneda1, moneda2, moneda3, billete1, billete2, billete3, billete4, billete5, parqueo, historial_parqueo, dicc_cajero):

    # grabar archivo de configuración (archivo tipo string por líneas.)
    archivo_configuracion = open("configuración.dat", "w")
    archivo_configuracion.write(str(cant_espacios) + "\n")
    archivo_configuracion.write(str(precio_por_hora) + "\n")
    archivo_configuracion.write(str(pago_minimo) + "\n")
    archivo_configuracion.write(str(redondeo) + "\n")
    archivo_configuracion.write(str(minutos_maximos) + "\n")
    archivo_configuracion.write(str(moneda1) + "\n")
    archivo_configuracion.write(str(moneda2) + "\n")
    archivo_configuracion.write(str(moneda3) + "\n")
    archivo_configuracion.write(str(billete1) + "\n")
    archivo_configuracion.write(str(billete2) + "\n")
    archivo_configuracion.write(str(billete3) + "\n")
    archivo_configuracion.write(str(billete4) + "\n")
    archivo_configuracion.write(str(billete5) + "\n")
    archivo_configuracion.close()
    
    
    # grabar archivo de parqueo (archivo tipo binario)
    archivo_parqueo = open("parqueo.dat", "wb")
    print("grabar", parqueo)
    pickle.dump(parqueo, archivo_parqueo)
    archivo_parqueo.close()


    # grabar archivo de historial_parqueo (archivo tipo binario)
    archivo_historial_parqueo = open("historial_parqueo.dat", "wb")
    pickle.dump(historial_parqueo, archivo_historial_parqueo)
    archivo_historial_parqueo.close()

    # grabar archivo de cajero (archivo tipo binario)
    archivo_cajero = open("cajero.dat", "wb")
    pickle.dump(dicc_cajero, archivo_cajero)
    archivo_cajero.close()   

        
    return


############################################################











""" * * * * * * * * * f u n c i ó n    p r i n c i p a l * * * * * * * """
                
# FUNCIÓN PRINCIPAL

# Menú inicial

# leer datos grabados en los archivos para asignarlos a las variables que usa el programa
cant_espacios, precio_por_hora, pago_minimo, redondeo, minutos_maximos, moneda1, moneda2, moneda3, billete1, billete2, billete3, billete4, billete5, parqueo, historial_parqueo, dicc_cajero = leer_archivos()  

raiz = Tk()
raiz.title("Estacionamiento de Vehículos")
raiz.geometry("850x658")
raiz.config(bg="beige")
raiz.grid_rowconfigure(0, weight=1)
raiz.grid_columnconfigure(0, weight=1)

icon_image = Image.open("icono.png") #Agregarle un ícono a la ventana
icon_photo = ImageTk.PhotoImage(icon_image)
raiz.iconphoto(False, icon_photo)

#Barra de menús
barraMenu = Menu(raiz)
raiz.config(menu=barraMenu) #Agregando la barra a la ventana inicial

# Creando cada menú
mnuConfiguracion = Menu(barraMenu, tearoff=0)
mnuDinero_del_Cajero = Menu(barraMenu, tearoff=0)
mnuEntrada_de_vehiculo = Menu(barraMenu, tearoff=0)
mnuCajero = Menu(barraMenu, tearoff=0)
mnuSalida_de_vehiculo = Menu(barraMenu, tearoff=0)
mnuReporte_de_ingresos_de_dinero = Menu(barraMenu, tearoff=0)
mnuAyuda = Menu(barraMenu, tearoff=0)
mnuAcerca_de = Menu(barraMenu, tearoff=0)

# Agregando las opciones de la barra de menús
barraMenu.add_cascade(label="Configuración", command=configuracion)
barraMenu.add_cascade(label="Dinero del cajero", menu=mnuDinero_del_Cajero)
barraMenu.add_cascade(label="Entrada de vehículo", command=entrada_vehiculo)
barraMenu.add_cascade(label="Cajero", command=cajero)
barraMenu.add_cascade(label="Salida de vehículo", command=salida_vehiculo)
barraMenu.add_cascade(label="Reporte de ingresos de dinero", command=reporte_ingresos)
barraMenu.add_cascade(label="Ayuda", command=ayuda)
barraMenu.add_cascade(label="Acerca de", command=acerca_de)
barraMenu.add_command(label="Salir", command=cerrar_aplicacion)

# Creando los submenús de Dinero del Cajero
mnuDinero_del_Cajero.add_command(label="Saldo del cajero", command=lambda: saldo_cajero(dicc_cajero))
mnuDinero_del_Cajero.add_command(label="Cargar cajero", command=lambda: cargar_cajero(dicc_cajero))

#Frames
#0. Frame inicial
inicio_frame = tk.Frame(raiz, bg="beige")
inicio_frame.grid(row=0, column=0, sticky='nsew')
label_inicio = tk.Label(inicio_frame, text="Bienvenido al Estacionamiento de Vehículos", font=("Consolas", 22, "bold"), bg="beige")
label_inicio.pack(pady=(20, 20))

imagen_de_fondo = tk.PhotoImage(file="icono.png")
label_imagen = tk.Label(inicio_frame, image=imagen_de_fondo, bg="beige")
label_imagen.pack(pady=(0, 20))



##print("espacios", cant_espacios)
##print("hora", precio_por_hora)
##print("minimo", pago_minimo)
##print("redondeo", redondeo)
##print("max", minutos_maximos)
##print("mon1", moneda1)
##print("mon2", moneda2)
##print("mon3", moneda3)
##print("bill1", billete1)
##print("bill2", billete2)
##print("bill3", billete3)
##print("bill4", billete4)
##print("bill5", billete5)
##print("lista parqueo es:", parqueo)
##print("dicc_cajero es:", dicc_cajero)
##print("el historial:", historial_parqueo)

mostrar_frame(inicio_frame)
raiz.mainloop()




            



