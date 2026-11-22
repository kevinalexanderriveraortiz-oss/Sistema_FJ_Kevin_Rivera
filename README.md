# Sistema_FJ_Kevin_Rivera

Sistema Integral de Gestión de Clientes, Servicios y Reservas para la empresa **Software FJ**.
Proyecto de la Fase 4 del curso Programación (213023) - UNAD.

## Descripción
Aplicación en Python orientada a objetos que gestiona clientes, servicios y reservas
completamente en memoria (listas y objetos), sin base de datos. Aplica abstracción,
herencia, polimorfismo, encapsulación y manejo avanzado de excepciones.
Los errores y eventos se registran en el archivo `sistema.log`.

## Estructura del proyecto
- `excepciones.py`: excepción base `ErrorSistemaFJ` y excepciones personalizadas.
- `modelos.py`: clases abstractas `EntidadBase` y `Servicio`, clase `Cliente` y servicios
  especializados (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`).
- `reserva.py`: clase `Reserva` (estados PENDIENTE, CONFIRMADA, CANCELADA).
- `gestor_sistema.py`: gestión de listas internas y registro de eventos en el log.
- `main.py`: simulación de 12 operaciones (válidas e inválidas).

## Cómo ejecutar
1. Instalar Python 3.
2. Descargar o clonar este repositorio.
3. En la carpeta del proyecto, ejecutar:

   python main.py

4. Revisar el archivo `sistema.log` generado.

## Autor
Kevin Alexander Rivera Ortiz - Grupo 213023A_2204
