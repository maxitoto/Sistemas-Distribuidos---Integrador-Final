# ⚙️ Microservicios y Contenedores (dist1 & dist2)

Esta sección contiene la lógica de negocio del sistema. Los nodos de servicios son estandarizados e intercambiables, y no tienen salida directa a internet; solo responden a las peticiones delegadas por el Gateway.

## 🐳 Arquitectura Docker
Cada nodo ejecuta un enjambre de 4 contenedores gestionados mediante `docker-compose`:
1. **nginx-web (Frontend):** Sirve la interfaz gráfica en HTML/CSS (Puerto 80).
2. **editorial-api (Backend):** Microservicio Flask en el puerto 8081.
3. **autor-api (Backend):** Microservicio Flask en el puerto 8082.
4. **libro-api (Backend):** Microservicio Flask en el puerto 8083.

## 🔒 Control de Concurrencia
Para evitar condiciones de carrera (Race Conditions) al escribir en el almacenamiento compartido, los microservicios utilizan la librería de Python `portalocker`, asegurando el bloqueo de exclusión mutua de los archivos JSON a través de la red.

## 🚀 Despliegue
1. Asegurarse de tener el puerto 80 y los puertos de las APIs habilitados en el firewall (`ufw`).
2. Verificar que la carpeta NFS esté montada localmente en `/var/www/html`.
3. Ejecutar el orquestador:
   ```bash
   docker-compose up --build -d