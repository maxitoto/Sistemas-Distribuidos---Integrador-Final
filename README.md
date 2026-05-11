# 🛡️ Gateway y Proxy Inverso (dist0)

Este componente actúa como la única puerta de enlace pública del sistema. Se encarga de recibir el tráfico web, gestionar los certificados de seguridad y distribuir la carga entre los nodos de trabajo internos.

## ⚙️ Tecnologías
- **Nginx:** Actúa como proxy reverso (`proxy_pass`).
- **SSL/TLS:** Certificados autofirmados para garantizar conexiones HTTPS seguras.

## 🚦 Balanceo de Carga (Round Robin)
La distribución del tráfico se realiza mediante un algoritmo de Round Robin asimétrico (1:2):
- El nodo **dist2** procesa el doble de peticiones que el nodo **dist1**.
- Esto se logra configurando los `upstream` en el archivo `.conf` asignando `weight=1` a dist1 y `weight=2` a dist2.

## 🛠️ Despliegue
1. Copiar el archivo de configuración `distribuidos.conf` a `/etc/nginx/sites-available/`.
2. Crear un enlace simbólico hacia `/etc/nginx/sites-enabled/`.
3. Verificar la sintaxis con `sudo nginx -t`.
4. Reiniciar el servicio: `sudo systemctl restart nginx`.