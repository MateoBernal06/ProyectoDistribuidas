# Sistema de Gestión de Productos Distribuido
Este proyecto implementa un sistema web distribuido de gestión de productos usando Flask y Docker.

## Ejecución

1. **Nodos:**
   - Nodo 1: http://localhost:5001
   - Nodo 2: http://localhost:5002
   - Nodo 3: http://localhost:5003


## Funcionalidades Implementadas

### 1. Sistema de Autenticación

- Inicio de sesión 
- Registro de nuevos usuarios

### 2. Gestión de Productos
- Registro de productos con los siguientes campos:
  - Código (único)
  - Nombre
  - Descripción
  - Categoría
  - Cantidad en stock

### 3. Validaciones
- Códigos de productos únicos
- Validación de campos obligatorios
- Verificación de disponibilidad


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
