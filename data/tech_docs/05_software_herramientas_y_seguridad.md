# Software, Herramientas y Seguridad de la Información — NubeSoft IT Support

Versión 4.0 · Responsable: IT Support & Security

## 1. Instalación de software

El software aprobado se instala desde el Portal de Autoservicio (Self Service en macOS, Company Portal en Windows) sin permisos de administrador. El catálogo incluye navegadores, IDEs (VS Code, IntelliJ), Docker Desktop, Postman, herramientas de diseño (Figma), clientes de bases de datos y utilidades de productividad.

Para instalar software que no está en el catálogo:

1. Abrir una "Solicitud de software" en el portal de IT, indicando el nombre, el uso y si procesa datos de clientes.
2. Seguridad revisa la licencia, el origen y los permisos. Si el software procesa datos personales o de clientes, también lo revisa el área Legal (evaluación de proveedor).
3. El plazo de revisión es de 5 días hábiles.

## 2. Software prohibido

Está prohibido instalar: software pirateado o con licencias no válidas, herramientas de acceso remoto no aprobadas (por ejemplo TeamViewer personal), clientes torrent, VPNs personales y extensiones de navegador que lean el contenido de todas las páginas sin aprobación de Seguridad.

## 3. Licencias de software pagas (SaaS)

Las licencias de herramientas SaaS pagas (por ejemplo Jira, GitHub, Figma, Notion, Datadog) se piden en el portal de IT. IT gestiona la asignación de licencias y Finance gestiona el pago al proveedor. Las licencias sin uso durante 60 días se reasignan automáticamente. No está permitido contratar herramientas SaaS con tarjeta corporativa sin la aprobación previa de IT, porque genera "shadow IT" y riesgos de seguridad.

## 4. Uso de herramientas de inteligencia artificial

- Herramientas aprobadas: el asistente corporativo de IA (con contrato empresarial que no usa los datos para entrenar modelos) y el asistente de código integrado en el IDE con la licencia corporativa.
- Está prohibido ingresar en herramientas de IA no aprobadas: datos personales de clientes, código fuente propietario, credenciales, información financiera no pública o documentos confidenciales.
- El contenido generado con IA debe ser revisado por una persona antes de enviarse a clientes o fusionarse en el repositorio.

## 5. Clasificación de la información

- Pública: información publicada en el sitio web o en materiales de marketing.
- Interna: información para uso de cualquier persona de NubeSoft (wiki, procesos internos).
- Confidencial: información de clientes, contratos, información financiera, código fuente. Se comparte solo con quienes la necesitan.
- Restringida: datos personales sensibles, credenciales, claves de cifrado, datos de tarjetas de pago. Acceso mínimo, cifrado obligatorio y auditoría de accesos.

## 6. Compartir archivos

Los archivos se guardan en Google Drive corporativo. Por defecto, los documentos se comparten solo dentro del dominio nubesoft.com. Para compartir con personas externas (clientes, proveedores) se debe usar un enlace con fecha de vencimiento y con acceso de solo lectura cuando sea posible. Está prohibido subir información confidencial a servicios de almacenamiento personales (Dropbox, WeTransfer, Google Drive personal).

## 7. Copias de seguridad

Los datos de Google Drive, el correo y los repositorios se respaldan automáticamente. Los archivos guardados solo en el disco local de la notebook no se respaldan: el trabajo debe guardarse en Drive o en el repositorio. Para recuperar un archivo borrado de Drive hace menos de 30 días, se puede usar la papelera; para períodos mayores (hasta 1 año), hay que pedirlo a IT con un ticket.

## 8. Correo electrónico y Slack

- El correo corporativo tiene una cuota de 50 GB.
- Las reglas de reenvío automático hacia direcciones externas están bloqueadas.
- En Slack, los canales públicos son el lugar por defecto para conversar de trabajo. Los canales compartidos con clientes ("Slack Connect") requieren aprobación de IT y llevan el prefijo #ext-.
- Los mensajes de Slack se conservan 2 años; los de canales #ext- se conservan 5 años por requisitos contractuales.

## 9. Desarrollo seguro

- Todo cambio de código pasa por un pull request con al menos una aprobación.
- El escaneo de secretos ("secret scanning") bloquea los commits que contienen credenciales.
- Las dependencias con vulnerabilidades críticas deben actualizarse en 7 días; las altas, en 30 días.
- Las pruebas de penetración externas se hacen dos veces por año, y los hallazgos críticos se corrigen en 15 días.

## 10. Capacitación obligatoria en seguridad

El curso anual de Seguridad de la Información en NubeAcademy es obligatorio para todas las personas. Debe completarse antes del 31 de marzo de cada año. Quien no lo complete pierde temporalmente el acceso a herramientas que contienen datos de clientes hasta completarlo.
