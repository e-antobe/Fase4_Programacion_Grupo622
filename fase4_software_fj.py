"""
UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
CURSO: PROGRAMACIÓN (CÓDIGO: 213023)
FASE 4: COMPONENTE PRÁCTICO - PRÁCTICAS SIMULADAS
EMPRESA: SOFTWARE FJ - SISTEMA DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS

Descripción:
Programa modular en Python que implementa la gestión de clientes, servicios
y reservas para la empresa Software FJ. Incorpora encapsulamiento, herencia,
clases abstractas, polimorfismo, sobrecarga simulada de métodos, manejo avanzado
de excepciones personalizadas (try / except / else / finally) y registro
sistemático de logs de auditoría en archivo local.
"""

import logging
import re
from abc import ABC, abstractmethod
from datetime import datetime

# ==============================================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGGING
# ==============================================================================
LOG_FILENAME = "software_fj.log"

logging.basicConfig(
    filename=LOG_FILENAME,
    filemode="a",
    format="%(asctime)s [%(levelname)s] (%(module)s): %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)
logger = logging.getLogger("SoftwareFJLogger")


# ==============================================================================
# EXCEPCIONES PERSONALIZADAS (HERENCIA DE EXCEPTION)
# ==============================================================================
class SoftwareFJError(Exception):
    """Excepción base para el sistema Software FJ."""
    pass

class AutenticacionError(SoftwareFJError):
    """Se dispara cuando falla el inicio de sesión."""
    pass

class ClienteInvalidoError(SoftwareFJError):
    """Se dispara cuando los datos del cliente son inválidos o están duplicados."""
    pass

class ServicioNoDisponibleError(SoftwareFJError):
    """Se dispara cuando un servicio no cumple con los requisitos o está inactivo."""
    pass

class ReservaInvalidaError(SoftwareFJError):
    """Se dispara cuando una reserva incumple las reglas de negocio."""
    pass

class HorarioInvalidoError(SoftwareFJError):
    """Se dispara cuando el formato u orden de las horas en 24h es erróneo."""
    pass


# ==============================================================================
# CLASE: Usuario (MÓDULO DE AUTENTICACIÓN)
# ==============================================================================
class Usuario:
    """
    Clase que representa un usuario del sistema para control de acceso.
    Atributos encapsulados: _username, _password
    """
    def __init__(self, username="admin", password="UNAD123"):
        self._username = str(username).strip()
        self._password = str(password).strip()

    def validar(self, input_user, input_pass):
        """
        Valida las credenciales ingresadas.
        Lanza AutenticacionError si la validación falla.
        """
        logger.info(f"Intento de autenticación para usuario: '{input_user}'")
        try:
            if self._username == str(input_user).strip() and self._password == str(input_pass).strip():
                logger.info("Autenticación exitosa.")
                return True
            else:
                raise AutenticacionError("Credenciales incorrectas. Usuario o contraseña no válidos.")
        except AutenticacionError as ex:
            logger.warning(f"Fallo de autenticación: {ex}")
            raise
        except Exception as ex:
            logger.error(f"Error inesperado durante la autenticación: {ex}")
            raise SoftwareFJError(f"Error del sistema en login: {ex}")
        else:
            pass
        finally:
            logger.info("Finalizado proceso de verificación de credenciales.")


# ==============================================================================
# CLASE: Cliente (ENCAPSULAMIENTO Y VALIDACIONES)
# ==============================================================================
class Cliente:
    """
    Clase que representa a un cliente de Software FJ.
    Atributos encapsulados: _id_cliente, _nombre, _email, _telefono
    """
    def __init__(self, id_cliente, nombre, email, telefono):
        self._id_cliente = str(id_cliente).strip()
        self._nombre = str(nombre).strip()
        self.email = email        # Usa el setter con validación
        self.telefono = telefono  # Usa el setter con validación

    @property
    def id_cliente(self):
        return self._id_cliente

    @property
    def nombre(self):
        return self._nombre

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_email, str(valor).strip()):
            raise ClienteInvalidoError(f"El correo electrónico '{valor}' no tiene un formato válido.")
        self._email = str(valor).strip()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        val_clean = str(valor).strip()
        if not val_clean.isdigit() or len(val_clean) < 7:
            raise ClienteInvalidoError(f"El teléfono '{valor}' debe contener únicamente números (mínimo 7 dígitos).")
        self._telefono = val_clean

    def __str__(self):
        return f"Cliente [{self._id_cliente}] {self._nombre} | Email: {self._email} | Tel: {self._telefono}"


# ==============================================================================
# JERARQUÍA POO: CLASE ABSTRACTA Servicio Y DERIVADAS
# ==============================================================================
class Servicio(ABC):
    """
    Clase Abstracta que representa un servicio ofrecido por Software FJ.
    Atributos encapsulados: _id_servicio, _nombre_servicio, _tarifa_base
    """
    def __init__(self, id_servicio, nombre_servicio, tarifa_base):
        self._id_servicio = str(id_servicio).strip()
        self._nombre_servicio = str(nombre_servicio).strip()
        
        if float(tarifa_base) <= 0:
            raise ServicioNoDisponibleError(f"La tarifa base del servicio '{nombre_servicio}' debe ser mayor a 0.")
        self._tarifa_base = float(tarifa_base)

    @property
    def id_servicio(self):
        return self._id_servicio

    @property
    def nombre_servicio(self):
        return self._nombre_servicio

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @abstractmethod
    def calcular_costo(self, descuento=0.0, impuesto=0.19, recargo=0.0):
        """Método abstracto para calcular el costo total con sobrecarga simulada."""
        pass

    @abstractmethod
    def obtener_descripcion(self):
        """Método abstracto para obtener la descripción del servicio."""
        pass


class ReservaSala(Servicio):
    """
    Servicio de reserva de salas de conferencias / reuniones.
    """
    def __init__(self, id_servicio, nombre_servicio, tarifa_base, capacidad_personas, horas_reserva):
        super().__init__(id_servicio, nombre_servicio, tarifa_base)
        if int(capacidad_personas) <= 0:
            raise ServicioNoDisponibleError("La capacidad de la sala debe ser mayor a 0 personas.")
        if float(horas_reserva) <= 0:
            raise ServicioNoDisponibleError("La duración de la reserva debe ser mayor a 0 horas.")
        
        self._capacidad_personas = int(capacidad_personas)
        self._horas_reserva = float(horas_reserva)

    def calcular_costo(self, descuento=0.0, impuesto=0.19, recargo=0.0):
        subtotal = (self._tarifa_base * self._horas_reserva) + recargo
        monto_descuento = subtotal * descuento
        subtotal_desc = subtotal - monto_descuento
        total = subtotal_desc * (1 + impuesto)
        return round(total, 2)

    def obtener_descripcion(self):
        return f"Sala: {self._nombre_servicio} | Capacidad: {self._capacidad_personas} personas | Horas: {self._horas_reserva}h"


class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos tecnológicos (laptops, proyectores, servidores).
    """
    def __init__(self, id_servicio, nombre_servicio, tarifa_base, tipo_equipo, dias_alquiler):
        super().__init__(id_servicio, nombre_servicio, tarifa_base)
        if int(dias_alquiler) <= 0:
            raise ServicioNoDisponibleError("Los días de alquiler deben ser mayores a 0.")
        self._tipo_equipo = str(tipo_equipo).strip()
        self._dias_alquiler = int(dias_alquiler)

    def calcular_costo(self, descuento=0.0, impuesto=0.19, recargo=0.0):
        desc_volumen = 0.05 if self._dias_alquiler >= 5 else 0.0
        desc_total = min(1.0, descuento + desc_volumen)
        
        subtotal = (self._tarifa_base * self._dias_alquiler) + recargo
        subtotal_desc = subtotal * (1 - desc_total)
        total = subtotal_desc * (1 + impuesto)
        return round(total, 2)

    def obtener_descripcion(self):
        return f"Equipo: {self._tipo_equipo} ({self._nombre_servicio}) | Días: {self._dias_alquiler}"


class AsesoriaEspecializada(Servicio):
    """
    Servicio de consultoría y asesoría técnica en desarrollo de software.
    """
    def __init__(self, id_servicio, nombre_servicio, tarifa_base, nivel_consultor, horas_asesoria):
        super().__init__(id_servicio, nombre_servicio, tarifa_base)
        if float(horas_asesoria) <= 0:
            raise ServicioNoDisponibleError("Las horas de asesoría deben ser mayores a 0.")
        
        self._nivel_consultor = str(nivel_consultor).strip().upper() # JUNIOR, SENIOR, MASTER
        self._horas_asesoria = float(horas_asesoria)

    def calcular_costo(self, descuento=0.0, impuesto=0.19, recargo=0.0):
        multiplicador_nivel = {"JUNIOR": 1.0, "SENIOR": 1.5, "MASTER": 2.0}.get(self._nivel_consultor, 1.0)
        subtotal = (self._tarifa_base * multiplicador_nivel * self._horas_asesoria) + recargo
        subtotal_desc = subtotal * (1 - descuento)
        total = subtotal_desc * (1 + impuesto)
        return round(total, 2)

    def obtener_descripcion(self):
        return f"Asesoría: {self._nombre_servicio} | Nivel: {self._nivel_consultor} | Horas: {self._horas_asesoria}h"


# ==============================================================================
# CLASE: Reserva
# ==============================================================================
class Reserva:
    """
    Clase que vincula un Cliente, un Servicio y un Horario.
    Atributos encapsulados: _id_reserva, _cliente, _servicio, _hora_inicio, _hora_fin, _estado
    """
    def __init__(self, id_reserva, cliente, servicio, hora_inicio_str, hora_fin_str):
        self._id_reserva = str(id_reserva).strip()
        
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("El objeto cliente proporcionado no es válido.")
        self._cliente = cliente

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("El objeto servicio proporcionado no es válido.")
        self._servicio = servicio

        # Validar horas en formato 24h (HH:MM)
        self._h_inicio_dec = self._parse_hhmm(hora_inicio_str)
        self._h_fin_dec = self._parse_hhmm(hora_fin_str)

        if self._h_fin_dec <= self._h_inicio_dec:
            raise HorarioInvalidoError(
                f"La hora de finalización ({hora_fin_str}) debe ser estrictamente posterior a la hora de inicio ({hora_inicio_str})."
            )

        self._hora_inicio_str = hora_inicio_str
        self._hora_fin_str = hora_fin_str
        self._estado = "CONFIRMADA"

    def _parse_hhmm(self, hora_str):
        """Valida y convierte 'HH:MM' de 24h a valor decimal."""
        hora_str = str(hora_str).strip()
        if ":" not in hora_str:
            raise HorarioInvalidoError(f"Formato de hora '{hora_str}' inválido. Debe ser HH:MM (ejemplo: 14:30).")
        partes = hora_str.split(":")
        if len(partes) != 2:
            raise HorarioInvalidoError(f"Formato de hora '{hora_str}' no reconocido.")
        try:
            h = int(partes[0])
            m = int(partes[1])
            if not (0 <= h <= 23 and 0 <= m <= 59):
                raise HorarioInvalidoError(f"Hora fuera del rango 00:00 - 23:59: '{hora_str}'.")
            return h + (m / 60.0)
        except ValueError:
            raise HorarioInvalidoError(f"Los componentes de la hora '{hora_str}' deben ser números enteros.")

    def cancelar_reserva(self):
        if self._estado == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva [{self._id_reserva}] ya se encuentra cancelada.")
        self._estado = "CANCELADA"
        logger.info(f"Reserva [{self._id_reserva}] cancelada correctamente.")

    def calcular_total_reserva(self, descuento=0.0, impuesto=0.19, recargo=0.0):
        if self._estado == "CANCELADA":
            return 0.0
        return self._servicio.calcular_costo(descuento=descuento, impuesto=impuesto, recargo=recargo)

    def obtener_resumen(self):
        costo = self.calcular_total_reserva()
        return (
            f"RESERVA [{self._id_reserva}] | Estado: {self._estado}\n"
            f"  - Cliente: {self._cliente.nombre} ({self._cliente.email})\n"
            f"  - Servicio: {self._servicio.obtener_descripcion()}\n"
            f"  - Horario: {self._hora_inicio_str} a {self._hora_fin_str} (24h)\n"
            f"  - Costo Total (Inc. IVA): ${costo:,.2f}"
        )


# ==============================================================================
# GESTOR CENTRAL DEL SISTEMA (SOFTWARE FJ MANAGER)
# ==============================================================================
class SoftwareFJManager:
    """
    Controlador principal que administra clientes, servicios y reservas.
    Demuestra bloques try / except / else / finally y logging exhaustivo.
    """
    def __init__(self):
        self._usuario_sistema = Usuario("admin", "UNAD123")
        self._sesion_activa = False
        self._clientes = {}    # id -> Cliente
        self._servicios = {}   # id -> Servicio
        self._reservas = {}    # id -> Reserva

    def iniciar_sesion(self, user, pwd):
        logger.info(f"Intentando inicio de sesión con usuario '{user}'...")
        try:
            self._sesion_activa = self._usuario_sistema.validar(user, pwd)
        except AutenticacionError as ex:
            print(f"❌ ERROR DE AUTENTICACIÓN: {ex}")
            logger.warning(f"Inicio de sesión rechazado: {ex}")
            return False
        except Exception as ex:
            print(f"❌ ERROR CRÍTICO DEL SISTEMA: {ex}")
            logger.error(f"Fallo grave en inicio de sesión: {ex}", exc_info=True)
            return False
        else:
            print(f"✅ ¡Bienvenido al Sistema Software FJ! Sesión iniciada correctamente.")
            logger.info("Sesión iniciada con éxito por el usuario administrador.")
            return True
        finally:
            logger.info("Operación de inicio de sesión completada.")

    def registrar_cliente(self, id_cliente, nombre, email, telefono):
        logger.info(f"Registrando cliente [{id_cliente}]...")
        try:
            if not self._sesion_activa:
                raise AutenticacionError("Debe iniciar sesión para registrar clientes.")
            
            if id_cliente in self._clientes:
                raise ClienteInvalidoError(f"El cliente con ID '{id_cliente}' ya se encuentra registrado.")
            
            nuevo_cliente = Cliente(id_cliente, nombre, email, telefono)
            self._clientes[id_cliente] = nuevo_cliente
        except (ClienteInvalidoError, AutenticacionError) as ex:
            print(f"⚠️ REGLA DE NEGOCIO VIOLADA: {ex}")
            logger.warning(f"Error al registrar cliente [{id_cliente}]: {ex}")
            return None
        except Exception as ex:
            print(f"❌ ERROR INESPERADO AL REGISTRAR CLIENTE: {ex}")
            logger.error(f"Fallo no controlado en cliente [{id_cliente}]: {ex}", exc_info=True)
            return None
        else:
            print(f"✅ Cliente registrado con éxito: {nuevo_cliente}")
            logger.info(f"Cliente [{id_cliente}] registrado exitosamente en memoria.")
            return nuevo_cliente
        finally:
            logger.info(f"Finalizado proceso de registro para cliente ID [{id_cliente}].")

    def registrar_servicio(self, servicio_obj):
        logger.info(f"Registrando nuevo servicio [{servicio_obj.id_servicio}]...")
        try:
            if not self._sesion_activa:
                raise AutenticacionError("Debe iniciar sesión para registrar servicios.")
            
            if servicio_obj.id_servicio in self._servicios:
                raise ServicioNoDisponibleError(f"El servicio con ID '{servicio_obj.id_servicio}' ya existe.")
            
            self._servicios[servicio_obj.id_servicio] = servicio_obj
        except (ServicioNoDisponibleError, AutenticacionError) as ex:
            print(f"⚠️ REGLA DE NEGOCIO VIOLADA: {ex}")
            logger.warning(f"Error al registrar servicio: {ex}")
            return None
        except Exception as ex:
            print(f"❌ ERROR INESPERADO EN SERVICIO: {ex}")
            logger.error(f"Fallo no controlado en registro de servicio: {ex}", exc_info=True)
            return None
        else:
            print(f"✅ Servicio registrado exitosamente: {servicio_obj.obtener_descripcion()}")
            logger.info(f"Servicio [{servicio_obj.id_servicio}] registrado en memoria.")
            return servicio_obj
        finally:
            logger.info("Finalizado intento de registro de servicio.")

    def crear_reserva(self, id_reserva, id_cliente, id_servicio, h_inicio, h_fin):
        logger.info(f"Procesando creación de reserva [{id_reserva}]...")
        try:
            if not self._sesion_activa:
                raise AutenticacionError("Debe iniciar sesión para realizar reservas.")

            if id_reserva in self._reservas:
                raise ReservaInvalidaError(f"La reserva con ID '{id_reserva}' ya existe.")

            cliente = self._clientes.get(id_cliente)
            if not cliente:
                raise ClienteInvalidoError(f"No existe ningún cliente registrado con el ID '{id_cliente}'.")

            servicio = self._servicios.get(id_servicio)
            if not servicio:
                raise ServicioNoDisponibleError(f"No existe ningún servicio registrado con el ID '{id_servicio}'.")

            nueva_reserva = Reserva(id_reserva, cliente, servicio, h_inicio, h_fin)
            self._reservas[id_reserva] = nueva_reserva

        except (ReservaInvalidaError, ClienteInvalidoError, ServicioNoDisponibleError, HorarioInvalidoError, AutenticacionError) as ex:
            print(f"⚠️ RESERVA RECHAZADA: {ex}")
            logger.warning(f"Fallo al crear reserva [{id_reserva}]: {ex}")
            return None
        except Exception as ex:
            print(f"❌ ERROR INESPERADO EN RESERVA: {ex}")
            logger.error(f"Error crítico en reserva [{id_reserva}]: {ex}", exc_info=True)
            return None
        else:
            print(f"✅ ¡RESERVA EXITOSA!\n{nueva_reserva.obtener_resumen()}")
            logger.info(f"Reserva [{id_reserva}] creada y confirmada exitosamente.")
            return nueva_reserva
        finally:
            logger.info(f"Finalizado proceso de reserva [{id_reserva}].")


# ==============================================================================
# SCRIPT DE DEMOSTRACIÓN AUTOMATIZADA: 10 OPERACIONES SECUENCIALES
# ==============================================================================
def ejecutar_demostración_10_operaciones():
    print("=" * 80)
    print("       SOFTWARE FJ - SIMULACIÓN DE 10 OPERACIONES DE PRUEBA (FASE 4)")
    print("=" * 80)
    print("Iniciando prueba automatizada con captura de excepciones y registro en log...\n")

    sistema = SoftwareFJManager()

    # --------------------------------------------------------------------------
    # OPERACIÓN 1: Intento de inicio de sesión con credenciales INCORRECTAS (Error 1)
    # --------------------------------------------------------------------------
    print("\n--- OPERACIÓN 1: Intento de Login con Contraseña Errónea ---")
    sistema.iniciar_sesion("admin", "ClaveErrónea123")

    # --------------------------------------------------------------------------
    # OPERACIÓN 2: Inicio de sesión EXITOSO con credenciales VÁLIDAS (Éxito 1)
    # --------------------------------------------------------------------------
    print("\n--- OPERACIÓN 2: Login Exitoso con Credenciales Oficiales ---")
    sistema.iniciar_sesion("admin", "UNAD123")

    # --------------------------------------------------------------------------
    # OPERACIÓN 3: Registro de Cliente VÁLIDO (Éxito 2)
    # --------------------------------------------------------------------------
    print("\n--- OPERACIÓN 3: Registro de Cliente 1 (Válido) ---")
    sistema.registrar_cliente("C101", "Carlos Mendoza", "carlos.mendoza@email.com", "3001234567")

    # --------------------------------------------------------------------------
    # OPERACIÓN 4: Registro de Cliente con Email INVÁLIDO (Error 2)
    # --------------------------------------------------------------------------
    print("\n--- OPERACIÓN 4: Registro de Cliente con Email Mal Formado ---")
    sistema.registrar_cliente("C102", "Ana Gómez", "correo_invalido_sin_arroba", "3159876543")

    # --------------------------------------------------------------------------
    # OPERACIÓN 5: Registro de Servicios VÁLIDOS (Éxito 3)
    # --------------------------------------------------------------------------
    print("\n--- OPERACIÓN 5: Registro de Servicios (Sala, Equipo, Asesoría) ---")
    sala_conferencias = ReservaSala("S-01", "Sala Auditorium VIP", tarifa_base=50000, capacidad_personas=20, horas_reserva=3)
    alquiler_laptop = AlquilerEquipo("S-02", "Alquiler Laptops", tarifa_base=30000, tipo_equipo="MacBook Pro", dias_alquiler=5)
    consultoria_dev = AsesoriaEspecializada("S-03", "Arquitectura de Software", tarifa_base=80000, nivel_consultor="SENIOR", horas_asesoria=4)

    sistema.registrar_servicio(sala_conferencias)
    sistema.registrar_servicio(alquiler_laptop)
    sistema.registrar_servicio(consultoria_dev)

    # --------------------------------------------------------------------------
    # OPERACIÓN 6: Registro de Servicio con Tarifa Base INVÁLIDA (Error 3)
    # --------------------------------------------------------------------------
    print("\n--- OPERACIÓN 6: Intento de Registro de Servicio con Tarifa Negativa ---")
    try:
        servicio_invalido = ReservaSala("S-99", "Sala Ilegal", tarifa_base=-10000, capacidad_personas=5, horas_reserva=2)
        sistema.registrar_servicio(servicio_invalido)
    except ServicioNoDisponibleError as ex:
        print(f"⚠️ CAPTURADO EN CAPA SUPERIOR: {ex}")

    # --------------------------------------------------------------------------
    # OPERACIÓN 7: Crear Reserva VÁLIDA para Cliente C101 (Éxito 4)
    # --------------------------------------------------------------------------
    print("\n--- OPERACIÓN 7: Creación de Reserva Válida (C101 + S-01) ---")
    sistema.crear_reserva("R-1001", "C101", "S-01", h_inicio="09:00", h_fin="12:00")

    # --------------------------------------------------------------------------
    # OPERACIÓN 8: Crear Reserva para Cliente INEXISTENTE (Error 4)
    # --------------------------------------------------------------------------
    print("\n--- OPERACIÓN 8: Intento de Reserva con Cliente Inexistente (C999) ---")
    sistema.crear_reserva("R-1002", "C999", "S-02", h_inicio="14:00", h_fin="17:00")

    # --------------------------------------------------------------------------
    # OPERACIÓN 9: Crear Reserva con Secuencia Horaria INVÁLIDA (Error 5)
    # --------------------------------------------------------------------------
    print("\n--- OPERACIÓN 9: Intento de Reserva donde Hora Fin es Anterior a Hora Inicio ---")
    sistema.crear_reserva("R-1003", "C101", "S-03", h_inicio="16:00", h_fin="11:00")

    # --------------------------------------------------------------------------
    # OPERACIÓN 10: Crear Segunda Reserva VÁLIDA para Alquiler de Equipo (Éxito 5)
    # --------------------------------------------------------------------------
    print("\n--- OPERACIÓN 10: Creación de Reserva Válida de Alquiler de Equipo (C101 + S-02) ---")
    sistema.crear_reserva("R-1004", "C101", "S-02", h_inicio="08:00", h_fin="18:00")

    print("\n" + "=" * 80)
    print("   ¡SIMULACIÓN FINALIZADA! Todos los eventos y excepciones fueron capturados.")
    print(f"   Se ha generado el archivo de auditoría: '{LOG_FILENAME}'")
    print("=" * 80)


if __name__ == "__main__":
    ejecutar_demostración_10_operaciones()
