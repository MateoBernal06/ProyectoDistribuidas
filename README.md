# Sistema de Gestión de Productos Distribuido

Este proyecto implementa un sistema web distribuido de gestión de productos usando Flask y Docker.

## Características

- **Inicio de sesión:** Sistema de autenticación de usuarios
- **Gestión de productos:** Registro de productos con código único
- **Validación:** No permite códigos de productos duplicados
- **Consulta en tiempo real:** API para verificar disponibilidad de productos
- **Arquitectura distribuida:** Tres nodos independientes ejecutando la misma aplicación

## Estructura del Proyecto

```
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias de Python
├── Dockerfile            # Configuración del contenedor
├── docker-compose.yml    # Configuración de los tres nodos
├── templates/            # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── productos.html
│   ├── nuevo_producto.html
│   └── consultar_disponibilidad.html
└── data/                # Directorios de bases de datos por nodo
    ├── node1/
    ├── node2/
    └── node3/
```

## Instalación y Ejecución

### Prerequisitos
- Docker
- Docker Compose

### Pasos para ejecutar

1. **Clonar o descargar el proyecto**

2. **Ejecutar los tres nodos con Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Acceder a los nodos:**
   - Nodo 1: http://localhost:5001
   - Nodo 2: http://localhost:5002
   - Nodo 3: http://localhost:5003

## Credenciales por defecto

- **Usuario:** admin
- **Contraseña:** admin123

## Funcionalidades Implementadas

### 1. Sistema de Autenticación
- Inicio de sesión con validación
- Registro de nuevos usuarios
- Gestión de sesiones

### 2. Gestión de Productos
- Registro de productos con los siguientes campos:
  - Código (único)
  - Nombre
  - Descripción
  - Unidad de medida
  - Categoría
  - Cantidad en stock

### 3. Validaciones
- Códigos de productos únicos
- Validación de campos obligatorios
- Verificación de disponibilidad

### 4. Consulta en Tiempo Real
- API REST para consultar productos
- Interfaz web para verificar disponibilidad
- Actualización automática del estado

## API Endpoints

- `GET /api/producto/<codigo>` - Consultar producto específico
- `GET /api/productos` - Listar todos los productos

## Notas Técnicas

- Cada nodo tiene su propia base de datos SQLite independiente
- Los datos no se sincronizan automáticamente entre nodos
- Cada nodo es completamente funcional de forma independiente
- La aplicación usa Bootstrap para el diseño responsive

## Comandos Útiles

```bash
# Ejecutar los contenedores
docker-compose up -d

# Ver logs de un nodo específico
docker-compose logs web-node-1

# Detener todos los nodos
docker-compose down

# Reconstruir los contenedores
docker-compose up --build
```
