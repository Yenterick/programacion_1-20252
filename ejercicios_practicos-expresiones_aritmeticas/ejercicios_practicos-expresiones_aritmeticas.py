# Nivel 1: Básico (Precedencia Simple)

# Ejercicio 1.1: Predice el Resultado

print(5 + 3 * 2)

# Tu prediccion: 11
# Resultado real: 11
# Explicación: Por jerarquía de operaciones primero se opera 3 * 2, lo que da 6, 
# después se le suma el 5 para llegar al 11.


# Ejercicio 1.2: Paréntesis

print((5 + 3) * 2)

# Tu prediccion: 16
# Resultado real: 16
# Explicación: Debido a que en esta añadimos un paréntesis, ahora se hace primero
# lo que está dentro del paréntesis, después se realiza la multiplicación.


# Ejercicio 1.3: División

print(10 / 2)
print(10 // 2)
print(10 % 2)

# Tus predicciones: 5.0, 5, 0.


# Ejercios 1.4: Potencia

print(2 ** 3)
print(2 ^ 3)

# Tus predicciones: 8, 1.



# Ejercicio 1.5: Negación

print(5 - -3)
print(-5 * -3)

# Tus predicciones: 8, 15.


# Nivel 2: Intermedio (Expresiones Complejas)

# Ejercicio 2.1: Múltiples Operadores

print(2 + 3 * 4 - 5)

# Tu predicción: 9.
# Paso a paso: 1. Multiplicación (3 * 4 = 12) - 2. Suma (2 + 12 = 14) - 3. Resta (14 - 5 = 9).


# Ejercicios 2.2: División y Multiplicación

print(20 / 4 * 2)
print(20 / (4 * 2))

# Tus predicciones: 10.0, 2.5.


# Ejercicio 2.3: Módulo en Expresión

print(17 % 5 + 2 * 3)

# Tu predicción: 8.


# Ejercicio 2.4: Potencias Anidadas

print(2 ** 3 ** 2)
print((2 ** 3) ** 2)

# Tus predicciones: 512, 64.


# Ejercicio 2.5: Expresión Compleja

print(10 + 5 * 2 - 8 / 4 + 3)

# Tu predicción: 21.0
# Paso a paso: 1. Multiplicación (5 * 2 = 10) - 2. División (8 / 4 = 2.0) - 3. Suma (10 + 10 = 20)
# 4. Resta (20 - 2.0 = 18.0) - 5. Suma (18.0 + 3 = 21.0)


# Nivel 3: Avanzado (Problemas del Mundo Real)

# Ejercicio 3.1: Cálculo de Impuestos

# Calcula el total con impuesto del 15% sobre una compra de $100.

price = 100
tax_rate = 0.15

# Escribe la expresión correcta:
total = price * (1 + tax_rate)


# Ejercicio 3.2: Conversión de Temperatura

# Convierte 25°C a Fahrenheit usando la fórmula: F = (C × 9/5) + 32

celsius = 25

# Escribe la expresión:
fahrenheit = (celsius * 9 / 5) + 32


# Ejercicio 3.3: Promedio de Calificaciones

# Calcula el promedio de 3 calificaciones: 85, 90, 78

grade1 = 85
grade2 = 90
grade3 = 78

# Escribe la expresión correcta:
average = (grade1 + grade2 + grade3) / 3


# Ejercicio 3.4: Dividir Cuenta

# 4 amigos van a cenar. La cuenta es $127.50. Calcula cuánto paga cada uno.

total_bill = 127.50
num_people = 4

per_person = total_bill / num_people


# Ejercicio 3.5: Tiempo Restante
# Tienes 125 minutos. ¿Cuántas horas y minutos son?

total_minutes = 125

hours = total_minutes // 60
minutes = total_minutes % 60


# 🎯 PROYECTO FINAL: Calculadora de Expresiones
# Descripción
# Crea un programa que:

# Solicite una expresión al usuario
# Evalúe la expresión
# Muestre el resultado
# Maneje errores básicos
# Requisitos Mínimos
# Evaluar y mostrar resultado
# Manejar división por cero
# Manejar expresiones inválidas

def calculadora():
    print(f"{'%'*15} CALCULADORA {'%'*15}")
    historial = []

    while True:
        expresion = input("Ingresa una expresión ( +, -, *, /, //, %, ** ) - [ historial, salir ]: ").strip()
    
        if expresion.lower() == "salir":
            break

        if expresion.lower() == "historial":
            if historial:
                print(f"{'%'*15} HISTORIAL {'%'*15}")
                for i, (operacion, resultado) in enumerate(historial):
                    print(f"{i + 1}. {operacion} = {resultado}")
            else:
                print("Historial vacío.")
            continue

        else:
            if not expresion:
                print("Ingrese una expresión.")
            else:
                try:
                    resultado = eval(expresion)

                    historial.append((expresion, resultado))
                    print(f"Resultado: {resultado}.")
                    print(f"Tipo: {type(resultado).__name__}.")

                except ZeroDivisionError:
                    print("No se puede dividir entre 0.")

                except:
                    print("Ingrese una expresión válida.")

if __name__ == "__main__":
    calculadora()


# Ejercicios de Debugging

# Debug 1: Encuentra el Error

# Este código debería calcular el promedio
a = 10
b = 20
c = 30
average = a + b + c / 3
print(f"Promedio: {average}")

# ¿Qué está mal?: La suma de los 3 valores debería estar en paréntesis porque si no se evalúa
# primero la división (average = (a + b + c) / 3)


# Debug 2: Encuentra el Error
# Calcular 20% de descuento sobre $50

price = 50
discount = 20
final = price - discount * price
print(f"Precio final: ${final}")

# ¿Qué está mal?: Está multiplicando el descuento por el precio sin antes volverlo un porcentaje
# (final = price - (discount / 100) * price)