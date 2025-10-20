#!/usr/bin/env python3
"""
PARCIAL 2 - EJERCICIOS (Parte 1)
Estudiante: Juan David Martínez González
Fecha: 18/10/2025
"""

# ===========================================================================
# EJERCICIO 1: EXPRESIONES ARITMÉTICAS (10 puntos)
# ===========================================================================

def calculadora_cientifica(operacion, a, b):
    try:
        # Válido las entradas númericas para cerciorarme de que sean int o float.
        if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
            raise ValueError("Los parámetros deben ser numéricos (int o float)")

        # Hago una función por cada una de las operaciones permitidas, cómo serán funciones sencillas simplemente meto varios lambdas en un diccionario.
        operaciones = {
            "suma": lambda x, y: x + y,
            "resta": lambda x, y: x - y,
            "multiplicacion": lambda x, y: x * y,
            "division": lambda x, y: x / y,
            "potencia": lambda x, y: x ** y,
            "modulo": lambda x, y: x % y
        }

        # Valido que la operación sí se encuentre entre las operaciones soportadas.
        if operacion not in operaciones:
            raise ValueError(
                f"Operación inválida: '{operacion}'. "
                "Operaciones válidas: suma, resta, multiplicacion, division, potencia, modulo"
            )

        # Verifico división por cero.
        if operacion == "division" and b == 0:
            raise ZeroDivisionError("No se puede realizar division por cero")
        if operacion == "modulo" and b == 0:
            raise ZeroDivisionError("No se puede realizar modulo por cero")

        # Ejecutó la función dentro del diccionario dependiendo de la entrada.
        resultado = operaciones[operacion](a, b)

        # Retorno redondeando a dos decimales.
        return round(resultado, 2)

    except ZeroDivisionError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception:
        print("Error desconocido en la operación.")



# ===========================================================================
# EJERCICIO 2: EXPRESIONES LÓGICAS Y RELACIONALES (12 puntos)
# ===========================================================================

class ValidadorPassword:
    def __init__(self, min_longitud=8, requiere_mayuscula=True, 
                 requiere_minuscula=True, requiere_numero=True, 
                 requiere_especial=True):
        self.min_longitud = min_longitud
        self.requiere_mayuscula = requiere_mayuscula
        self.requiere_minuscula = requiere_minuscula
        self.requiere_numero = requiere_numero
        self.requiere_especial = requiere_especial
    
    def validar(self, password):
        errores = []

        # Valido la longitud
        if len(password) < self.min_longitud:
            errores.append("Longitud mínima no cumplida")

        # Valido mayúsculas
        if self.requiere_mayuscula and not any(c.isupper() for c in password):
            errores.append("Falta mayúscula")

        # Valido minúsculas
        if self.requiere_minuscula and not any(c.islower() for c in password):
            errores.append("Falta minúscula")

        # Valido números
        if self.requiere_numero and not any(c.isdigit() for c in password):
            errores.append("Falta número")

        # Valido carácteres especiales
        especiales = "!@#$%^&*()-_=+[]{};:,<.>/?|\\"
        if self.requiere_especial and not any(c in especiales for c in password):
            errores.append("Falta carácter especial")

        # Retorno resultado
        if errores:
            return (False, errores)
        else:
            return (True, [])

    def es_fuerte(self, password):

        # Valido la longitud 
        if len(password) < 12:
            return False

        tiene_mayuscula = any(c.isupper() for c in password)
        tiene_minuscula = any(c.islower() for c in password)
        tiene_numero = any(c.isdigit() for c in password)
        especiales = "!@#$%^&*()-_=+[]{};:,<.>/?|\\"
        tiene_especial = any(c in especiales for c in password)

        return all([tiene_mayuscula, tiene_minuscula, tiene_numero, tiene_especial])


# ===========================================================================
# EJERCICIO 3: ESTRUCTURAS DE DATOS (15 puntos)
# ===========================================================================

class GestorInventario:
    # Inicializo el inventario.  
    def __init__(self):
        self.inventario = {}

    # Agrego un producto con el código como key, pero antes, verifico que no esté ni que tenga algún valor inválido.
    def agregar_producto(self, codigo, nombre, precio, cantidad, categoria):
        try:
            if codigo in self.inventario:
                raise ValueError(f"El producto con código '{codigo}' ya existe.")
            
            if precio < 0 or cantidad < 0:
                raise ValueError("El precio y la cantidad deben ser valores no negativos.")
            
            self.inventario[codigo] = {
                "nombre": nombre,
                "precio": float(precio),
                "cantidad": int(cantidad),
                "categoria": categoria
            }
        except ValueError as e:
            print(f"Error: {e}")

    # Añado o disminuyo stock dependiendo del valor, pero antes verifico que el código sí exista y que el stock nuevo no sea negativo.
    def actualizar_stock(self, codigo, cantidad_cambio):
        try:
            if codigo not in self.inventario:
                raise ValueError(f"El producto con código '{codigo}' no existe.")

            nuevo_stock = self.inventario[codigo]["cantidad"] + cantidad_cambio
            if nuevo_stock < 0:
                raise ValueError("El stock resultante no puede ser negativo.")

            self.inventario[codigo]["cantidad"] = nuevo_stock
        except ValueError as e:
            print(f"Error: {e}")

    # Busco por categoria y retorno el código, el nombre y el precio.
    def buscar_por_categoria(self, categoria):
        resultado = []
        for codigo, datos in self.inventario.items():
            if datos["categoria"].lower() == categoria.lower():
                resultado.append((codigo, datos["nombre"], datos["precio"]))
        return resultado

    # Busco en todo el diccionario los que tienen una cantidad inferior al límite ingresado, y creo un k : v con el código y la cantidad.
    def productos_bajo_stock(self, limite=10):
        bajos = {
            codigo: datos["cantidad"]
            for codigo, datos in self.inventario.items()
            if datos["cantidad"] < limite
        }
        return bajos

    # Hago una sumatoria de precio * cantidad en cada uno de los artículos.
    def valor_total_inventario(self):
        total = sum(
            datos["precio"] * datos["cantidad"]
            for datos in self.inventario.values()
        )
        return round(total, 2)

    # Hago una tupla por cada artículo la cual contiene código y valor en inventario, después la ordeno de manera invertida por valor, y hago un split de 0 a n.
    def top_productos(self, n=5):
        valores = [
            (codigo, datos["precio"] * datos["cantidad"])
            for codigo, datos in self.inventario.items()
        ]
        valores.sort(key=lambda x: x[1], reverse=True)
        return valores[:n]


# ===========================================================================
# EJERCICIO 4: ESTRUCTURAS DE CONTROL (10 puntos)
# ===========================================================================

def es_bisiesto(anio):
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

# Verifico que sea un mes válido, retorno 29 si las condiciones hacen que sea bisiesto, y, sino, retorno por posición en un arreglo de todos los días por mes.
def dias_en_mes(mes, anio):
    try:
        if mes < 1 or mes > 12:
            raise ValueError("Mes inválido. Debe estar entre 1 y 12.")
        
        dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        if mes == 2 and (es_bisiesto(anio)):
            return 29
        return dias_por_mes[mes - 1]
    except ValueError as e:
        print(f"Error: {e}")
        return None

# Genero un calendario con los días organizados por semanas, empezando desde el día indicado (0 = Lunes).
# Cada semana la separo en una nueva línea y alineo los días bajo los nombres de la semana.
# Uso la función dias_en_mes() para saber cuántos días tiene el mes.
def generar_calendario(mes, anio, dia_inicio=0):
    try:
        dias = dias_en_mes(mes, anio)
        if dias is None:
            return ""
    except ValueError as e:
        print(f"Error: {e}")
        return ""

    encabezado = "Lu Ma Mi Ju Vi Sa Do"
    calendario = encabezado + "\n"
    fila = "    " * dia_inicio

    for dia in range(1, dias + 1):
        fila += f"{dia:2d}  "
        dia_inicio = (dia_inicio + 1) % 7
        if dia_inicio == 0:
            calendario += fila.rstrip() + "\n"
            fila = ""

    if fila:
        calendario += fila.rstrip() + "\n"

    return calendario.strip()

# ===========================================================================
# EJERCICIO 5: ESTRUCTURAS DE REPETICIÓN (13 puntos)
# ===========================================================================

def analizar_ventas(ventas):
    try:
        # Verifico que la lista no esté vacía ni sea inválida.
        if not isinstance(ventas, list) or not ventas:
            raise ValueError("La lista de ventas está vacía o no es válida.")

        total_ventas = 0
        total_descuentos = 0
        producto_cantidades = {}
        venta_mayor = None
        mayor_monto = 0

        # Recorro todas las ventas y acumulo los valores.
        for venta in ventas:
            # Verifico que la venta tenga las claves esperadas.
            if not all(k in venta for k in ['producto', 'cantidad', 'precio', 'descuento']):
                raise ValueError("Cada venta debe tener 'producto', 'cantidad', 'precio' y 'descuento'.")

            subtotal = venta['cantidad'] * venta['precio']
            descuento = subtotal * venta['descuento']
            total = subtotal - descuento

            total_ventas += total
            total_descuentos += descuento

            # Acumulo cantidad por producto para luego saber cuál se vendió más.
            producto_cantidades[venta['producto']] = producto_cantidades.get(venta['producto'], 0) + venta['cantidad']

            # Comparo para determinar la venta mayor.
            if total > mayor_monto:
                mayor_monto = total
                venta_mayor = venta

        # Saco el producto más vendido buscando el de mayor cantidad acumulada.
        producto_mas_vendido = max(producto_cantidades, key=producto_cantidades.get)
        promedio_por_venta = round(total_ventas / len(ventas), 2)

        return {
            'total_ventas': round(total_ventas, 2),
            'promedio_por_venta': promedio_por_venta,
            'producto_mas_vendido': producto_mas_vendido,
            'venta_mayor': venta_mayor,
            'total_descuentos': round(total_descuentos, 2)
        }

    except ValueError as e:
        print(f"Error: {e}")
        return {}
    except Exception:
        print("Error desconocido al analizar ventas.")
        return {}


def encontrar_patrones(numeros):
    try:
        # Verifico que sea una lista numérica válida.
        if not isinstance(numeros, list) or not all(isinstance(n, (int, float)) for n in numeros):
            raise ValueError("Debe recibir una lista de números válidos.")
        if len(numeros) < 2:
            raise ValueError("La lista debe tener al menos dos elementos para encontrar patrones.")

        sec_asc = sec_desc = 0
        max_asc = max_desc = 1
        actual_asc = actual_desc = 1

        # Cuento repeticiones.
        repetidos = {}
        for n in numeros:
            repetidos[n] = repetidos.get(n, 0) + 1
        repetidos = {k: v for k, v in repetidos.items() if v > 1}

        # Recorro y detecto cambios ascendentes o descendentes.
        for i in range(1, len(numeros)):
            if numeros[i] > numeros[i-1]:
                actual_asc += 1
                actual_desc = 1
            elif numeros[i] < numeros[i-1]:
                actual_desc += 1
                actual_asc = 1
            else:
                actual_asc = actual_desc = 1

            if actual_asc > 1 and (i == len(numeros)-1 or numeros[i+1] <= numeros[i]):
                sec_asc += 1
            if actual_desc > 1 and (i == len(numeros)-1 or numeros[i+1] >= numeros[i]):
                sec_desc += 1

            max_asc = max(max_asc, actual_asc)
            max_desc = max(max_desc, actual_desc)

        return {
            'secuencias_ascendentes': sec_asc,
            'secuencias_descendentes': sec_desc,
            'longitud_max_ascendente': max_asc,
            'longitud_max_descendente': max_desc,
            'numeros_repetidos': repetidos
        }

    except ValueError as e:
        print(f"Error: {e}")
        return {}
    except Exception:
        print("Error desconocido al analizar patrones.")
        return {}


def simular_crecimiento(principal, tasa_anual, anios, aporte_anual=0):
    try:
        # Verifico que los parámetros sean válidos.
        if principal < 0 or tasa_anual < 0 or anios <= 0 or aporte_anual < 0:
            raise ValueError("Los valores deben ser no negativos y los años mayores que cero.")

        resultado = []
        balance = principal

        # Recorro cada año y aplico el interés compuesto.
        for anio in range(1, anios + 1):
            balance += aporte_anual
            interes = balance * tasa_anual
            balance += interes

            # Guardo los resultados de cada año.
            resultado.append({
                'anio': anio,
                'balance': round(balance, 2),
                'interes_ganado': round(interes, 2)
            })

        return resultado

    except ValueError as e:
        print(f"Error: {e}")
        return []
    except Exception:
        print("Error desconocido al simular el crecimiento.")
        return []


# ===========================================================================
# CASOS DE PRUEBA
# ===========================================================================

if __name__ == "__main__":
    print("="*70)
    print(" PRUEBAS DE EJERCICIOS")
    print("="*70)
    
    # Aquí puedes añadir tus propias pruebas
    
    print("\nEjercicio 1: Calculadora")
    print(calculadora_cientifica("division", 10, 3))  # Retorna: 3.33
    print(calculadora_cientifica("potencia", 2, 8))   # Retorna: 256.0
    print(calculadora_cientifica("division", 10, 0))  # Lanza ZeroDivisionError
    print(calculadora_cientifica("raiz", 4, 2))       # Lanza ValueError
    
    print("\nEjercicio 2: Validador de Password")
    validador = ValidadorPassword(min_longitud=8)
    print(validador.validar("Abc123!"))         # (False, ['Longitud mínima no cumplida'])
    print(validador.validar("Abc123!@"))        # (True, [])
    print(validador.validar("abcdefgh"))        # (False, ['Falta mayúscula', ...])
    print(validador.es_fuerte("Abc123!@#$Xyz")) # True
    
    print("\nEjercicio 3: Gestor de Inventario")
    inv = GestorInventario()
    inv.agregar_producto("P001", "Laptop", 1200.00, 15, "Electrónica")
    inv.agregar_producto("P002", "Mouse", 25.50, 5, "Accesorios")
    inv.agregar_producto("P003", "Teclado", 85.00, 8, "Accesorios")

    inv.actualizar_stock("P001", -3)  # Reduce stock
    print(inv.productos_bajo_stock(10))  # {'P002': 5, 'P003': 8}
    print(inv.buscar_por_categoria("Accesorios"))  # [('P002', 'Mouse', 25.5), ...]
    print(inv.valor_total_inventario())  # Suma total
    print(inv.top_productos(2))  # Top 2 productos por valor
    
    print("\nEjercicio 4: Calendario")
    print(es_bisiesto(2024))  # True
    print(es_bisiesto(2100))  # False
    print(es_bisiesto(2000))  # True
    print(dias_en_mes(2, 2024))  # 29
    print(dias_en_mes(2, 2023))  # 28
    print(generar_calendario(1, 2024, 0))  # Calendario de enero 2024
    
    print("\nEjercicio 5: Análisis de Datos")
    ventas = [
    {'producto': 'Laptop', 'cantidad': 2, 'precio': 1000, 'descuento': 0.1},
    {'producto': 'Mouse', 'cantidad': 10, 'precio': 20, 'descuento': 0.0},
    {'producto': 'Laptop', 'cantidad': 3, 'precio': 1000, 'descuento': 0.15}
    ]
    print(analizar_ventas(ventas))

    numeros = [1, 2, 3, 2, 1, 2, 3, 4, 5, 3, 3, 3]
    print(encontrar_patrones(numeros))

    print(simular_crecimiento(1000, 0.05, 5, 100))
    
