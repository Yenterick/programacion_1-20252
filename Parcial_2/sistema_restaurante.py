#!/usr/bin/env python3
"""
PROBLEMA INTEGRADOR DE PRÁCTICA
Sistema de Gestión de Restaurante

Nombre: Juan David Martínez González
Fecha: 18/10/2025
"""

from datetime import datetime, time

# ===========================================================================
# EXCEPCIONES PERSONALIZADAS
# ===========================================================================

class ErrorRestaurante(Exception):
    pass

# Se lanza cuando no se encuentra un plato.
class PlatoNoEncontrado(ErrorRestaurante):
    def __init__(self, codigo_plato):
        self.codigo_plato = codigo_plato
        super().__init__(f"Plato con código '{codigo_plato}' no encontrado en el menú")

# Se lanza cuando una mesa que solicitamos está ocupada.
class MesaNoDisponible(ErrorRestaurante):
    def __init__(self, numero_mesa, hora_disponible=None):
        self.numero_mesa = numero_mesa
        self.hora_disponible = hora_disponible
        mensaje = f"Mesa {numero_mesa} no disponible"
        if hora_disponible:
            mensaje += f", próxima disponibilidad: {hora_disponible}"
        super().__init__(mensaje)

# Se lanza cuando hay más comensales que capacidad.
class CapacidadExcedida(ErrorRestaurante):
    def __init__(self, numero_mesa, capacidad, comensales):
        self.numero_mesa = numero_mesa
        self.capacidad = capacidad
        self.comensales = comensales
        super().__init__(f"Mesa {numero_mesa}: capacidad {capacidad}, comensales {comensales}")

# Se lanza cuando un pedido tiene un problema.
class PedidoInvalido(ErrorRestaurante):
    def __init__(self, razon):
        self.razon = razon
        super().__init__(f"Pedido inválido: {razon}")


# ===========================================================================
# CLASE PRINCIPAL: SISTEMA RESTAURANTE
# ===========================================================================

class SistemaRestaurante:
    """Sistema completo de gestión de restaurante."""
    
    def __init__(self, num_mesas=10, tasa_impuesto=0.16, propina_sugerida=0.15):
        # Inicializo el menú vacío
        self.menu = {}

        # Inicializo las mesas
        self.mesas = {i: {"capacidad": 4, "ocupado": False, "comensales": 0, "hora_reserva": None, "pedido_id": None}
                      for i in range(1, num_mesas + 1)}

        # Estructura de pedidos
        self.pedidos = {}
        self.contador_pedidos = 0

        # Configuración general
        self.tasa_impuesto = float(tasa_impuesto)
        self.propina_sugerida = float(propina_sugerida)

        # Estadísticas
        self.platos_vendidos = {}
        self.ventas_diarias = []
    
    # ============ GESTIÓN DE MENÚ ============
    
    # Agrego un nuevo plato al menú validando los datos.
    def agregar_plato(self, codigo, nombre, categoria, precio):
        if not codigo or not isinstance(codigo, str):
            raise ValueError("Código de plato inválido.")
        if codigo in self.menu:
            raise KeyError(f"El plato con código '{codigo}' ya existe.")
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if precio < 0:
            raise ValueError("El precio debe ser no negativo.")

        self.menu[codigo] = {
            "nombre": nombre,
            "categoria": categoria,
            "precio": float(precio),
            "disponible": True
        }
    
    # Cambio la disponibilidad de un plato.
    def cambiar_disponibilidad(self, codigo, disponible):
        if codigo not in self.menu:
            raise PlatoNoEncontrado(codigo)
        self.menu[codigo]["disponible"] = bool(disponible)
    
    # Busco platos que cumplan con los filtros.
    def buscar_platos(self, categoria=None, precio_max=None):
        resultados = []
        for codigo, plato in self.menu.items():
            if not plato.get("disponible", True):
                continue
            if categoria and plato.get("categoria", "").lower() != categoria.lower():
                continue
            if precio_max is not None and plato.get("precio", 0) > precio_max:
                continue
            datos = plato.copy()
            datos["codigo"] = codigo
            resultados.append(datos)
        return resultados
    
    # ============ GESTIÓN DE MESAS ============
    
    # Configuro la capacidad de una mesa.
    def configurar_mesa(self, numero, capacidad):
        if numero not in self.mesas:
            raise ValueError("Número de mesa inválido.")
        if capacidad < 1:
            raise ValueError("Capacidad debe ser al menos 1.")
        self.mesas[numero]["capacidad"] = int(capacidad)
    
    # Reservo una mesa verificando disponibilidad.
    def reservar_mesa(self, numero, comensales, hora):
        if numero not in self.mesas:
            raise ValueError("Número de mesa inválido.")
        mesa = self.mesas[numero]

        if mesa["ocupado"]:
            raise MesaNoDisponible(numero, mesa["hora_reserva"])

        if comensales > mesa["capacidad"]:
            raise CapacidadExcedida(numero, mesa["capacidad"], comensales)

        if not isinstance(hora, (str, datetime, time)):
            raise ValueError("Hora inválida.")

        mesa["ocupado"] = True
        mesa["comensales"] = int(comensales)
        mesa["hora_reserva"] = hora
        mesa["pedido_id"] = None
    
    # Libero una mesa y restauro su estado inicial.
    def liberar_mesa(self, numero):
        if numero not in self.mesas:
            raise ValueError("Número de mesa inválido.")
        mesa = self.mesas[numero]
        if not mesa["ocupado"]:
            raise ValueError("La mesa no está ocupada.")
        mesa.update({"ocupado": False, "comensales": 0, "hora_reserva": None, "pedido_id": None})
    
    # Retorno mesas libres con capacidad suficiente.
    def mesas_disponibles(self, comensales):
        disponibles = []
        for numero, mesa in self.mesas.items():
            if not mesa["ocupado"] and mesa["capacidad"] >= comensales:
                disponibles.append(numero)
        return disponibles
    
    # ============ GESTIÓN DE PEDIDOS ============
    
    # Verifico que la mesa exista y no esté ocipada y añado el pedido con los datos necesarios.
    def crear_pedido(self, numero_mesa):
        if numero_mesa not in self.mesas:
            raise ValueError("Número de mesa inválido.")
        mesa = self.mesas[numero_mesa]
        if not mesa["ocupado"]:
            raise PedidoInvalido("La mesa no está reservada.")

        self.contador_pedidos += 1
        id_pedido = f"O{self.contador_pedidos:04d}"
        self.pedidos[id_pedido] = {
            "numero_mesa": numero_mesa,
            "items": {},
            "pagado": False,
            "fecha": datetime.now(),
            "subtotal": 0.0,
            "impuesto": 0.0,
            "propina": 0.0,
            "total": 0.0
        }

        mesa["pedido_id"] = id_pedido
        return id_pedido
    
    # Agrego un plato a un pedido existente.
    def agregar_item(self, id_pedido, codigo_plato, cantidad=1):
        if id_pedido not in self.pedidos:
            raise PedidoInvalido("Pedido no existe.")
        pedido = self.pedidos[id_pedido]
        if pedido["pagado"]:
            raise PedidoInvalido("El pedido ya fue pagado.")
        if codigo_plato not in self.menu:
            raise PlatoNoEncontrado(codigo_plato)
        plato = self.menu[codigo_plato]
        if not plato.get("disponible", True):
            raise ValueError("El plato no está disponible.")
        if cantidad < 1:
            raise ValueError("Cantidad inválida.")

        pedido["items"][codigo_plato] = pedido["items"].get(codigo_plato, 0) + int(cantidad)
    
    # Calculo el valor del pedido si existe, sumo el valor de cada item y luego calculo valores secundarios como impuestos o propina.
    def calcular_total(self, id_pedido, propina_porcentaje=None):
        if id_pedido not in self.pedidos:
            raise PedidoInvalido("Pedido no existe.")
        pedido = self.pedidos[id_pedido]

        subtotal = 0.0
        for codigo, cantidad in pedido["items"].items():
            precio = self.menu[codigo]["precio"]
            subtotal += precio * cantidad

        impuesto = round(subtotal * self.tasa_impuesto, 2)
        porcentaje_propina = self.propina_sugerida if propina_porcentaje is None else float(propina_porcentaje)
        propina = round(subtotal * porcentaje_propina, 2)
        total = round(subtotal + impuesto + propina, 2)

        pedido["subtotal"] = round(subtotal, 2)
        pedido["impuesto"] = impuesto
        pedido["propina"] = propina
        pedido["total"] = total

        return {
            "subtotal": pedido["subtotal"],
            "impuesto": pedido["impuesto"],
            "propina": pedido["propina"],
            "total": pedido["total"]
        }
    
    # Marco un pedido como pagado y actualizo estadísticas.
    def pagar_pedido(self, id_pedido, propina_porcentaje=None):
        if id_pedido not in self.pedidos:
            raise PedidoInvalido("Pedido no existe.")
        pedido = self.pedidos[id_pedido]
        if pedido["pagado"]:
            raise PedidoInvalido("El pedido ya fue pagado.")

        totales = self.calcular_total(id_pedido, propina_porcentaje)
        pedido["pagado"] = True

        venta = {
            "id_pedido": id_pedido,
            "numero_mesa": pedido["numero_mesa"],
            "fecha": pedido["fecha"],
            "subtotal": pedido["subtotal"],
            "impuesto": pedido["impuesto"],
            "propina": pedido["propina"],
            "total": pedido["total"],
            "items": pedido["items"].copy()
        }
        self.ventas_diarias.append(venta)

        for codigo, cantidad in pedido["items"].items():
            self.platos_vendidos[codigo] = self.platos_vendidos.get(codigo, 0) + cantidad

        mesa = self.mesas[pedido["numero_mesa"]]
        return totales
    
    # ============ REPORTES Y ESTADÍSTICAS ============
    
    # Hago una lista con los datos importantes de cada plato, la organizo y la corto de 0 a n.
    def platos_mas_vendidos(self, n=5):
        lista = [(codigo,
                  self.menu[codigo]["nombre"] if codigo in self.menu else codigo,
                  cantidad)
                 for codigo, cantidad in self.platos_vendidos.items()]
        lista.sort(key=lambda x: x[2], reverse=True)
        return lista[:n]
    

    def ventas_por_categoria(self):
        agrupado = {}
        for venta in self.ventas_diarias:
            for codigo, cantidad in venta["items"].items():
                categoria = self.menu.get(codigo, {}).get("categoria", "Sin Categoria")
                monto = self.menu.get(codigo, {}).get("precio", 0) * cantidad
                agrupado[categoria] = agrupado.get(categoria, 0.0) + monto
        return {k: round(v, 2) for k, v in agrupado.items()}
    
    # Hago una sumatoria de cada valor monetario en ventas diarias, después saco los pedidos pagados y el promedio, al final retorno un diccionario con toda la información necesaria.
    def reporte_ventas_dia(self):
        total_ventas = sum(v["total"] for v in self.ventas_diarias)
        total_impuestos = sum(v["impuesto"] for v in self.ventas_diarias)
        total_propinas = sum(v["propina"] for v in self.ventas_diarias)
        pedidos_pagados = len(self.ventas_diarias)
        promedio = round(total_ventas / pedidos_pagados, 2) if pedidos_pagados else 0.0

        return {
            "total_ventas": round(total_ventas, 2),
            "total_impuestos": round(total_impuestos, 2),
            "total_propinas": round(total_propinas, 2),
            "pedidos_pagados": pedidos_pagados,
            "promedio_por_pedido": promedio
        }
    
    # Hago listas con el numero de las mesas dependiendo de si están ocupadas o no, además saco los pedidos que no se han pagado y todo esto lo retorno en un diccionario.
    def estado_restaurante(self):
        mesas_ocupadas = [num for num, mesa in self.mesas.items() if mesa["ocupado"]]
        mesas_libres = [num for num, mesa in self.mesas.items() if not mesa["ocupado"]]
        pedidos_activos = [pid for pid, pedido in self.pedidos.items() if not pedido["pagado"]]

        return {
            "mesas_ocupadas": mesas_ocupadas,
            "mesas_libres": mesas_libres,
            "pedidos_activos": pedidos_activos,
            "total_pedidos": len(self.pedidos)
        }
    
    # ============ UTILIDADES ============
    
    # Con open abro o creo el archivo al que voy a exportar y escribo en el formato propuesto todos los valores de platos.
    def exportar_menu(self, archivo='menu.txt'):
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                for codigo, plato in self.menu.items():
                    linea = f"{codigo}|{plato['nombre']}|{plato['categoria']}|{plato['precio']}|{int(plato.get('disponible', True))}\n"
                    f.write(linea)
        except Exception as e:
            print(f"Error al exportar menú: {e}")
    
    # Con open abro el archivo de catálogo que voy a importar y por cada línea, separo los valores con el formato propuesto y los voy añadiendo.
    def importar_menu(self, archivo='menu.txt'):
        exitosos = 0
        errores = []
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                for i, linea in enumerate(f, 1):
                    try:
                        codigo, nombre, categoria, precio, disponible = linea.strip().split('|')
                        if codigo in self.menu:
                            raise ValueError("Código duplicado")
                        self.agregar_plato(codigo, nombre, categoria, float(precio))
                        self.menu[codigo]["disponible"] = bool(int(disponible))
                        exitosos += 1
                    except Exception as e:
                        errores.append((i, str(e)))
        except FileNotFoundError:
            raise
        return {"exitosos": exitosos, "errores": errores}


# ===========================================================================
# EJEMPLO DE USO
# ===========================================================================

if __name__ == "__main__":
    print("=" * 70)
    print(" SISTEMA DE GESTIÓN DE RESTAURANTE")
    print("=" * 70)
    
    # Crear sistema
    restaurante = SistemaRestaurante(num_mesas=5)
    
    # Aquí puedes probar tu implementación
    print("\nAgrega tus pruebas aquí...")
    # Crear sistema
    restaurante = SistemaRestaurante(num_mesas=5, tasa_impuesto=0.16, propina_sugerida=0.15)

    # Configurar mesas
    restaurante.configurar_mesa(1, 4)
    restaurante.configurar_mesa(2, 2)
    restaurante.configurar_mesa(3, 6)

    # Agregar platos al menú
    restaurante.agregar_plato("E001", "Ensalada César", "entrada", 85.00)
    restaurante.agregar_plato("P001", "Filete de Res", "plato_fuerte", 350.00)
    restaurante.agregar_plato("P002", "Pasta Alfredo", "plato_fuerte", 180.00)
    restaurante.agregar_plato("D001", "Tiramisú", "postre", 95.00)
    restaurante.agregar_plato("B001", "Limonada", "bebida", 45.00)

    # Reservar mesa
    restaurante.reservar_mesa(1, 3, "14:30")

    # Crear pedido
    id_pedido = restaurante.crear_pedido(1)
    restaurante.agregar_item(id_pedido, "E001", 2)
    restaurante.agregar_item(id_pedido, "P001", 2)
    restaurante.agregar_item(id_pedido, "B001", 3)

    # Calcular y pagar
    totales = restaurante.calcular_total(id_pedido, propina_porcentaje=0.18)
    print(f"Total a pagar: ${totales['total']:.2f}")

    resultado_pago = restaurante.pagar_pedido(id_pedido, propina_porcentaje=0.18)
    print(f"Pago procesado: {resultado_pago}")

    # Liberar mesa
    restaurante.liberar_mesa(1)

    # Reportes
    print(restaurante.platos_mas_vendidos(3))
    print(restaurante.ventas_por_categoria())
    print(restaurante.reporte_ventas_dia())
    print(restaurante.estado_restaurante())

    # Exportar menú
    restaurante.exportar_menu("menu_backup.txt")

    # Manejo de excepciones
    try:
        restaurante.agregar_item(id_pedido, "X999", 1)  # Plato no existe
    except PlatoNoEncontrado as e:
        print(f"Error: {e}")
    except PedidoInvalido as e:
        print(f"Error {e}")

    try:
        restaurante.reservar_mesa(1, 10, "18:00")  # Excede capacidad
    except CapacidadExcedida as e:
        print(f"Error: {e}")