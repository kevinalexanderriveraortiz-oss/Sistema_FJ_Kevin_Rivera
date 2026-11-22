"""
Módulo de excepciones personalizadas para el Sistema Integral de Software FJ.
Permite identificar, clasificar y encadenar errores específicos de negocio.
"""


class ErrorSistemaFJ(Exception):
    """Excepción base para todos los errores controlados del sistema Software FJ."""

    def __init__(self, mensaje: str, codigo_error: str = "ERR-000"):
        # Almacena un código identificador del error para facilitar la auditoría en logs
        self.codigo_error = codigo_error
        # Invoca el constructor de la clase padre Exception con el mensaje formateado
        super().__init__(f"[{codigo_error}] {mensaje}")


class DatosInvalidosError(ErrorSistemaFJ):
    """Se lanza cuando los parámetros de entrada tienen formato incorrecto o están vacíos."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-DATOS")


class ClienteNoValidoError(ErrorSistemaFJ):
    """Se lanza cuando falla la validación de los datos personales de un cliente."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-CLIENTE")


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta reservar o crear un servicio inactivo o mal configurado."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-SERVICIO")


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza cuando una operación de reserva (confirmar, cancelar o calcular) no es permitida."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-RESERVA")


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando el cálculo de tarifas, impuestos o descuentos produce valores inválidos."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-CALCULO")
