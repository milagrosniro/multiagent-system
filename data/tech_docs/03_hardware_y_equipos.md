# Hardware, Equipos y Periféricos — NubeSoft IT Support

Versión 3.4 · Responsable: IT Support (Endpoint Team)

## 1. Equipo estándar por rol

- Ingeniería, Datos y Diseño: MacBook Pro 14" con 32 GB de RAM y 1 TB de almacenamiento, o una notebook Linux equivalente (Lenovo ThinkPad P1) a pedido.
- Resto de las áreas: MacBook Air 13" con 16 GB de RAM, o Dell Latitude 7450 con Windows 11 a elección.
- Todas las personas reciben: mochila, mouse, teclado inalámbrico y auriculares con micrófono con cancelación de ruido.

Los monitores externos no son parte del kit de IT: se cubren con el estipendio de equipamiento remoto de RR. HH. o están disponibles en las oficinas.

## 2. Ciclo de renovación

Las notebooks se renuevan cada 3 años. IT contacta a la persona 30 días antes de la fecha de renovación. Se puede pedir una renovación anticipada si el equipo tiene fallas de hardware recurrentes y no es económico repararlo; IT evalúa cada caso.

## 3. Solicitar hardware o periféricos adicionales

Los periféricos adicionales (adaptadores, cargador extra, dock, teclado ergonómico) se piden en el portal de IT, sección "Solicitud de hardware". Los pedidos de hasta USD 150 se aprueban automáticamente; los superiores requieren aprobación de la persona líder. El tiempo de entrega es de 5 a 10 días hábiles según el país.

Si alguien compra un periférico por su cuenta sin pasar por IT, no se reembolsa por el circuito de IT; en algunos casos puede reembolsarse como gasto, según la política de gastos de Finance.

## 4. Equipos dañados

Si la notebook se daña (pantalla rota, derrame de líquido, teclado que no responde):

1. Abrir un ticket en el portal de IT con la categoría "Hardware dañado", fotos y descripción.
2. IT envía un equipo de reemplazo en un plazo de 2 días hábiles en ciudades con oficina y de 5 días hábiles en otras ubicaciones.
3. El equipo dañado se devuelve con la etiqueta prepaga que envía IT.

Los daños accidentales están cubiertos por la garantía extendida corporativa. Si hay daños repetidos por negligencia (más de 2 en 12 meses), el caso se revisa con el People Partner.

## 5. Pérdida o robo de equipos

La pérdida o el robo de una notebook, un teléfono corporativo o una llave de seguridad es un incidente de seguridad. Pasos obligatorios:

1. Reportarlo de inmediato, como máximo dentro de las 2 horas de detectado, en el canal de Slack #security-incidents o llamando a la mesa de ayuda (+54 11 5555-0100, interno 4357).
2. IT bloquea el equipo y ejecuta el borrado remoto con la herramienta de gestión de dispositivos (MDM).
3. Si hubo robo, hacer la denuncia policial y cargar la copia en el ticket, porque la necesita la aseguradora.
4. Seguridad evalúa si el equipo contenía datos personales de clientes. Si es así, el área Legal analiza si corresponde notificar a autoridades o clientes según la política de privacidad y de respuesta a brechas de datos.

Todas las notebooks tienen cifrado de disco completo (FileVault en macOS, BitLocker en Windows, LUKS en Linux), lo que reduce el riesgo de exposición de datos.

## 6. Gestión de dispositivos (MDM)

Todos los equipos corporativos están enrolados en el MDM ("Jamf" para macOS, "Intune" para Windows). El MDM aplica:

- Cifrado de disco obligatorio.
- Bloqueo de pantalla automático a los 5 minutos de inactividad.
- Actualizaciones del sistema operativo: deben instalarse dentro de los 7 días de publicadas; las actualizaciones de seguridad críticas, dentro de las 48 horas.
- Antivirus y EDR ("CrowdStrike Falcon"), que no pueden desactivarse.

## 7. Dispositivos personales (BYOD)

Se puede usar el teléfono personal para el correo corporativo, Slack y Okta Verify si se instala el perfil de trabajo de Intune, que separa los datos corporativos de los personales. IT solo puede borrar el perfil de trabajo, nunca los datos personales. No se permite acceder a sistemas internos ni a código fuente desde computadoras personales.

## 8. Impresoras y salas de reunión

Las impresoras de las oficinas se usan con la credencial corporativa ("impresión segura": el documento sale solo al acercar la credencial). Las salas de reunión tienen equipos de videoconferencia Google Meet; para reportar una falla en una sala, escanear el código QR pegado en la mesa.

## 9. Devolución del equipo al finalizar la relación laboral

Al desvincularse, la persona tiene 10 días hábiles desde su último día para devolver la notebook y los periféricos corporativos con la caja y la etiqueta prepaga que envía IT. Antes de devolverlo no se debe formatear el equipo: IT hace el borrado seguro y la copia de respaldo que corresponda.
