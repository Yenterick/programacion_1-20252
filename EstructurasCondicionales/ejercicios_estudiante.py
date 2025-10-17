#!/usr/bin/env python3
"""
EJERCICIOS PARA ESTUDIANTES - ESTRUCTURAS CONDICIONALES
Completa los siguientes ejercicios mientras exploramos los conceptos confusos.
"""

def ejercicio_1():
    """
    Completa este código para que evalúe correctamente si un número es:
    - Positivo (mayor que 0)
    - Negativo (menor que 0)
    - Cero
    """
    numero = int(input("Introduce un número entero: "))
    
    # Completa el código aquí
    if numero == 0:
        print("El número es 0")
    elif numero > 0:
        print("El número es positivo")
    else:
        print("El número es negativo")
    
    return "¡Completa el ejercicio!"

def ejercicio_2():
    """
    El siguiente código contiene errores en las condiciones.
    Encuentra y corrige los errores.
    """
    edad = int(input("Introduce tu edad: "))
    
    # Este código tiene errores a propósito
    if edad == 18:
        print("Tienes exactamente 18 años")
    elif edad < 18:
        print("Eres menor de edad")
    else:
        print("Eres mayor de edad")
    
    # Corrige el código aquí
    # ...
    
    return "¡Completa el ejercicio!"

def ejercicio_3():
    """
    Reescribe este código condicional anidado usando operadores lógicos (and, or)
    para hacerlo más legible.
    """
    llueve = input("¿Está lloviendo? (s/n): ").lower() == "s"
    frio = input("¿Hace frío? (s/n): ").lower() == "s"
    
    # Código original anidado
    print("Versión original anidada:")
    if llueve:
        if frio:
            print("Lleva paraguas y abrigo")
        else:
            print("Lleva paraguas")
    else:
        if frio:
            print("Lleva abrigo")
        else:
            print("Disfruta el día")
    
    # Tu versión mejorada usando operadores lógicos
    print("\nTu versión mejorada:")
    # Completa el código aquí
    if llueve and frio:
        print("Lleva paraguas y abrigo")
    elif llueve and not frio:
        print("Lleva paraguas")
    elif frio:
        print("Lleva abrigo")
    else:
        print("Disfruta el día")
    
    
    return "¡Completa el ejercicio!"

def ejercicio_4():
    """
    Corrige el orden de las condiciones para que funcione correctamente.
    Queremos mostrar el nivel de alerta según la temperatura:
    - Peligro extremo: más de 40°C
    - Alerta alta: entre 30°C y 40°C
    - Precaución: entre 25°C y 30°C
    - Normal: menos de 25°C
    """
    temperatura = float(input("Introduce la temperatura actual: "))
    
    # Este código tiene el orden incorrecto de condiciones
    print("Código original (incorrecto):")
    if temperatura > 25:
        print("Nivel: Precaución")
    elif temperatura > 30:
        print("Nivel: Alerta alta")
    elif temperatura > 40:
        print("Nivel: Peligro extremo")
    else:
        print("Nivel: Normal")
    
    # Corrige el orden de las condiciones
    print("\nTu versión corregida:")
    # Completa el código aquí
    if temperatura > 40:
        print("Nivel: Peligro extremo")
    elif temperatura > 30:
        print("Nivel: Alerta alta")
    elif temperatura > 25:
        print("Nivel: Precaución")
    else:
        print("Nivel: Normal")

    return "¡Completa el ejercicio!"

def ejercicio_5():
    """
    Simplifica los siguientes condicionales usando el operador ternario.
    """
    puntuacion = int(input("Introduce tu puntuación (0-100): "))
    
    # Versión con if-else
    print("Versión con if-else:")
    if puntuacion >= 60:
        resultado = "Aprobado"
    else:
        resultado = "Suspenso"
    print(resultado)
    
    # Tu versión con operador ternario
    print("\nTu versión con operador ternario:")
    # Completa el código aquí
    resultado = "Aprobado" if puntuacion >= 60 else "Suspenso"
    print(resultado)
    
    return "¡Completa el ejercicio!"

def ejercicio_6():
    """
    Crea una función que determine si un año es bisiesto.
    Un año es bisiesto si:
    - Es divisible por 4
    - No es divisible por 100, a menos que también sea divisible por 400
    """
    año = int(input("Introduce un año: "))
    
    # Completa esta función
    def es_bisiesto(año):
        return (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)
    
    if es_bisiesto(año):
        print(f"{año} es bisiesto")
    else:
        print(f"{año} no es bisiesto")
    
    return "¡Completa el ejercicio!"

def menu():
    """
    Muestra un menú para seleccionar qué ejercicio ejecutar.
    """
    print("\n" + "=" * 50)
    print("EJERCICIOS DE ESTRUCTURAS CONDICIONALES".center(50))
    print("=" * 50)
    
    print("\nSelecciona un ejercicio:")
    print("1. Evaluar si un número es positivo, negativo o cero")
    print("2. Corregir errores en condiciones")
    print("3. Simplificar condicionales anidados")
    print("4. Corregir orden de condiciones")
    print("5. Usar operador ternario")
    print("6. Determinar si un año es bisiesto")
    print("0. Salir")
    
    try:
        opcion = int(input("\nIngresa el número del ejercicio (0-6): "))
        return opcion
    except ValueError:
        print("Entrada inválida. Ingresa un número del 0 al 6.")
        return -1

def main():
    """
    Función principal para ejecutar los ejercicios.
    """
    while True:
        opcion = menu()
        
        if opcion == 0:
            print("¡Hasta luego!")
            break
        elif opcion == 1:
            ejercicio_1()
        elif opcion == 2:
            ejercicio_2()
        elif opcion == 3:
            ejercicio_3()
        elif opcion == 4:
            ejercicio_4()
        elif opcion == 5:
            ejercicio_5()
        elif opcion == 6:
            ejercicio_6()
        else:
            print("Opción inválida. Intenta de nuevo.")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    ejercicio_6()

