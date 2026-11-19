# Fase4_Programacion_Grupo622

# Software FJ - Sistema de Gestión de Clientes, Servicios y Reservas
Universidad Nacional Abierta y a Distancia (UNAD)
Curso: Programación (Código: 213023)
Fase 4: Componente Práctico - Prácticas Simuladas

## Descripción del Proyecto
Software FJ es un sistema modular desarrollado en Python enfocado en la administración de clientes, servicios tecnológicos y reservas corporativas sin dependencia de bases de datos externas (gestión en memoria).

El objetivo principal de este desarrollo es demostrar la robustez del software mediante el Manejo Avanzado de Excepciones Personalizadas (try / except / else / finally) y la trazabilidad de operaciones mediante un sistema de registros de auditoría (Logging).

## Arquitectura de Software y POO
1. Encapsulamiento y Validaciones:
   - Usuario: Control de acceso mediante autenticación (admin / UNAD123).
   - Cliente: Atributos privados (_id_cliente, _nombre, _email, _telefono) con validaciones de expresiones regulares (Regex).

2. Jerarquía de Clases e Herencia Abstracta:
   - Servicio (Clase Abstracta - ABC): Define los métodos abstractos calcular_costo() y obtener_descripcion().
   - Subclases: ReservaSala, AlquilerEquipo, AsesoriaEspecializada.

3. Excepciones Personalizadas:
   - SoftwareFJError, AutenticacionError, ClienteInvalidoError, ServicioNoDisponibleError, ReservaInvalidaError, HorarioInvalidoError.

4. Trazabilidad de Logs (software_fj.log):
   - Registro automático de eventos INFO, WARNING y ERROR.

## Instrucciones de Ejecución
1. Descargar o clonar el repositorio de GitHub.
2. Ejecutar la solución en Python:
   python fase4_software_fj.py
3. Revisar el archivo de auditoría generado:
   software_fj.log

## Resumen de las 10 Operaciones Simuladas
1. Login con clave errónea -> Captura AutenticacionError
2. Login con credenciales válidas -> Acceso concedido
3. Registro de Cliente C101 -> Exitoso
4. Registro de Cliente con email inválido -> Captura ClienteInvalidoError
5. Registro de 3 Servicios -> Exitoso
6. Registro de Servicio con tarifa negativa -> Captura ServicioNoDisponibleError
7. Reserva R-1001 válida -> Reserva confirmada y costo calculado
8. Reserva R-1002 con cliente inexistente -> Captura ClienteInvalidoError
9. Reserva R-1003 con horario fin < inicio -> Captura HorarioInvalidoError
10. Reserva R-1004 válida de equipo -> Reserva confirmada con descuento por días
