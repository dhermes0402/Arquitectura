# Proyecto: Arquitectura de Microservicios con Docker Compose

Este proyecto guía a los estudiantes para crear y desplegar un archivo `docker-compose.yaml` que define una arquitectura de microservicios utilizando contenedores Docker. La aplicación incluye cuatro servicios:

1. **Base de Datos (MySQL)**
2. **Servicio de Login (Python Flask)**
3. **API de Productos (Node.js)**
4. **Aplicación Web (PHP)**

A continuación, se detalla la configuración de cada servicio y cómo desplegar el sistema completo.

---

## **Requisitos Previos**

1. Tener instalado Docker y Docker Compose.
   - Verifica con:
     ```bash
     docker --version
     docker-compose --version
     ```
2. Asegúrate de que los directorios y archivos requeridos (`init.sql`, `Dockerfile`, etc.) están correctamente creados.

---

## **Estructura del Proyecto**

La estructura del proyecto debe ser la siguiente:
```
.
├── docker-compose.yaml
├── db
│   └── init.sql
├── login
│   └── Dockerfile
├── api
│   └── Dockerfile
├── php
│   └── Dockerfile
```

---

## **Descripción de los Contenedores**

### **1. Base de Datos (contenedor_bd)**
- **Imagen base**: `mysql:5.7`
- **Propósito**: Almacenar las bases de datos `authentication` y `shop`.
- **Volúmenes**:
  - `micro_db_data`: Persistencia de datos de la base de datos.
  - `./db/init.sql`: Script de inicialización para crear tablas y datos iniciales.
- **Variables de entorno**:
  - `MYSQL_ROOT_PASSWORD`: Contraseña del usuario root de MySQL.
- **Red**: `app_network`.

### **2. Servicio de Login (contenedor_login)**
- **Ruta Dockerfile**: `./login/Dockerfile`
- **Propósito**: Gestionar autenticaciones mediante JWT.
- **Puertos expuestos**: `5000:5000`
- **Variables de entorno**:
  - `DB_HOST`: Nombre del contenedor de la base de datos.
  - `DB_USER`: Usuario de la base de datos.
  - `DB_PASSWORD`: Contraseña de la base de datos.
  - `DB_NAME_AUTH`: Nombre de la base de datos de autenticación.
- **Dependencias**: Depende de `contenedor_bd`.
- **Red**: `app_network`.

### **3. API de Productos (contenedor_api)**
- **Ruta Dockerfile**: `./api/Dockerfile`
- **Propósito**: Proporcionar endpoints para interactuar con los productos.
- **Puertos expuestos**: `5001:5001`
- **Variables de entorno**:
  - `DB_HOST`: Nombre del contenedor de la base de datos.
  - `DB_USER`: Usuario de la base de datos.
  - `DB_PASSWORD`: Contraseña de la base de datos.
  - `DB_NAME_SHOP`: Nombre de la base de datos de productos.
  - `LOGIN_SERVICE`: URL del servicio de login.
- **Dependencias**: Depende de `contenedor_bd` y `contenedor_login`.
- **Red**: `app_network`.

### **4. Aplicación Web (contenedor_php)**
- **Ruta Dockerfile**: `./php/Dockerfile`
- **Propósito**: Interfaz web para que los usuarios interactúen con el sistema.
- **Puertos expuestos**: `8080:80`
- **Variables de entorno**:
  - `LOGIN_SERVICE`: URL del servicio de login.
  - `API_SERVICE`: URL del servicio API.
- **Dependencias**: Depende de `contenedor_login` y `contenedor_api`.
- **Red**: `app_network`.

---

## **Instrucciones de Implementación**

### **1. Construir y desplegar los contenedores**
Ejecuta los siguientes comandos en el directorio que contiene `docker-compose.yaml`:

1. Construir las imágenes y crear los contenedores:
   ```bash
   docker-compose up --build
   ```

2. Verifica que los contenedores están en ejecución:
   ```bash
   docker ps
   ```

### **2. Pruebas de conexión**
- Accede a la base de datos para verificar que se crearon las tablas y datos iniciales:
  ```bash
  docker exec -it contenedor_bd mysql -uroot -proot
  ```
- Prueba el servicio de login en `http://localhost:5000`.
- Prueba la API de productos en `http://localhost:5001`.
- Accede a la interfaz web en `http://localhost:8080`.

---

## **Consideraciones Administrativas**

1. **Inicialización de la base de datos**:
   - Verifica que el archivo `init.sql` contiene las instrucciones necesarias para crear las bases de datos y tablas.

2. **Reinicio de servicios**:
   - Para reiniciar los contenedores sin perder datos:
     ```bash
     docker-compose restart
     ```
   - Para reiniciar desde cero (incluyendo la base de datos):
     ```bash
     docker-compose down --volumes
     docker-compose up --build
     ```

3. **Depuración**:
   - Revisa los logs de cada contenedor para diagnosticar problemas:
     ```bash
     docker logs <container_name>
     ```

