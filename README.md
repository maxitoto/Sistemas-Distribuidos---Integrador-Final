# Sistema Distribuido - Proyecto Integrador Final 🚓

Bienvenido al repositorio del proyecto integrador para la materia de Sistemas Distribuidos. 
Este sistema fue diseñado para gestionar la persistencia y concurrencia de datos (editoriales, autores, libros) en un entorno de red descentralizado, aplicando conceptos de alta disponibilidad y tolerancia a fallos.

## 🏗️ Arquitectura del Sistema
El proyecto simula una infraestructura distribuida compuesta por 4 nodos virtuales:
- **dist0 (Gateway):** Proxy inverso y balanceador de carga.
- **dist1 y dist2 (Servicios):** Nodos obreros que ejecutan microservicios en contenedores.
- **sdist3 (Almacenamiento):** Servidor NFS central para garantizar la consistencia estricta.

## 🗂️ Navegación del Repositorio
El código y las configuraciones están divididos modularmente. Por favor, dirígete a las siguientes carpetas/ramas para ver la documentación y el código específico de cada componente:

* ➡️ **[`/gateway`](./gateway):** Configuración del Proxy Inverso (Nginx) y SSL.
* ➡️ **[`/services`](./services):** Código fuente de las APIs (Flask), Nginx interno y orquestación con Docker Compose.
* ➡️ **[`/NFS`](./NFS):** Configuraciones del servidor de archivos de red y la base de datos JSON.