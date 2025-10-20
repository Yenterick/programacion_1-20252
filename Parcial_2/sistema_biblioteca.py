#!/usr/bin/env python3
"""
PARCIAL 2 - PROBLEMA INTEGRADOR (Parte 2)
Sistema de Gestión de Biblioteca Digital

Estudiante: Juan David Martínez González
Fecha: 18/10/2025
"""

from datetime import datetime, timedelta

# ===========================================================================
# EXCEPCIONES PERSONALIZADAS (5 puntos)
# ===========================================================================

class ErrorBiblioteca(Exception):
    pass

# Se lanza cuando un libro no se encuentra.
class LibroNoEncontrado(ErrorBiblioteca):
    def __init__(self, isbn):
        self.isbn = isbn
        super().__init__(f"Libro con ISBN {isbn} no encontrado")

# Se lanza cuando un libro no tiene copias disponibles.
class LibroNoDisponible(ErrorBiblioteca):
    def __init__(self, isbn, titulo):
        self.isbn = isbn
        self.titulo = titulo
        super().__init__(f"No hay copias disponibles de '{titulo}'")

# Se lanza cuando no se encuentra la ID de un usuario.
class UsuarioNoRegistrado(ErrorBiblioteca):
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        super().__init__(f"Usuario con ID '{id_usuario}' no está registrado")

# Se lanza cuando se ha excedido el límite de prestamos.
class LimitePrestamosExcedido(ErrorBiblioteca):
    def __init__(self, id_usuario, limite):
        self.id_usuario = id_usuario
        self.limite = limite
        super().__init__(f"Usuario {id_usuario} excede límite de {limite} préstamos")

# Se lanza cuando un préstamo se ha vencido por cierta cantidad de días.
class PrestamoVencido(ErrorBiblioteca):
    def __init__(self, id_prestamo, dias_retraso):
        self.id_prestamo = id_prestamo
        self.dias_retraso = dias_retraso
        super().__init__(f"Préstamo {id_prestamo} está vencido por {dias_retraso} días")


# ===========================================================================
# CLASE PRINCIPAL: SISTEMA BIBLIOTECA (35 puntos)
# ===========================================================================

class SistemaBiblioteca:
    def __init__(self, dias_prestamo=14, multa_por_dia=1.0, limite_prestamos=3):
        # Inicializo las estructuras de datos principales y parámetros de configuración.
        self.catalogo = {}
        self.usuarios = {}
        self.prestamos = {}
        self.dias_prestamo = dias_prestamo
        self.multa_por_dia = multa_por_dia
        self.limite_prestamos = limite_prestamos
        self.contador_prestamos = 0

    # ============ GESTIÓN DE CATÁLOGO ============

    def agregar_libro(self, isbn, titulo, autor, anio, categoria, copias):
        # Valido todas las condicines necesarias para agregar el libro.
        if not (isinstance(isbn, str) and isbn.isdigit() and len(isbn) == 13):
            raise ValueError("El ISBN debe ser una cadena de 13 dígitos.")
        if not titulo or not autor:
            raise ValueError("El título y el autor no pueden estar vacíos.")
        if not (1000 <= anio <= datetime.now().year):
            raise ValueError("El año no es válido.")
        if copias < 1:
            raise ValueError("Debe haber al menos una copia.")
        if isbn in self.catalogo:
            raise KeyError(f"El libro con ISBN {isbn} ya existe.")

        # Guardo la información en el diccionario principal.
        self.catalogo[isbn] = {
            "titulo": titulo,
            "autor": autor,
            "anio": anio,
            "categoria": categoria,
            "copias_total": copias,
            "copias_disponibles": copias,
            "prestamos_totales": 0
        }

    # Reviso que el libro exista, y si es así actualizo su valor de copias totales y copias disponibles.
    def actualizar_copias(self, isbn, cantidad_cambio):
        if isbn not in self.catalogo:
            raise LibroNoEncontrado(isbn)

        nuevo_total = self.catalogo[isbn]["copias_total"] + cantidad_cambio
        nuevo_disp = self.catalogo[isbn]["copias_disponibles"] + cantidad_cambio

        if nuevo_total < 0 or nuevo_disp < 0:
            raise ValueError("El número de copias no puede ser negativo.")

        self.catalogo[isbn]["copias_total"] = nuevo_total
        self.catalogo[isbn]["copias_disponibles"] = nuevo_disp

    # Recorro el catálogo y retorno coincidencias como lista de diccionarios.
    def buscar_libros(self, criterio='titulo', valor='', categoria=None):
        resultados = []
        valor = valor.lower()
        for isbn, info in self.catalogo.items():
            if categoria and info["categoria"].lower() != categoria.lower():
                continue
            if valor in str(info.get(criterio, '')).lower():
                libro = info.copy()
                libro["isbn"] = isbn
                resultados.append(libro)
        return resultados

    # ============ GESTIÓN DE USUARIOS ============

    # Reviso que el ID no exista, que el nombre tenga información, y que el correo sea válido, después de esto lo añado al diccionario de usuarios.
    def registrar_usuario(self, id_usuario, nombre, email):
        if id_usuario in self.usuarios:
            raise ValueError("El ID de usuario ya existe.")
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if "@" not in email or "." not in email:
            raise ValueError("El correo electrónico no es válido.")

        self.usuarios[id_usuario] = {
            "nombre": nombre,
            "email": email,
            "fecha_registro": datetime.now(),
            "prestamos_activos": [],
            "historial": [],
            "multas_pendientes": 0.0
        }

    # Reviso que el usuario exista y que cumpla las condiciones necesarias para hacer un prestamo, y, retorno la información obtenida.
    def obtener_estado_usuario(self, id_usuario):
        if id_usuario not in self.usuarios:
            raise UsuarioNoRegistrado(id_usuario)

        usuario = self.usuarios[id_usuario]
        puede_prestar = (
            len(usuario["prestamos_activos"]) < self.limite_prestamos
            and usuario["multas_pendientes"] <= 50
        )

        return {
            "nombre": usuario["nombre"],
            "prestamos_activos": len(usuario["prestamos_activos"]),
            "puede_prestar": puede_prestar,
            "multas_pendientes": usuario["multas_pendientes"]
        }

    # ============ GESTIÓN DE PRÉSTAMOS ============

    def prestar_libro(self, isbn, id_usuario):
        # Se verifica que el libro y usuario existan.
        if id_usuario not in self.usuarios:
            raise UsuarioNoRegistrado(id_usuario)
        if isbn not in self.catalogo:
            raise LibroNoEncontrado(isbn)

        usuario = self.usuarios[id_usuario]
        libro = self.catalogo[isbn]

        # Se verifica que hayan copias disponibles y se pueda hacer el prestamo.
        if libro["copias_disponibles"] == 0:
            raise LibroNoDisponible(isbn, libro["titulo"])
        if len(usuario["prestamos_activos"]) >= self.limite_prestamos:
            raise LimitePrestamosExcedido(id_usuario, self.limite_prestamos)
        if usuario["multas_pendientes"] > 50:
            raise ValueError("El usuario tiene multas pendientes superiores a 50.")

        # Se actualiza la información tanto del libro como del usuario, además se registra el prestamo.
        self.contador_prestamos += 1
        id_prestamo = f"P{self.contador_prestamos:04d}"

        fecha_prestamo = datetime.now()
        fecha_vencimiento = fecha_prestamo + timedelta(days=self.dias_prestamo)

        self.prestamos[id_prestamo] = {
            "isbn": isbn,
            "id_usuario": id_usuario,
            "fecha_prestamo": fecha_prestamo,
            "fecha_vencimiento": fecha_vencimiento,
            "fecha_devolucion": None,
            "multa": 0.0
        }

        usuario["prestamos_activos"].append(id_prestamo)
        libro["copias_disponibles"] -= 1
        libro["prestamos_totales"] += 1

        return id_prestamo

    def devolver_libro(self, id_prestamo):
        """
        Gestiono la devolución de un libro prestado.
        Verifico que el préstamo exista, que no se haya devuelto antes,
        y calculo la multa en caso de retraso.
        """

        # Verifico que el préstamo exista y que no se haya devuelto antes.
        if id_prestamo not in self.prestamos:
            raise KeyError("El préstamo no existe.")
        prestamo = self.prestamos[id_prestamo]
        if prestamo["fecha_devolucion"] is not None:
            raise ValueError("El préstamo ya fue devuelto.")

        # Calculo los días de retraso comparando la fecha actual con la de vencimiento.
        fecha_actual = datetime.now()
        dias_retraso = (fecha_actual - prestamo["fecha_vencimiento"]).days

        # Si el resultado es negativo (el usuario devolvió antes), lo corrijo a 0.
        dias_retraso = max(0, dias_retraso)

        # Calculo la multa solo si hay retraso.
        multa = dias_retraso * self.multa_por_dia

        # Registro la devolución y la multa dentro del préstamo.
        prestamo["fecha_devolucion"] = fecha_actual
        prestamo["multa"] = multa

        # Actualizo la información del usuario y del libro.
        usuario = self.usuarios[prestamo["id_usuario"]]
        libro = self.catalogo[prestamo["isbn"]]
        libro["copias_disponibles"] += 1

        usuario["prestamos_activos"].remove(id_prestamo)
        usuario["historial"].append(id_prestamo)
        usuario["multas_pendientes"] += multa

        # Genero un mensaje adecuado según haya o no multa.
        mensaje = "Devolución exitosa" if multa == 0 else f"Multa aplicada: ${multa}"

        # Retorno los resultados del proceso.
        return {"dias_retraso": dias_retraso, "multa": multa, "mensaje": mensaje}


    # Se verifica que el prestamo exista y se actualiza la fecha de vencimiento.
    def renovar_prestamo(self, id_prestamo):
        if id_prestamo not in self.prestamos:
            raise KeyError("El préstamo no existe.")
        prestamo = self.prestamos[id_prestamo]
        if datetime.now() > prestamo["fecha_vencimiento"]:
            raise PrestamoVencido(id_prestamo, (datetime.now() - prestamo["fecha_vencimiento"]).days)

        prestamo["fecha_vencimiento"] += timedelta(days=self.dias_prestamo)
        return f"Préstamo {id_prestamo} renovado hasta {prestamo['fecha_vencimiento'].date()}"

    # ============ ESTADÍSTICAS Y REPORTES ============

    # Se organiza una lista con la información necesaria para el cálculo y después de esto se recorta de 0 a n dependiendo del top que queramos.
    def libros_mas_prestados(self, n=10):
        lista = [
            (isbn, info["titulo"], info["prestamos_totales"])
            for isbn, info in self.catalogo.items()
        ]
        lista.sort(key=lambda x: x[2], reverse=True)
        return lista[:n]

    # Se organiza una lista con la información necesaria para el cálculo y después de esto se recorta de 0 a n dependiendo del top que queramos.
    def usuarios_mas_activos(self, n=5):
        lista = [
            (id_u, u["nombre"], len(u["historial"]))
            for id_u, u in self.usuarios.items()
        ]
        lista.sort(key=lambda x: x[2], reverse=True)
        return lista[:n]

    # Se hace un escaneo de información importante de la categoría seleccionada y se mete a un diccionario.
    def estadisticas_categoria(self, categoria):
        libros_categoria = {
            isbn: info for isbn, info in self.catalogo.items()
            if info["categoria"].lower() == categoria.lower()
        }

        if not libros_categoria:
            return {}

        total_libros = len(libros_categoria)
        total_copias = sum(l["copias_total"] for l in libros_categoria.values())
        copias_prestadas = sum(
            l["copias_total"] - l["copias_disponibles"]
            for l in libros_categoria.values()
        )
        tasa = (copias_prestadas / total_copias) * 100 if total_copias > 0 else 0
        popular = max(libros_categoria.values(), key=lambda x: x["prestamos_totales"])["titulo"]

        return {
            "total_libros": total_libros,
            "total_copias": total_copias,
            "copias_prestadas": copias_prestadas,
            "tasa_prestamo": round(tasa, 2),
            "libro_mas_popular": popular
        }

    # Se verifica por cada valor en prestamos la fecha de vencimiento para poder añadirlos a una lista de vencidos con los datos necesarios que retornaremos, como la multa.
    def prestamos_vencidos(self):
        vencidos = []
        hoy = datetime.now()
        for id_p, datos in self.prestamos.items():
            if datos["fecha_devolucion"] is None and datos["fecha_vencimiento"] < hoy:
                dias_retraso = (hoy - datos["fecha_vencimiento"]).days
                multa = dias_retraso * self.multa_por_dia
                libro = self.catalogo[datos["isbn"]]
                vencidos.append({
                    "id_prestamo": id_p,
                    "isbn": datos["isbn"],
                    "titulo": libro["titulo"],
                    "id_usuario": datos["id_usuario"],
                    "dias_retraso": dias_retraso,
                    "multa_acumulada": multa
                })
        return vencidos


    def reporte_financiero(self, fecha_inicio=None, fecha_fin=None):
        total = 0
        pagadas = 0
        pendientes = 0
        prestamos_con_multa = 0
        multas = []

        # Recorro todos los préstamos registrados en el sistema.
        for p in self.prestamos.values():
            # Si el préstamo tiene una multa, lo tengo en cuenta en el análisis.
            if p["multa"] > 0:
                fecha = p["fecha_devolucion"] or p["fecha_prestamo"]
                if (fecha_inicio and fecha < fecha_inicio) or (fecha_fin and fecha > fecha_fin):
                    continue
                # Cuento este préstamo como uno con multa.
                prestamos_con_multa += 1
                multas.append(p["multa"])
                total += p["multa"]

        # Recorro todos los usuarios para sumar las multas pendientes.
        for u in self.usuarios.values():
            pendientes += u["multas_pendientes"]

        # Calculo las multas pagadas restando las pendientes al total general.
        pagadas = max(0, total - pendientes)

        # Calculo el promedio por multa, asegurándome de no dividir entre cero.
        promedio = round(total / prestamos_con_multa, 2) if prestamos_con_multa else 0

        # Retorno un diccionario con todos los resultados redondeados a 2 decimales.
        return {
            "total_multas": round(total, 2),
            "multas_pagadas": round(pagadas, 2),
            "multas_pendientes": round(pendientes, 2),
            "prestamos_con_multa": prestamos_con_multa,
            "promedio_multa": promedio
        }

    # ============ UTILIDADES ============

    # Con open abro o creo el archivo al que voy a exportar y escribo en el formato propuesto todos los valores de catalogo.
    def exportar_catalogo(self, archivo='catalogo.txt'):
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                for isbn, info in self.catalogo.items():
                    f.write(f"{isbn}|{info['titulo']}|{info['autor']}|{info['anio']}|"
                            f"{info['categoria']}|{info['copias_total']}\n")
        except Exception as e:
            print(f"Error al exportar catálogo: {e}")

    # Con open abro el archivo de catálogo que voy a importar y por cada línea, separo los valores con el formato propuesto y los voy añadiendo.
    def importar_catalogo(self, archivo='catalogo.txt'):
        exitosos = 0
        errores = []
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                for i, linea in enumerate(f, 1):
                    try:
                        isbn, titulo, autor, anio, categoria, copias = linea.strip().split('|')
                        if isbn in self.catalogo:
                            raise ValueError("ISBN duplicado")
                        self.agregar_libro(isbn, titulo, autor, int(anio), categoria, int(copias))
                        exitosos += 1
                    except Exception as e:
                        errores.append((i, str(e)))
        except FileNotFoundError:
            print(f"Archivo '{archivo}' no encontrado.")
        return {"exitosos": exitosos, "errores": errores}


# ===========================================================================
# CASOS DE PRUEBA BÁSICOS
# ===========================================================================

if __name__ == "__main__":
    print("="*70)
    print(" PRUEBAS DEL SISTEMA DE BIBLIOTECA")
    print("="*70)

    # Crear instancia del sistema
    biblioteca = SistemaBiblioteca(dias_prestamo=7, multa_por_dia=2.0, limite_prestamos=3)

    # 1. Agregar libros al catálogo
    biblioteca.agregar_libro("9780134685991", "Effective Python", "Brett Slatkin", 2019, "Programación", 5)
    biblioteca.agregar_libro("9780135404676", "Python Crash Course", "Eric Matthes", 2019, "Programación", 3)
    biblioteca.agregar_libro("9781449355739", "Fluent Python", "Luciano Ramalho", 2015, "Programación", 2)

    # 2. Registrar usuarios
    biblioteca.registrar_usuario("U001", "Ana García", "ana@email.com")
    biblioteca.registrar_usuario("U002", "Carlos López", "carlos@email.com")

    # 3. Realizar préstamos
    try:
        id_p1 = biblioteca.prestar_libro("9780134685991", "U001")
        id_p2 = biblioteca.prestar_libro("9780135404676", "U001")
        print(f"Préstamos realizados: {id_p1}, {id_p2}")
    except ErrorBiblioteca as e:
        print(f"Error: {e}")

    # 4. Buscar libros
    resultados = biblioteca.buscar_libros(criterio='autor', valor='python')
    print(f"Libros encontrados: {len(resultados)}")

    # 5. Devolver con retraso (simular)
    # Modifica fecha_vencimiento para simular retraso
    resultado_dev = biblioteca.devolver_libro(id_p1)
    print(f"Devolución: {resultado_dev}")

    # 6. Estadísticas
    print(biblioteca.libros_mas_prestados(3))
    print(biblioteca.estadisticas_categoria("Programación"))
    print(biblioteca.reporte_financiero())

    # 7. Exportar catálogo
    biblioteca.exportar_catalogo("catalogo_backup.txt")

    # 8. Manejo de excepciones específicas
    try:
        biblioteca.prestar_libro("9999999999999", "U001")  # ISBN no existe
    except LibroNoEncontrado as e:
        print(f"Capturado correctamente: {e}")

    try:
        for i in range(5):
            biblioteca.prestar_libro("9780134685991", "U002")  # Exceder límite
    except LimitePrestamosExcedido as e:
        print(f"Límite controlado: {e}")