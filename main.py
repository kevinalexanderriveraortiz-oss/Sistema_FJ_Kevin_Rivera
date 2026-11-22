"""
Punto de entrada principal del Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ.
Autor: Kevin Alexander Rivera Ortiz
Curso: Programación (213023) - UNAD
"""

from modelos import Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from gestor_sistema import GestorSistemaFJ
from excepciones import ErrorSistemaFJ


def ejecutar_simulacion() -> None:
    """Ejecuta 12 escenarios completos (válidos e inválidos) para validar la robustez del sistema."""
    print("INICIANDO SIMULACIÓN DEL SISTEMA INTEGRAL SOFTWARE FJ...\n")
    sistema = GestorSistemaFJ("sistema.log")

    # 1. Registro válido de cliente 1
    print("--- Operación 1: Registro válido de Cliente ---")
    c1 = Cliente("CLI-01", "Kevin Rivera", "kevin.rivera@unad.edu.co", "3104567890")
    sistema.registrar_cliente(c1)

    # 2. Registro válido de cliente 2
    print("\n--- Operación 2: Registro válido de segundo Cliente ---")
    c2 = Cliente("CLI-02", "Anny Penagos", "anny.penagos@correo.com", "3159876543")
    sistema.registrar_cliente(c2)

    # 3. Intento inválido de creación de cliente (correo sin dominio y teléfono corto)
    print("\n--- Operación 3: Creación inválida de Cliente (datos corruptos) ---")
    try:
        c_invalido = Cliente("CLI-03", "Jo", "correo_invalido", "123")
        sistema.registrar_cliente(c_invalido)
    except ErrorSistemaFJ as e:
        sistema._logger.error(f"Validación de entrada bloqueó cliente inválido: {e}")
        print(f"[ERROR CONTROLADO] {e}")

    # 4. Registro válido de Cliente con ID duplicado
    print("\n--- Operación 4: Intento de registro de Cliente con ID duplicado ---")
    c_duplicado = Cliente("CLI-01", "Carlos Gómez", "carlos@correo.com", "3001112233")
    sistema.registrar_cliente(c_duplicado)

    # 5. Creación válida de 3 servicios especializados (Polimorfismo)
    print("\n--- Operación 5: Creación válida de Servicios especializados ---")
    sala_a = ReservaSala("SRV-01", "Sala Innovación Norte", 80000, capacidad=12)
    equipo_1 = AlquilerEquipo("SRV-02", "Workstation Ryzen 9 + GPU", 35000, categoria="Alto Rendimiento")
    asesoria_1 = AsesoriaEspecializada("SRV-03", "Arquitectura Cloud & Python", 120000, especialidad="Backend")
    sistema.registrar_servicio(sala_a)
    sistema.registrar_servicio(equipo_1)
    sistema.registrar_servicio(asesoria_1)

    # 6. Creación incorrecta de servicio (tarifa negativa)
    print("\n--- Operación 6: Creación inválida de Servicio (tarifa negativa) ---")
    try:
        sala_mala = ReservaSala("SRV-04", "Sala Defectuosa", -50000, capacidad=5)
        sistema.registrar_servicio(sala_mala)
    except ErrorSistemaFJ as e:
        sistema._logger.error(f"Validación bloqueó servicio inválido: {e}")
        print(f"[ERROR CONTROLADO] {e}")

    # 7. Reserva exitosa de Sala con descuento del 10% (Método sobrecargado)
    print("\n--- Operación 7: Reserva exitosa de Sala con descuento ---")
    r1 = sistema.crear_y_confirmar_reserva("RES-001", c1, sala_a, horas=4, descuento=0.10)

    # 8. Reserva fallida por servicio no disponible (Sala ya ocupada por RES-001)
    print("\n--- Operación 8: Reserva fallida (Sala ya reservada/no disponible) ---")
    sistema.crear_y_confirmar_reserva("RES-002", c2, sala_a, horas=2)

    # 9. Reserva fallida por parámetros inválidos (Alquiler de equipo por 1 hora, mínimo son 2h)
    print("\n--- Operación 9: Reserva fallida (Duración menor al mínimo permitido) ---")
    sistema.crear_y_confirmar_reserva("RES-003", c2, equipo_1, horas=1)

    # 10. Reserva fallida por cálculo inconsistente (Descuento del 150%)
    print("\n--- Operación 10: Reserva fallida (Descuento inconsistente > 100%) ---")
    sistema.crear_y_confirmar_reserva("RES-004", c2, asesoria_1, horas=3, descuento=1.5)

    # 11. Reserva exitosa de Asesoría Especializada
    print("\n--- Operación 11: Reserva exitosa de Asesoría Especializada ---")
    r5 = sistema.crear_y_confirmar_reserva("RES-005", c2, asesoria_1, horas=3, descuento=0.05)

    # 12. Cancelación de reserva y nueva reserva exitosa sobre la sala liberada
    print("\n--- Operación 12: Cancelación de RES-001 y re-reserva exitosa de la Sala ---")
    sistema.cancelar_reserva(r1)
    sistema.crear_y_confirmar_reserva("RES-006", c2, sala_a, horas=3)

    # Muestra resumen final y verifica que el programa terminó sin interrupciones
    sistema.mostrar_resumen_general()
    print("Simulación finalizada correctamente. Revise el archivo 'sistema.log' para auditoría.")


if __name__ == "__main__":
    ejecutar_simulacion()
