# TP2 - Base de Datos NoSQL: Alquiler de Capítulos de The Mandalorian

Este proyecto es el Trabajo Práctico Nº 2 para la materia "Bases de Datos NoSQL" de la Licenciatura en Sistemas de Información. Consiste en una aplicación web desarrollada en **Python (Flask)** que utiliza **Redis** como base de datos en memoria para gestionar el estado, reservas y alquileres temporales de los capítulos de la serie *The Mandalorian*.

## 🚀 Tecnologías Utilizadas

- **Backend:** Python 3, Flask
- **Base de Datos NoSQL:** Redis (operando en `localhost:6379`)
- **Librería de Conexión:** `redis-py`
- **Frontend:** HTML5, CSS3, Jinja2 (Motor de plantillas)

## 🎯 Funcionalidades Principales

1. **Listado de Capítulos:**
   La ruta principal (`/`) lista los 24 capítulos correspondientes a las 3 temporadas de *The Mandalorian*, consultando en tiempo real a Redis el estado de cada uno.

2. **Lógica de Reserva (Expiración Corta):**
   Un capítulo "Disponible" puede ser reservado por el usuario. Esto cambia el estado a "Reservado" en Redis con un tiempo de expiración (TTL) de **4 minutos (240 segundos)**. Una vez finalizado el tiempo sin confirmarse el pago, la clave expira en Redis y el capítulo vuelve automáticamente a estar "Disponible".

3. **Lógica de Alquiler (Expiración Larga):**
   Una vez confirmado el alquiler (pago de $500), el estado se actualiza en memoria a "Alquilado" con un tiempo de expiración de **24 horas (86400 segundos)**.

4. **Interfaz Dinámica (Temática Star Wars):**
   El diseño web responsivo incorpora el uso de fuentes espaciales (*Orbitron*), colores neón sobre fondos oscuros, y actualizaciones visuales de los estados usando distintivos:
   - 🟢 Verde: Disponible
   - 🟡 Amarillo: Reservado
   - 🔴 Rojo: Alquilado

## 🛠 Instalación y Ejecución

### Requisitos Previos
- Python 3.x
- Servidor de Redis en ejecución (puerto `6379`).

### Pasos a seguir

1. **Clonar el código fuente:**
   ```bash
   git clone https://github.com/DelValleMateo/TP2_BASE_DE_DATOS_NSQL.git
   cd TP2_BASE_DE_DATOS_NSQL/TP-2-CODIGO
   ```

2. **Instalar dependencias necesarias:**
   Es recomendable usar un entorno virtual de Python. Luego, desde la consola, instalar:
   ```bash
   pip install Flask redis
   ```

3. **Asegurar la conexión de Redis:**
   Verificar que Redis se encuentre con el servicio corriendo en `localhost` mediante el comando `redis-server` (o equivalente según el sistema operativo).

4. **Iniciar la aplicación:**
   ```bash
   python app.py
   ```
   *La web estará funcional y escuchando peticiones en `http://localhost:5000`.*
