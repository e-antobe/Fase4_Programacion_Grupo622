# Fase4_Programacion_Grupo622

# Software FJ - Sistema de Gestión de Clientes, Servicios y Reservas
Universidad Nacional Abierta y a Distancia (UNAD)  
Curso: Programación (Código: 213023)  
Fase 4: Componente Práctico - Prácticas Simuladas  

## Descripción del Proyecto

Software FJ es un sistema modular desarrollado en Python enfocado en la administración de clientes, servicios tecnológicos y reservas corporativas sin dependencia de bases de datos externas (gestión en memoria).

El objetivo principal de este desarrollo es demostrar la robustez del software mediante el Manejo Avanzado de Excepciones Personalizadas (`try / except / else / finally`) y la trazabilidad de operaciones mediante un sistema de registros de auditoría (`software_fj.log`).

---

## Arquitectura de Software y POO

1. **Encapsulamiento y Validaciones:**
   - **Usuario:** Control de acceso mediante autenticación (`admin` / `UNAD123`).
   - **Cliente:** Atributos privados (`_id_cliente`, `_nombre`, `_email`, `_telefono`) con validaciones de expresiones regulares (Regex) para correos y teléfonos.

2. **Jerarquía de Clases e Herencia Abstracta:**
   - **Servicio (Clase Abstracta - ABC):** Define los métodos abstractos `calcular_costo()` y `obtener_descripcion()`.
   - **Subclases:** `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`.

3. **Excepciones Personalizadas:**
   - `SoftwareFJError` (Clase base de excepción)
   - `AutenticacionError`
   - `ClienteInvalidoError`
   - `ServicioNoDisponibleError`
   - `ReservaInvalidaError`
   - `HorarioInvalidoError`

4. **Trazabilidad de Logs (`software_fj.log`):**
   - Registro automático de eventos `INFO`, `WARNING` y `ERROR`.

---

## Historial de Commits y Registro de Contribución Individual

### Contexto del Desarrollo
De acuerdo con la Guía de Aprendizaje y el protocolo establecido en las Webconferencias del curso, se publicó oportunamente en el foro colaborativo de la Fase 4 la invitación al equipo de trabajo fijando un plazo límite de respuesta. Ante la falta de contestación de los compañeros de grupo, el proyecto fue desarrollado de forma **individual** por el estudiante autor de este repositorio.

### Resumen de Commits Registrados en GitHub
El desarrollo en Git se gestionó de forma incremental con los siguientes *commits* principales:

| Hash / Commit | Descripción del Avance | Módulo / Archivos |
| :--- | :--- | :--- |
| `commit 1` | `feat: Estructura inicial del repositorio y setup del proyecto` | `README.md` |
| `commit 2` | `feat: Modelo POO - Clases Usuario, Cliente y Servicio (ABC)` | `fase4_software_fj.py` |
| `commit 3` | `feat: Clases derivadas ReservaSala, AlquilerEquipo y AsesoriaEspecializada` | `fase4_software_fj.py` |
| `commit 4` | `feat: Implementación de excepciones personalizadas y estructura try/except` | `fase4_software_fj.py` |
| `commit 5` | `feat: Integración del sistema de logs (logging) a archivo software_fj.log` | `fase4_software_fj.py`, `software_fj.log` |
| `commit 6` | `test: Simulación secuencial de 10 operaciones de prueba válidas e inválidas` | `fase4_software_fj.py` |
| `commit 7` | `docs: Actualización de documentación README con evidencias de commits` | `README.md` |

---

## Instrucciones de Ejecución

1. Clonar o descargar el repositorio público.
2. Ejecutar la solución en Python:
   ```bash
   python fase4_software_fj.py
   ```
3. Revisar el archivo de auditoría generado en la misma carpeta:
   ```bash
   software_fj.log
   ```

---

## Resumen de las 10 Operaciones Simuladas

1. **Login con clave errónea:** Captura `AutenticacionError` y registra warning.
2. **Login con credenciales válidas:** Acceso concedido exitosamente.
3. **Registro de Cliente C101:** Exitoso (Carlos Mendoza).
4. **Registro de Cliente con email mal formado:** Captura `ClienteInvalidoError`.
5. **Registro de 3 Servicios (Sala, Equipo, Asesoría):** Registro exitoso en memoria.
6. **Registro de Servicio con tarifa negativa:** Captura `ServicioNoDisponibleError`.
7. **Reserva R-1001 válida:** Reserva confirmada y costo calculado ($178,500.00).
8. **Reserva R-1002 con cliente inexistente (C999):** Captura `ClienteInvalidoError`.
9. **Reserva R-1003 con hora fin anterior a inicio:** Captura `HorarioInvalidoError`.
10. **Reserva R-1004 válida de alquiler de equipo:** Reserva confirmada con descuento aplicado ($169,575.00).
10. Reserva R-1004 válida de equipo -> Reserva confirmada con descuento por días
