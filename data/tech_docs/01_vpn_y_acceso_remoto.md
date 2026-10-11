# VPN y Acceso Remoto — NubeSoft IT Support

Versión 5.0 · Responsable: IT Support & Security

## 1. ¿Cuándo es obligatoria la VPN?

La VPN corporativa "NubeConnect" (basada en WireGuard) es obligatoria para:

- Acceder a sistemas internos: el repositorio de código, los entornos de staging, la consola de bases de datos, el wiki interno y los paneles de monitoreo.
- Trabajar desde cualquier red que no sea la red cableada de las oficinas, incluyendo redes de hogar, coworkings, aeropuertos y hoteles.
- Trabajar desde otro país durante el programa Work from Anywhere.

Las herramientas SaaS públicas (correo, Slack, PeopleHub, Spendly) funcionan sin VPN, pero se recomienda mantenerla activa siempre que se use una red pública.

## 2. Instalación del cliente VPN

1. Abrir el "Portal de Autoservicio" (Self Service en macOS, Company Portal en Windows).
2. Buscar "NubeConnect VPN" e instalarlo. En Linux, seguir la guía del wiki interno con el paquete .deb firmado.
3. Iniciar sesión con el usuario corporativo (nombre.apellido@nubesoft.com) y aprobar la notificación de MFA en la app Okta Verify.
4. Elegir el servidor más cercano: "AR-BUE", "UY-MVD", "MX-CDMX" o "ES-MAD". El modo "Automático" elige el de menor latencia.

## 3. Problemas frecuentes de la VPN

### La VPN no conecta ("Handshake did not complete")

- Verificar la conexión a internet sin VPN abriendo cualquier sitio público.
- Cerrar sesión en NubeConnect, reiniciar el cliente y volver a iniciar sesión.
- Verificar que la fecha y hora del equipo sean correctas: un desfasaje de más de 2 minutos invalida el token.
- Algunas redes de hoteles bloquean el puerto UDP 51820. En ese caso, activar el modo "TCP fallback" en Configuración > Avanzado.

### La VPN conecta pero no cargan los sistemas internos

- Ejecutar el diagnóstico "Probar conectividad" del cliente, que verifica DNS y rutas.
- Vaciar la caché de DNS: en Windows ejecutar `ipconfig /flushdns`; en macOS, `sudo dscacheutil -flushcache`.
- Si el problema sigue, abrir un ticket en el portal de IT con la captura del diagnóstico.

### La VPN se desconecta cada pocos minutos

- Desactivar el ahorro de energía de la placa Wi-Fi.
- Actualizar el cliente a la última versión desde el Portal de Autoservicio. Las versiones anteriores a la 3.2 tienen un error conocido de reconexión.

## 4. Sesiones y tiempos de expiración

La sesión de VPN dura 12 horas; después hay que volver a autenticarse con MFA. Una sesión inactiva por más de 60 minutos se cierra automáticamente. Por seguridad, no se permite más de una sesión de VPN activa por usuario al mismo tiempo.

## 5. Acceso a servidores y bases de datos

El acceso SSH a servidores de producción no se hace con claves personales permanentes. Se usa el bastión "Teleport", que emite certificados de corta duración (8 horas) luego de autenticarse con MFA. El acceso de lectura a bases de datos de producción requiere un rol aprobado por la persona líder técnica del equipo y por Seguridad, y queda auditado. El acceso de escritura a producción solo se otorga de forma temporal ("just-in-time") por un máximo de 2 horas, asociado a un ticket de incidente o de cambio.

## 6. Escritorio remoto y soporte remoto

Cuando IT necesita conectarse al equipo de una persona para dar soporte, usa la herramienta "AnyAssist". La persona siempre debe aceptar la sesión de manera explícita con un código de 6 dígitos que le dicta el técnico. Nadie de IT pedirá nunca la contraseña de una persona, ni por teléfono, ni por chat, ni por correo.

## 7. Wi-Fi de las oficinas

- Red "NubeSoft-Corp": para equipos corporativos, autenticación automática por certificado.
- Red "NubeSoft-Guest": para visitas y dispositivos personales. La contraseña cambia todos los lunes y se publica en las pantallas de recepción. Está aislada de la red interna.

Los dispositivos personales (teléfonos, tablets) no deben conectarse a la red "NubeSoft-Corp".
