# Mesa de Ayuda, Gestión de Incidentes y SLA — NubeSoft IT Support

Versión 6.0 · Responsable: IT Support & SRE

## 1. Canales de soporte de IT

- Portal de IT (it.nubesoft.com): canal principal para abrir tickets. Todas las solicitudes deben quedar registradas aquí.
- Slack #it-help: para consultas rápidas. Un bot convierte el mensaje en ticket si no se resuelve en 15 minutos.
- Teléfono de la mesa de ayuda: +54 11 5555-0100, interno 4357. Solo para urgencias o cuando no se puede acceder a la cuenta.
- Correo it-support@nubesoft.com: crea un ticket automáticamente.

El horario de atención de la mesa de ayuda es de lunes a viernes de 8:00 a 20:00 (hora de Buenos Aires). Fuera de ese horario, solo se atienden incidentes de prioridad P1 y P2 a través de la guardia.

## 2. Prioridades y tiempos de respuesta (SLA internos)

| Prioridad | Descripción | Primera respuesta | Resolución objetivo |
|---|---|---|---|
| P1 - Crítica | Caída de un servicio para clientes o incidente de seguridad activo | 15 minutos, 24x7 | 4 horas |
| P2 - Alta | Funcionalidad importante degradada o un equipo completo bloqueado | 1 hora, 24x7 | 8 horas |
| P3 - Media | Una persona bloqueada (sin acceso, equipo que no funciona) | 4 horas hábiles | 2 días hábiles |
| P4 - Baja | Solicitudes, consultas, mejoras | 1 día hábil | 5 días hábiles |

La prioridad la sugiere quien abre el ticket y la confirma IT. Clasificar como P1 algo que no lo es de forma reiterada se informa a la persona líder.

## 3. Incidentes de producción

Un incidente de producción es cualquier evento que afecta a clientes: caída de la plataforma, errores masivos, degradación grave del rendimiento o pérdida de datos. El procedimiento es:

1. Declarar el incidente en Slack con el comando `/incident declare`, que crea el canal #inc-AAAAMMDD-nombre.
2. Asignar un Incident Commander (IC), que coordina la respuesta; por defecto es la persona de guardia del equipo SRE.
3. Actualizar el estado en la página pública status.nubesoft.com cada 30 minutos mientras dure un incidente P1.
4. Una vez mitigado, declarar el incidente como resuelto con `/incident resolve`.
5. Escribir un postmortem sin culpables ("blameless") dentro de los 5 días hábiles para incidentes P1 y P2.

## 4. Guardias (on-call)

Los equipos de ingeniería tienen rotaciones de guardia semanales administradas en PagerDuty. La persona de guardia debe confirmar ("acknowledge") una alerta en 5 minutos para P1 y en 15 minutos para P2. Si no responde, PagerDuty escala automáticamente a la persona de guardia secundaria y luego al Engineering Manager. Las reglas de compensación de las guardias están en la política de RR. HH.

## 5. Incidentes de seguridad

Cualquier sospecha de incidente de seguridad (correo de phishing, malware, acceso no autorizado, pérdida de un equipo, filtración de una credencial) debe reportarse de inmediato en el canal #security-incidents o al correo security@nubesoft.com. No se debe intentar investigar por cuenta propia ni borrar evidencia. El equipo de Seguridad responde en 15 minutos las 24 horas. Si el incidente involucra datos personales, Seguridad avisa al área Legal, que evalúa las obligaciones de notificación.

## 6. Correos de phishing

Si llega un correo sospechoso:

- No hacer clic en enlaces ni descargar adjuntos.
- Usar el botón "Reportar phishing" en Gmail, que lo envía a Seguridad y lo elimina de la bandeja.
- Si ya se hizo clic o se ingresaron credenciales, cambiar la contraseña de inmediato y avisar en #security-incidents.

Seguridad hace simulaciones de phishing cada trimestre. Quien cae en dos simulaciones seguidas debe repetir el curso de concientización.

## 7. Gestión de cambios

Los cambios en infraestructura de producción requieren un "change request" aprobado en el portal de IT. Los cambios estándar (preaprobados, como un deploy con pipeline verde) no necesitan aprobación manual. Los cambios normales requieren la revisión de una segunda persona del equipo. Hay un "freeze" de cambios no urgentes en producción del 20 de diciembre al 5 de enero.

## 8. Encuestas de satisfacción

Al cerrar cada ticket se envía una encuesta de una pregunta (1 a 5). El objetivo del equipo de IT Support es mantener una satisfacción promedio de 4,5 o más y resolver el 70% de los tickets en el primer contacto.
