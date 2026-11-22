"""
Módulo de modelos orientados a objetos para Software FJ.
Implementa abstracción, encapsulación, herencia, polimorfismo y métodos sobrecargados.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from excepciones import (
    ClienteNoValidoError,
    DatosInvalidosError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)


class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad general dentro del sistema."""

    def __init__(self, id_entidad: str):
        # Valida que el identificador no sea nulo ni una cadena vacía
        if not id_entidad or not isinstance(id_entidad, str) or not id_entidad.strip():
            raise DatosInvalidosError("El identificador de la entidad no puede estar vacío.")
        # Atributo protegido con el identificador único
        self._id = id_entidad.strip()
        # Registra la marca de tiempo exacta en que se instanció el objeto
        self._fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id(self) -> str:
        """Retorna el identificador único de la entidad."""
        return self._id

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto obligatorio para describir cada entidad."""
        pass


class Cliente(EntidadBase):
    """Representa un cliente de Software FJ con encapsulación y validaciones estrictas."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        # Inicializa la clase abstracta padre
        super().__init__(id_cliente)
        # Usa los setters encapsulados para validar cada dato desde la creación
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        # Verifica que el nombre tenga al menos 3 caracteres alfabéticos válidos
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteNoValidoError(f"Nombre de cliente inválido: '{valor}'. Debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        # Valida estructura básica de correo electrónico
        if not valor or "@" not in valor or "." not in valor.split("@")[-1]:
            raise ClienteNoValidoError(f"Correo electrónico inválido para {self._nombre}: '{valor}'.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        # Verifica que el teléfono contenga únicamente dígitos y longitud mínima de 7
        limpio = str(valor).strip()
        if not limpio.isdigit() or len(limpio) < 7:
            raise ClienteNoValidoError(f"Teléfono inválido para {self._nombre}: '{valor}'.")
        self._telefono = limpio

    def obtener_resumen(self) -> str:
        """Implementación polimórfica del resumen del cliente."""
        return f"Cliente [{self.id}] {self.nombre} | Email: {self.correo} | Tel: {self.telefono}"


class Servicio(EntidadBase, ABC):
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, disponible: bool = True):
        super().__init__(id_servicio)
        if not nombre or not nombre.strip():
            raise ServicioNoDisponibleError("El nombre del servicio no puede estar vacío.")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioNoDisponibleError(f"La tarifa por hora ({tarifa_hora}) debe ser mayor a cero.")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self, horas: int) -> None:
        """Valida restricciones específicas de duración o uso de cada servicio."""
        pass

    @abstractmethod
    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """
        Método sobrecargado mediante parámetros opcionales para calcular el costo final
        aplicando descuentos e impuestos según las reglas de cada subclase.
        """
        pass

    def _aplicar_impuestos_y_descuentos(self, subtotal: float, descuento: float, impuesto: float) -> float:
        """Método auxiliar protegido que valida consistencia financiera en los cálculos."""
        if descuento < 0 or descuento >= 1:
            raise CalculoInconsistenteError(f"Porcentaje de descuento fuera de rango (0 a 0.99): {descuento}")
        if impuesto < 0 or impuesto > 0.5:
            raise CalculoInconsistenteError(f"Porcentaje de impuesto inválido: {impuesto}")
        valor_con_descuento = subtotal * (1 - descuento)
        total = valor_con_descuento * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError("El total calculado no puede ser menor o igual a cero.")
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio especializado para alquiler de salas tecnológicas y de reuniones."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioNoDisponibleError("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad = capacidad

    def validar_parametros(self, horas: int) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError(f"La sala '{self.nombre}' no se encuentra disponible.")
        if not isinstance(horas, int) or horas < 1 or horas > 12:
            raise DatosInvalidosError("La reserva de sala debe ser entre 1 y 12 horas.")

    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self.validar_parametros(horas)
        # Recargo fijo de mantenimiento por uso de sala tecnológica
        subtotal = (self.tarifa_hora * horas) + 15000.0
        return self._aplicar_impuestos_y_descuentos(subtotal, descuento, impuesto)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "Ocupada"
        return f"Sala [{self.id}] {self.nombre} (Capacidad: {self._capacidad} pers.) - ${self.tarifa_hora:,.0f}/h [{estado}]"


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de estaciones de trabajo y hardware."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, categoria: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        self._categoria = categoria.strip() if categoria else "General"

    def validar_parametros(self, horas: int) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El equipo '{self.nombre}' no está disponible para alquiler.")
        if not isinstance(horas, int) or horas < 2:
            raise DatosInvalidosError("El alquiler de equipos requiere un mínimo de 2 horas.")

    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self.validar_parametros(horas)
        # Incluye seguro obligatorio del 5% sobre el valor base del hardware
        subtotal = (self.tarifa_hora * horas) * 1.05
        return self._aplicar_impuestos_y_descuentos(subtotal, descuento, impuesto)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "En uso"
        return f"Equipo [{self.id}] {self.nombre} ({self._categoria}) - ${self.tarifa_hora:,.0f}/h [{estado}]"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría en arquitectura de software y TI."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, especialidad: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        self._especialidad = especialidad.strip() if especialidad else "Ingeniería de Software"

    def validar_parametros(self, horas: int) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError(f"La asesoría '{self.nombre}' no tiene agenda disponible.")
        if not isinstance(horas, int) or horas <= 0:
            raise DatosInvalidosError("La duración de la asesoría debe ser de al menos 1 hora.")

    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self.validar_parametros(horas)
        subtotal = self.tarifa_hora * horas
        return self._aplicar_impuestos_y_descuentos(subtotal, descuento, impuesto)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Asesoría [{self.id}] {self.nombre} ({self._especialidad}) - ${self.tarifa_hora:,.0f}/h [{estado}]"
