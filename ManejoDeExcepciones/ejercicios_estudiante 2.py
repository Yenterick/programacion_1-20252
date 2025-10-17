#!/usr/bin/env python3
"""
EJERCICIOS PARA ESTUDIANTES - MANEJO DE EXCEPCIONES
Versión completada
"""

# ===========================================================================
# Ejercicio 1: Encuentra y arregla el except desnudo
# ===========================================================================
print("\n--- EJERCICIO 1: ARREGLA EL EXCEPT DESNUDO ---\n")

def calcular_promedio(numeros):
    try:
        total = sum(numeros)
        promedio = total / len(numeros)
        return promedio
    except ZeroDivisionError:
        print("Error: La lista está vacía, no se puede dividir entre cero.")
        return None
    except TypeError:
        print("Error: Todos los elementos deben ser números.")
        return None

# print(calcular_promedio([1, 2, 3, 4, 5]))
# print(calcular_promedio([]))
# print(calcular_promedio([1, 2, 'a']))


# ===========================================================================
# Ejercicio 2: Añade retroalimentación al usuario
# ===========================================================================
print("\n--- EJERCICIO 2: AÑADE RETROALIMENTACIÓN ---\n")

def guardar_datos(datos, archivo):
    try:
        with open(archivo, 'w') as f:
            f.write(str(datos))
        print(f"Datos guardados correctamente en {archivo}.")
        return True
    except FileNotFoundError:
        print("Error: La ruta especificada no existe.")
    except PermissionError:
        print("Error: No tienes permisos para escribir en este archivo.")
    except Exception as e:
        print(f"Error inesperado: {e}")
    return False

# guardar_datos({"usuario": "Ana"}, "datos.txt")
# guardar_datos({"usuario": "Ana"}, "/ruta/invalida/datos.txt")


# ===========================================================================
# Ejercicio 3: Usa else y finally correctamente
# ===========================================================================
print("\n--- EJERCICIO 3: USA ELSE Y FINALLY ---\n")

def procesar_archivo(nombre_archivo):
    f = None
    try:
        f = open(nombre_archivo, 'r')
        contenido = f.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no existe.")
    else:
        print("Archivo leído correctamente:")
        print(contenido)
    finally:
        if f:
            f.close()
            print("Archivo cerrado correctamente.")

# procesar_archivo("existente.txt")
# procesar_archivo("faltante.txt")


# ===========================================================================
# Ejercicio 4: Lanza excepciones apropiadas
# ===========================================================================
print("\n--- EJERCICIO 4: LANZA EXCEPCIONES ---\n")

def crear_usuario(nombre_usuario, edad, email):
    if len(nombre_usuario) < 3:
        raise ValueError("El nombre de usuario debe tener al menos 3 caracteres.")
    if not isinstance(edad, int):
        raise TypeError("La edad debe ser un número entero.")
    if edad < 0 or edad > 150:
        raise ValueError("La edad debe estar entre 0 y 150.")
    if '@' not in email:
        raise ValueError("El email debe contener '@'.")
    print("Usuario creado correctamente.")
    return {"nombre": nombre_usuario, "edad": edad, "email": email}

# crear_usuario("Ana", 25, "ana@example.com")


# ===========================================================================
# Ejercicio 5: Crea excepciones personalizadas
# ===========================================================================
print("\n--- EJERCICIO 5: EXCEPCIONES PERSONALIZADAS ---\n")

class SaldoInsuficienteError(Exception):
    def __init__(self, saldo, monto):
        self.saldo = saldo
        self.monto = monto
        super().__init__(f"Saldo insuficiente: necesitas ${monto}, tienes ${saldo}")

class MontoInvalidoError(Exception):
    pass

def retirar(saldo, monto):
    if monto <= 0:
        raise MontoInvalidoError("El monto debe ser mayor que 0.")
    if monto > saldo:
        raise SaldoInsuficienteError(saldo, monto)
    return saldo - monto

# print(retirar(100, 50))
# retirar(100, 150)
# retirar(100, -10)


# ===========================================================================
# Ejercicio 6: Maneja excepciones en bucles
# ===========================================================================
print("\n--- EJERCICIO 6: EXCEPCIONES EN BUCLES ---\n")

def procesar_lista_numeros(lista_strings):
    exitosos = []
    errores = []
    for s in lista_strings:
        try:
            n = int(s)
            exitosos.append(n * 2)
        except ValueError as e:
            errores.append((s, str(e)))
    return exitosos, errores

# resultados, errores = procesar_lista_numeros(["1", "2", "abc", "4", "xyz"])
# print(f"Exitosos: {resultados}")
# print(f"Errores: {errores}")


# ===========================================================================
# Ejercicio 7: Re-lanza excepciones apropiadamente
# ===========================================================================
print("\n--- EJERCICIO 7: RE-LANZA EXCEPCIONES ---\n")

def operacion_critica(valor):
    try:
        resultado = 100 / int(valor)
        return resultado
    except (ValueError, ZeroDivisionError) as e:
        print(f"Error en operacion_critica: {e}")
        raise  # Re-lanza la excepción

# print(operacion_critica("10"))
# try:
#     operacion_critica("0")
# except ZeroDivisionError:
#     print("Llamador: Manejó el error.")


# ===========================================================================
# Ejercicio 8: Excepción con múltiples except
# ===========================================================================
print("\n--- EJERCICIO 8: MÚLTIPLES EXCEPT ---\n")

def calculadora_segura(operacion, a, b):
    try:
        if operacion == "suma":
            return a + b
        elif operacion == "resta":
            return a - b
        elif operacion == "multiplicacion":
            return a * b
        elif operacion == "division":
            return a / b
        else:
            raise ValueError("Operación inválida.")
    except ZeroDivisionError:
        return "Error: No se puede dividir entre cero."
    except TypeError:
        return "Error: Ambos operandos deben ser números."
    except ValueError as e:
        return f"Error: {e}"

# print(calculadora_segura("suma", 10, 5))
# print(calculadora_segura("division", 10, 0))
# print(calculadora_segura("suma", 10, "5"))
# print(calculadora_segura("invalida", 10, 5))


# ===========================================================================
# Ejercicio 9: Contexto de excepción
# ===========================================================================
print("\n--- EJERCICIO 9: CONTEXTO DE EXCEPCIÓN ---\n")

def parsear_configuracion(json_string):
    import json
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError("Error al parsear configuración JSON.") from e

# print(parsear_configuracion('{"nombre": "Ana"}'))
# parsear_configuracion('json invalido')


# ===========================================================================
# Ejercicio 10: Proyecto completo
# ===========================================================================
print("\n--- EJERCICIO 10: PROYECTO COMPLETO ---\n")

class ErrorInventario(Exception):
    pass

class ProductoNoEncontrado(ErrorInventario):
    pass

class StockInsuficiente(ErrorInventario):
    pass

class Inventario:
    def __init__(self):
        self.productos = {}

    def agregar_producto(self, codigo, nombre, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        if codigo in self.productos:
            raise KeyError(f"El producto con código '{codigo}' ya existe.")
        self.productos[codigo] = {"nombre": nombre, "cantidad": cantidad}
        print(f"Producto '{nombre}' agregado con éxito.")

    def retirar_stock(self, codigo, cantidad):
        if codigo not in self.productos:
            raise ProductoNoEncontrado(f"El producto '{codigo}' no existe.")
        if cantidad > self.productos[codigo]["cantidad"]:
            raise StockInsuficiente(f"Stock insuficiente para '{codigo}'.")
        self.productos[codigo]["cantidad"] -= cantidad
        print(f"Retirado {cantidad} unidades de '{codigo}'.")

    def obtener_producto(self, codigo):
        if codigo not in self.productos:
            raise ProductoNoEncontrado(f"El producto '{codigo}' no existe.")
        return self.productos[codigo]

# Ejemplo de uso:
# inventario = Inventario()
# inventario.agregar_producto("001", "Laptop", 10)
# print(inventario.obtener_producto("001"))
# inventario.retirar_stock("001", 5)
# inventario.retirar_stock("001", 20)


# ===========================================================================
# Reflexión Final
# ===========================================================================
print("\n" + "=" * 70)
print(" ¡EJERCICIOS COMPLETADOS! ")
print("=" * 70 + "\n")
