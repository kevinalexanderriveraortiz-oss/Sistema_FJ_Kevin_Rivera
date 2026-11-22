"""
Módulo de gestión de reservas para Software FJ.
Integra Cliente y Servicio con control de estados y encadenamiento de excepciones.
"""

from modelos import EntidadBase, Cliente, Servicio
from excepciones import ReservaInvalidaError, ErrorSistemaFJ


class Reserva(EntidadBase):
    """Representa una reserva que vincula un cliente, un servicio y su duración."""

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, horas: int):
        super().__init__(id_reserva)
        # Valida que los objetos recibidos pertenezcan a las jerarquías esperadas
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("Se requiere una instancia válida de Cliente para crear la reserva.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Se requiere una instancia válida de Servicio para crear la reserva.")

        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = "PENDIENTE"
        self._costo_total = 0.0

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    def procesar_y_confirmar(self, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """
        Calcula el costo y confirma la reserva.
        Implementa encadenamiento de excepciones (raise ... from e) ante fallos de cálculo o disponibilidad.
        """
        if self._estado == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva {self.id} está cancelada y no puede confirmarse.")
        if self._estado == "CONFIRMADA":
            raise ReservaInvalidaError(f"La reserva {self.id} ya se encuentra confirmada.")

        try:
            # Delega el cálculo polimórfico al servicio correspondiente
            self._costo_total = self._servicio.calcular_costo(self._horas, descuento, impuesto)
            self._estado = "CONFIRMADA"
            # Marca el servicio como ocupado tras confirmar la reserva
            self._servicio.disponible = False
            return self._costo_total
        except ErrorSistemaFJ as error_origen:
            # Encadena la excepción original dentro de una ReservaInvalidaError para trazabilidad
            raise ReservaInvalidaError(
                f"No fue posible procesar la reserva {self.id} para el cliente {self._cliente.nombre}."
            ) from error_origen

    def cancelar(self) -> None:
        """Cancela una reserva activa y libera la disponibilidad del servicio."""
        if self._estado == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva {self.id} ya había sido cancelada previamente.")
        self._estado = "CANCELADA"
        self._servicio.disponible = True

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id}] | Estado: {self._estado} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} ({self._horas}h) | Total: ${self._costo_total:,.2f}"
        )
