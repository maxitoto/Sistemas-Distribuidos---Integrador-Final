# 📚 Proyecto Integrador: Sistema de Gestión Editorial

Este repositorio utiliza una arquitectura de microservicios distribuida en múltiples nodos.

| Rama | Propósito | Destino (VM) | Tecnología |
| :--- | :--- | :--- | :--- |
| `web` | Frontend del sistema | `dist3` | Apache, PHP, JS |
| `services` | APIs de Autor, Libro y Editorial | `dist1`, `dist2` | Python (Flask), Docker |
| `gateway` | Proxy Inverso y Balanceador | `dist0` | Nginx |
| `main` | **Orquestación Global** | Desarrollo local | Todo el stack |