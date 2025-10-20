#!/usr/bin/env python3
"""
PROBLEMA INTEGRADOR DE PRÁCTICA
Sistema de Gestión de Restaurante

Nombre: Juan David Martínez González
Fecha: 18/10/2025
"""

from sistema_restaurante import *

# =======================================================================
# PRUEBAS INDIVIDUALES
# =======================================================================

def prueba_agregar_platos():
    print("\n" + "="*60)
    print(" TEST: Agregar Platos")
    print("="*60)

    restaurante = SistemaRestaurante()

    # Agregar platos válidos
    restaurante.agregar_plato("P001", "Filete de Res", "Plato Fuerte", 35000)
    restaurante.agregar_plato("B001", "Limonada", "Bebida", 9000)
    print("✓ Platos agregados correctamente.")

    # Intentar agregar un código repetido
    try:
        restaurante.agregar_plato("P001", "Repetido", "Plato Fuerte", 20000)
    except KeyError as e:
        print(f"✓ Duplicado detectado correctamente: {e}")

    print("✓ Prueba completada")


def prueba_reservar_mesa():
    print("\n" + "="*60)
    print(" TEST: Reservar Mesa")
    print("="*60)

    restaurante = SistemaRestaurante()

    # Configuración inicial de la mesa
    restaurante.configurar_mesa(1, 4)

    # Reserva válida
    restaurante.reservar_mesa(1, 3, "12:00")
    print("✓ Reserva creada correctamente.")

    # Intentar reservar una mesa ocupada
    try:
        restaurante.reservar_mesa(1, 2, "13:00")
    except MesaNoDisponible as e:
        print(f"✓ Mesa no disponible controlada: {e}")

    # Intentar reservar con más personas de las permitidas
    try:
        restaurante.reservar_mesa(2, 10, "14:00")
    except CapacidadExcedida as e:
        print(f"✓ Capacidad excedida controlada: {e}")

    print("✓ Prueba completada")


def prueba_crear_pedido():
    print("\n" + "="*60)
    print(" TEST: Crear Pedido")
    print("="*60)

    restaurante = SistemaRestaurante()
    restaurante.configurar_mesa(1, 4)
    restaurante.reservar_mesa(1, 2, "12:30")

    # Pedido válido
    id_pedido = restaurante.crear_pedido(1)
    print(f"✓ Pedido creado correctamente con ID: {id_pedido}")

    # Pedido con mesa no reservada
    try:
        restaurante.crear_pedido(2)
    except PedidoInvalido as e:
        print(f"✓ Controlado: {e}")

    print("✓ Prueba completada")


def prueba_agregar_items():
    print("\n" + "="*60)
    print(" TEST: Agregar Ítems al Pedido")
    print("="*60)

    restaurante = SistemaRestaurante()

    # Agregar menú base
    restaurante.agregar_plato("P001", "Filete de Res", "Plato fuerte", 35000)
    restaurante.agregar_plato("B001", "Limonada", "Bebida", 9000)

    # Configurar mesa y pedido
    restaurante.configurar_mesa(1, 4)
    restaurante.reservar_mesa(1, 2, "14:00")
    id_pedido = restaurante.crear_pedido(1)

    # Agregar ítems válidos
    restaurante.agregar_item(id_pedido, "P001", 2)
    restaurante.agregar_item(id_pedido, "B001", 1)
    print("✓ Ítems agregados correctamente.")

    # Agregar un plato inexistente
    try:
        restaurante.agregar_item(id_pedido, "X999", 1)
    except PlatoNoEncontrado as e:
        print(f"✓ Controlado: {e}")

    print("✓ Prueba completada")


def prueba_calcular_y_pagar():
    print("\n" + "="*60)
    print(" TEST: Calcular Total y Pago")
    print("="*60)

    restaurante = SistemaRestaurante()

    # Configurar menú y pedido
    restaurante.agregar_plato("P001", "Filete de Res", "Plato fuerte", 35000)
    restaurante.agregar_plato("B001", "Limonada", "Bebida", 9000)
    restaurante.configurar_mesa(1, 4)
    restaurante.reservar_mesa(1, 2, "15:00")
    id_pedido = restaurante.crear_pedido(1)
    restaurante.agregar_item(id_pedido, "P001", 2)
    restaurante.agregar_item(id_pedido, "B001", 3)

    # Calcular totales
    totales = restaurante.calcular_total(id_pedido, propina_porcentaje=0.18)
    print(f"✓ Total calculado correctamente: ${totales['total']:.2f}")

    # Procesar pago
    resultado_pago = restaurante.pagar_pedido(id_pedido)
    print(f"✓ Pago procesado correctamente: {resultado_pago}")

    print("✓ Prueba completada")


def prueba_reportes():
    print("\n" + "="*60)
    print(" TEST: Reportes del Sistema")
    print("="*60)

    restaurante = SistemaRestaurante()
    restaurante.agregar_plato("P001", "Filete de Res", "Plato fuerte", 35000)
    restaurante.agregar_plato("B001", "Limonada", "Bebida", 9000)
    restaurante.configurar_mesa(1, 4)
    restaurante.reservar_mesa(1, 2, "16:00")

    id_pedido = restaurante.crear_pedido(1)
    restaurante.agregar_item(id_pedido, "P001", 2)
    restaurante.agregar_item(id_pedido, "B001", 1)
    restaurante.pagar_pedido(id_pedido)

    # Mostrar estadísticas
    print("✓ Platos más vendidos:", restaurante.platos_mas_vendidos())
    print("✓ Ventas por categoría:", restaurante.ventas_por_categoria())
    print("✓ Reporte de ventas:", restaurante.reporte_ventas_dia())
    print("✓ Estado del restaurante:", restaurante.estado_restaurante())

    print("✓ Prueba completada")


def prueba_exportar_importar():
    print("\n" + "="*60)
    print(" TEST: Exportar e Importar Menú")
    print("="*60)

    restaurante = SistemaRestaurante()

    # Crear menú base
    restaurante.agregar_plato("P001", "Filete de Res", "Plato fuerte", 35000)
    restaurante.agregar_plato("B001", "Limonada", "Bebida", 9000)

    # Exportar a archivo
    restaurante.exportar_menu("menu_prueba.txt")
    print("✓ Exportación completada.")

    # Importar desde archivo
    restaurante2 = SistemaRestaurante()
    resultado = restaurante2.importar_menu("menu_prueba.txt")
    print(f"✓ Importación resultado: {resultado}")

    print("✓ Prueba completada")


def prueba_excepciones():
    print("\n" + "="*60)
    print(" TEST: Excepciones Personalizadas")
    print("="*60)

    restaurante = SistemaRestaurante()

    # Crear pedido sin mesa reservada
    try:
        restaurante.crear_pedido(1)
    except PedidoInvalido as e:
        print(f"✓ Excepción controlada: {e}")

    # Lanzar excepción personalizada
    try:
        raise PlatoNoEncontrado("X999")
    except PlatoNoEncontrado as e:
        print(f"✓ Excepción controlada: {e}")

    print("✓ Prueba completada")

# =======================================================================
# EJECUTAR TODAS LAS PRUEBAS
# =======================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print(" PRUEBAS DEL SISTEMA DE GESTIÓN DE RESTAURANTE")
    print("="*70)

    pruebas = [
        prueba_agregar_platos,
        prueba_reservar_mesa,
        prueba_crear_pedido,
        prueba_agregar_items,
        prueba_calcular_y_pagar,
        prueba_reportes,
        prueba_exportar_importar,
        prueba_excepciones
    ]

    exitosas = 0
    total = len(pruebas)

    # Ejecutar cada prueba y contar resultados
    for prueba in pruebas:
        try:
            prueba()
            exitosas += 1
        except Exception as e:
            print(f"✗ Error en {prueba.__name__}: {e}")

    # Mostrar resumen final
    print("\n" + "="*70)
    print(" RESUMEN DE PRUEBAS")
    print("="*70)
    print(f"✓ Exitosas: {exitosas}/{total}")
    print(f"✗ Fallidas: {total - exitosas}/{total}")
    print("="*70)
