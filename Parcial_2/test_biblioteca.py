#!/usr/bin/env python3
"""
PARCIAL 2 - CASOS DE PRUEBA
Sistema de Biblioteca Digital
Estudiante: Juan David Martínez González
Fecha: 18/10/2025
"""

from sistema_biblioteca import *
from datetime import datetime, timedelta

# ==============================================================
# PRUEBAS INDIVIDUALES
# ==============================================================

def prueba_agregar_libros():
    print("\n" + "="*60)
    print(" TEST: Agregar Libros")
    print("="*60)
    
    biblioteca = SistemaBiblioteca()
    
    # Agrego libro válido
    biblioteca.agregar_libro("9780134685991", "Effective Python", "Brett Slatkin", 2019, "Programación", 5)
    print("✓ Libro agregado correctamente.")
    
    # Intentar agregar libro duplicado
    try:
        biblioteca.agregar_libro("9780134685991", "Effective Python", "Brett Slatkin", 2019, "Programación", 5)
    except KeyError as e:
        print(f"✓ Duplicado detectado correctamente: {e}")
    
    # ISBN inválido
    try:
        biblioteca.agregar_libro("123", "Test", "Autor", 2020, "General", 1)
    except ValueError as e:
        print(f"✓ ISBN inválido controlado: {e}")

    print("✓ Prueba completada")


def prueba_registrar_usuarios():
    print("\n" + "="*60)
    print(" TEST: Registrar Usuarios")
    print("="*60)
    
    biblioteca = SistemaBiblioteca()
    
    # Usuario válido
    biblioteca.registrar_usuario("U001", "Ana García", "ana@email.com")
    print("✓ Usuario registrado correctamente.")
    
    # Usuario duplicado
    try:
        biblioteca.registrar_usuario("U001", "Ana García", "ana@email.com")
    except ValueError as e:
        print(f"✓ Duplicado detectado correctamente: {e}")
    
    # Email inválido
    try:
        biblioteca.registrar_usuario("U002", "Carlos", "correo_invalido")
    except ValueError as e:
        print(f"✓ Email inválido controlado: {e}")

    print("✓ Prueba completada")


def prueba_prestar_libros():
    print("\n" + "="*60)
    print(" TEST: Préstamos")
    print("="*60)
    
    biblioteca = SistemaBiblioteca(limite_prestamos=1)
    biblioteca.agregar_libro("9780134685991", "Effective Python", "Brett Slatkin", 2019, "Programación", 1)
    biblioteca.registrar_usuario("U001", "Ana García", "ana@email.com")
    
    # Préstamo exitoso
    id_prestamo = biblioteca.prestar_libro("9780134685991", "U001")
    print(f"✓ Préstamo exitoso con ID: {id_prestamo}")
    
    # Libro no disponible
    try:
        biblioteca.prestar_libro("9780134685991", "U001")
    except LibroNoDisponible as e:
        print(f"✓ Controlado: {e}")
    
    # Usuario no registrado
    try:
        biblioteca.prestar_libro("9780134685991", "U999")
    except UsuarioNoRegistrado as e:
        print(f"✓ Usuario no registrado detectado: {e}")
    
    print("✓ Prueba completada")


def prueba_devolver_libros():
    print("\n" + "="*60)
    print(" TEST: Devolución y Multas")
    print("="*60)
    
    biblioteca = SistemaBiblioteca(multa_por_dia=2.0)
    biblioteca.agregar_libro("9780134685991", "Effective Python", "Brett Slatkin", 2019, "Programación", 2)
    biblioteca.registrar_usuario("U001", "Ana García", "ana@email.com")
    id_p = biblioteca.prestar_libro("9780134685991", "U001")
    
    # Simular retraso
    biblioteca.prestamos[id_p]["fecha_vencimiento"] = datetime.now() - timedelta(days=3)
    resultado = biblioteca.devolver_libro(id_p)
    print(f"✓ Resultado devolución con multa: {resultado}")
    
    # Intentar devolver préstamo inexistente
    try:
        biblioteca.devolver_libro("PX999")
    except KeyError as e:
        print(f"✓ Error controlado: {e}")

    print("✓ Prueba completada")


def prueba_estadisticas():
    print("\n" + "="*60)
    print(" TEST: Estadísticas")
    print("="*60)
    
    biblioteca = SistemaBiblioteca()
    biblioteca.agregar_libro("9780134685991", "Effective Python", "Brett Slatkin", 2019, "Programación", 5)
    biblioteca.agregar_libro("9780135404676", "Python Crash Course", "Eric Matthes", 2019, "Programación", 3)
    biblioteca.registrar_usuario("U001", "Ana García", "ana@email.com")
    biblioteca.registrar_usuario("U002", "Carlos López", "carlos@email.com")
    
    biblioteca.prestar_libro("9780134685991", "U001")
    biblioteca.prestar_libro("9780135404676", "U002")
    
    print("Libros más prestados:", biblioteca.libros_mas_prestados(2))
    print("Usuarios más activos:", biblioteca.usuarios_mas_activos(2))
    print("Estadísticas de categoría:", biblioteca.estadisticas_categoria("Programación"))
    print("Préstamos vencidos:", biblioteca.prestamos_vencidos())

    print("✓ Prueba completada")


def prueba_excepciones():
    print("\n" + "="*60)
    print(" TEST: Excepciones Personalizadas")
    print("="*60)
    
    biblioteca = SistemaBiblioteca()
    
    # Intentar prestar libro inexistente
    biblioteca.registrar_usuario("U001", "Ana García", "ana@email.com")
    try:
        biblioteca.prestar_libro("9999999999999", "U001")
    except LibroNoEncontrado as e:
        print(f"✓ Excepción correcta: {e}")

    # Intentar prestar con usuario no registrado
    biblioteca.agregar_libro("9780134685991", "Effective Python", "Brett Slatkin", 2019, "Programación", 1)
    try:
        biblioteca.prestar_libro("9780134685991", "U999")
    except UsuarioNoRegistrado as e:
        print(f"✓ Excepción correcta: {e}")
    
    print("✓ Prueba completada")


def prueba_importar_exportar():
    print("\n" + "="*60)
    print(" TEST: Importar/Exportar")
    print("="*60)
    
    biblioteca = SistemaBiblioteca()
    biblioteca.agregar_libro("9780134685991", "Effective Python", "Brett Slatkin", 2019, "Programación", 5)
    
    # Exportar catálogo
    biblioteca.exportar_catalogo("catalogo_test.txt")
    print("✓ Exportación completada.")
    
    # Importar catálogo
    resultado = biblioteca.importar_catalogo("catalogo_test.txt")
    print(f"✓ Importación resultado: {resultado}")

    print("✓ Prueba completada")


def prueba_renovar_prestamo():
    print("\n" + "="*60)
    print(" TEST: Renovación de Préstamos")
    print("="*60)
    
    biblioteca = SistemaBiblioteca()
    biblioteca.agregar_libro("9780134685991", "Effective Python", "Brett Slatkin", 2019, "Programación", 1)
    biblioteca.registrar_usuario("U001", "Ana García", "ana@email.com")
    id_p = biblioteca.prestar_libro("9780134685991", "U001")
    
    # Renovar préstamo válido
    print("✓", biblioteca.renovar_prestamo(id_p))
    
    # Simular préstamo vencido
    biblioteca.prestamos[id_p]["fecha_vencimiento"] = datetime.now() - timedelta(days=2)
    try:
        biblioteca.renovar_prestamo(id_p)
    except PrestamoVencido as e:
        print(f"✓ Renovación vencida controlada: {e}")
    
    print("✓ Prueba completada")


def prueba_reporte_financiero():
    print("\n" + "="*60)
    print(" TEST: Reporte Financiero")
    print("="*60)
    
    biblioteca = SistemaBiblioteca(multa_por_dia=2.0)
    biblioteca.agregar_libro("9780134685991", "Effective Python", "Brett Slatkin", 2019, "Programación", 2)
    biblioteca.registrar_usuario("U001", "Ana García", "ana@email.com")
    id_p = biblioteca.prestar_libro("9780134685991", "U001")
    biblioteca.prestamos[id_p]["fecha_vencimiento"] = datetime.now() - timedelta(days=3)
    biblioteca.devolver_libro(id_p)
    
    print("Reporte financiero:", biblioteca.reporte_financiero())
    print("✓ Prueba completada")


# ==============================================================
# EJECUTAR TODAS LAS PRUEBAS
# ==============================================================

def ejecutar_todas_las_pruebas():
    print("\n" + "="*70)
    print(" EJECUTANDO SUITE COMPLETA DE PRUEBAS")
    print("="*70)
    
    pruebas = [
        prueba_agregar_libros,
        prueba_registrar_usuarios,
        prueba_prestar_libros,
        prueba_devolver_libros,
        prueba_estadisticas,
        prueba_excepciones,
        prueba_importar_exportar,
        prueba_renovar_prestamo,
        prueba_reporte_financiero
    ]
    
    exitosas = 0
    fallidas = 0
    
    for prueba in pruebas:
        try:
            prueba()
            exitosas += 1
        except Exception as e:
            print(f"✗ Error en {prueba.__name__}: {e}")
            fallidas += 1
    
    print("\n" + "="*70)
    print(" RESUMEN DE PRUEBAS")
    print("="*70)
    print(f"✓ Exitosas: {exitosas}/{len(pruebas)}")
    print(f"✗ Fallidas: {fallidas}/{len(pruebas)}")
    print("="*70)


if __name__ == "__main__":
    ejecutar_todas_las_pruebas()
