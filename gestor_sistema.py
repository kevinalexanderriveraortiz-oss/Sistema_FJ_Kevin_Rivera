"""
Módulo controlador del sistema Software FJ.
Gestiona colecciones internas en memoria y registra todos los eventos y errores en archivo de logs.
"""

import logging
from datetime import datetime
from modelos import Cliente, Servicio
from reserva import Reserva
from excepciones import ErrorSistemaFJ, DatosInvalidosError


class GestorSistemaFJ:
    """Controlador central que administra clientes, servicios y reservas sin base de datos."""

    def __init__(self, archivo_log: str = "sistema.log"):
        # Listas internas en memoria para almacenar objetos del sistema
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []
        self._archivo_log = archivo_log
        self._configurar_logger()

    def _configurar_logger(self) -> None:
        """Configura el registro de auditoría en archivo plano con formato estructurado."""
        self._logger = logging.getLogger("SoftwareFJ")
        self._logger.setLevel(logging.INFO)
        # Evita duplicar handlers si se instancia más de una vez
        if not self._logger.handlers:
            handler = logging.FileHandler(self._archivo_log, mode="w", encoding="utf-8")
            formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S")
            handler.setFormatter(formato)
            self._logger.addHandler(handler)

    def registrar_cliente(self, cliente: Cliente) -> bool:
        """Registra un cliente validando duplicados con bloque try/except/else/finally."""
        try:
            # Verifica que no exista otro cliente con el mismo ID
            if any(c.id == cliente.id for c in self._clientes):
                raise DatosInvalidosError(f"Ya existe un cliente registrado con el ID '{cliente.id}'.")
        except ErrorSistemaFJ as e:
            self._logger.error(f"Fallo al registrar cliente: {e}")
            print(f"[ERROR CONTROLADO] {e}")
            return False
        else:
            # Se ejecuta únicamente si no ocurrió ninguna excepción en el bloque try
            self._clientes.append(cliente)
            self._logger.info(f"Cliente registrado exitosamente: {cliente.obtener_resumen()}")
            print(f"[OK] {cliente.obtener_resumen()}")
            return True
        finally:
            # Bloque de cierre que deja constancia de finalización de la operación
            self._logger.info(f"Auditoría de operación registrar_cliente finalizada ({datetime.now().strftime('%H:%M:%S')}).")

    def registrar_servicio(self, servicio: Servicio) -> bool:
        """Agrega un servicio al catálogo interno del sistema."""
        try:
            if any(s.id == servicio.id for s in self._servicios):
                raise DatosInvalidosError(f"Ya existe un servicio con el ID '{servicio.id}'.")
            self._servicios.append(servicio)
            self._logger.info(f"Servicio agregado: {servicio.obtener_resumen()}")
            print(f"[OK] {servicio.obtener_resumen()}")
            return True
        except ErrorSistemaFJ as e:
            self._logger.error(f"Error al registrar servicio: {e}")
            print(f"[ERROR CONTROLADO] {e}")
            return False

    def crear_y_confirmar_reserva(
        self, id_reserva: str, cliente: Cliente, servicio: Servicio, horas: int, descuento: float = 0.0
    ) -> Reserva | None:
        """Crea y confirma una reserva manejando excepciones encadenadas sin detener la aplicación."""
        try:
            nueva_reserva = Reserva(id_reserva, cliente, servicio, horas)
            nueva_reserva.procesar_y_confirmar(descuento=descuento)
        except ErrorSistemaFJ as e:
            # Registra tanto el error principal como la causa encadenada (__cause__)
            detalle_causa = f" | Causa raíz: {e.__cause__}" if e.__cause__ else ""
            self._logger.error(f"Error en reserva {id_reserva}: {e}{detalle_causa}")
            print(f"[ERROR CONTROLADO] {e}{detalle_causa}")
            return None
        else:
            self._reservas.append(nueva_reserva)
            self._logger.info(f"Reserva confirmada: {nueva_reserva.obtener_resumen()}")
            print(f"[OK] {nueva_reserva.obtener_resumen()}")
            return nueva_reserva
        finally:
            self._logger.info(f"Proceso de reserva '{id_reserva}' cerrado de forma segura.")

    def cancelar_reserva(self, reserva: Reserva) -> bool:
        """Cancela una reserva existente controlando errores de estado."""
        try:
            if reserva is None:
                raise DatosInvalidosError("No se puede cancelar una reserva inexistente (None).")
            reserva.cancelar()
            self._logger.info(f"Reserva cancelada: {reserva.obtener_resumen()}")
            print(f"[OK] Cancelación exitosa -> {reserva.obtener_resumen()}")
            return True
        except ErrorSistemaFJ as e:
            self._logger.error(f"Error al cancelar reserva: {e}")
            print(f"[ERROR CONTROLADO] {e}")
            return False

    def mostrar_resumen_general(self) -> None:
        """Imprime el estado consolidado en memoria al finalizar la simulación."""
        print("\n" + "=" * 70)
        print("RESUMEN CONSOLIDADO EN MEMORIA - SOFTWARE FJ")
        print(f"Clientes activos: {len(self._clientes)} | Servicios catalogados: {len(self._servicios)} | Reservas registradas: {len(self._reservas)}")
        print("=" * 70)
