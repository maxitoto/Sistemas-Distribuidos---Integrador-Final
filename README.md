# 💾 Almacenamiento Centralizado (sdist3)

Este servidor centraliza toda la persistencia del sistema utilizando el protocolo **NFS (Network File System)**. Actúa como la única fuente de verdad (Single Source of Truth) para las bases de datos en formato JSON.

## 📂 Configuración de Exportación
El directorio `/var/www/html` es exportado a las IPs de los nodos de servicios.

La configuración en `/etc/exports` utiliza las siguientes directivas críticas:
- `rw`: Permite lectura y escritura a los nodos.
- `sync`: Obliga al servidor NFS a confirmar la escritura física en el disco antes de responder al cliente, garantizando la persistencia ante caídas eléctricas.
- `no_wdelay`: Desactiva las micropausas del protocolo, forzando escrituras inmediatas. Esto es vital para el correcto funcionamiento de los bloqueos (`locks`) que ejecutan las APIs.

## 🔗 Montaje en Clientes
Los nodos `dist1` y `dist2` deben montar este sistema de archivos de forma permanente editando su archivo `/etc/fstab` para evitar pérdidas de conexión durante los reinicios del sistema operativo.